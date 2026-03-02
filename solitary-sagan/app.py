from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from deep_translator import GoogleTranslator
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Supported regional languages
LANGUAGES = {
    'hi': 'Hindi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'gu': 'Gujarati',
    'bn': 'Bengali',
    'pa': 'Punjabi'
}

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    target_lang = data.get('language', 'hi') # Default to Hindi

    try:
        # 1. Translate user message to English (simulating a backend that understands English)
        translated_to_en = GoogleTranslator(source='auto', target='en').translate(user_message)
        
        # 2. Simple chatbot logic (echo with a prefix for now)
        bot_response_en = f"You said: {translated_to_en}. How can I help you more?"
        
        # 3. Translate response back to target regional language
        bot_response_regional = GoogleTranslator(source='en', target=target_lang).translate(bot_response_en)
        
        return jsonify({
            'response': bot_response_regional,
            'original_en': translated_to_en,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'response': "I'm sorry, I had trouble understanding that.",
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/languages', methods=['GET'])
def get_languages():
    return jsonify(LANGUAGES)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
