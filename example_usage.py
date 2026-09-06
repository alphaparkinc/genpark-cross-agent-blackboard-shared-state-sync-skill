"""
Demonstration of genpark-cross-agent-blackboard-shared-state-sync-skill
"""

from client import BlackboardSharedStateClient

def main():
    blackboard = BlackboardSharedStateClient()

    notifications = []
    # Agent 2 subscribes to 'mission_status'
    blackboard.subscribe("mission_status", lambda k, v, a: notifications.append(f"Received update from {a}: {k} -> {v}"))

    # Agent 1 updates shared state
    blackboard.set_key("mission_status", "IN_PROGRESS", agent_id="Agent_Planner")
    print("State 'mission_status':", blackboard.get_key("mission_status"))
    print("Notification triggered:", notifications)

    # Atomic CAS update
    cas_ok = blackboard.compare_and_swap("mission_status", "IN_PROGRESS", "COMPLETED", agent_id="Agent_Executor")
    print("Atomic CAS Success:", cas_ok)
    print("Final State:", blackboard.get_key("mission_status"))

if __name__ == "__main__":
    main()
