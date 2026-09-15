from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ActionRequest(BaseModel):
    agent_id: str
    action_type: str
    target: str

# Point 3: Risk-Based Action Classification
HIGH_RISK_ACTIONS = ["write_file", "execute_shell", "delete_file"]
LOW_RISK_ACTIONS = ["read_file", "list_dir", "get_status"]

# Point 13: Immutable Audit Logging (Simulated with an append-only list)
audit_log = []

@app.post("/request_action")
async def request_action(req: ActionRequest):
    # Log the attempt immediately
    audit_log.append({"status": "PENDING", "request": req.dict()})
    
    # Check action risk level
    if req.action_type in LOW_RISK_ACTIONS:
        audit_log[-1]["status"] = "APPROVED_AUTOMATIC"
        return {"status": "approved", "message": "Low-risk action auto-approved."}
        
    elif req.action_type in HIGH_RISK_ACTIONS:
        # Point 4: Human-in-the-Loop Controls
        print(f"\n[URGENT] Agent {req.agent_id} is requesting a HIGH RISK action: {req.action_type} on {req.target}")
        # In a real scenario, this would send a push notification to an admin.
        # Here we simulate waiting for an admin response.
        audit_log[-1]["status"] = "BLOCKED_PENDING_HUMAN"
        raise HTTPException(status_code=403, detail="High-risk action blocked. Requires human authorization.")
    
    else:
        audit_log[-1]["status"] = "DENIED_UNKNOWN_ACTION"
        raise HTTPException(status_code=400, detail="Unknown action type denied by default.")

@app.get("/logs")
async def get_logs():
    return {"audit_log": audit_log}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
