from __future__ import annotations

import argparse
from collections.abc import Sequence

from bookwriter.agents.orchestrator import Orchestrator
from bookwriter.domain.interview_questions import load_interview_questions, question_by_field
from bookwriter.domain.models import BookProject, Interview
from bookwriter.domain.model_profiles import load_model_profiles
from bookwriter.domain.token_usage import TokenUsageLedger, TokenUsageRecord
from bookwriter.storage.json_store import JsonProjectStore
from bookwriter.workflows.book_project import BookProjectWorkflow


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "interview":
        return run_interview(args)
    if args.command == "status":
        return run_status(args)
    if args.command == "approve-concept":
        return run_approve_concept(args)
    if args.command == "market":
        return run_market(args)
    if args.command == "publisher-offer":
        return run_publisher_offer(args)
    if args.command == "kdp-checklist":
        return run_kdp_checklist(args)
    if args.command == "models":
        return run_models()
    if args.command == "questions":
        return run_questions()
    if args.command == "usage":
        return run_usage(args)
    if args.command == "token-log":
        return run_token_log(args)
    parser.print_help()
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bookwriter")
    subparsers = parser.add_subparsers(dest="command")

    interview = subparsers.add_parser("interview", help="Create a project from interview inputs.")
    interview.add_argument("--name", default="")
    interview.add_argument("--topic")
    interview.add_argument("--target-audience")
    interview.add_argument("--book-type")
    interview.add_argument("--desired-result")
    interview.add_argument("--tone")
    interview.add_argument("--length-goal")
    interview.add_argument("--export-format")
    interview.add_argument("--value-proposition")
    interview.add_argument("--reader-problem")
    interview.add_argument("--sales-goal", default="")

    status = subparsers.add_parser("status", help="Show project status.")
    status.add_argument("project_id")

    approve = subparsers.add_parser("approve-concept", help="Approve concept and create outline.")
    approve.add_argument("project_id")
    approve.add_argument("--chapters", type=int)

    market = subparsers.add_parser("market", help="Prepare preliminary market assessment.")
    market.add_argument("project_id")

    publisher = subparsers.add_parser("publisher-offer", help="Prepare publisher offer draft.")
    publisher.add_argument("project_id")
    publisher.add_argument("--publisher", default="Target publisher")

    kdp = subparsers.add_parser("kdp-checklist", help="Prepare Amazon KDP upload checklist.")
    kdp.add_argument("project_id")

    subparsers.add_parser("models", help="Show configured Ollama model routing.")
    subparsers.add_parser("questions", help="Show configured interview questionnaire.")

    usage = subparsers.add_parser("usage", help="Show token and cost usage.")
    usage.add_argument("--project-id")

    token_log = subparsers.add_parser("token-log", help="Append a token usage record.")
    token_log.add_argument("--project-id", required=True)
    token_log.add_argument("--task", required=True)
    token_log.add_argument("--model", required=True)
    token_log.add_argument("--input-tokens", type=int, required=True)
    token_log.add_argument("--output-tokens", type=int, required=True)
    token_log.add_argument("--agent", default="")
    token_log.add_argument("--chapter-number", type=int)
    token_log.add_argument("--run-focus", default="")
    return parser


def run_interview(args: argparse.Namespace) -> int:
    workflow = BookProjectWorkflow()
    interview = Interview(
        topic=_value(args.topic, "topic"),
        target_audience=_value(args.target_audience, "target_audience"),
        book_type=_value(args.book_type, "book_type"),
        desired_result=_value(args.desired_result, "desired_result"),
        tone=_value(args.tone, "tone"),
        length_goal=_value(args.length_goal, "length_goal"),
        export_format=_value(args.export_format, "export_format"),
        value_proposition=_value(args.value_proposition, "value_proposition"),
        reader_problem=_value(args.reader_problem, "reader_problem"),
        sales_goal=args.sales_goal or "",
    )
    project, path = workflow.create_from_interview(args.name, interview)
    _print_project_summary(project)
    print(f"Saved: {path}")
    return 0 if not project.blockers else 2


def run_status(args: argparse.Namespace) -> int:
    project = JsonProjectStore().load(args.project_id)
    _print_project_summary(project)
    return 0


def run_approve_concept(args: argparse.Namespace) -> int:
    store = JsonProjectStore()
    project = store.load(args.project_id)
    updated = Orchestrator().approve_concept(project, chapter_count=args.chapters)
    path = store.save(updated)
    _print_project_summary(updated)
    print(f"Saved: {path}")
    return 0 if not updated.blockers else 2


def run_market(args: argparse.Namespace) -> int:
    store = JsonProjectStore()
    project = store.load(args.project_id)
    updated = Orchestrator().prepare_market_assessment(project)
    path = store.save(updated)
    _print_project_summary(updated)
    if updated.market_assessment:
        print(f"Sales chances: {updated.market_assessment.sales_chances}")
    print(f"Saved: {path}")
    return 0 if not updated.blockers else 2


def run_publisher_offer(args: argparse.Namespace) -> int:
    store = JsonProjectStore()
    project = store.load(args.project_id)
    updated = Orchestrator().prepare_publisher_offer(project, args.publisher)
    path = store.save(updated)
    _print_project_summary(updated)
    if updated.publisher_offers:
        print(f"Offer prepared for: {updated.publisher_offers[-1].target_publisher}")
    print(f"Saved: {path}")
    return 0 if not updated.blockers else 2


def run_kdp_checklist(args: argparse.Namespace) -> int:
    store = JsonProjectStore()
    project = store.load(args.project_id)
    updated = Orchestrator().prepare_kdp_checklist(project)
    path = store.save(updated)
    _print_project_summary(updated)
    latest = updated.publishing_checklists[-1]
    print(f"Checklist: {latest.platform} / {latest.status}")
    print(f"Saved: {path}")
    return 0 if not latest.blockers else 2


def run_models() -> int:
    profiles = load_model_profiles()
    print(f"Provider: {profiles.provider}")
    print(f"Base URL: {profiles.base_url}")
    print(f"Primary model: {profiles.primary_model}")
    print(f"Secondary model: {profiles.secondary_model}")
    print("Tasks:")
    for task, profile in sorted(profiles.tasks.items()):
        print(f"- {task}: {profile.model}")
    return 0


def run_questions() -> int:
    questions = load_interview_questions()
    current_stage = ""
    for question in questions:
        if question.stage != current_stage:
            current_stage = question.stage
            print(f"[{current_stage}]")
        required = "required" if question.required else "optional"
        print(f"- {question.field} ({required}): {question.prompt}")
    return 0


def run_usage(args: argparse.Namespace) -> int:
    summary = TokenUsageLedger().summary(project_id=args.project_id)
    print(f"Records: {summary.records}")
    print(f"Input tokens: {summary.input_tokens}")
    print(f"Output tokens: {summary.output_tokens}")
    print(f"Total tokens: {summary.total_tokens}")
    print(f"Estimated API cost: {summary.estimated_cost:.6f} {summary.currency}")
    return 0


def run_token_log(args: argparse.Namespace) -> int:
    record = TokenUsageLedger().append(
        TokenUsageRecord(
            project_id=args.project_id,
            task=args.task,
            model=args.model,
            input_tokens=args.input_tokens,
            output_tokens=args.output_tokens,
            agent=args.agent,
            chapter_number=args.chapter_number,
            run_focus=args.run_focus,
        )
    )
    print(f"Logged: {record.request_id}")
    print(f"Total tokens: {record.total_tokens}")
    print(f"Estimated API cost: {record.estimated_cost:.6f} {record.currency}")
    return 0


def _value(current: str | None, field: str) -> str:
    if current is not None:
        return current.strip()
    question = question_by_field(field)
    prompt = question.prompt if question else field
    return input(f"{prompt}: ").strip()


def _print_project_summary(project: BookProject) -> None:
    print(f"Project ID: {project.project_id}")
    print(f"Name: {project.name}")
    print(f"Stage: {project.stage}")
    print(f"Status: {project.status}")
    if project.concept:
        print(f"Concept: {project.concept.working_title} / {project.concept.status}")
    if project.outline:
        print(f"Outline chapters: {len(project.outline)}")
    if project.blockers:
        print("Blockers:")
        for blocker in project.blockers:
            print(f"- {blocker}")


if __name__ == "__main__":
    raise SystemExit(main())
