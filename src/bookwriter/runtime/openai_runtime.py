from __future__ import annotations

import json
import os
import socket
from dataclasses import dataclass
from urllib import error, request

from bookwriter.domain.model_profiles import ModelProfiles, load_model_profiles
from bookwriter.domain.token_usage import TokenCostCatalog, TokenUsageLedger, TokenUsageRecord
from bookwriter.runtime.env import load_env_file
from bookwriter.runtime.model_runtime import ModelInvocation, ModelOutput
from bookwriter.runtime.ollama_runtime import ModelRuntimeBlocked, estimate_tokens


@dataclass(slots=True)
class OpenAIChatRuntime:
    profiles: ModelProfiles
    ledger: TokenUsageLedger
    model: str = "gpt-5-mini"
    base_url: str = "https://api.openai.com/v1"
    api_key_env: str = "OPENAI_API_KEY"
    timeout_seconds: int = 180
    max_completion_tokens: int | None = None
    max_estimated_cost: float | None = None
    enabled: bool = True

    @classmethod
    def from_config(cls) -> OpenAIChatRuntime:
        return cls(profiles=load_model_profiles(), ledger=TokenUsageLedger())

    def invoke(self, invocation: ModelInvocation) -> ModelOutput:
        load_env_file()
        api_key = os.environ.get(self.api_key_env, "").strip()
        if not api_key:
            raise ModelRuntimeBlocked([f"Missing API key in environment: {self.api_key_env}."])

        profile = self.profiles.tasks[invocation.task]
        model = invocation.model or self.model
        output_limit = self.max_completion_tokens or profile.max_output_tokens
        system_prompt = invocation.system_prompt or (
            "Du bist ein Bookwriter-Agent. Antworte ausschliesslich mit validem JSON, "
            "ohne Markdown, ohne Erklaertext und ohne Codeblock."
        )
        input_tokens_estimate = estimate_tokens(system_prompt + "\n" + invocation.prompt)
        self._validate_cost_profile(model, input_tokens_estimate, output_limit)

        body: dict[str, object] = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": invocation.prompt},
            ],
            "temperature": profile.temperature,
            "max_completion_tokens": output_limit,
            "store": False,
        }
        if invocation.expected_json:
            body["response_format"] = {"type": "json_object"}

        response = self._post_chat(body, api_key)
        content = _chat_content(response)
        usage = response.get("usage", {})
        input_tokens = int(_usage_value(usage, "prompt_tokens", input_tokens_estimate))
        output_tokens = int(_usage_value(usage, "completion_tokens", estimate_tokens(content)))
        output = ModelOutput(
            text=content,
            model=str(response.get("model") or model),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            metadata={
                "provider": "openai",
                "base_url": self.base_url,
                "endpoint": "chat_completions",
            },
        )
        if invocation.project_id:
            record = self.ledger.append(
                TokenUsageRecord(
                    project_id=invocation.project_id,
                    task=invocation.task,
                    model=model,
                    input_tokens=output.input_tokens,
                    output_tokens=output.output_tokens,
                    agent=invocation.agent,
                    chapter_number=invocation.chapter_number,
                    run_focus=invocation.run_focus,
                )
            )
            output.metadata["estimated_cost"] = f"{record.estimated_cost:.6f}"
            output.metadata["currency"] = record.currency
        return output

    def _validate_cost_profile(
        self,
        model: str,
        input_tokens_estimate: int,
        output_limit: int,
    ) -> None:
        catalog = TokenCostCatalog()
        try:
            estimated_cost = catalog.estimate_cost(model, input_tokens_estimate, output_limit)
        except KeyError as missing_profile:
            raise ModelRuntimeBlocked([str(missing_profile)]) from missing_profile
        if self.max_estimated_cost is not None and estimated_cost > self.max_estimated_cost:
            raise ModelRuntimeBlocked(
                [
                    "Estimated external model cost exceeds configured run limit: "
                    f"{estimated_cost:.6f} > {self.max_estimated_cost:.6f} "
                    f"{catalog.profile_for(model).currency}."
                ]
            )

    def _post_chat(self, body: dict[str, object], api_key: str) -> dict[str, object]:
        url = self.base_url.rstrip("/") + "/chat/completions"
        payload = json.dumps(body).encode("utf-8")
        req = request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except error.HTTPError as http_error:
            details = http_error.read().decode("utf-8", errors="replace")
            raise ModelRuntimeBlocked(
                [f"OpenAI request failed: HTTP {http_error.code}: {details}"]
            ) from http_error
        except error.URLError as url_error:
            raise ModelRuntimeBlocked([f"OpenAI request failed: {url_error}"]) from url_error
        except (TimeoutError, socket.timeout) as timeout_error:
            raise ModelRuntimeBlocked(
                [f"OpenAI request timed out after {self.timeout_seconds} seconds."]
            ) from timeout_error


def _chat_content(response: dict[str, object]) -> str:
    choices = response.get("choices", [])
    if not isinstance(choices, list) or not choices:
        return ""
    first = choices[0]
    if not isinstance(first, dict):
        return ""
    message = first.get("message", {})
    if not isinstance(message, dict):
        return ""
    return str(message.get("content", ""))


def _usage_value(usage: object, key: str, fallback: int) -> int:
    if not isinstance(usage, dict):
        return fallback
    value = usage.get(key)
    return int(value) if value is not None else fallback
