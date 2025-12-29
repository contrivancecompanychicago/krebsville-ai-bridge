import requests

API_URL = "https://api.sheety.co/2038ea59d35e3cf806679a2706330dc9/cosineZone1Master/gameState"

def restore_patient_000():
    # Target Patient 000 specifically
    update_data = {"status": "ACTIVE", "insurance_tier": "EQUITY_RESTORED"}
    response = requests.patch(f"{API_URL}/patient_id/000", json={"data": update_data})
    
    if response.status_code == 200:
        return "✅ Humanity Audit Successful: Patient 000 re-indexed."
    return "❌ Connection Failed: The Archivist blocked the API."
