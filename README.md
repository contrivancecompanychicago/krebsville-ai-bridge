# krebsville-ai-bridge
# 🏥 Krebsville Nights: Information Warfare
**Project Title:** Public Nuisance City - Zone 0 to Zone 1 Core Integration  
**Concept:** A multi-platform RPG exploring Health Equity and Systemic Bias.

## 🛠️ Technical Stack
- **Language:** Python 3.10+
- **Platform:** Discord (via discord.py)
- **Database:** Firebase/Firestore (Live Reality Sync)
- **Story Engine:** Obsidian (Handbook/Wiki)
- **Deployment:** [GitHub Repo Link]

---

## 🏛️ Project Structure
- `/bot.py`: The Main DOVIC Engine (Handles Slash Commands & Buttons).
- `/logic/`:
    - `tug_of_war.py`: Manages the Equity vs. Efficiency poles.
    - `humanity_audit.py`: The Player's script to bypass PADOOS bias.
- `/data/`:
    - `weapons.json`: Definition of digital and clinical tools.
    - `firebase_config.py`: Connection handler for Firestore.
- `/docs/`: Obsidian vault markdown files.

---

## 🚀 Setup & Installation

### 1. Prerequisites
- Create a [Discord Developer Bot](https://discord.com/developers/applications).
- Initialize a [Firebase Project](https://console.firebase.google.com/) and download the `serviceAccountKey.json`.

### 2. Environment Variables
Create a `.env` file in the root directory:
```env
DISCORD_TOKEN=your_bot_token_here
FIREBASE_CREDENTIALS_PATH=./serviceAccountKey.json
GUILD_ID=your_server_id
