from __future__ import annotations

from bookwriter.agents.base import AgentResult
from bookwriter.domain.models import BrainstormingFunnel, IdeaProposal
from bookwriter.domain.status import ApprovalStatus


class BrainstormAgent:
    name = "Brainstorm Agent"

    def create_funnel(self, seed: str = "") -> AgentResult[BrainstormingFunnel]:
        topic_seed = seed.strip() or "ein neues Buchprojekt"
        proposals = [
            IdeaProposal(
                title=f"Der erste Schritt zu {topic_seed}",
                category="Sachbuch",
                target_audience="Erwachsene Einsteiger",
                premise=f"Ein klarer Leitfaden, der {topic_seed} praktisch erklaert.",
                what_if=f"Was waere, wenn Leser {topic_seed} ohne Vorwissen anwenden koennten?",
                conflict="Unsicherheit gegen klare Handlungsschritte",
                format_hint="E-Book oder Taschenbuch",
            ),
            IdeaProposal(
                title=f"Die Geschichte hinter {topic_seed}",
                category="Belletristik",
                target_audience="Young Adult oder Erwachsene",
                premise="Eine Figur muss eine Entscheidung treffen, die ihr Leben veraendert.",
                what_if=f"Was waere, wenn {topic_seed} als persoenlicher Konflikt erzaehlt wird?",
                conflict="innerer Wandel gegen aeusseren Druck",
                format_hint="Taschenbuch oder E-Book",
            ),
            IdeaProposal(
                title=f"{topic_seed} fuer junge Leser",
                category="Kinder- und Jugendbuch",
                target_audience="Kinder oder Jugendliche",
                premise="Ein altersgerechtes Abenteuer vermittelt ein klares Thema.",
                what_if=f"Was waere, wenn Kinder {topic_seed} durch eine Figur erleben?",
                conflict="Neugier gegen Hindernisse",
                format_hint="Hardcover oder Vorlesebuch",
            ),
            IdeaProposal(
                title=f"Praxisbuch {topic_seed}",
                category="Fachbuch",
                target_audience="Fachpublikum",
                premise="Ein strukturiertes Werk mit Methoden, Beispielen und Checklisten.",
                what_if=f"Was waere, wenn {topic_seed} als Arbeitsbuch aufgebaut wird?",
                conflict="Komplexitaet gegen systematische Anwendung",
                format_hint="Softcover/Broschur",
            ),
            IdeaProposal(
                title=f"Kleine Geschichten ueber {topic_seed}",
                category="Vorlesebuch",
                target_audience="juengere Kinder",
                premise="Kurze Episoden mit wiederkehrenden Figuren und klarer Botschaft.",
                what_if=f"Was waere, wenn {topic_seed} in fuenf kurzen Geschichten erklaert wird?",
                conflict="Alltagssituation gegen kleine Herausforderung",
                format_hint="Hardcover",
            ),
        ]
        funnel = BrainstormingFunnel(
            seed=topic_seed,
            proposals_5=proposals,
            proposals_3=proposals[:3],
            selected_1=proposals[0],
            status=ApprovalStatus.PENDING_REVIEW,
        )
        return AgentResult(
            agent=self.name,
            output=funnel,
            status=funnel.status,
            notes=["Brainstorming funnel created with 5, 3, and 1 proposal levels."],
        )
