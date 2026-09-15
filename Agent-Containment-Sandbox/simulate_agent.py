import requests
import time

GATEWAY_URL = "http://localhost:8000/request_action"

def attempt_action(action_type, target):
    print(f"\n[Agent] Attempting action: {action_type} on {target}...")
    try:
        payload = {
            "agent_id": "test-agent-001",
            "action_type": action_type,
            "target": target
        }
        response = requests.post(GATEWAY_URL, json=payload)
        if response.status_code == 200:
            print(f"[Agent] Success: {response.json().get('message')}")
        else:
            print(f"[Agent] Blocked ({response.status_code}): {response.json().get('detail')}")
    except requests.exceptions.ConnectionError:
        print("[Agent] Error: Cannot connect to the Gateway. Is it running?")

if __name__ == "__main__":
    print("Starting simulated agent...")
    
    # 1. Normal behavior (Low risk)
    time.sleep(1)
    attempt_action("read_file", "data.csv")
    
    # 2. Agent goes rogue and tries to run unauthorized commands rapidly
    time.sleep(2)
    print("\n--- Agent Behavior Diverges (Going Rogue) ---")
    
    attempt_action("execute_shell", "rm -rf /") # Strike 1
    time.sleep(3)
    attempt_action("write_file", "malicious_payload.sh") # Strike 2
    time.sleep(3)
    attempt_action("delete_file", "audit_logs.txt") # Strike 3 - Should trigger the Kill Switch!
    
    print("\n[Agent] Attempting to continue execution...")
    time.sleep(2)
    attempt_action("read_file", "secret_keys.env")
