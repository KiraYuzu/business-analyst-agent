import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

from agent.prompts import SYSTEM_PROMPT
from tools.ask_user import ask_user

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

AVAILABLE_ACTIONS = ["ask_user", "finish"]

## Define the decision schema for the LLM's response
DECISION_SCHEMA = {
    "type": "object",
    "properties": {
        "action":{
            "type": "string",
            "enum": AVAILABLE_ACTIONS,
        },
        "reason": {
            "type": "string"
        },
        "question": {
            "type": "string"
        }
    },
    "required": [
        "action",
        "reason",
        "question"
    ],
    "additionalProperties": False
}

def save_debug_state(state):
    with open("debug_state.json", "w") as file:
        json.dump(state, file, indent=4)

def ask_llm(state):
    """
    This function sends the current state of the agent to the LLM and receives a response.
    It uses the SYSTEM_PROMPT to guide the LLM's behavior and expects a JSON response
    that adheres to the DECISION_SCHEMA.
    """
    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=SYSTEM_PROMPT,
        input=json.dumps(state),
        text={
            "format": {
                "type": "json_schema",
                "name": "decision_schema",
                "strict": True,
                "schema": DECISION_SCHEMA
            }
        }
    )
    
    # Extract the content from the LLM's response
    llm_output = response.output[0].content[0].text
    print(f"LLM Output: {llm_output}")  # Debugging line to see the raw output from the LLM
    return json.loads(llm_output)

def update_state(state, action, reason, question=None):
    """
    This function updates the agent's state based on the action taken by the LLM.
    It modifies the 'status' and 'conversation_history' fields of the state.
    If the action is 'finish', it also sets 'completed' to True.
    """
    state["conversation_history"].append({
        "action": action,
        "reason": reason,
        "question": question
    })

    if action == "ask_user":
        state["status"] = "NEED_CLARIFICATION"
    elif action == "finish":
        state["status"] = "REQUIREMENT_COMPLETE"
        state["completed"] = True
    
    return state

def run_agent(state):
    """
    This function runs the agent in a loop until the requirement is completed.
    It continuously asks the LLM for actions and updates the state accordingly.
    If the LLM decides to ask the user a question, it uses the ask_user function
    to get the user's input and updates the state with the response.
    """

    while not state["completed"]:
        decision = ask_llm(state) ## 1. Ask LLM what should happen next
        action = decision["action"]
        reason = decision["reason"]
        question = decision.get("question")

        # 2. Execute the selected action
        if action == "ask_user" and question:
            user_response = ask_user(question)
            # 3. Store the conversation in the state, state means the current state of the agent, which includes the requirement, status, conversation history, and completion status.
            state["conversation_history"].append({
                "action": "ask_user",
                "response": user_response
            })

        state = update_state(state, action, reason, question)

        # Save the current state to a debug file for inspection
        save_debug_state(state)
        
    return state

