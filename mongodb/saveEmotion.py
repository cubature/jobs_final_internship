import datetime
import pprint
from pymongo import MongoClient
import gridfs
from bson.objectid import ObjectId

server = 'localhost'
port = 27017
analysisConversationDB = 'EmoticChatbot'
multimediaFilesDB = 'MultimediaFiles'

client = MongoClient(server, port)
emoticChatbotDb = client[analysisConversationDB]
conversations = emoticChatbotDb['conversations']
mediaFilesDb = client[multimediaFilesDB]
fs = gridfs.GridFS(mediaFilesDb)

def saveAnalysis(deltaTime, image, sound, theme, userId, feedback, analysis):
	"""save the analysis of emotion of one clip in the database
	
	Args: 
		deltaTime: A number representing the duration of the clip in millisecond
		image: A string of the path of the file of the image
		sound: A string of the path of the file of the sound
		theme: A string representing the theme of the conversation
		userId: A string(?) of the user's ID
		feedback: An object about the user's feedback. Its structure is:
			{
				'getWhatWasExpectedMarck': An integer in [1, 5] representing the rate of the evaluation of the user, 5 = very good,
				'comment': A string describing the problem of the chatbot from the user
			}
		analysis: An array of the analysis result of the different API:
			[
				{
					'apiName': A string of the API name,
					'joy': A number of the possibility of being this type of emotion,
					'surprise': idem,
					...
				},
				...
			]
			
	Returns: 
		An ObjectId representing the id of the saved data
	"""
	imageId = fs.put(open(image, "rb"))
	soundId = fs.put(open(sound, "rb"))

	conversation = {
		'deltaTime': deltaTime,
		'image': imageId,
		'sound': soundId,
		'theme': theme,
		'userId': userId,
		'feedback': feedback,
		'analysis': analysis
	}

	return conversations.insert_one(conversation).inserted_id;


if __name__ == '__main__':
	# data to be saved
	deltaTime = 5000
	image = "./original/Capture.PNG"
	sound = "./original/sound_1525099358795.wav"
	theme = "congé"
	userId = 1111
	feedback = {
		'getWhatWasExpectedMark': 4,
		'comment': "was hard to get that answer"
	}
	analysis = [
		{
			'apiName': "BeyondVerbal",
			'joy': 0.2,
			'surprise': 0.8
		}
	]

	# save the data in the database
	insertedId = saveAnalysis(deltaTime, image, sound, theme, userId, feedback, analysis)
	pprint.pprint(insertedId)

	# print the data just saved
	storedData = conversations.find_one({'_id': insertedId})
	pprint.pprint(storedData)

	# get the multimedia files
	imgId = storedData['image']
	sndId = storedData['sound']
	img = fs.get(imgId)
	snd = fs.get(sndId)

	# save the multimedia files with another filename to verify if we can read the multimedia files from MongoDB correctly
	writeImg = open("./outputs/img.png", "wb")
	writeImg.write(img.read())
	writeImg.close()
	writeSnd = open("./outputs/snd.wav", "wb")
	writeSnd.write(snd.read())
	writeSnd.close()

	# delete the files just saved in the database
	fs.delete(sndId)
	fs.delete(imgId)
	conversations.delete_one({'_id': insertedId})

	# test if the files are well deleted
	test = conversations.find_one()
	pprint.pprint(test)
	print(fs.exists(imgId))
	print(fs.exists(sndId))

	# drop the test database
	# client.drop_database(analysisConversationDB)
	# client.drop_database(multimediaFilesDB)