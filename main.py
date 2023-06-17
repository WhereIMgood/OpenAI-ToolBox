import openai
import time
import requests
import shutil
import openai_init

your_api_key = input("Enter your openai api key : ")
openai.api_key = your_api_key

openai_init.init()

def typeWriter(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.01)
    print()

def logger(api):
	current_date = time.strftime("%Y-%m-%d")
	file = open('logs/log.txt', 'r')
	content = file.read()
	file.close()
	write = open('logs/log.txt', 'w')
	if api == "gpt3.5-turbo":
		write.write(content+"\n"+f"YOU USED {api} at {current_date}")
	elif api == "stt":
		write.write(content+"\n"+f"YOU USED {api} at {current_date}")
	elif api == "image-generator":
		write.write(content+"\n"+f"YOU USED {api} at {current_date}")
	else:
		write.write(content+"\n"+f"UNKNOWN ERROR {current_date}")

def stt():
	logger('stt')
	print("\nStt Launched")
	audio_path = input("audio-path : ")
	audio_file= open(audio_path, "rb")
	transcript = openai.Audio.transcribe("whisper-1", audio_file)
	result = transcript["text"]
	print("Saving the result into a text file...")
	filename = input("Enter the filename for the textfile : ")
	file = open(f'stt/{filename}.txt', 'w')
	file.write(result)
	print("Done.")
	file.close()

def img_downloader(url):
	image_url = url
	print("Saving the image...")
	image_name = input("Enter image name : ")
	response = requests.get(image_url, stream=True)

	if response.status_code == 200:
	    with open(f"images/{image_name}.jpg", "wb") as file:
	        response.raw.decode_content = True
	        shutil.copyfileobj(response.raw, file)
	    response.close()
	    print("Image downloaded successfully, check the images/ folder.")
	else:
	    print("Unable to download the image. Status code:", response.status_code)

def send_message(message_log):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=message_log,
        max_tokens=50,
        temperature=0.7
    )
    for choice in response.choices:
    	if "text" in choice:
    		return choice.text
    	return response.choices[0].message.content

def image_generator():
	logger('image-generator')
	print("\nImage-generator Launched")
	prompt = input("imagine: ")
	response = openai.Image.create(
  		prompt=prompt,
  		n=1,
  		size="1024x1024"
	)
	image_url = response['data'][0]['url']
	img_downloader(image_url)

def gpt3():
	logger('gpt3.5-turbo')
	current_date = time.strftime("%Y-%m-%d")
	log = open('logs/log.txt', 'w')
	log.write(f'YOU USED GPT3.5-TURBO AT {current_date}')
	log.close()
	print("\nGPT3.5-Turbo Launched")
	message_log = [{"role": "system", "content": "You are a helpful assistant."}]
	while True:
		user_input = input("You: ")
		if user_input=="quit":
			break
		else:
			message_log.append({"role": "user", "content": user_input})
			response = send_message(message_log)
			message_log.append({"role": "assistant", "content": response})
			typeWriter(response)


def main():
	print("Welcome to OpenAI ToolBox !")
	print("""
			[1] gpt3.5-turbo
			[2] image-generator
			[3] speech-to-text

			Choose from 1 - 3.
		""")
	print("\nThe OpenAI API ToolBox Script is a Python script that integrates multiple OpenAI API's into a single program, providing users with the ability to test different OpenAI models and functionalities on their own computer. The script allows users to interact with various AI-powered features such as chat-based language generation and speech-to-text conversion.")
	function_map = {
	    "1": gpt3,
	    "2":image_generator,
	    "3":stt
	}

	user_input = input("\nWhich api you want to use: ").lower()

	if user_input in function_map:
	    function_map[user_input]()
	else:
	    print("Invalid command")

if __name__ == "__main__":
	main()
