import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import datetime

# --- CONFIGURATION ---
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1450550975193419987/gUrheH5qooV43zrvgCa9rrXopB0NYfpUJ9E3M03EkxEeVTR7CecpP4qhfTgZbUzI7exa"
# The ID is found in the URL of your spreadsheet
ZELDA_SHEET_ID = "14-1Cd0qA1xyQ9rsXhiE9eab2E0VnXIOpZN3a72CDxwE"
MASTER_SHEET_ID = "1iNem7lUd_Ws0UjtzkfrEtT1e23Z4Umw6uKKBGG78Hs4"

# 1. Setup Google Sheets Access
# Note: You'll need a 'creds.json' file from Google Cloud Console
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

def launch_mission_01():
    # --- PHASE 1: DISCORD BROADCAST ---
    payload = {
        "content": "🗞️ **THE SUNNY KREBS TIMES: PYTHON EDITION**",
        "embeds": [{
            "title": "🚨 ALERT: MEIJER ALLERGEN DETECTED",
            "description": "Python Engine has detected a Blue Energy leak in Triage Bay 4.\n\n**Task:** Perform the Rite of the Bolus.",
            "color": 3447003
        }]
    }
    requests.post(DISCORD_WEBHOOK_URL, json=payload)
    print("✅ Discord Broadcast Sent.")

def deliver_reward():
    # --- PHASE 2: WRITE TO SHEETS ---
    # Log to Master Bridge
    master_sheet = client.open_by_key(MASTER_SHEET_ID).worksheet("BotW_Bridge")
    master_sheet.append_row([str(datetime.datetime.now()), "Dr. Sharma", "BOLUS SUCCESS", "Python Trigger"])
    
    # Manifest in Zelda Sheet
    zelda_sheet = client.open_by_key(ZELDA_SHEET_ID).worksheet("Hyrule_Inventory")
    zelda_sheet.append_row([str(datetime.datetime.now()), "Sheikah Stick-Pin", "MANIFESTED", "Python Engine"])
    
    print("✅ Reward manifested in Zelda Sheet.")

# Run the sequence
if __name__ == "__main__":
    launch_mission_01()
    # In a real game, you'd wait for a player trigger, 
    # but for testing, we will run the reward immediately:
    deliver_reward()
