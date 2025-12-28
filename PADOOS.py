import os
from firebase_admin import credentials, firestore, initialize_app

# 1. Accessing your Firebase Service Account (Securely)
# In GitHub, use Secrets; locally, use a .env file
cred = credentials.Certificate("firebase-adminsdk.json")
initialize_app(cred)

db = firestore.client()

def get_padoos_logic():
    # Pulls the current 'Unequal Treatment' settings
    doc_ref = db.collection('System_Logic').document('PADOOS_Status')
    return doc_ref.get().to_dict()

# This is the function your Discord Bot calls when the player types !audit
def execute_humanity_audit(player_id):
    current_logic = get_padoos_logic()
    # The 'Hero' move: Changing the bias from Corporate to Equity
    if current_logic['bias_type'] == "CORPORATE_TIER":
        # Overwrite the logic
        db.collection('System_Logic').document('PADOOS_Status').update({
            'bias_type': 'HUMAN_EQUITY',
            'last_auditor': player_id
        })
        return "SUCCESS: PADOOS Bias Neutralized."
