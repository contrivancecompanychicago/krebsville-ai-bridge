import firebase_admin
from firebase_admin import credentials, firestore
import random

# Initialize Firebase
db = firestore.client()

def calculate_tug_of_war(action_type, player_logic_score):
    # Reference to the Zone 0 document
    zone_ref = db.collection('Zones').document('zone_0_administration')
    data = zone_ref.get().to_dict()
    
    current_humanity = data['metadata']['integrity']
    malice_level = data['systems']['reality_anchor']['malice_interference']
    
    if action_type == "GRANT_HUMANITY_AUDIT":
        # Player (Hero) pulls the pole toward Equity
        # Logic: (Player Score / Malice) = Pull Strength
        pull_strength = (player_logic_score * 5) - (malice_level * 10)
        new_integrity = min(100, current_humanity + pull_strength)
        message = "🔵 Dr. Grant: 'The data is stabilizing! Keep pushing!'"
        
    elif action_type == "ARCHIVIST_INTRUSION":
        # The Villain pulls the pole toward Deletion
        pull_strength = random.randint(5, 15)
        new_integrity = max(0, current_humanity - pull_strength)
        message = "🟣 The Archivist: 'Inefficiency is a disease. I am the cure.'"

    # Update Firestore
    zone_ref.update({
        'metadata.integrity': new_integrity,
        'npc_states.dr_grant.digital_sync_percent': 100 - new_integrity
    })
    
    return new_integrity, message
