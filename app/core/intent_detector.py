from enum import Enum
from typing import Optional
from pydantic import BaseModel
from app.core.llm import get_llm


class Intent(str, Enum):
    GREETING = "greeting"
    SERVICE_CLIENT = "service_client"
    OTHER = "other"


class IntentResult(BaseModel):
    #Resultat de la detection d'intention
    intent: Intent
    response: Optional[str] = None


class IntentDetector:
    _instance: Optional["IntentDetector"] = None

    # Patterns de salutations avec leurs reponses
    GREETING_PATTERNS = {
        "bonjour": "Bonjour ! Comment puis-je vous aider ?",
        "bonsoir": "Bonsoir ! Comment puis-je vous aider ?",
        "salut": "Salut ! Comment puis-je vous aider ?",
        "hello": "Bonjour ! Comment puis-je vous aider ?",
        "hi": "Bonjour ! Comment puis-je vous aider ?",
        "coucou": "Bonjour ! Comment puis-je vous aider ?",
        "merci": "Je vous en prie ! N'hesitez pas si vous avez d'autres questions.",
        "thanks": "Je vous en prie ! N'hesitez pas si vous avez d'autres questions.",
        "au revoir": "Au revoir ! Bonne journee !",
        "bye": "Au revoir ! Bonne journee !",
        "a bientot": "A bientot ! Bonne journee !",
        "je ne comprends pas": "Je suis desole si ma reponse n'etait pas claire. Pouvez-vous reformuler votre question ?",
        "pas clair": "Je suis desole si ma reponse n'etait pas claire. Pouvez-vous reformuler votre question ?",
        "c'est clair": "Parfait ! Avez-vous d'autres questions ?",
        "ok": "Parfait ! Avez-vous d'autres questions ?",
        "d'accord": "Parfait ! Avez-vous d'autres questions ?",
        "compris": "Parfait ! Avez-vous d'autres questions ?",
    }

    OTHER_RESPONSE = (
        "Je suis un assistant specialise dans le service client. "
        "Je ne peux pas vous aider sur ce sujet. "
        "Avez-vous une question concernant nos services ?"
    )

    CLASSIFICATION_PROMPT = """Tu es un classificateur d'intentions. Analyse le message et retourne UNIQUEMENT une des 3 categories.

CATEGORIES:
1. "greeting" - Salutations et messages de politesse: bonjour, salut, merci, au revoir, je ne comprends pas, c'est clair, ok, d'accord
2. "service_client" - Questions sur le service client, compte, paiement, problemes techniques, fonctionnalites de l'application
3. "other" - Tout le reste (questions generales, hors champ de competence du service client)

Message: "{question}"

Reponds avec UN SEUL MOT: greeting, service_client ou other"""

    def __init__(self):
        self.llm = get_llm()

    def _check_greeting_pattern(self, question: str) -> Optional[str]:
        """Verifie si le message correspond a un pattern de salutation."""
        question_lower = question.lower().strip()

        # Verification exacte ou contenance
        for pattern, response in self.GREETING_PATTERNS.items():
            if pattern in question_lower or question_lower == pattern:
                return response
        return None

    def classify(self, question: str) -> IntentResult:
        """Classifie le message en une des 3 intentions."""
        # 1. Verification rapide des patterns de salutation (sans LLM)
        greeting_response = self._check_greeting_pattern(question)
        if greeting_response:
            return IntentResult(intent=Intent.GREETING, response=greeting_response)

        # 2. Classification via LLM pour les autres cas
        prompt = self.CLASSIFICATION_PROMPT.format(question=question)
        response = self.llm.invoke(prompt)

        # Extraire la reponse du LLM
        if isinstance(response.content, list) and len(response.content) > 0:
            intent_text = response.content[0].get('text', '').strip().lower()
        elif isinstance(response.content, str):
            intent_text = response.content.strip().lower()
        else:
            intent_text = str(response.content).strip().lower()


        if "greeting" in intent_text:
            # Si le LLM detecte greeting mais pas de pattern, reponse generique
            return IntentResult(
                intent=Intent.GREETING,
                response="Comment puis-je vous aider ?"
            )
        elif "service_client" in intent_text:
            return IntentResult(intent=Intent.SERVICE_CLIENT)
        else:
            return IntentResult(intent=Intent.OTHER, response=self.OTHER_RESPONSE)

    def get_greeting_response(self, question: str) -> str:
        """Retourne une reponse appropriee pour les salutations."""
        response = self._check_greeting_pattern(question)
        return response or "Bonjour ! Comment puis-je vous aider ?"

    def get_other_response(self) -> str:
        """Retourne le message pour les questions hors champ."""
        return self.OTHER_RESPONSE


_detector_instance: Optional[IntentDetector] = None


def get_intent_detector() -> IntentDetector:
    #Factory singleton pour IntentDetector
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = IntentDetector()
    return _detector_instance
