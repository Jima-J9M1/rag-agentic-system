class EscalationHandler:
    def escalate(self, reason: str, payload: dict):
        print("⚠️ HUMAN ESCALATION REQUIRED")
        print("Reason:", reason)
        print("Payload:", payload)

        return {
            "status": "needs_human_review",
            "reason": reason
        }
