# Krebsville Nights: Zone 0

**Version 0.0.0 — Version 0 prototype**

A deterministic prequel prototype to **Krebsville Nights: Unequal Treatment Part 1**. The project keeps its FastAPI story backend and Colab-compatible Python functions, and includes a small browser-based Three.js alley game.

## What’s included

- FastAPI backend for session-based story progression and simple stats
- Choice-based narrative with stable scene and choice IDs
- Character registry with session-specific Witness display name
- A simple Three.js browser client featuring a rainy alley, controllable Witness, radio, clinic entrance, and maintenance hatch
- Characters appear as text and dialogue; this prototype does not include character portraits, authored character animations, or detailed 3D character models
- Preset deterministic story content; no AI API, credentials, Firebase, Discord messaging, or game service integrations

## Character roster

- **The Witness** — player-controlled character. Display name comes from the session's `player_name`.
- **The Radio Voice** — unidentified remote voice heard through the damaged radio; identity undisclosed.
- **The Clinic Nurse** — unnamed, observant, cautious healthcare worker concerned about patients.
- **The Municipal Dispatcher** — remote municipal employee contacting the Witness about a transfer; motives remain ambiguous.

The arrival scene contains only the Witness; the radio is an environmental object until investigated. Radio route: Witness and remote Radio Voice. Clinic route: Witness and Clinic Nurse. Hatch route: Witness alone. Dispatch: Witness and remote Municipal Dispatcher. Dr. Frederick M. Grant, Nurse Carter, Maria Voss, and characters from Scar City do not appear in this opening prototype.

## Version 0 scope and 3D direction

Version 0 is an early playable slice, not a finished 3D RPG. The browser client is built with Three.js, while Python/FastAPI remains responsible for sessions, story choices, character participation, and statistics. The client calls the existing story endpoints, so the Colab workflow and direct Python calls remain available independently of the 3D view. Godot is not required.

The first 3D slice focuses on the alley: move the Witness with **WASD** or the arrow keys, approach the radio, clinic door, or maintenance hatch, and press **E** or click an object to investigate. The client displays the backend's narrative text, choices, characters, and stats. Use the story buttons as an alternative to navigating to an object.

The simple scene uses placeholder geometry and a Three.js module loaded from jsDelivr; a connection to the internet is required to load that module in the browser. The current prototype does not include detailed character/environment assets, portraits, a full animation system, persistence across server restarts, or a full 3D RPG feature set. Future improvements such as route-specific lighting and object animation, save/resume, richer interaction prompts, and mobile polish are ideas for later work, not claims about the current implementation.

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

This repository declares **Version 0.0.0 (Version 0)** in `VERSION` and `APP_VERSION` / FastAPI metadata. This is a prototype version declaration; it does not imply a feature-complete 3D release.

## License

Apache 2.0
