import os
import time

def init():
	print("Initializing openai-toolbox...")
	if os.path.exists('images'):
		pass
	elif os.path.exists('stt'):
		pass
	elif os.path.exists('logs'):
		pass

	else:
		print("Making the 'images' folder to store generated images")
		os.mkdir('images')
		print("Making the 'stt' folder to store transcribed audio's")
		os.mkdir('stt')
		print("Making the 'logs' folder to store the logs")
		os.mkdir('logs')
		log_file = open('logs/log.txt', 'w')
		log_file.write("")
		log_file.close()

	time.sleep(0.5)
	print("Done.")