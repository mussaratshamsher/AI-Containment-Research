import time
import subprocess
import requests

AGENT_CONTAINER_NAME = "rogue-agent-container"
GATEWAY_LOGS_URL = "http://localhost:8000/logs"

def check_agent_behavior():
    try:
        response = requests.get(GATEWAY_LOGS_URL)
        if response.status_code == 200:
            logs = response.json().get("audit_log", [])
            
            # Point 8 & 10: Trajectory-level monitoring & Predefined boundaries
            denied_count = 0
            for entry in logs[-5:]: # Look at the last 5 actions
                if entry["status"] in ["DENIED_UNKNOWN_ACTION", "BLOCKED_PENDING_HUMAN"]:
                    denied_count += 1
            
            # If the agent attempts 3 unauthorized actions in a row, trigger shutdown
            if denied_count >= 3:
                trigger_emergency_shutdown("Agent exceeded unauthorized action threshold (3 strikes).")
    except Exception as e:
        # Gateway might not be up yet, or connection failed
        pass

def trigger_emergency_shutdown(reason: str):
    print(f"\n[CRITICAL ALERT] {reason}")
    print("[KILL SWITCH ACTIVATED] Initiating Containment Protocol...")
    
    # Point 7 & 14: Containment Before Destruction
    print("1. Isolating Network (Disconnecting container from default network)...")
    subprocess.run(["docker", "network", "disconnect", "bridge", AGENT_CONTAINER_NAME], capture_output=True)
    
    print("2. Suspending Compute (Pausing container)...")
    subprocess.run(["docker", "pause", AGENT_CONTAINER_NAME], capture_output=True)
    
    # Point 6: Credential Revocation (Simulated)
    print("3. Revoking Agent API Keys via IAM...")
    
    print("Containment Complete. Awaiting human forensic review.")
    exit(0)

if __name__ == "__main__":
    print("Independent Kill Switch Armed. Monitoring Agent Trajectory...")
    while True:
        check_agent_behavior()
        time.sleep(2) # Poll every 2 seconds
