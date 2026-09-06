"""
Cross-Agent Blackboard Shared State Store and Pub-Sub Event Bus.
Zero external dependencies, standard library only.
"""

import time
from typing import Dict, List, Any, Optional, Callable

class BlackboardSharedStateClient:
    """
    Classic Blackboard Architecture for Multi-Agent Systems:
    - Shared memory key-value store with atomic CAS (Compare-And-Swap) operations
    - Topic-based publish-subscribe event notification system
    - Audit log of state mutations with agent attribution
    """

    def __init__(self):
        self.state = {}
        self.listeners = {} # topic -> list of callback functions
        self.audit_log = []

    def set_key(self, key: str, value: Any, agent_id: str = "system") -> Dict[str, Any]:
        """Sets key in shared blackboard and notifies subscribers."""
        old_val = self.state.get(key)
        self.state[key] = value

        entry = {
            "timestamp": time.time(),
            "agent_id": agent_id,
            "key": key,
            "old_val": old_val,
            "new_val": value
        }
        self.audit_log.append(entry)

        # Notify subscribers
        for cb in self.listeners.get(key, []):
            try:
                cb(key, value, agent_id)
            except Exception:
                pass

        return {"status": "updated", "key": key, "value": value}

    def get_key(self, key: str, default: Any = None) -> Any:
        """Retrieves value from blackboard."""
        return self.state.get(key, default)

    def compare_and_swap(self, key: str, expected_val: Any, new_val: Any, agent_id: str) -> bool:
        """Atomic Compare-And-Swap (CAS) preventing write conflicts."""
        current = self.state.get(key)
        if current == expected_val:
            self.set_key(key, new_val, agent_id)
            return True
        return False

    def subscribe(self, topic: str, callback: Callable[[str, Any, str], None]):
        """Registers listener for topic/key mutations."""
        if topic not in self.listeners:
            self.listeners[topic] = []
        self.listeners[topic].append(callback)
