import time
from language_utils.language_skill import LanguageSkill
from language_utils.language_mode import LanguageMode


# Creates a simple task name given a skill and id.
# e.g. "AbstractiveSummarization Task 1"
def create_task_name(skill: LanguageSkill, id: int) -> str:
    return LanguageSkill.to_str(skill) + " Task " + str(id)


# Formats a task with its kind and name.
def format_task(task: dict) -> dict:
    skill = task["skill"]
    del task["skill"]
    task["kind"] = LanguageSkill.to_str(skill)
    task["taskName"] = create_task_name(skill, 1)
    return task


# Formats a single document with an id given a {text, language} dict.
def format_document(doc: dict) -> dict:
    doc["id"] = "1"
    return doc


# Creates a conversation item from a speaker's line and id.
def create_conversation_item(line: str, id: int) -> dict:
    name_and_text = line.split(":", maxsplit=1)
    name = name_and_text[0].strip()
    text = name_and_text[1].strip()
    return {
        "id": id,
        "participantId": name,
        "role": name if name.lower() in {"customer", "agent"} else "generic",
        "text": text
    }


# Creates a list of conversation items from a text conversation.
def create_conversation_items(text: str) -> list[dict]:
    conversation_items = []
    id = 1
    lines = text.replace("  ", "\n").split("\n")
    lines = filter(lambda line: len(line.strip()) != 0, lines)
    for line in lines:
        conversation_items.append(create_conversation_item(line, id))
        id += 1
    return conversation_items


# Formats a conversation from a {text, language, modality} dict.
def format_conversation(conv: dict) -> dict:
    text = conv["text"]
    del conv["text"]
    conv["id"] = "input 1"
    conv["conversationItems"] = create_conversation_items(text)
    return conv


# Format CLU conversation item given a {text, language, modality} dict.
def format_clu(input):
    input["id"] = "1"
    input["participantId"] = "1"
    return input


# Function to obtain "analysisInput" field of API input based on skill.
def analysis_input_func(skill: LanguageSkill):
    if skill == LanguageSkill.CONVERSATION_SUMMARIZATION:
        return lambda input: {"conversations": [format_conversation(input)]}
    elif skill == LanguageSkill.CONVERSATIONAL_LANGUAGE_UNDERSTANDING:
        return lambda input: {"conversationItem": format_clu(input)}
    else:
        return lambda input: {"documents": [format_document(input)]}


# Function to format sync input based on skill.
def format_sync_func(skill: LanguageSkill):
    if skill == LanguageSkill.TRANSLATION:
        return lambda input, _: [input]
    return lambda input, parameters: {
        "kind": LanguageSkill.to_str(skill),
        "analysisInput": analysis_input_func(skill)(input),
        "parameters": parameters
    }


# Function to format async input based on skill.
def format_async_func(skill: LanguageSkill):
    return lambda input, parameters: {
        "displayName": LanguageSkill.to_str(skill) + "Job:" + str(time.time()),
        "analysisInput": analysis_input_func(skill)(input),
        "tasks": [format_task({"skill": skill, "parameters": parameters})]
    }


# Format input based on skill and mode.
def format_input(input: dict,
                 parameters: dict,
                 skill: LanguageSkill,
                 mode: LanguageMode) -> dict:
    if mode == LanguageMode.SYNC:
        format_func = format_sync_func(skill)
    else:
        format_func = format_async_func(skill)
    return format_func(input, parameters)
