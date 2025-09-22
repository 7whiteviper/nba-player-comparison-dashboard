import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Load dataset
df = pd.read_csv("players.csv")

app = dash.Dash(__name__)
app.title = "NBA Player Comparison Dashboard"
server = app.server  # for hosting, if needed later

players = sorted(df["Player"].unique())
seasons = sorted(df["Season"].unique())

app.layout = html.Div(
    style={"maxWidth": "1100px", "margin": "0 auto", "padding": "24px"},
    children=[
        html.H1("NBA Player Comparison Dashboard", style={"textAlign": "center"}),

        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr", "gap": "12px"},
            children=[
                html.Div([
                    html.Label("Select Player A"),
                    dcc.Dropdown(players, value="LeBron James", id="player-a", clearable=False),
                ]),
                html.Div([
                    html.Label("Select Player B"),
                    dcc.Dropdown(players, value="Stephen Curry", id="player-b", clearable=False),
                ]),
                html.Div([
                    html.Label("Select Season"),
                    dcc.Dropdown(seasons, value="2022-23", id="season", clearable=False),
                ]),
            ]
        ),

        html.Div(style={"height": "12px"}),

        dcc.Graph(id="radar-chart"),
        dcc.Graph(id="bar-chart"),
        dcc.Graph(id="line-chart"),
    ]
)

@app.callback(
    [Output("radar-chart", "figure"),
     Output("bar-chart", "figure"),
     Output("line-chart", "figure")],
    [Input("player-a", "value"),
     Input("player-b", "value"),
     Input("season", "value")]
)
def update_charts(player_a, player_b, season):
    season_df = df[df["Season"] == season]
    stats = ["PTS", "AST", "REB", "FG%", "3P%", "FT%"]

    if player_a == player_b:
        # if same player selected, just duplicate so plots still render
        player_b = player_b + " (dup)"

    pa_row = season_df[season_df["Player"] == player_a.replace(" (dup)", "")]
    pb_row = season_df[season_df["Player"] == player_b.replace(" (dup)", "")]
    if pa_row.empty or pb_row.empty:
        # fallback: just use first two rows to avoid crashes
        pa_row = season_df.iloc[[0]]
        pb_row = season_df.iloc[[1]]

    pa = pa_row[stats].iloc[0].values.tolist()
    pb = pb_row[stats].iloc[0].values.tolist()

    # Radar
    radar = go.Figure()
    radar.add_trace(go.Scatterpolar(r=pa, theta=stats, fill="toself", name=player_a))
    radar.add_trace(go.Scatterpolar(r=pb, theta=stats, fill="toself", name=player_b))
    radar.update_layout(
        title=f"Skill Profile — {season}",
        polar=dict(radialaxis=dict(visible=True)),
        legend_title_text="Players",
        margin=dict(l=30, r=30, t=60, b=30)
    )

    # Grouped Bar
    bar = go.Figure()
    bar.add_bar(name=player_a, x=stats, y=pa)
    bar.add_bar(name=player_b, x=stats, y=pb)
    bar.update_layout(
        title="Stat Averages Comparison",
        barmode="group",
        margin=dict(l=30, r=30, t=60, b=30),
        yaxis_title="Value"
    )

    # Simple synthetic scoring trend (10 games) anchored around PTS
    games = list(range(1, 11))
    pa_pts = pa_row["PTS"].iloc[0]
    pb_pts = pb_row["PTS"].iloc[0]
    pa_trend = [pa_pts + ((i % 5) - 2) for i in games]
    pb_trend = [pb_pts + ((i % 4) - 1) for i in games]

    line = go.Figure()
    line.add_scatter(x=games, y=pa_trend, mode="lines+markers", name=player_a)
    line.add_scatter(x=games, y=pb_trend, mode="lines+markers", name=player_b)
    line.update_layout(
        title="Scoring Trend (sample values)",
        xaxis_title="Game",
        yaxis_title="Points",
        margin=dict(l=30, r=30, t=60, b=30)
    )

    return radar, bar, line

if __name__ == "__main__":
    # Use 0.0.0.0 so it also works in containers or cloud; keep default port.
    app.run_server(host="0.0.0.0", port=8050, debug=True)
