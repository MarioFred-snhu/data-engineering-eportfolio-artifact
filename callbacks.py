# callbacks.py
from dash.dependencies import Input, Output
from dash import dcc, html
import plotly.express as px
import pandas as pd
import dash_leaflet as dl

from helpers import (
    get_breed_column,
    get_outcome_type_column,
    get_age_column,
    DEFAULT_LOCATION
)


def register_callbacks(app, df, logger):
    # =============================================================
    # TAB 1 – RESCUE READY (FILTER + TABLE)
    # =============================================================
    @app.callback(
        [Output("datatable-rescue", "data"),
         Output("datatable-rescue", "selected_rows")],
        Input("filter-type-rescue", "value"),
    )
    def update_rescue_table(filter_type):
        logger.info(f"[Rescue] Filter selected: {filter_type}")

        # Normalize blank/None
        if not filter_type:
            filter_type = "ALL"

        dff = df.copy()
        breed_col = get_breed_column(dff)

        if not breed_col or filter_type == "ALL":
            logger.info(f"[Rescue] Returning ALL rows. breed_col={breed_col}, rows={len(dff)}")
            return dff.to_dict("records"), []

        # Detect age column
        age_col = get_age_column(dff)
        if age_col:
            dff[age_col] = pd.to_numeric(dff[age_col], errors="coerce")

        # Rescue definitions
        if filter_type == "water":
            breeds = ["Labrador", "Retriever", "Newfoundland"]
            age_limit = 2
        elif filter_type == "mountain":
            breeds = ["German Shepherd", "Malamute", "Sheepdog"]
            age_limit = 3
        elif filter_type == "disaster":
            breeds = ["Doberman", "German Shepherd", "Bloodhound"]
            age_limit = 3
        else:
            return dff.to_dict("records"), []

        logger.info(f"[Rescue] Rows before filter: {len(dff)} (breed_col={breed_col}, age_col={age_col})")

        # Partial match filter
        pattern = "|".join(b.lower() for b in breeds)

        rescue_df = dff[
            dff[breed_col]
            .astype(str)
            .str.lower()
            .str.contains(pattern, na=False)
        ]

        # Apply age filter
        if age_col:
            rescue_df = rescue_df[rescue_df[age_col] <= age_limit]

        logger.info(f"[Rescue] Rows after filter: {len(rescue_df)}")

        return rescue_df.to_dict("records"), []

    # =============================================================
    # RESCUE PIE CHART
    # =============================================================
    @app.callback(
        Output("graph-rescue", "children"),
        Input("datatable-rescue", "derived_virtual_data"),
    )
    def update_rescue_pie(table_data):
        if not table_data:
            return [html.P("No data available")]

        dff = pd.DataFrame(table_data)
        breed_col = get_breed_column(dff)

        if not breed_col:
            return [html.P("Breed data unavailable")]

        fig = px.pie(dff, names=breed_col, title="Rescue-Ready Dogs by Breed")
        fig.update_layout(height=400)

        return [
            dcc.Graph(
                figure=fig,
                style={"height": "100%"},
                config={"responsive": True}
            )
        ]

    # =============================================================
    # RESCUE MAP (UPDATED)
    # =============================================================
    @app.callback(
        Output("map-rescue", "children"),
        [Input("datatable-rescue", "derived_virtual_data"),
         Input("datatable-rescue", "derived_virtual_selected_rows")]
    )
    def update_rescue_map(table_data, selected_rows):
        def default_map():
            return dl.Map(
                center=DEFAULT_LOCATION,
                zoom=10,
                style={"width": "100%", "height": "450px"},
                children=[dl.TileLayer()]
            )

        # If nothing to show yet, return default
        if not table_data or not selected_rows:
            return [default_map()]

        dff = pd.DataFrame(table_data)

        # Debug (helps you confirm selection + columns)
        logger.info(f"[Map] selected_rows={selected_rows}")
        logger.info(f"[Map] table columns={list(dff.columns)} rows={len(dff)}")

        row_index = selected_rows[0]

        # Guard: selection can be out of range after filtering/sorting
        if row_index >= len(dff):
            logger.warning(f"[Map] row_index out of range: {row_index} for {len(dff)} rows")
            return [default_map()]

        # Auto-detect lat/lon column names
        lat_col_candidates = ["location_lat", "lat", "latitude", "location_latitude"]
        lon_col_candidates = ["location_long", "location_lon", "lon", "longitude", "location_longitude"]

        lat_col = next((c for c in lat_col_candidates if c in dff.columns), None)
        lon_col = next((c for c in lon_col_candidates if c in dff.columns), None)

        if not lat_col or not lon_col:
            logger.warning(f"[Map] Missing lat/lon columns. Found: {list(dff.columns)}")
            return [default_map()]

        # Parse coordinates safely
        try:
            lat = float(dff.iloc[row_index][lat_col])
            lon = float(dff.iloc[row_index][lon_col])
        except Exception as e:
            logger.warning(f"[Map] Bad lat/lon values: {e}")
            return [default_map()]

        breed_col = get_breed_column(dff)
        tooltip_text = dff.iloc[row_index].get(breed_col, "Unknown") if breed_col else "Unknown"
        popup_text = dff.iloc[row_index].get("name_intake", dff.iloc[row_index].get("name", "Unknown"))

        logger.info(f"[Map] Using coords lat={lat}, lon={lon}, tooltip={tooltip_text}")

        return [
            dl.Map(
                center=[lat, lon],
                zoom=10,
                style={"width": "100%", "height": "450px"},
                children=[
                    dl.TileLayer(),
                    dl.Marker(
                        position=[lat, lon],
                        children=[
                            dl.Tooltip(tooltip_text),
                            dl.Popup(popup_text)
                        ]
                    )
                ]
            )
        ]

    # =============================================================
    # TAB 2 – ADOPTION & FOSTER
    # =============================================================
    @app.callback(
        [Output("datatable-adopt", "data"),
         Output("graph-adopt", "children")],
        Input("outcome-filter-adopt", "value"),
    )
    def update_adopt_view(outcome_filter):
        # Normalize blank/None to "all"
        if not outcome_filter:
            outcome_filter = "all"

        logger.info(f"[Adopt] Outcome filter selected: '{outcome_filter}'")

        dff = df.copy()
        outcome_col = get_outcome_type_column(dff)
        breed_col = get_breed_column(dff)

        logger.info(f"[Adopt] outcome_col={outcome_col}, breed_col={breed_col}, rows before={len(dff)}")

        if outcome_col and outcome_filter != "all":
            dff = dff[
                dff[outcome_col].astype(str).str.strip()
                == str(outcome_filter).strip()
            ]

        logger.info(f"[Adopt] rows after filter={len(dff)}")

        if not outcome_col or not breed_col:
            return dff.to_dict("records"), [html.P("Outcome or breed data unavailable.")]

        counts = (
            dff.groupby([outcome_col, breed_col])
            .size()
            .reset_index(name="count")
        )

        fig = px.bar(
            counts,
            x=breed_col,
            y="count",
            color=outcome_col,
            title="Outcome Counts by Breed"
        )
        fig.update_layout(height=450)

        return dff.to_dict("records"), [dcc.Graph(figure=fig, style={"height": "100%"})]