import json
import random
import pickle
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS # type: ignore

app = Flask(__name__)
CORS(app)

try:
    with open('chatbot_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('intents.json', 'r', encoding='utf-8') as f:
        intents = json.load(f)
except FileNotFoundError as e:
    print(f"Erro: Arquivo não encontrado - {e}. Certifique-se de que 'chatbot_model.pkl' e 'intents.json' existem.")
    exit()

responses_dict = {intent['tag']: intent['responses'] for intent in intents['intents']}
FALLBACK_TAG = "fallback" 

@app.route('/')
def home():
    """Rota principal que renderiza a página HTML do chatbot."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Rota que recebe a mensagem do usuário e retorna a resposta do chatbot."""
    try:
        user_message = request.json['message']
        
        probabilities = model.predict_proba([user_message])[0]
        max_prob = max(probabilities)
        
        CONFIDENCE_THRESHOLD = 0.1
        
        if max_prob > CONFIDENCE_THRESHOLD:
            tag = model.predict([user_message])[0]
        else:
            tag = FALLBACK_TAG
            
        response = random.choice(responses_dict.get(tag, responses_dict[FALLBACK_TAG]))
        
        return jsonify({'response': response})

    except Exception as e:
        print(f"Erro no endpoint /chat: {e}")
        return jsonify({'response': 'Ocorreu um erro no servidor. Tente novamente.'}), 500

if __name__ == '__main__':
    app.run(debug=True)