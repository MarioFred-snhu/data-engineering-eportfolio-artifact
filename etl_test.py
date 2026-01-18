from CRUD_Python_Module.crud import AnimalShelter
from etl.Data_Loader import DataLoader
from etl.ETL_Manager import ETLManager
from etl.logger import get_logger
import pandas as pd



# -------------------------
# Setup
# -------------------------
logger = get_logger("etl_test")

# Connect to MongoDB Atlas (uses .env)
db = AnimalShelter()

# Create DataLoader + ETLManager
loader = DataLoader(db, logger)
etl = ETLManager(db, logger, loader)

# -------------------------
# Test Extraction
# -------------------------
print("\n🔍 TESTING EXTRACTION...")
intakes_df, outcomes_df = etl.extraction()

print(f"Intakes loaded: {len(intakes_df)}")
print(f"Outcomes loaded: {len(outcomes_df)}")

print("\n📄 Intakes sample:")
print(intakes_df.head())

print("\n📄 Outcomes sample:")
print(outcomes_df.head())

# -------------------------
# Test Transform
# -------------------------
print("\n⚙️ TESTING TRANSFORMATION...")
merged_df = etl.transform(intakes_df, outcomes_df)

print(f"Merged dataset: {len(merged_df)} records")
print(merged_df.head())

# -------------------------
# Test Load to Dashboard
# -------------------------
print("\n📊 TESTING LOAD STAGE...")
dashboard_df = etl.load_to_dashboard(merged_df)

print("Final dashboard dataframe sample:")
print(dashboard_df.head())