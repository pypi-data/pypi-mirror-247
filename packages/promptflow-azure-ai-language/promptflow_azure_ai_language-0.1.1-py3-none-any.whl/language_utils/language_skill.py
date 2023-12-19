from enum import Enum
from language_utils.language_mode import LanguageMode

MAX_SYNC_CHARS = 5120
MAX_ASYNC_CHARS = 125000
MAX_TRANSLATION_CHARS = 50000
CONVERSATION_SKILL_BOUNDARY = 2


# Supported language skills:
class LanguageSkill(Enum):
    # Conversation:
    CONVERSATION_SUMMARIZATION = 0
    CONVERSATIONAL_LANGUAGE_UNDERSTANDING = 1
    # Document:
    ABSTRACTIVE_SUMMARIZATION = 2
    EXTRACTIVE_SUMMARIZATION = 3
    PII = 4
    SENTIMENT_ANALYSIS = 5
    ENTITY_RECOGNITION = 6
    KEY_PHRASE_EXTRACTION = 7
    LANGUAGE_DETECTION = 8
    # Translation:
    TRANSLATION = 9

    @staticmethod
    def to_str(skill):
        return skill_to_str.get(skill, "Unsupported")

    # Does skill deal with conversations rather than documents?
    @staticmethod
    def is_conversational(skill):
        return skill.value < CONVERSATION_SKILL_BOUNDARY

    @staticmethod
    def is_async_capable(skill):
        return skill_to_async_capabilities.get(skill, False)

    @staticmethod
    def get_mode(skill, num_chars):
        mode = skill_to_default_mode.get(skill, LanguageMode.SYNC)

        if mode == LanguageMode.SYNC and num_chars > get_max_sync_chars(skill):
            if LanguageSkill.is_async_capable(skill):
                mode = LanguageMode.ASYNC
            else:
                raise RuntimeError("Unable to process this many tokens.")

        if mode == LanguageMode.ASYNC and num_chars > MAX_ASYNC_CHARS:
            raise RuntimeError("Unable to process this many tokens.")

        return mode

    @staticmethod
    def get_inter_path(skill, mode):
        if skill == LanguageSkill.TRANSLATION:
            return "/translate"
        elif LanguageSkill.is_conversational(skill):
            return conversation_inter_paths[mode]
        else:
            return document_inter_paths[mode]


def get_max_sync_chars(skill):
    if skill == LanguageSkill.TRANSLATION:
        return MAX_TRANSLATION_CHARS
    else:
        return MAX_SYNC_CHARS


skill_to_str = {
    LanguageSkill.ABSTRACTIVE_SUMMARIZATION: "AbstractiveSummarization",
    LanguageSkill.EXTRACTIVE_SUMMARIZATION: "ExtractiveSummarization",
    LanguageSkill.CONVERSATION_SUMMARIZATION:
        "ConversationalSummarizationTask",
    LanguageSkill.PII: "PiiEntityRecognition",
    LanguageSkill.SENTIMENT_ANALYSIS: "SentimentAnalysis",
    LanguageSkill.ENTITY_RECOGNITION: "EntityRecognition",
    LanguageSkill.KEY_PHRASE_EXTRACTION: "KeyPhraseExtraction",
    LanguageSkill.LANGUAGE_DETECTION: "LanguageDetection",
    LanguageSkill.CONVERSATIONAL_LANGUAGE_UNDERSTANDING: "Conversation",
    LanguageSkill.TRANSLATION: "Translate"
}

skill_to_async_capabilities = {
    LanguageSkill.ABSTRACTIVE_SUMMARIZATION: True,
    LanguageSkill.EXTRACTIVE_SUMMARIZATION: True,
    LanguageSkill.CONVERSATION_SUMMARIZATION: True,
    LanguageSkill.PII: True,
    LanguageSkill.SENTIMENT_ANALYSIS: True,
    LanguageSkill.ENTITY_RECOGNITION: True,
    LanguageSkill.KEY_PHRASE_EXTRACTION: True,
    LanguageSkill.LANGUAGE_DETECTION: False,
    LanguageSkill.CONVERSATIONAL_LANGUAGE_UNDERSTANDING: False,
    LanguageSkill.TRANSLATION: False
}

skill_to_default_mode = {
    LanguageSkill.ABSTRACTIVE_SUMMARIZATION: LanguageMode.ASYNC,
    LanguageSkill.EXTRACTIVE_SUMMARIZATION: LanguageMode.ASYNC,
    LanguageSkill.CONVERSATION_SUMMARIZATION: LanguageMode.ASYNC,
    LanguageSkill.PII: LanguageMode.SYNC,
    LanguageSkill.SENTIMENT_ANALYSIS: LanguageMode.SYNC,
    LanguageSkill.ENTITY_RECOGNITION: LanguageMode.SYNC,
    LanguageSkill.KEY_PHRASE_EXTRACTION: LanguageMode.SYNC,
    LanguageSkill.LANGUAGE_DETECTION: LanguageMode.SYNC,
    LanguageSkill.CONVERSATIONAL_LANGUAGE_UNDERSTANDING: LanguageMode.SYNC,
    LanguageSkill.TRANSLATION: LanguageMode.SYNC
}

document_inter_paths = {
    LanguageMode.SYNC: "/language/:analyze-text",
    LanguageMode.ASYNC: "/language/analyze-text/jobs"
}

conversation_inter_paths = {
    LanguageMode.SYNC: "/language/:analyze-conversations",
    LanguageMode.ASYNC: "/language/analyze-conversations/jobs"
}
