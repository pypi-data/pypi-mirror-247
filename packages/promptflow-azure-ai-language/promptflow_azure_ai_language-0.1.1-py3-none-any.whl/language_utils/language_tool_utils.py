import requests
from language_utils.language_skill import LanguageSkill
from language_utils.language_client import LanguageClient
from language_utils.language_formatter_utils import format_input
from language_utils.language_parser_utils import parse_response


# Runs a language skill given its config.
def run_language_skill(skill_config: dict):
    # Obtain config info:
    api_key = skill_config["connection"].secrets["api_key"]
    endpoint = skill_config["connection"].configs["endpoint"]
    region = skill_config["connection"].configs.get("region", None)

    max_retries = skill_config["max_retries"]
    max_wait = skill_config["max_wait"]

    query_parameters = skill_config["query_parameters"]
    input = skill_config["input"]
    task_parameters = skill_config["task_parameters"]
    skill = skill_config["skill"]

    # Translation skill has field "Text" instead of "text":
    if "Text" in input:
        input_length = len(input["Text"])
    else:
        input_length = len(input["text"])

    mode = LanguageSkill.get_mode(skill, input_length)
    inter_path = LanguageSkill.get_inter_path(skill, mode)

    # Create json input:
    json_input = format_input(input=input,
                              parameters=task_parameters,
                              skill=skill,
                              mode=mode)
    print(f"Input: {json_input}")

    # Create client and submit request:
    client = LanguageClient(endpoint=endpoint,
                            inter_path=inter_path,
                            api_key=api_key,
                            region=region)

    response = client.run_endpoint(json_obj=json_input,
                                   query_parameters=query_parameters,
                                   mode=mode,
                                   max_retries=max_retries,
                                   max_wait=max_wait)
    print(f"Status code: {response.status_code}")

    try:
        response.raise_for_status()
        json_response = response.json()
        print(f"Response: {json_response}")

        if skill_config["parse_response"]:
            # Parse response:
            return parse_response(response=response, skill=skill, mode=mode)

        return json_response
    except requests.HTTPError as error:
        print(error)
        return error
