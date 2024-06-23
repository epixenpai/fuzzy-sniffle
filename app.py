from flask import Flask, render_template, request, jsonify
from characterai import pycai
import asyncio
import os
import edge_tts
from playsound import playsound
from datetime import datetime
char = 'MhTU6bxiAQSNCWtVAu1zRz-HvJlH-eZBVcY2HNT1q9g'    #epixy
char1='dOPyGlfG6mq2VrT1fWuESrUTuMGKwZnO6Npq2543d2E' #aibuddy
app = Flask(__name__)

# Initialize Character AI client
client = pycai.Client('2aeee7a58ff0d839b0a3c854cb7bf07291357720')  # Replace with your actual API key
me = client.get_me()

# Define the file to save chat_id
CHAT_ID_FILE = "chat_id.txt"
def get_current_datetime():
    now = datetime.now()
    return now.strftime("date: %Y-%m-%d time:%H:%M"+ " (please dont say it until i ask you to assit me in any time/date related query")
def remove_text_between_double_asterisks(text):
    new_text = ''
    inside_asterisks = False

    for char in text:
        if char == '*':
            inside_asterisks = not inside_asterisks
        elif not inside_asterisks:
            new_text += char

    return new_text

def load_chat_id():
    if os.path.exists(CHAT_ID_FILE):
        with open(CHAT_ID_FILE, 'r') as f:
            return f.read().strip()
    return None

def save_chat_id(chat_id):
    with open(CHAT_ID_FILE, 'w') as f:
        f.write(chat_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    time = get_current_datetime()
    user_input = request.json['input'] +""+time

    # Simulate API call (replace with actual interaction with c.ai)
    with client.connect() as chat:
        chat_id = load_chat_id()
        if not chat_id:
            new, answer = chat.new_chat(char, me.id)  # Replace with your actual character ID
            chat_id = new.chat_id
            save_chat_id(chat_id)

        # Send user message to c.ai
        message = chat.send_message(char, chat_id, user_input)
        response_text = message.text

    return jsonify({'response': response_text})

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    text = data['text']

    # Save audio and play it
    asyncio.run(speak(text))
    return jsonify({'status': 'success'})

async def speak(text, voice="en-US-AvaNeural"):
    communicate = edge_tts.Communicate(text, voice)
    output_file = "output1.mp3"
    await communicate.save(output_file)
    playsound(output_file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
