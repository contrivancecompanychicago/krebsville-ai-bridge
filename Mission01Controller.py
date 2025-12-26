import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import time

# --- SETUP ---
# Paste your IDs from the URL of each sheet
MASTER_ID = "1iNem7lUd_Ws0UjtzkfrEtT1e23Z4Umw6uKKBGG78Hs4"
ZELDA_ID = "14-1Cd0qA1xyQ9rsXhiE9eab2E0VnXIOpZN3a72CDxwE"
WEBHOOK_URL = "https://discord.com/api/webhooks/1450550975193419987/gUrheH5qooV43zrvgCa9rrXopB0NYfpUJ9E3M03EkxEeVTR7CecpP4qhfTgZbUzI7exa"

# Authorize Google
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

def start_mission_1_zone_1():
    print("🚀 Initializing Mission 1: Zone 1 (Triage Bay 4)...")
    
    # 1. Post Newspaper to Discord
    news_payload = {
        "content": "🗞️ **THE SUNNY KREBS TIMES**",
        "embeds": [{
            "title": "🚨 ALERT: MEIJER ALLERGEN INCURSION",
            "description": "Dr. Sharma, the Python Engine has detected a reality leak.\nTarget: Undeclared Milk in Dark Chocolate.\n\n**STATUS:** Awaiting Rite of the Bolus.",
            "color": 16711680 # Red
        }]
    }
    requests.post(WEBHOOK_URL, json=news_payload)
    print("✅ Discord Alert Dispatched.")

    # 2. Update the Hospital Master Sheet (BotW_Bridge)
    master_ss = client.open_by_key(MASTER_ID)
    bridge_tab = master_ss.worksheet("BotW_Bridge")
    bridge_tab.append_row([time.ctime(), "Dr. Sharma", "MISSION START", "Meijer Incursion"])
    print("✅ Master Sheet Updated.")

def solve_mission_1():
    print("💉 Executing Rite of the Bolus...")
    
    # 3. Manifest Item in Zelda Sheet (Hyrule_Inventory)
    zelda_ss = client.open_by_key(ZELDA_ID)
    inv_tab = zelda_ss.worksheet("Hyrule_Inventory")
    inv_tab.append_row([time.ctime(), "Sheikah Stick-Pin", "PURIFIED", "Mission 1 Reward"])
    
    # 4. Final Discord Ping
    win_payload = {"content": "✅ **MISSION COMPLETE.** Reality Anchored. The **Sheikah Stick-Pin** is now in your inventory."}
    requests.post(WEBHOOK_URL, json=win_payload)
    print("✅ Reward Manifested. Mission 1 Success.")

# GAMEPLAY EXECUTION
if __name__ == "__main__":
    start_mission_1_zone_1()
    # In a real game, you'd wait for user input here
    input("Press Enter once you have 'Stabilized the Bridge' in the Hospital...")
    solve_mission_1()
