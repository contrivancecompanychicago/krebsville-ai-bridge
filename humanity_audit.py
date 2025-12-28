# FILE: humanity_audit.py
# PURPOSE: Counteract Archivist Bias in the Triage Algorithm

import firebase_admin
from firebase_admin import firestore

db = firestore.client()

def run_audit(player_id):
    # 1. Target the biased Triage Logic
    triage_ref = db.collection('System_Logic').document('triage_rules')
    
    # 2. Locate the "Economic Tier" variable inserted by the Archivist
    current_rules = triage_ref.get().to_dict()
    
    if "economic_tier" in current_rules['priority_formula']:
        print("🚨 BIAS DETECTED: System is prioritizing Insurance Tier over Clinical Need.")
        
        # 3. The Overwrite: Replace Corporate Logic with Medical Necessity
        new_formula = "patient_vitals + time_sensitive_trauma"
        
        triage_ref.update({
            "priority_formula": new_formula,
            "last_auditor": player_id,
            "equity_status": "RESTORED"
        })
        
        print("✅ SUCCESS: Humanity Audit complete. Triage leveled.")
    else:
        print("ℹ️ System is currently stable. No bias found.")
