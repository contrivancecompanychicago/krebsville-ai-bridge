from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Literal, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

APP_VERSION = "0.0.0"
WEB_DIR = Path(__file__).resolve().parent / "web"

app = FastAPI(
    title="Krebsville AI Bridge",
    version=APP_VERSION,
    description=(
        "Text-based Zone 0 prequel for Krebsville Nights: "
        "Unequal Treatment Part 1."
    ),
)


class StartRequest(BaseModel):
    player_name: str = Field(default="Visitor", min_length=1, max_length=64)
    source: str = Field(default="onboarding")


class AdvanceRequest(BaseModel):
    session_id: str
    choice_id: Optional[str] = None
    message: Optional[str] = None


class SessionState(BaseModel):
    session_id: str
    player_name: str
    current_scene: str
    stats: Dict[str, int] = Field(default_factory=lambda: {
        "clarity": 0,
        "trust": 0,
        "pressure": 0,
        "resolve": 0,
    })
    history: List[str] = Field(default_factory=list)


PresenceType = Literal["local", "remote"]

# Character records are deliberately kept separate from the narrative prose.
# Names for the Witness are supplied per session rather than stored here.
CHARACTER_REGISTRY = {
    "witness": {
        "id": "witness",
        "name": "The Witness",
        "role": "Player character",
        "description": (
            "A new arrival in Zone 0 investigating warnings, missing records, "
            "and unequal access to resources."
        ),
        "player_controlled": True,
        "presence": "local",
    },
    "radio_voice": {
        "id": "radio_voice",
        "name": "The Radio Voice",
        "role": "Unidentified radio contact",
        "description": (
            "An unidentified person communicating urgently through a damaged radio; "
            "their identity remains undisclosed."
        ),
        "player_controlled": False,
        "presence": "remote",
    },
    "clinic_nurse": {
        "id": "clinic_nurse",
        "name": "The Clinic Nurse",
        "role": "Healthcare worker",
        "description": (
            "An unnamed, observant and cautious healthcare worker concerned about patients."
        ),
        "player_controlled": False,
        "presence": "local",
    },
    "municipal_dispatcher": {
        "id": "municipal_dispatcher",
        "name": "The Municipal Dispatcher",
        "role": "Municipal employee",
        "description": (
            "A municipal employee contacting the Witness about witnessing a transfer; "
            "their motives are ambiguous."
        ),
        "player_controlled": False,
        "presence": "remote",
    },
}


# Scene prose and character participation are maintained independently.
STORY = {
    "arrival": {
        "title": "The Alley Behind the Clinic",
        "characters": ["witness"],
        "text": (
            "The rain keeps falling on Krebsville as you wake beneath a rusted fire escape. "
            "A half-broken radio sits in the alley, its speaker hissing without a clear voice. "
            "On the other side of the alley, the Family Clinic is lit like a confession booth."
        ),
        "choices": [
            {"id": "radio", "label": "Listen to the radio", "next_scene": "radio"},
            {"id": "clinic", "label": "Slip toward the clinic", "next_scene": "clinic"},
            {"id": "hatch", "label": "Inspect the maintenance hatch", "next_scene": "hatch"},
        ],
    },
    "radio": {
        "title": "A Voice in the Static",
        "characters": ["witness", "radio_voice"],
        "text": (
            "The Radio Voice (remote) says, 'If you hear this, you are early enough to matter. "
            "Krebsville is already counting on you to choose who gets the truth.' "
            "A loose wire sparks behind the dumpster."
        ),
        "choices": [
            {"id": "follow", "label": "Follow the voice's warning", "next_scene": "dispatch"},
            {"id": "silence", "label": "Keep listening in silence", "next_scene": "dispatch"},
        ],
    },
    "clinic": {
        "title": "The Waiting Room",
        "characters": ["witness", "clinic_nurse"],
        "text": (
            "Inside the clinic, the Clinic Nurse sorts files under a flickering lamp. The room smells "
            "like antiseptic, dust, and something older: fear. She looks up. The Clinic Nurse says, "
            "'I can tell you what is missing. I can't promise who is safe to ask.'"
        ),
        "choices": [
            {"id": "truth", "label": "Tell her the truth about the radio", "next_scene": "dispatch"},
            {"id": "quiet", "label": "Ask for the names of the missing", "next_scene": "dispatch"},
        ],
    },
    "hatch": {
        "title": "The Service Tunnel",
        "characters": ["witness"],
        "text": (
            "Beneath the hatch is a narrow service tunnel lined with old meters and electrical tape. "
            "Someone has written the words 'Don't let the city decide' in the dust."
        ),
        "choices": [
            {"id": "route", "label": "Follow the tunnel toward the station", "next_scene": "dispatch"},
            {"id": "archive", "label": "Take the ledger hidden under the stair", "next_scene": "dispatch"},
        ],
    },
    "dispatch": {
        "title": "The City Makes a Call",
        "characters": ["witness", "municipal_dispatcher"],
        "text": (
            "A municipal line clicks alive. The Municipal Dispatcher (remote) says, 'Your presence "
            "has been noted. We require a witness to the next transfer. Participation is voluntary.' "
            "The line stays open, leaving the motive unclear."
        ),
        "choices": [
            {"id": "accept", "label": "Accept the assignment and go in", "next_scene": "ending"},
            {"id": "refuse", "label": "Refuse and stay on the outside", "next_scene": "ending"},
        ],
    },
    "ending": {
        "title": "A Line Is Drawn",
        "characters": ["witness"],
        "text": (
            "The night settles around you, and Krebsville finally reveals its shape: not a city of monsters, but a machine built "
            "to move people before they can speak. Your choices do not end the story. They start the version that is still hidden "
            "from the official record."
        ),
        "choices": [],
    },
}

SESSIONS: Dict[str, SessionState] = {}


def characters_for_scene(session: SessionState, scene_id: str) -> List[dict]:
    """Return the scene roster with the Witness's session-specific display name."""
    scene = STORY.get(scene_id, STORY["ending"])
    participants = []
    for character_id in scene["characters"]:
        character = CHARACTER_REGISTRY[character_id]
        participants.append(
            {
                "id": character["id"],
                "display_name": (
                    session.player_name if character["player_controlled"] else character["name"]
                ),
                "role": character["role"],
                "presence": character["presence"],
            }
        )
    return participants


def apply_choice(session: SessionState, choice_id: str) -> None:
    scene = STORY.get(session.current_scene)
    if not scene:
        return

    choice_map = {c["id"]: c for c in scene.get("choices", [])}
    choice = choice_map.get(choice_id)
    if not choice:
        raise HTTPException(status_code=400, detail="Invalid choice for this scene.")

    next_scene = choice.get("next_scene", session.current_scene)
    session.current_scene = next_scene
    session.history.append(f"choice:{choice_id}")

    if choice_id == "radio":
        session.stats["clarity"] += 2
        session.stats["trust"] += 1
    elif choice_id == "clinic":
        session.stats["trust"] += 2
        session.stats["pressure"] += 1
    elif choice_id == "hatch":
        session.stats["clarity"] += 3
        session.stats["resolve"] += 1
    elif choice_id == "follow":
        session.stats["resolve"] += 2
    elif choice_id == "silence":
        session.stats["clarity"] += 1
    elif choice_id == "truth":
        session.stats["trust"] += 2
        session.stats["clarity"] += 1
    elif choice_id == "quiet":
        session.stats["pressure"] += 2
    elif choice_id == "route":
        session.stats["resolve"] += 2
    elif choice_id == "archive":
        session.stats["clarity"] += 2
        session.stats["trust"] += 1
    elif choice_id == "accept":
        session.stats["resolve"] += 3
        session.stats["pressure"] += 1
    elif choice_id == "refuse":
        session.stats["clarity"] += 2
        session.stats["trust"] += 1


@app.get("/")
def game_home() -> FileResponse:
    """Serve the optional browser game while keeping API and Colab calls intact."""
    return FileResponse(WEB_DIR / "index.html")


app.mount("/game-assets", StaticFiles(directory=WEB_DIR), name="game-assets")


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "krebsville-ai-bridge",
        "version": APP_VERSION,
    }


@app.post("/api/onboarding/start")
def start_game(payload: StartRequest) -> dict:
    session_id = str(uuid4())
    session = SessionState(
        session_id=session_id,
        player_name=payload.player_name,
        current_scene="arrival",
        stats={"clarity": 0, "trust": 0, "pressure": 0, "resolve": 0},
        history=["session_started"],
    )
    SESSIONS[session_id] = session
    scene = STORY[session.current_scene]
    return {
        "session_id": session_id,
        "message": scene["text"],
        "title": scene["title"],
        "choices": scene["choices"],
        "characters": characters_for_scene(session, session.current_scene),
        "version": APP_VERSION,
    }


@app.post("/api/onboarding/advance")
def advance_game(payload: AdvanceRequest) -> dict:
    session = SESSIONS.get(payload.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    if payload.choice_id:
        apply_choice(session, payload.choice_id)
    elif payload.message:
        message = payload.message.strip().lower()
        current_scene = STORY.get(session.current_scene, {})
        choice_map = {c["label"].lower(): c for c in current_scene.get("choices", [])}
        choice = choice_map.get(message)
        if choice is None:
            raise HTTPException(status_code=400, detail="Message does not match any available choice.")
        apply_choice(session, choice["id"])

    current_scene = STORY.get(session.current_scene, STORY["ending"])
    return {
        "session_id": session.session_id,
        "player_name": session.player_name,
        "title": current_scene["title"],
        "message": current_scene["text"],
        "choices": current_scene.get("choices", []),
        "stats": session.stats,
        "characters": characters_for_scene(session, session.current_scene),
        "version": APP_VERSION,
    }


@app.get("/api/onboarding/session/{session_id}")
def get_session(session_id: str) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    current_scene = STORY.get(session.current_scene, STORY["ending"])
    return {
        "session_id": session.session_id,
        "player_name": session.player_name,
        "current_scene": session.current_scene,
        "title": current_scene["title"],
        "message": current_scene["text"],
        "choices": current_scene.get("choices", []),
        "stats": session.stats,
        "history": session.history,
        "characters": characters_for_scene(session, session.current_scene),
        "version": APP_VERSION,
    }


@app.get("/api/version")
def version() -> dict:
    return {"version": APP_VERSION, "name": "Krebsville AI Bridge"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
