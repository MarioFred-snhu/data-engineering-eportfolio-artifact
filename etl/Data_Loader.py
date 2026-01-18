import pandas as pd


class DataLoader:
    def __init__(self, db, logger):
        self.db = db
        self.logger = logger

    # ------------------
    # Load Intake Data
    # ------------------
    def load_intakes(self, query=None):
        """Load intake records from MongoDB and return a clean DataFrame."""
        try:
            self.logger.info("DataLoader: Loading intake records from MongoDB.")

            # Read from MongoDB
            data = self.db.read(query if query else {}, collection="intakes")
            df = pd.DataFrame(data)

            # ---------------------------------------------------------
            # 1. Remove MongoDB ObjectId
            # ---------------------------------------------------------
            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            # ---------------------------------------------------------
            # 2. Standardize column names (NEW Enhancement)
            # ---------------------------------------------------------
            df.columns = [
                col.strip().lower().replace(" ", "_")
                for col in df.columns
            ]

            # ---------------------------------------------------------
            # 3. Drop records missing animal_id (NEW Algorithm)
            # ---------------------------------------------------------
            if "animal_id" in df.columns:
                before = len(df)
                df = df.dropna(subset=["animal_id"])
                after = len(df)
                dropped = before - after
                self.logger.info(f"DataLoader: Dropped {dropped} intake rows missing animal_id.")

            df["animal_id"] = df["animal_id"].astype(str)

            # ---------------------------------------------------------
            # 4. Convert datetime_intake string → datetime (NEW)
            # ---------------------------------------------------------
            if "datetime_intake" in df.columns:
                df["datetime_intake"] = pd.to_datetime(df["datetime_intake"], errors="coerce")

            # ---------------------------------------------------------
            # 5. Create index using animal_id for fast join performance (NEW DS)
            # ---------------------------------------------------------
            if "animal_id" in df.columns:
                df = df.set_index("animal_id", drop=False)

            # ---------------------------------------------------------
            # 6. Final log + return
            # ---------------------------------------------------------
            self.logger.info(f"DataLoader: Loaded {len(df)} cleaned intake records.")
            return df

        except Exception as e:
            self.logger.error(f"DataLoader: Intake loading failed: {e}")
            return pd.DataFrame()

    # ------------------------------------
    # Load outcome
    # ------------------------------------
    def load_outcomes(self, query=None):
        """Load outcome CSV Records from MongoDB and return a clean DataFrame."""
        try:
            self.logger.info("Dataloader: Loading outcome records from MongoDB.")

            # Read from MongoDB
            data = self.db.read(query if query else {}, collection="outcomes")
            df = pd.DataFrame(data)

            # -------------------------------------------
            # 1. Remove MongoDB ObjectId
            # -------------------------------------------
            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            # -------------------------------------------
            # 2. Standardize column names (NEW)
            # -------------------------------------------
            df.columns = [
                col.strip().lower().replace(" ", "_")
                for col in df.columns
            ]

            # -------------------------------------------
            # 3. Drop rows missing animal_id (NEW Algorithm)
            # -------------------------------------------
            if "animal_id" in df.columns:
                before = len(df)
                df = df.dropna(subset=["animal_id"])
                after = len(df)
                dropped = before - after
                self.logger.info(
                    f"DataLoader: Dropped {dropped} outcome rows missing animal_id."
                )

            df["animal_id"] = df["animal_id"].astype(str)

            # -------------------------------------------
            # 4. Convert outcome datetime string → datetime (NEW)
            # -------------------------------------------
            if "datetime_outcome" in df.columns:
                df["datetime_outcome"] = pd.to_datetime(
                    df["datetime_outcome"], errors="coerce"
                )

            # -------------------------------------------
            # 5. Set index to animal_id for faster merging (NEW DS)
            # -------------------------------------------
            if "animal_id" in df.columns:
                df = df.set_index("animal_id", drop=False)

            # -------------------------------------------
            # Final log + return
            # -------------------------------------------
            self.logger.info(f"DataLoader: Loaded {len(df)} cleaned outcome records.")
            return df

        except Exception as e:
            self.logger.error(f"DataLoader: Outcome loading failed: {e}")
            return pd.DataFrame()