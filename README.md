# Krebsville AI Bridge

Version 0.0.0

A text-based onboarding prequel game backend for Krebsville Nights: Unequal Treatment Part 1.

## Overview

This repository has been repurposed as a lightweight narrative backend for a chat-driven onboarding story in the Krebsville universe. The backend supports a short game loop, saves session state, and emits story scenes and choices to a frontend client or Discord/terminal interface.

## Story premise

The story sits before the main events of Krebsville Nights: Unequal Treatment Part 1, and follows a new witness arriving in the city just as the municipal machine starts moving against the people it claims to protect.

## Features

- FastAPI backend for session-driven story progression
- Choice-based branching narrative
- Session tracking with simple stats
- JSON API suitable for web, chat, or Discord frontends
- Version 0 declaration for early pre-release onboarding flow

## Local setup

1. Create a virtual environment
2. Install dependencies:
   pip install -r requirements.txt
3. Run the app:
   uvicorn app:app --reload
4. Visit:
   http://localhost:8000/docs

## API quick start

Start a game session:

curl -X POST http://localhost:8000/api/onboarding/start \
  -H "Content-Type: application/json" \
  -d '{"player_name":"Avery","source":"web"}'

Advance the story:

curl -X POST http://localhost:8000/api/onboarding/advance \
  -H "Content-Type: application/json" \
  -d '{"session_id":"<SESSION_ID>","choice_id":"radio"}'

Check a session:

curl http://localhost:8000/api/onboarding/session/<SESSION_ID>

## Project version

The repo version is now declared as 0.0.0 in both the app metadata and the VERSION file.

## License

Apache 2.0
