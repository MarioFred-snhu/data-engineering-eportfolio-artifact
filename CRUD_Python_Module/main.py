from crud import AnimalShelter

#Create an instance of the aAnimalShelter class using .env credentials
db = AnimalShelter()

#test a basic read from database
try:
    results = db.read({})
    print("Connection test successful")
    print("Document found:", len(results))
except Exception as e:
    print("Connection test failed", e)