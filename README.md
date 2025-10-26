# Elephant Hunt

Elephant Hunt is an interactive campus scavenger hunt game built for the ACM chapter at California State University, Fullerton.  
Teams race to find QR-coded elephants placed around campus while guided by riddles from the Guardian chatbot.  

## Overview

Each team is assigned a path of stations across campus. The Guardian chatbot provides a riddle for the next station.  
Teams must solve the riddle, locate the physical elephant, and scan its QR code. The backend validates progress, awards points, and updates the leaderboard.  

The first team to reach the final elephant wins, but all teams can complete the hunt at their own pace.  

## Features

- Guardian chatbot powered by xAI Grok
  - Provides short riddles and limited hints
  - Refuses to reveal exact station names
- Supabase backend for all game state
  - Teams, stations, paths, and scoring stored in database tables
  - Server-side validation of scans
- QR-coded elephants
  - Each QR encodes the team slug, station ID, and scan flag
  - Only the expected station advances the team
- Real-time leaderboard
  - Displays ranks, scores, and standings during play
- Streamlit frontend
  - Branding and instructions page
  - Guardian chat interface with styled bubbles
  - Live leaderboard view

## Architecture
![Architecture](https://media.discordapp.net/attachments/1299155448959598595/1415746119173935224/Web_Application_Flowchart_with_Grok_and_Supabase.png?ex=68c453d2&is=68c30252&hm=6baf2a388a9c417be18b65343257450a0beab2e50ddfd9bf9a5712d0141b54e3&=&format=webp&quality=lossless&width=1920&height=1280)
- Frontend  
  Built in Streamlit. Handles chat UI, team input, QR scan handling, and leaderboard rendering.  

- Backend  
  Supabase (Postgres + API) stores:
  - `teams`: slugs, names, winner timestamps
  - `stations`: station IDs and metadata
  - `paths`: ordered station list per team and current progress
  - `score_events`: point logs for each correct scan  

- Guardian LLM  
  Grok is called via the OpenAI-compatible API. Each response is seeded by the station’s riddle and scrubbed for restricted aliases. Responses are short and consistent, with one stronger hint available per station.  

- QR Generation  
  QR codes are generated with Python. Each encodes a deep link in the form:  
```https://<app-url>/?team=<slug>&station=<station_id>&scan=1```

## Technology Stack

- Python 3.10+
- Streamlit for the frontend
- Supabase for database and RPC functions
- OpenAI client for xAI Grok integration
- QRCode and Pillow for QR generation

## Installation

Clone the repository and install requirements:

```bash
git clone https://github.com/<your-org>/tuffy-hunt.git
cd tuffy-hunt
pip install -r requirements.txt
```

## Configuration

Secrets are stored in ```bash .streamlit/secrets.toml```:
```toml
SUPABASE_URL = "..."
SUPABASE_ANON_KEY = "..."

GROK_API_KEY = "..."
GROK_API_URL = "https://api.x.ai/v1"
GROK_MODEL   = "grok-4-0709"

MAX_TOKENS_PER_REPLY = "160"
TEMPERATURE = "0.25"
DAILY_REQUEST_LIMIT = "200"
DAILY_COMPLETION_TOKEN_LIMIT = "50000"
```

Provide a .streamlit/secrets.toml.example in the repository for setup instructions.

## Running Locally
```bash streamlit run ui.py```
Open the app http://localhost:8501

Use ```bash qrs.py``` to generate QR packs per team:

```bash
python qrs.py --base-url "http://localhost:8501" --team red-1234
```

