from __future__ import annotations

import json
import math
from dataclasses import dataclass
from urllib import request

from bookwriter.domain.model_profiles import ModelProfiles, load_model_profiles
from bookwriter.domain.model_selection import select_model_for_task
from bookwriter.domain.token_usage import TokenUsageLedger, TokenUsageRecord
from bookwriter.runtime.model_runtime import ModelInvocation, ModelOutput


class ModelRuntimeBlocked(RuntimeError):
    def __init__(self, blockers: list[str]) -> None:
        super().__init__("; ".join(blockers))
        self.blockers = blockers


@dataclass(slots=True)
class OllamaRuntime:
    profiles: ModelProfiles
    ledger: TokenUsageLedger
    timeout_seconds: int = 600
    enabled: bool = True

    @classmethod
    def from_config(cls) -> OllamaRuntime:
        return cls(profiles=load_model_profiles(), ledger=TokenUsageLedger())

    def invoke(self, invocation: ModelInvocation) -> ModelOutput:
        profile = self.profiles.tasks[invocation.task]
        model = invocation.model or profile.model
        system_prompt = invocation.system_prompt or (
            "Du bist ein Bookwriter-Agent. Antworte ausschliesslich mit validem JSON, "
            "ohne Markdown, ohne Erklaertext und ohne Codeblock."
        )
        input_tokens = estimate_tokens(system_prompt + "\n" + invocation.prompt)
        context_tokens = self.profiles.model_context_tokens.get(
            model,
            profile.preferred_context_tokens
            or self.profiles.preferred_review_context_tokens,
        )
        selection = select_model_for_task(
            self.profiles,
            task=invocation.task,
            available_context_tokens=context_tokens,
            input_tokens=input_tokens,
            requested_model=model,
        )
        if not selection.ok:
            raise ModelRuntimeBlocked(selection.blockers)

        body = {
            "model": selection.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": invocation.prompt},
            ],
            "stream": False,
            "options": {
                "temperature": profile.temperature,
                "num_ctx": context_tokens,
            },
        }
        if invocation.expected_json:
            body["format"] = "json"

        response = self._post_chat(body)
        content = _chat_content(response)
        output = ModelOutput(
            text=content,
            model=selection.model,
            input_tokens=int(response.get("prompt_eval_count") or input_tokens),
            output_tokens=int(response.get("eval_count") or estimate_tokens(content)),
            metadata={
                "provider": self.profiles.provider,
                "base_url": self.profiles.base_url,
            },
        )
        if invocation.project_id:
            self.ledger.append(
                TokenUsageRecord(
                    project_id=invocation.project_id,
                    task=invocation.task,
                    model=output.model,
                    input_tokens=output.input_tokens,
                    output_tokens=output.output_tokens,
                    agent=invocation.agent,
                    chapter_number=invocation.chapter_number,
                    run_focus=invocation.run_focus,
                )
            )
        return output

    def _post_chat(self, body: dict[str, object]) -> dict[str, object]:
        url = self.profiles.base_url.rstrip("/") + "/api/chat"
        payload = json.dumps(body).encode("utf-8")
        req = request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=self.timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))


def estimate_tokens(text: object) -> int:
    if text is None:
        return 0
    return max(1, math.ceil(len(str(text)) / 4))


def _chat_content(response: dict[str, object]) -> str:
    message = response.get("message")
    if isinstance(message, dict):
        return str(message.get("content", ""))
    return str(response.get("response", ""))
