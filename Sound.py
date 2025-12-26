import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import time
import sys
import select
from playsound import playsound # NEW: Audio Support

# --- SETUP ---
MASTER_ID = "1iNem7lUd_Ws0UjtzkfrEtT1e23Z4Umw6uKKBGG78Hs4"
ZELDA_ID = "14-1Cd0qA1xyQ9rsXhiE9eab2E0VnXIOpZN3a72CDxwE"
WEBHOOK_URL = "https://discord.com/api/webhooks/1450550975193419987/gUrheH5qooV43zrvgCa9rrXopB0NYfpUJ9E3M03EkxEeVTR7CecpP4qhfTgZbUzI7exa"
TIME_LIMIT = 60 

# Authorize
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

def play_mission_1():
    print(f"🚨 MISSION START: Triage Bay 4 destabilizing...")
    requests.post(WEBHOOK_URL, json={"content": "⚠️ **CRITICAL ALERT:** 60s to Simulation Collapse."})
    
    start_time = time.time()
    
    # Wait for user input
    i, o, e = select.select([sys.stdin], [], [], TIME_LIMIT)

    if i:
        # --- SUCCESS STATE ---
        print("✅ Success! Performing Rite of the Bolus...")
        
        # PLAY SOUND EFFECT
        try:
            playsound('item_get.mp3') 
        except:
            print("(Sound file not found, skipping audio)")

        # Log to Zelda Sheet
        zelda_ss = client.open_by_key(ZELDA_ID).worksheet("Hyrule_Inventory")
        zelda_ss.append_row([time.ctime(), "Sheikah Stick-Pin", "PURIFIED", "Mission 1 Reward"])
        
        requests.post(WEBHOOK_URL, json={"content": "✅ **ITEM MANIFESTED:** Check your inventory for the Sheikah Stick-Pin."})
    else:
        # --- FAILURE STATE ---
        print("❌ TIMEOUT: Reality Collapsed.")
        # Play a 'failure' sound if you have one
        # playsound('game_over.mp3')
        
        zelda_ss = client.open_by_key(ZELDA_ID).worksheet("Hyrule_Inventory")
        zelda_ss.append_row([time.ctime(), "Calamity Gunk", "CORRUPTED", "Timeout Failure"])
        
        requests.post(WEBHOOK_URL, json={"content": "💀 **SIMULATION ERROR:** Calamity Gunk detected in local memory."})

if __name__ == "__main__":
    play_mission_1()
