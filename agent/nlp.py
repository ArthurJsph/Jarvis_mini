import pickle
import os
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer

class NLPProcessor:
    def __init__(self, model_dir='../models'):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(script_dir, model_dir, 'model.pkl')
        self.vectorizer_path = os.path.join(script_dir, model_dir, 'vectorizer.pkl')
        self.model = self._load_pickle(self.model_path)
        self.vectorizer = self._load_pickle(self.vectorizer_path)
        # Embeddings model
        self.embedding_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    def _load_pickle(self, path):
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except Exception:
            print(f"Erro ao carregar {path}")
            return None

    def is_ready(self):
        return isinstance(self.model, BaseEstimator) and isinstance(self.vectorizer, TfidfVectorizer)

    def transform_text(self, text):
        if not self.vectorizer:
            raise ValueError("Vetorizador não carregado.")
        return self.vectorizer.transform([text.lower()])

    def predict_intent(self, text, confidence_threshold=0.75):
        if not self.is_ready():
            print("Modelos de NLP ausentes ou inválidos.")
            return None
        text_vectorized = self.transform_text(text)
        probabilities = self.model.predict_proba(text_vectorized)[0]
        max_idx = np.argmax(probabilities)
        max_probability = probabilities[max_idx]
        intent = self.model.classes_[max_idx]
        if max_probability >= confidence_threshold:
            return {"intent": intent, "confidence": float(max_probability)}
        else:
            return {"intent": "desconhecido", "confidence": float(max_probability)}

    def predict_all(self, text):
        if not self.is_ready():
            print("Modelos de NLP ausentes ou inválidos.")
            return []
        text_vectorized = self.transform_text(text)
        probabilities = self.model.predict_proba(text_vectorized)[0]
        intents = self.model.classes_
        return sorted(
            [{"intent": intents[i], "confidence": float(probabilities[i])} for i in range(len(intents))],
            key=lambda x: x["confidence"], reverse=True
        )

    def update_model(self, model_path, vectorizer_path):
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.model = self._load_pickle(self.model_path)
        self.vectorizer = self._load_pickle(self.vectorizer_path)

    def save_model(self, model, vectorizer, model_path=None, vectorizer_path=None):
        if model_path is None:
            model_path = self.model_path
        if vectorizer_path is None:
            vectorizer_path = self.vectorizer_path
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
        with open(vectorizer_path, "wb") as f:
            pickle.dump(vectorizer, f)
        self.update_model(model_path, vectorizer_path)

    def is_confident(self, confidence, threshold=0.75):
        return confidence >= threshold

    def embed_text(self, text):
        """Retorna embedding de uma sentença com Sentence Transformers."""
        return self.embedding_model.encode(text, convert_to_tensor=True)

    def embed_texts(self, texts):
        """Retorna embeddings para várias sentenças."""
        return self.embedding_model.encode(texts, convert_to_tensor=True)

if __name__ == '__main__':
    nlp = NLPProcessor()
    if nlp.is_ready():
        test_phrases = [
            "oi tudo bem",
            "crie uma pasta para o meu projeto",
            "qual o comando pra listar arquivos?",
            "obrigado pela ajuda",
            "executar meu script python",
            "uma frase sem sentido algum"
        ]
        for phrase in test_phrases:
            prediction = nlp.predict_intent(phrase)
            if prediction:
                print(f"Frase: '{phrase}' -> Intenção: {prediction['intent']} (Confiança: {prediction['confidence']:.2f})")

        # Exemplo de previsão de todas intenções
        all_preds = nlp.predict_all("preciso criar um diretório novo")
        print("Todas intenções com probabilidade:", all_preds)

        # Teste embed
        emb = nlp.embed_text("Olá, você pode me ajudar?")
        print("Embedding shape:", emb.shape)
    else:
        print("Modelos não disponíveis para previsão.")
