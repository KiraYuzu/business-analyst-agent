import json

from pathlib import Path
from agent.agent import run_agent
from agent.state import AgentState
from requirement.generator import generate_requirement
from requirement.validator import validate_requirement
from config import LOG_FOLDER

def print_header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def main():
    # Get the initial requirement from the user
    print_header("BUSINESS ANALYST AI")
    requirement = input("\n📝 Enter your business requirement:\n> ")

    # Create the initial state
    state: AgentState = {
        "requirement": requirement,
        "status": "REQUIREMENT_RECEIVED",
        "conversation_history": [],
        "completed": False
    }

    # --------------------------------
    # 1. Requirement Gathering
    # --------------------------------
    print_header("REQUIREMENT GATHERING")
    final_state = run_agent(state)
    save_json("agent_state.json", final_state)

    # --------------------------------
    # 2. Generate Requirement
    # --------------------------------

    print_header("GENERATING BUSINESS REQUIREMENT")
    structured_requirement = generate_requirement(final_state)
    save_json(
        "structured_requirement.json",
        structured_requirement
    )

    # --------------------------------
    # 3. Validate Requirement
    # --------------------------------

    print_header("VALIDATING REQUIREMENT")

    missing = validate_requirement(structured_requirement)

    validation_result = {
        "is_complete": len(missing) == 0,
        "missing_fields": missing
    }

    save_json(
        "validation_result.json",
        validation_result
    )

    # --------------------------------
    # 4. Display Result
    # --------------------------------
    if missing:
        print("\n⚠️  Requirement requires further clarification.\n")
        print("Missing information:")

        for item in missing:
            print(f"  • {item}")
    else:
        print("\n✅ Requirement is complete and ready for review.")

def save_json(filename, data):
    path = LOG_FOLDER / filename

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"💾 Saved: {path}")

if __name__ == "__main__":
    main()