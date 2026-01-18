from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from dotenv import load_dotenv
import os


# Load environment variables from .env
load_dotenv()


class AnimalShelter:
    """Enhanced CRUD class for MongoDB Atlas with environment-based credentials and improved structure."""

    def __init__(self):
        """Initialize secure MongoDB connection using environment-based credentials."""
        try:
            # Load credentials from .env
            username = os.getenv("MONGO_USER")
            password = os.getenv("MONGO_PASS")
            cluster = os.getenv("MONGO_CLUSTER")
            db_name = os.getenv("MONGO_DB", "aac")

            # Validate required values
            if not all([username, password, cluster]):
                raise Exception("Missing required MongoDB credentials in .env file.")

            # Build the secure connection string
            mongo_uri = (
                f"mongodb+srv://{username}:{password}@{cluster}.mongodb.net/"
                f"{db_name}?retryWrites=true&w=majority"
            )

            # Create the client and select database
            self.client = MongoClient(mongo_uri)
            self.database = self.client[db_name]

            print("Connected to MongoDB Atlas successfully using secure .env variables.")

        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB Atlas: {e}")
            raise

        # ---------------------------------------
        # INDEXES FOR PERFORMANCE (Enhancement #2)
        # ---------------------------------------

        try:
            # Create indexes on fields frequently used in queries/filters
            self.database["animals"].create_index("animal_type")
            self.database["animals"].create_index("breed")
            self.database["animals"].create_index("outcome_type")

            print("Indexes created successfully for performance optimization.")

        except Exception as e:
            print(f"Index creation failed: {e}")

    # -------------------------------
    # CREATE
    # -------------------------------
    def create(self, data: dict, collection: str):
        """Insert a new document into the MongoDB collection."""
        if not collection:
            raise Exception("Collection name required.")
        if not data:
            return False

        try:
            result = self.database[collection].insert_one(data)
            return result.acknowledged
        except OperationFailure as e:
            print(f"Create failed: {e}")
            return False

    # -------------------------------
    # READ (NO PAGINATION – DASH HANDLES IT)
    # -------------------------------
    def read(self, query: dict, collection: str):
        """Read ALL documents that match the query (no pagination)."""
        if not collection:
            raise Exception("Collection name required.")

        try:
            if query is None:
                query = {}

            return list(self.database[collection].find(query))

        except OperationFailure as e:
            print(f"Read failed: {e}")
            return []
    # -------------------------------
    # UPDATE
    # -------------------------------
    def update(self, query: dict, new_data: dict, collection: str):
        """Update documents that match query."""
        if not collection:
            raise Exception("Collection name required.")
        try:
            result = self.database[collection].update_many(query, {"$set": new_data})
            return result.modified_count
        except OperationFailure as e:
            print(f"Update failed: {e}")
            return 0

    # -------------------------------
    # DELETE
    # -------------------------------
    def delete(self, query: dict, collection: str):
        """Delete documents that match query."""
        if not collection:
            raise Exception("Collection name required.")
        try:
            result = self.database[collection].delete_many(query)
            return result.deleted_count
        except OperationFailure as e:
            print(f"Delete failed: {e}")
            return 0

    #-----------------------
    # Aggregation pipelines
    #-----------------------

    # Breed Distribution pipeline
    def breed_distribution(self, collection: str = "animals"):
        """Aggregation pipeline: count animals per breed."""
        pipeline = [
            {"$group": {"_id": "$breed", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        return list(self.database[collection].aggregate(pipeline))

    # Age distribution pipeline
    def age_distribution(self, collection: str = "animals"):
        """Aggregation pipeline: count animals by age group."""
        pipeline = [
            {"$group": {"_id": "$age_group", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        return list(self.database[collection].aggregate(pipeline))

    # Rescue ready pipeline
    def rescue_ready(self, collection: str = "animals"):
        """Aggregation pipeline: animals marked rescue-ready."""
        pipeline = [
            {"$match": {"rescue_ready": True}}
        ]
        return list(self.database[collection].aggregate(pipeline))

    # Average days in Shelter pipeline
    def avg_days_in_shelter(self, collection: str = "animals"):
        pipeline = [
            {"$group": {"_id": None, "avg_days": {"$avg": "$days_in_shelter"}}}
        ]
        result = list(self.database[collection].aggregate(pipeline))
        return result[0]["avg_days"] if result else None