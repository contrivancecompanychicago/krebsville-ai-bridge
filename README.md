# Krebsville Nights: Zone 0

Version 0.0.0

A deterministic, text-based prequel to **Krebsville Nights: Unequal Treatment Part 1**. The opening begins in Zone 0, Scene 0: “The Alley Behind the Clinic.” The Witness investigates warnings, missing records, and unequal access to resources through radio, clinic, and maintenance-hatch routes.

## Overview

This repository provides a lightweight FastAPI story backend with session-based narrative progression and simple stats. Story text and choices are preset; no AI API, credentials, Firebase, Discord messaging, or other external services are used by the story engine.

Characters appear as text and dialogue. **Portraits, animation, and a 3D RPG client are not included.**

## Character roster

- **The Witness** — player-controlled character. The display name comes from `player_name` when starting a session.
- **The Radio Voice** — unidentified, urgent remote voice heard on the radio investigation route. Their identity stays undisclosed.
- **The Clinic Nurse** — unnamed, observant and cautious healthcare worker concerned about patients; appears on the clinic route.
- **The Municipal Dispatcher** — remote municipal employee who contacts the Witness about a transfer; their motives remain ambiguous.

The arrival scene includes only the Witness; the damaged radio is an environmental object until its route is chosen. The radio scene includes the Witness and remote Radio Voice, the clinic scene the Witness and Clinic Nurse, the hatch scene the Witness alone, and the dispatch scene the Witness and remote Municipal Dispatcher. Dr. Frederick M. Grant, Nurse Carter, Maria Voss, and Scar City characters do not appear in this opening prototype.

## Features

- FastAPI backend for session-driven story progression
- Choice-based branching narrative with stable scene and choice IDs
- Session tracking with simple stats and history
- Consistent scene character data in start, advance, and session responses
- Python-callable functions suitable for Google Colab workflows
- Version 0 declaration (`0.0.0`) in app metadata and the `VERSION` file

## Local setup

1. Create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   uvicorn app:app --reload
   ```
4. Visit <http://localhost:8000/docs>.

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

## Google Colab example

The existing Python function calls remain available. Print the scene roster after starting a session:

```python
from app import StartRequest, start_game

response = start_game(StartRequest(player_name="esmith19", source="colab"))
print(response["characters"])
```

To advance from Colab:

```python
from app import AdvanceRequest, advance_game

next_scene = advance_game(
    AdvanceRequest(session_id=response["session_id"], choice_id="radio")
)
print(next_scene["characters"])
```

## Tests

Run the focused roster and compatibility tests with:

```bash
python -m pytest
```

## Project version

This is the Version 0 Zone 0 prequel prototype. The repo version is declared as `0.0.0` in the FastAPI metadata and the `VERSION` file.

## License

Apache 2.0
