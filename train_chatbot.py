import json
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline

print("Iniciando o treinamento do chatbot...")

try:
    with open('intents.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    print("Erro: Arquivo 'intents.json' não encontrado. Certifique-se de que ele está no mesmo diretório.")
    exit()

training_sentences = []
training_labels = []

for intent in data['intents']:
    if 'patterns' in intent:
        for pattern in intent['patterns']:
            training_sentences.append(pattern)
            training_labels.append(intent['tag'])

if not training_sentences:
    print("Erro: Nenhuma frase de treinamento encontrada no arquivo 'intents.json'.")
    exit()

print(f"Encontradas {len(training_sentences)} frases para treinamento.")

model = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), SVC(kernel='linear', probability=True))

print("Treinando o modelo...")
model.fit(training_sentences, training_labels)

with open('chatbot_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Treinamento concluído! Modelo salvo como 'chatbot_model.pkl'.")