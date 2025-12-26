import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import time
import sys
import select

# --- SETUP ---
MASTER_ID = "1iNem7lUd_Ws0UjtzkfrEtT1e23Z4Umw6uKKBGG78Hs4"
ZELDA_ID = "14-1Cd0qA1xyQ9rsXhiE9eab2E0VnXIOpZN3a72CDxwE"
WEBHOOK_URL = "https://discord.com/api/webhooks/1450550975193419987/gUrheH5qooV43zrvgCa9rrXopB0NYfpUJ9E3M03EkxEeVTR7CecpP4qhfTgZbUzI7exa"
TIME_LIMIT = 60 # Seconds until the simulation collapses

# Authorize
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

def play_mission_1():
    print(f"🚨 MISSION START: You have {TIME_LIMIT} seconds to stabilize the bridge.")
    
    # 1. Start the Discord Alert
    requests.post(WEBHOOK_URL, json={"content": f"⚠️ **CRITICAL ALERT:** Triage Bay 4 is destabilizing. {TIME_LIMIT}s to failure."})
    
    start_time = time.time()
    
    print(f"Waiting for Dr. Sharma to press ENTER to perform the Rite of the Bolus...")
    
    # This block waits for Enter but times out
    i, o, e = select.select([sys.stdin], [], [], TIME_LIMIT)

    if i:
        # SUCCESS STATE
        elapsed = round(time.time() - start_time, 2)
        print(f"✅ Success! Rite performed in {elapsed} seconds.")
        
        # Manifest Reward
        zelda_ss = client.open_by_key(ZELDA_ID).worksheet("Hyrule_Inventory")
        zelda_ss.append_row([time.ctime(), "Sheikah Stick-Pin", "PURIFIED", f"Cleared in {elapsed}s"])
        
        requests.post(WEBHOOK_URL, json={"content": "✅ **REALITY ANCHORED.** Stick-Pin manifested."})
    else:
        # FAILURE STATE
        print("❌ TIMEOUT: Triage Bay 4 has de-rezzed.")
        
        # Log Failure to Master
        master_ss = client.open_by_key(MASTER_ID).worksheet("BotW_Bridge")
        master_ss.append_row([time.ctime(), "Dr. Sharma", "FAILURE", "Time Expired - Calamity Spread"])
        
        # Add "Corruption" to Zelda Sheet
        zelda_ss = client.open_by_key(ZELDA_ID).worksheet("Hyrule_Inventory")
        zelda_ss.append_row([time.ctime(), "Calamity Gunk", "CORRUPTED", "Penalty for Failure"])
        
        requests.post(WEBHOOK_URL, json={"content": "💀 **SIMULATION COLLAPSE.** The Calamity has spread to the Great Plateau."})

if __name__ == "__main__":
    play_mission_1()
