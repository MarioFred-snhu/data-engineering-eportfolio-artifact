# app.py – Main entry point for the enhanced Grazioso Salvare dashboard
import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dash import Dash

from CRUD_Python_Module.crud import AnimalShelter
from etl.logger import get_logger
from etl.Data_Loader import DataLoader
from etl.ETL_Manager import ETLManager

from layout import create_layout
from callbacks import register_callbacks


# -------------------------------------------------------------
# BACKEND SETUP: DB + LOGGER + ETL PIPELINE
# -------------------------------------------------------------

logger = get_logger("dashboard")

# Secure CRUD class (reads credentials from .env)
db = AnimalShelter()

# Data loader + ETL manager
loader = DataLoader(db=db, logger=logger)
etl_manager = ETLManager(db=db, logger=logger, loader=loader)

# Extract both collections
intakes_df, outcomes_df = etl_manager.extraction()

# Transform → merge → clean
merged_df = etl_manager.transform(intakes_df, outcomes_df)
df = etl_manager.load_to_dashboard(merged_df)

# Remove _id if present
if "_id" in df.columns:
    df = df.drop(columns=["_id"])


# -------------------------------------------------------------
# DASH APP SETUP
# -------------------------------------------------------------

app = Dash(__name__)

# Layout
app.layout = create_layout(df)

# Callbacks (must come after app + layout)
register_callbacks(app, df, logger)


# -------------------------------------------------------------
# MAIN
# -------------------------------------------------------------
if __name__ == "__main__":
    logger.info("Starting Dash server for Grazioso Salvare dashboard...")
    # Dash v2+ uses app.run (run_server is obsolete in your environment)
    app.run(debug=True, use_reloader=False)