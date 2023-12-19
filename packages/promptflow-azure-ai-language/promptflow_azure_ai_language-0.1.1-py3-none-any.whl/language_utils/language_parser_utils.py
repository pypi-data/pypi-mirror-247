from language_utils.language_skill import LanguageSkill
from language_utils.language_mode import LanguageMode


# Obtains 'results' field from an async response with a single task.
def get_async_results(response):
    json_res = response.json()
    return json_res["tasks"]["items"][0]["results"]


# Obtains 'results' field from an sync response.
def get_sync_results(response):
    json_res = response.json()
    if "results" in json_res:
        return json_res["results"]
    else:
        return json_res


# Return abstractive summary.
def parse_abstractive_summarization(doc_result: dict) -> str:
    return doc_result["summaries"][0]["text"]


# Return extracted summaries.
def parse_extractive_summarization(doc_result: dict) -> list[str]:
    sentences = doc_result["sentences"]
    return [s["text"] for s in sentences]


# Return aspect summary or summaries.
def parse_conversation_summarization(conv_result: dict):
    summaries = conv_result["summaries"]
    if len(summaries) == 1:
        return summaries[0]["text"]

    aspect_summaries = []
    for summary in summaries:
        aspect_summaries.append(summary["text"])
    return aspect_summaries


# Return redacted text.
def parse_pii(doc_result: dict) -> str:
    return doc_result["redactedText"]


# Return analyzed sentiment.
def parse_sentiment_analysis(doc_result: dict) -> str:
    return doc_result["sentiment"]


# Return detected language code.
def parse_language_detection(doc_result: dict) -> str:
    return doc_result["detectedLanguage"]["iso6391Name"]


# Return extracted key-phrases.
def parse_keyphrase_extraction(doc_result: dict) -> list[str]:
    return doc_result["keyPhrases"]


# Return recognized entities.
def parse_entity_recognition(doc_result: dict) -> dict[str, str]:
    entities = doc_result["entities"]
    recognized_entities = {}
    for entity in entities:
        recognized_entities[entity["text"]] = entity["category"]
    return recognized_entities


# Return user utterances and associated intents.
def parse_clu(clu_result: dict) -> dict[str, str]:
    utterance = clu_result["query"]
    top_intent = clu_result["prediction"]["topIntent"]
    return {"utterance": utterance, "intent": top_intent}


# Return translations.
def parse_translation(translations: list[dict]) -> dict[str, str]:
    parsed_translations = {}
    for translation in translations:
        parsed_translations[translation["to"]] = translation["text"]
    return parsed_translations


# Generate results func based on mode.
def generate_results_func(mode: LanguageMode):
    return get_sync_results if mode == LanguageMode.SYNC else get_async_results


# Generate function to obtain single task result
# based on if input was a document or conversation.
# For CLU the task result is under the "result" property:
# https://learn.microsoft.com/en-us/rest/api/language/2023-04-01/conversation-analysis-runtime/analyze-conversation?tabs=HTTP#conversation-project-result
def generate_inter_func(skill: LanguageSkill):
    if skill == LanguageSkill.CONVERSATION_SUMMARIZATION:
        return lambda results: results["conversations"][0]
    elif skill == LanguageSkill.CONVERSATIONAL_LANGUAGE_UNDERSTANDING:
        return lambda results: results["result"]
    elif skill == LanguageSkill.TRANSLATION:
        return lambda results: results[0]["translations"]
    else:
        return lambda results: results["documents"][0]


skill_to_parser_func = {
    LanguageSkill.ABSTRACTIVE_SUMMARIZATION: parse_abstractive_summarization,
    LanguageSkill.EXTRACTIVE_SUMMARIZATION: parse_extractive_summarization,
    LanguageSkill.CONVERSATION_SUMMARIZATION: parse_conversation_summarization,
    LanguageSkill.PII: parse_pii,
    LanguageSkill.SENTIMENT_ANALYSIS: parse_sentiment_analysis,
    LanguageSkill.ENTITY_RECOGNITION: parse_entity_recognition,
    LanguageSkill.KEY_PHRASE_EXTRACTION: parse_keyphrase_extraction,
    LanguageSkill.LANGUAGE_DETECTION: parse_language_detection,
    LanguageSkill.CONVERSATIONAL_LANGUAGE_UNDERSTANDING: parse_clu,
    LanguageSkill.TRANSLATION: parse_translation
}


# Generate parsing function based on skill.
def generate_parser_func(skill: LanguageSkill):
    return skill_to_parser_func.get(skill, lambda _: "Unrecognized skill")


# Parse API response.
def parse_response(response, skill: LanguageSkill, mode: LanguageMode):
    try:
        results = generate_results_func(mode)(response)
        task_result = generate_inter_func(skill)(results)
        parsed_result = generate_parser_func(skill)(task_result)
        return parsed_result
    except (KeyError, ValueError) as error:
        print(error)
        return None
