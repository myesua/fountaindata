from typing import Dict, Any, Tuple

def assess_risk(old_schema: Dict[str, Any], new_schema: Dict[str, Any]) -> Tuple[str, str]:
    old_required = set(old_schema.get('required', []))
    new_required = set(new_schema.get('required', []))
    
    # 1. High Risk: Removing a required field
    removed_required_fields = old_required - new_required
    if removed_required_fields:
        return "rejected", f"High-risk change detected: Cannot remove required fields: {removed_required_fields}. Requires manual review."

    # 2. Medium Risk: Adding a new required field
    added_required_fields = new_required - old_required
    if added_required_fields:
        return "rejected", f"High-risk change detected: Cannot add new required fields: {added_required_fields}. Requires manual review."
    
    # 3. Low Risk: Adding an optional field or other non-breaking change
    return "accepted_auto_approved", "Contract change is low risk (no required fields modified or removed). Auto-approved."