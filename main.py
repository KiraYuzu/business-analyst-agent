from agent.agent import run_agent
from agent.state import AgentState


def main():
    # Get the initial requirement from the user
    requirement = input("Enter your business requirement:\n> ")

    # Create the initial state
    state: AgentState = {
        "requirement": requirement,
        "status": "REQUIREMENT_RECEIVED",
        "conversation_history": [],
        "completed": False
    }

    # Start the agent
    final_state = run_agent(state)

    # Display the final state
    print("\n=============================")
    print("FINAL STATE")
    print("=============================")
    print(final_state)


if __name__ == "__main__":
    main()