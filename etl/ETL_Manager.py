import pandas as pd

class ETLManager:
    def __init__(self, db, logger, loader):
        self.db = db
        self.logger = logger
        self.loader = loader

#-------------------------------------
# Extract
#-------------------------------------
    def extraction(self, intake_query=None, outcome_query=None):
        """Extract raw data from MongoDB using DataLoader."""
        try:
            self.logger.info("Starting ETL: Extract stage")

            # If no query given, pull all animals
            if intake_query is None:
                intake_query = {}
            if outcome_query is None:
                outcome_query = {}

            intakes_df = self.loader.load_intakes(intake_query)
            outcomes_df = self.loader.load_outcomes(outcome_query)

            self.logger.info(f"Extract Complete: {len(intakes_df)} intakes, {len(outcomes_df)} outcomes records retrieved.")
            return intakes_df, outcomes_df

        except Exception as e:
            self.logger.error(f"Extraction failed: {e}")
            return None, None

    #---------------------
    # Deduplication (New)
    #----------------------
    def _deduplicate_by_animal(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Deduplicate records using a Python set for O(1) membership checks.
        """
        if df.empty or "animal_id" not in df.columns:
            return df

        seen = set()
        unique_rows = []

        for _, row in df.iterrows():
            aid = row["animal_id"]
            if aid not in seen:
                seen.add(aid)
                unique_rows.append(row)

        deduped_df = pd.DataFrame(unique_rows).reset_index(drop=True)
        self.logger.info(f"ETL: Deduplicated {len(df) - len(deduped_df)} rows (animal_id).")
        return deduped_df
#-------------------------------
# Transform
#-------------------------------
    def transform(self, intakes_df: pd.DataFrame, outcomes_df: pd.DataFrame):
        """Clean, deduplicate, filter, and merge intake and outcome datasets to prepare data for dashboard use."""
        try:
            self.logger.info("Beginning ETL: Transform stage")

            # ---------------------------------------------------
            # 1. Standardize column names
            # ---------------------------------------------------
            intakes_df.columns = [
                col.strip().lower().replace(" ", "_") for col in intakes_df.columns
            ]
            outcomes_df.columns = [
                col.strip().lower().replace(" ", "_") for col in outcomes_df.columns
            ]

            # ---------------------------------------------------
            # 2. Deduplicate class helper (NEW Algorithm)
            # ---------------------------------------------------
            intakes_df = self._deduplicate_by_animal(intakes_df)
            outcomes_df = self._deduplicate_by_animal(outcomes_df)

            # ---------------------------------------------------
            # 3. Merge on animal_id
            # ---------------------------------------------------
            if "animal_id" not in intakes_df.columns or "animal_id" not in outcomes_df.columns:
                raise Exception("'animal_id' column missing in one of the datasets")

            merged_df = intakes_df.merge(
                outcomes_df,
                on="animal_id",
                how="left",
                suffixes=("_intake", "_outcome")
            )

            # ---------------------------------------------------
            # 4. Derived fields (enhanced)
            # ---------------------------------------------------

            # (a) Convert age in weeks → years
            if "age_upon_outcome_in_weeks" in merged_df.columns:
                merged_df["age_in_years"] = merged_df["age_upon_outcome_in_weeks"].astype(float) / 52.0

            # (b) Extract intake + outcome year
            if "datetime_intake" in merged_df.columns:
                merged_df["intake_years"] = merged_df["datetime_intake"].astype(str).str[0:4]

            if "datetime_outcome" in merged_df.columns:
                merged_df["outcome_years"] = merged_df["datetime_outcome"].astype(str).str[0:4]

            # (c) Compute days_in_shelter (NEW Algorithm)
            if "datetime_intake" in merged_df.columns and "datetime_outcome" in merged_df.columns:
                merged_df["days_in_shelter"] = (
                        pd.to_datetime(merged_df["datetime_outcome"], errors="coerce") -
                        pd.to_datetime(merged_df["datetime_intake"], errors="coerce")
                ).dt.days
            else:
                merged_df["days_in_shelter"] = "Unknown"

            # ---------------------------------------------------
            # 5. Working Dog Classification (NEW Data Structure Use: set)
            # ---------------------------------------------------
            working_breeds = {
                "german shepherd dog",
                "labrador retriever",
                "golden retriever",
                "belgian malinois",
                "border collie",
                "australian cattle dog",
            }

            if "breed" in merged_df.columns:
                merged_df["is_working_dog"] = merged_df["breed"].astype(str).str.lower().apply(
                    lambda b: b in working_breeds
                )
            else:
                merged_df["is_working_dog"] = False

            # ---------------------------------------------------
            # 6. Fill missing values
            # ---------------------------------------------------
            merged_df = merged_df.fillna("Unknown")

            # ---------------------------------------------------
            # 7. Final log + return
            # ---------------------------------------------------
            self.logger.info(f"Transformation complete. Merged dataset contains {len(merged_df)} records.")
            return merged_df

        except Exception as e:
            self.logger.error(f"Transform failed: {e}")
            return pd.DataFrame()

    #------------------------
    # Load to Dashboard
    #------------------------
    def load_to_dashboard(self, df):
        """Final load stage before returning DataFrame to Dashboard."""
        try:
            self.logger.info("Starting ETL: Load stage")

            if "datetime_intake" in df.columns:
                df = df.sort_values("datetime_intake", ascending=False)

            # Any final structure or sorting goes here
            self.logger.info("Clean dataframe ready for dashboard.")
            return df

        except Exception as e:
            self.logger.error(f"Load failed: {e}")
            return df

    #-------------------------------------
    # Full ETL Pipeline Helper (New)
    #-------------------------------------
    def run_pipeline(self, intake_query=None, outcome_query=None):
        """
        Run the full ETL pipeline:
        1) Extract intake & outcome data
        2) Transform it (clean, deduplicate, merge, derive fields)
        3) Load it for dashboard use (sorting, final structure)
        """
        self.logger.info("Starting full ETL pipeline run.")

        # 1. Extract
        intakes_df = self.loader.load_intakes(intake_query)
        outcomes_df = self.loader.load_outcomes(outcome_query)

        # 2. Transform
        transformed_df = self.transform(intakes_df=intakes_df, outcomes_df=outcomes_df)

        # 3. Load
        final_df = self.load_to_dashboard(transformed_df)

        self.logger.info(
            f"ETL pipeline complete. Final dataframe contains {len(final_df)} records."
        )
        return final_df