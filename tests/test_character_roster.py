import copy

import pytest
from fastapi import HTTPException

from app import (
    APP_VERSION,
    AdvanceRequest,
    StartRequest,
    advance_game,
    get_session,
    start_game,
)


def _character(response, character_id):
    return next(character for character in response["characters"] if character["id"] == character_id)


def _start(name="Avery"):
    return start_game(StartRequest(player_name=name, source="colab"))


def test_supplied_player_name_is_witness_display_name_and_start_fields_remain():
    response = _start("esmith19")

    assert _character(response, "witness")["display_name"] == "esmith19"
    assert {"session_id", "message", "title", "choices", "version", "characters"} <= response.keys()
    assert response["version"] == APP_VERSION
    assert [character["id"] for character in response["characters"]] == ["witness"]


def test_sessions_keep_their_own_player_names():
    first = _start("Avery")
    second = _start("Mara")

    assert _character(get_session(first["session_id"]), "witness")["display_name"] == "Avery"
    assert _character(get_session(second["session_id"]), "witness")["display_name"] == "Mara"


def test_radio_route_has_remote_radio_voice():
    started = _start()
    response = advance_game(AdvanceRequest(session_id=started["session_id"], choice_id="radio"))

    assert {c["id"] for c in response["characters"]} == {"witness", "radio_voice"}
    assert _character(response, "radio_voice")["presence"] == "remote"
    assert _character(response, "witness")["presence"] == "local"


def test_clinic_route_has_local_unnamed_clinic_nurse():
    started = _start()
    response = advance_game(AdvanceRequest(session_id=started["session_id"], choice_id="clinic"))

    assert {c["id"] for c in response["characters"]} == {"witness", "clinic_nurse"}
    nurse = _character(response, "clinic_nurse")
    assert nurse["display_name"] == "The Clinic Nurse"
    assert nurse["presence"] == "local"


def test_hatch_route_has_only_witness():
    started = _start()
    response = advance_game(AdvanceRequest(session_id=started["session_id"], choice_id="hatch"))

    assert [character["id"] for character in response["characters"]] == ["witness"]


def test_dispatch_scene_has_remote_dispatcher_after_any_route():
    started = _start()
    advance_game(AdvanceRequest(session_id=started["session_id"], choice_id="radio"))
    response = advance_game(AdvanceRequest(session_id=started["session_id"], choice_id="follow"))

    assert {c["id"] for c in response["characters"]} == {"witness", "municipal_dispatcher"}
    assert _character(response, "municipal_dispatcher")["presence"] == "remote"
    assert [c["id"] for c in get_session(started["session_id"])["characters"]] == [
        "witness",
        "municipal_dispatcher",
    ]


def test_invalid_choice_does_not_change_scene_stats_history_or_characters():
    started = _start()
    before = copy.deepcopy(get_session(started["session_id"]))

    with pytest.raises(HTTPException) as error:
        advance_game(AdvanceRequest(session_id=started["session_id"], choice_id="not-a-choice"))

    assert error.value.status_code == 400
    assert get_session(started["session_id"]) == before


def test_colab_python_calls_and_existing_response_fields_are_compatible():
    started = start_game(StartRequest(player_name="esmith19", source="colab"))
    advanced = advance_game(AdvanceRequest(session_id=started["session_id"], choice_id="radio"))
    session = get_session(started["session_id"])

    assert {"session_id", "player_name", "title", "message", "choices", "stats", "version", "characters"} <= advanced.keys()
    assert {
        "session_id",
        "player_name",
        "current_scene",
        "title",
        "message",
        "choices",
        "stats",
        "history",
        "version",
        "characters",
    } <= session.keys()
    assert session["current_scene"] == "radio"
    assert session["player_name"] == "esmith19"
