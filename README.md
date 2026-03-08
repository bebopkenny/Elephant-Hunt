![Logo](./elephant_hunt_logo.png)

# Elephant Hunt

Elephant Hunt is an interactive campus scavenger hunt game built for the ACM chapter at California State University, Fullerton.  
Teams race to find QR-coded elephants placed around campus while guided by riddles from the Guardian chatbot.  

## Overview

Each team is assigned a path of stations across campus. The Guardian chatbot provides a riddle for the next station.  
Teams must solve the riddle, locate the physical elephant, and scan its QR code. The backend validates progress, awards points, and updates the leaderboard.  

The first team to reach the final elephant wins, but all teams can complete the hunt at their own pace.  

## Features

- Guardian chatbot powered by an LLM
  - Provides short riddles and limited hints
  - Refuses to reveal exact station names
- Supabase backend for all game state
  - Teams, stations, paths, and scoring stored in database tables
  - Server-side validation of scans
- QR-coded elephants
  - Each QR encodes the station ID and scan flag
  - Only the expected station advances the team
- Real-time leaderboard
  - Displays ranks, scores, and standings during play
- Streamlit frontend
  - Branding and instructions page
  - Guardian chat interface with styled bubbles
  - Live leaderboard view
  - Station progress indicator

## Architecture
![Architecture](./architecture(2).svg)
- Frontend  
  Built in Streamlit. Handles chat UI, team input, QR scan handling, and leaderboard rendering. Deployed on Streamlit Community Cloud.

- Backend  
  Supabase (Postgres + API) stores:
  - `teams`: slugs, names, winner timestamps
  - `stations`: station IDs and metadata
  - `paths`: ordered station list per team and current progress
  - `score_events`: point logs for each correct scan  

- Guardian LLM  
  The LLM is called via an OpenAI-compatible API. Each response is seeded by the station's riddle and scrubbed for restricted aliases. Responses are short and consistent, with one stronger hint available per station.  

- QR Generation  
  QR codes are generated with Python. There are 10 team-neutral QR codes, one per station. Each encodes a deep link in the form:  
```https://<app-url>/?station=<station_id>&scan=1```

## Technology Stack

- Python 3.10+
- Streamlit for the frontend
- Supabase for database and RPC functions
- OpenAI-compatible client for LLM integration
- QRCode and Pillow for QR generation

## Installation

Clone the repository and install requirements:

```bash
git clone https://github.com/<your-org>/elephant-hunt.git
cd elephant-hunt
pip install -r requirements.txt
```

## Configuration

Secrets are stored in `.streamlit/secrets.toml`:
```toml
SUPABASE_URL = "..."
SUPABASE_ANON_KEY = "..."

LLM_API_KEY = "..."
LLM_API_URL = "..."
LLM_MODEL   = "..."

MAX_TOKENS_PER_REPLY = "160"
TEMPERATURE = "0.25"
DAILY_REQUEST_LIMIT = "200"
DAILY_COMPLETION_TOKEN_LIMIT = "50000"
```

Provide a `.streamlit/secrets.toml.example` in the repository for setup instructions.

## Running Locally
```bash
streamlit run ui.py
```
Open the app at http://localhost:8501

## Deployment

The app is deployed on Streamlit Community Cloud. Push changes to the main branch and the app will automatically redeploy. Secrets are configured in the Streamlit Cloud dashboard under Settings.