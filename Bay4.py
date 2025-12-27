import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import time
import sys
import select

# --- CONFIG ---
MASTER_ID = "1iNem7lUd_Ws0UjtzkfrEtT1e23Z4Umw6uKKBGG78Hs4"
ZELDA_ID = "14-1Cd0qA1xyQ9rsXhiE9eab2E0VnXIOpZN3a72CDxwE"
WEBHOOK_URL = "https://discord.com/api/webhooks/1450550975193419987/gUrheH5qooV43zrvgCa9rrXopB0NYfpUJ9E3M03EkxEeVTR7CecpP4qhfTgZbUzI7exa"

# The Patient Data
PATIENTS = [
    {"id": "#001", "name": "Meijer", "condition": "Anaphylaxis", "reward": "First Aid Bandage"},
    {"id": "#002", "name": "Miller", "condition": "Laceration", "reward": "Sewing Kit"},
    {"id": "#003", "name": "Varga", "condition": "Heat Stroke", "reward": "Purified Water"},
    {"id": "#004", "name": "Kade", "condition": "Fracture", "reward": "Iron Scraps"},
    {"id": "#005", "name": "Unknown", "condition": "Reality Displacement", "reward": "Sheikah Stick-Pin"}
]

def run_triage_loop():
    print("🏥 TRIAGE PROTOCOL ACTIVATED: 5 PATIENTS IN BAY 4")
    total_saves = 0
    
    for p in PATIENTS:
        print(f"\n--- Current Patient: {p['id']} ({p['name']}) ---")
        print(f"Condition: {p['condition']}")
        
        # Notify Discord
        requests.post(WEBHOOK_URL, json={
            "content": f"🚨 **TRIAGE ALERT:** Patient {p['id']} is crashing! \nStatus: {p['condition']}. \nDr. Sharma, stabilize now!"
        })

        # 15 second timer per patient
        print("Waiting 15s for stabilization (Press ENTER)...")
        i, o, e = select.select([sys.stdin], [], [], 15)

        if i:
            print(f"✅ Patient {p['id']} Stabilized.")
            total_saves += 1
            # Log success to Master Sheet
            log_to_sheet(MASTER_ID, "BotW_Bridge", [time.ctime(), p['id'], "SAVED", p['reward']])
        else:
            print(f"❌ Patient {p['id']} LOST TO CALAMITY.")
            log_to_sheet(MASTER_ID, "BotW_Bridge", [time.ctime(), p['id'], "FAILURE", "Calamity Gunk"])
            requests.post(WEBHOOK_URL, json={"content": f"💀 **FAILURE:** Patient {p['id']} has de-rezzed. Horde Heat +10%."})

    # FINAL REWARD
    if total_saves == 5:
        print("\n🏆 FLAWLESS TRIAGE: Manifesting Sheikah Stick-Pin...")
        log_to_sheet(ZELDA_ID, "Hyrule_Inventory", [time.ctime(), "Sheikah Stick-Pin", "PURIFIED", "Full Bay 4 Clear"])
    else:
        print(f"\n⚠️ Triage Complete. {total_saves}/5 saved. Check Inventory for fallout.")

def log_to_sheet(sheet_id, tab_name, row):
    # This is a helper function to handle the writing logic
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).worksheet(tab_name)
    sheet.append_row(row)

if __name__ == "__main__":
    run_triage_loop()
