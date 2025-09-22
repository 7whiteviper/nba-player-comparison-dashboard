

# NBA Player Comparison Dashboard

An interactive dashboard (Python **Dash** + **Plotly**) for comparing NBA players’ season stats.

## Features
- Player A vs Player B for a selected season
- **Radar chart**: PTS, AST, REB, FG%, 3P%, FT%
- **Grouped bar chart**: side-by-side comparison
- **Trend line**: simple synthetic 10-game scoring trend (for demo)

## Quickstart

```bash
# 1) Clone
git clone https://github.com/YOUR_USERNAME/nba-player-comparison-dashboard.git
cd nba-player-comparison-dashboard

# 2) (Optional) Create a virtual environment
# macOS/Linux
python3 -m venv .venv && source .venv/bin/activate
# Windows
python -m venv .venv && .venv\Scripts\activate

# 3) Install deps
pip install -r requirements.txt

# 4) Run
python app.py
