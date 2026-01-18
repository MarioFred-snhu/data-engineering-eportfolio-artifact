# layout.py – Contains the full dashboard layout

from dash import html, dcc, dash_table
import base64
import os
import pandas as pd

from helpers import get_outcome_type_column


def create_layout(df):
    """Build and return the full Dash layout."""

    # Load the Grazioso Salvare logo (relative to this file)
    logo_path = os.path.join(os.path.dirname(__file__), "Grazioso Salvare Logo.png")
    with open(logo_path, "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode()

    # Outcome type options for the adoption tab dropdown
    outcome_col = get_outcome_type_column(df)
    if outcome_col:
        outcome_values = sorted(
            df[outcome_col]
            .astype(str)
            .str.strip()
            .replace("", pd.NA)
            .dropna()
            .unique()
        )

        outcome_options = (
            [{"label": "All", "value": "all"}] +
            [{"label": str(v), "value": str(v)} for v in outcome_values]
        )
    else:
        outcome_options = []

    return html.Div([
        # Title + logo
        html.Center(html.B(html.H1("Grazioso Salvare – Rescue & Adoption Dashboard"))),

        html.Div([
            html.Img(
                src=f"data:image/png;base64,{encoded_image}",
                style={"width": "150px", "marginRight": "20px"}
            ),
            html.H2("Dashboard by Mario Frederick")
        ], style={"display": "flex", "alignItems": "center"}),

        html.Hr(),

        dcc.Tabs(id="tabs", value="tab-rescue", children=[

            # ------------------------------------------------
            # TAB 1: RESCUE READY
            # ------------------------------------------------
            dcc.Tab(label="Rescue Ready", value="tab-rescue", children=[
                html.Br(),
                html.H3("Rescue-Ready Dogs"),

                # Rescue filters
                html.Div([
                    html.Label("Rescue Category:"),
                    dcc.Dropdown(
                        id="filter-type-rescue",
                        options=[
                            {"label": "All Rescue Ready Dogs", "value": "ALL"},
                            {"label": "Water Rescue", "value": "water"},
                            {"label": "Mountain / Wilderness Rescue", "value": "mountain"},
                            {"label": "Disaster / Tracking", "value": "disaster"},
                        ],
                        value="ALL",
                        clearable=False,
                        searchable=False,
                    ),
                ], style={"width": "20%", "float": "left"}),

                html.Div([
                    dash_table.DataTable(
                        id="datatable-rescue",
                        columns=[{"name": c, "id": c} for c in df.columns],
                        data=df.to_dict("records"),
                        row_selectable="single",
                        selected_rows=[],
                        style_table={"overflowX": "auto"},
                        style_cell={"textAlign": "left", "fontSize": 12},
                        page_size=10,
                    )
                ], style={"width": "78%", "float": "right"}),

                html.Div(style={"clear": "both"}),

                html.Br(), html.Hr(),

                html.Div(
                    style={"display": "flex"},
                    children=[
                        html.Div(id="graph-rescue", style={"width": "50%"}),
                        html.Div(id="map-rescue", style={"width": "50%", "height": "500px"}),
                    ],
                ),
            ]),

            # ------------------------------------------------
            # TAB 2: ADOPTION & FOSTER
            # ------------------------------------------------
            dcc.Tab(label="Adoption & Foster", value="tab-adopt", children=[
                html.Br(),
                html.H3("Adoption & Foster View"),

                html.Div([
                    html.Label("Outcome Type (Adoption / Foster / Transfer / etc.):"),
                    dcc.Dropdown(
                        id="outcome-filter-adopt",
                        options=outcome_options,
                        value="all",
                        clearable=False,
                        style={"width": "300px"}
                    )
                ]),

                html.Br(),

                dash_table.DataTable(
                    id="datatable-adopt",
                    columns=[{"name": c, "id": c} for c in df.columns],
                    data=df.to_dict("records"),
                    row_selectable="single",
                    selected_rows=[],
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "left", "fontSize": 12},
                    page_size=10,
                ),

                html.Br(), html.Hr(),

                html.Div(id="graph-adopt"),
            ]),
        ]),
    ])