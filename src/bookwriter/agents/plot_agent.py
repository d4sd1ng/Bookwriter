from __future__ import annotations

from bookwriter.agents.base import AgentResult
from bookwriter.domain.models import BookProject, Plot, PlotPoint, Treatment, TreatmentSection
from bookwriter.domain.status import ApprovalStatus


class PlotAgent:
    name = "Plot Agent"

    def run(self, project: BookProject) -> AgentResult[Plot]:
        interview = project.interview
        focus = interview.narrative_focus or "handlungsorientiert"
        points = [
            PlotPoint(
                sequence=1,
                title="Ausgangslage",
                function="Figur, Thema oder Leserproblem etablieren.",
                conflict="Status quo gegen Veraenderungsdruck",
                outcome="Zentrale Frage wird sichtbar.",
            ),
            PlotPoint(
                sequence=2,
                title="Ausloeser",
                function="Die Handlung oder Argumentation in Bewegung setzen.",
                conflict="Vermeidung gegen notwendige Entscheidung",
                outcome="Der Weg ist nicht mehr neutral.",
            ),
            PlotPoint(
                sequence=3,
                title="Konfrontation",
                function=f"{focus} zuspitzen.",
                conflict="Ziel gegen Hindernisse",
                outcome="Kosten und Konsequenzen werden klar.",
            ),
            PlotPoint(
                sequence=4,
                title="Wendepunkt",
                function="Neue Erkenntnis oder irreversible Entscheidung.",
                conflict="alte Loesung gegen neue Wahrheit",
                outcome="Finale Richtung steht fest.",
            ),
            PlotPoint(
                sequence=5,
                title="Aufloesung",
                function=f"Ende-Typ einloesen: {interview.ending_type}.",
                conflict="Erwartung gegen Ergebnis",
                outcome="Leser versteht die Konsequenz.",
            ),
        ]
        plot = Plot(
            structure=points,
            tension_arc=(
                f"Der Spannungsbogen folgt einem {focus}en Aufbau fuer "
                f"{interview.age_group}."
            ),
            turning_points=["Ausloeser", "Konfrontation", "Wendepunkt", "Aufloesung"],
            logic_questions=[
                "Sind Motivation und Ziel durchgehend nachvollziehbar?",
                "Passt das Ende zur gesetzten Leserwartung?",
            ],
            status=ApprovalStatus.PENDING_REVIEW,
        )
        return AgentResult(
            agent=self.name,
            output=plot,
            status=plot.status,
            notes=["Plot created and waiting for approval."],
        )


class TreatmentAgent:
    name = "Treatment Agent"

    def run(self, project: BookProject) -> AgentResult[Treatment]:
        if project.plot is None:
            raise ValueError("Treatment requires a plot.")
        sections = [
            TreatmentSection(
                sequence=point.sequence,
                title=point.title,
                summary=f"{point.function} Ergebnis: {point.outcome}",
                purpose=point.conflict,
            )
            for point in project.plot.structure
        ]
        treatment = Treatment(
            sections=sections,
            open_questions=[
                "Welche Szenen oder Abschnitte brauchen Quellen?",
                "Welche Kapitelgrenzen ergeben sich aus dem Treatment?",
            ],
            status=ApprovalStatus.PENDING_REVIEW,
        )
        return AgentResult(
            agent=self.name,
            output=treatment,
            status=treatment.status,
            notes=["Treatment created and waiting for approval."],
        )
