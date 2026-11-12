# Krebsville Nights: Zone 0

Version 0.0.0

A deterministic prequel prototype to **Krebsville Nights: Unequal Treatment Part 1**. The project keeps its FastAPI story backend and Colab-compatible Python functions, and now includes a small browser-based Three.js 3D alley game at the site root.

## What’s included

- FastAPI backend for session-based story progression and simple stats
- Choice-based narrative with stable scene and choice IDs
- Character registry with session-specific Witness display name
- A simple Three.js browser client featuring a rainy alley, controllable Witness, radio, clinic entrance, and maintenance hatch
- Characters appear as text and dialogue; this prototype does not include character portraits, animation, or detailed 3D character models
- Preset deterministic story content; no AI API, credentials, Firebase, Discord messaging, or game service integrations

## Character roster

- **The Witness** — player-controlled character. Display name comes from the session's `player_name`.
- **The Radio Voice** — unidentified remote voice heard through the damaged radio; identity undisclosed.
- **The Clinic Nurse** — unnamed, observant, cautious healthcare worker concerned about patients.
- **The Municipal Dispatcher** — remote municipal employee contacting the Witness about a transfer; motives remain ambiguous.

The arrival scene contains only the Witness; the radio is an environmental object until investigated. Radio route: Witness and remote Radio Voice. Clinic route: Witness and Clinic Nurse. Hatch route: Witness alone. Dispatch: Witness and remote Municipal Dispatcher. Dr. Frederick M. Grant, Nurse Carter, Maria Voss, and characters from Scar City do not appear in this opening prototype.

## Run the game locally

1. Install Python dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Start the server from the repository directory:
   ```bash
   uvicorn app:app --reload
   ```
3. Open <http://localhost:8000/> for the 3D game, or <http://localhost:8000/docs> for API documentation.

Use **WASD** or arrow keys to move. Approach the radio, clinic door, or hatch and press **E** (or click the object) to investigate. The narrative choices are displayed in the dialogue panel.

The Three.js module is loaded from jsDelivr, so an internet connection is needed to load the 3D client. The story API and Colab functions remain Python and do not depend on the 3D client.

## API quick start

Start a game session:

```bash
curl -X POST http://localhost:8000/api/onboarding/start \
  -H "Content-Type: application/json" \
  -d '{"player_name":"Avery","source":"web"}'
```

Advance the story:

```bash
curl -X POST http://localhost:8000/api/onboarding/advance \
  -H "Content-Type: application/json" \
  -d '{"session_id":"<SESSION_ID>","choice_id":"radio"}'
```

Check a session:

```bash
curl http://localhost:8000/api/onboarding/session/<SESSION_ID>
```

## Google Colab

The existing Python function calls remain available independently of the browser client:

```python
from app import StartRequest, start_game

response = start_game(StartRequest(player_name="esmith19", source="colab"))
print(response["characters"])
```

Advance the Colab session as before:

```python
from app import AdvanceRequest, advance_game

next_scene = advance_game(
    AdvanceRequest(session_id=response["session_id"], choice_id="radio")
)
print(next_scene["characters"])
```

## Tests

Run the roster and compatibility tests:

```bash
python -m pytest
```

## Project version

This remains the Version 0 Zone 0 prototype. The FastAPI metadata and `VERSION` file declare `0.0.0`.

## License

Apache 2.0
