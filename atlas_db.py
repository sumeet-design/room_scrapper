
from pymongo import MongoClient
from chapterliving import scrape_data


uri = 'mongodb+srv://sumeet:Sumeet97557@cluster0.p1aemog.mongodb.net/?retryWrites=true&w=majority'


# Establish a connection to the MongoDB cluster
client = MongoClient(uri)

# Access your database and collection
db = client['chapterlivings']  # Replace 'your_database_name' with your database name
collection = db['roomdetails']

no_of_times = int(input("Number of times you want to scrape and save data in the database: "))

for _ in range(no_of_times):
    

    data = scrape_data()  # Call the scrape_data function to get the data
    # Insert the scraped data into MongoDB
    result = collection.insert_one(data)
    print(f"Data inserted with ID: {result.inserted_id}")
