
class DialogueQualityValidator:
    def validate(self, dialogue):
        issues = []
        texts = " ".join(m.get("text","") for m in dialogue.get("messages",[]))
        if not texts: issues.append("EMPTY_DIALOGUE")
        if any(p in texts for p in ["{{","[PLACEHOLDER]","TODO","TBD","lorem"]): issues.append("PLACEHOLDER")
        return {"approved": len(issues)==0, "issues": issues, "status": "DIALOGUE_APPROVED" if len(issues)==0 else "DIALOGUE_REPAIR_REQUIRED"}
