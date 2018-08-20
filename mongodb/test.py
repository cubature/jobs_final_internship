import datetime
import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.test_database # select or create batabase
collection = db.test_collection # select or create collection
post = {
	"author": "Mike",
	"text": "My first blog post!",
	"tags": ["mongodb", "python", "pymongo"],
	"date": datetime.datetime.utcnow()
	}
posts = db.posts # another collection(?)
post_id = posts.insert_one(post).inserted_id
print(post_id)
print(db.collection_names(include_system_collections=False))

# find_one() find the last one inserted
pprint.pprint(posts.find_one())
# or
pprint.pprint(posts.find_one({"author": "Mike"}))


# bulk insert
print("--------------------------bulk insert-------------------------------")
new_posts = [
	{
		"author": "Mike",
		"text": "Another post!",
		"tags": ["bulk", "insert"],
		"date": datetime.datetime(2009, 11, 12, 11, 14)
	},
	{
		"author": "Eliot",
		"title": "MongoDB is fun",
		"text": "and pretty easy too",
		"date": datetime.datetime(2009, 11, 10, 10, 45)
	}
	]

result = posts.insert_many(new_posts)
print(result.inserted_ids)

for post in posts.find():
	pprint.pprint(post)






posts.delete_many({"author": "Mike"})
posts.delete_many({"author": "Eliot"})