import json
from openai import OpenAI

client = OpenAI()


REQUIREMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string"
        },
        "purpose": {
            "type": "string"
        },
        "target_users": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "features": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "business_rules": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "workflow": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "open_questions": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": [
        "title",
        "purpose",
        "target_users",
        "features",
        "business_rules",
        "workflow",
        "open_questions"
    ],
    "additionalProperties": False
}


GENERATOR_PROMPT = """
You are a Business Analyst AI.

Convert the conversation and retrieved company information
into a structured business requirement.

Only use information provided by the user or retrieved
from company documents.

Do not invent requirements.

If information is missing, leave the field empty and add
the missing information to open_questions.
"""


def generate_requirement(state):

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=GENERATOR_PROMPT,
        input=json.dumps(state),
        text={
            "format": {
                "type": "json_schema",
                "name": "requirement_schema",
                "strict": True,
                "schema": REQUIREMENT_SCHEMA
            }
        }
    )

    return json.loads(response.output_text)