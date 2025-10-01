import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import defaultdict

class KnowledgeBase:
    def __init__(self, json_paths):
        """
        Recebe uma lista de arquivos ou um único arquivo (string).
        """
        if isinstance(json_paths, str) or isinstance(json_paths, Path):
            json_paths = [json_paths]
        self.data_paths = [Path(p) for p in json_paths]
        self.knowledge = self.load_multiple_knowledges()
        self.intents = self.knowledge.get("intencoes", {})
        self.patterns = []
        self.pattern_to_intent = {}
        self._prepare_patterns()
        self.vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=1000)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.patterns) if self.patterns else None
        self.entities = self.knowledge.get("entidades", {})

    def load_knowledge(self, path):
        if not Path(path).is_file():
            raise FileNotFoundError(f"Arquivo {path} não encontrado.")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Faz fallback de estrutura, caso o "content" exista
        return data.get("content", data)

    def load_multiple_knowledges(self):
        """
        Une intenções e entidades de múltiplos arquivos JSON.
        """
        combined_intents = defaultdict(lambda: {"padroes": [], "respostas": []})
        combined_entities = defaultdict(set)

        for path in self.data_paths:
            data = self.load_knowledge(path)
            intents = data.get("intencoes", {})
            entities = data.get("entidades", {})
            for intent_name, intent_data in intents.items():
                combined_intents[intent_name]["padroes"].extend(intent_data.get("padroes", []))
                combined_intents[intent_name]["respostas"].extend(intent_data.get("respostas", []))
            for entity_name, entity_values in entities.items():
                combined_entities[entity_name].update(entity_values)

        # Remove duplicados e normaliza
        for intent in combined_intents.values():
            intent["padroes"] = list(set([p.lower() for p in intent["padroes"]]))
            intent["respostas"] = list(set(intent["respostas"]))

        entities_final = {k:list(v) for k,v in combined_entities.items()}
        return {"intencoes": dict(combined_intents), "entidades": entities_final}

    def get_intents(self):
        return self.intents

    def get_entities(self):
        return self.entities

    def find_responses(self, intent_name):
        intent = self.intents.get(intent_name, {})
        return intent.get("respostas", [])

    def find_patterns(self, intent_name):
        intent = self.intents.get(intent_name, {})
        return intent.get("padroes", [])

    def _prepare_patterns(self):
        for intent, details in self.intents.items():
            for pattern in details.get("padroes", []):
                pattern_lower = pattern.lower()
                self.patterns.append(pattern_lower)
                self.pattern_to_intent[pattern_lower] = intent

    def find_most_similar_pattern(self, user_text, threshold=0.5):
        if not self.tfidf_matrix or not self.patterns:
            return None
        user_vec = self.vectorizer.transform([user_text.lower()])
        similarities = cosine_similarity(user_vec, self.tfidf_matrix).flatten()
        max_idx = np.argmax(similarities)
        max_sim = similarities[max_idx]
        if max_sim >= threshold:
            return self.patterns[max_idx]
        return None

    def get_response_by_pattern(self, pattern):
        intent = self.pattern_to_intent.get(pattern)
        if intent:
            return self.find_responses(intent)
        return []

    def get_all_patterns(self):
        return self.patterns

    def add_new_intent(self, intent_name, patterns=None, responses=None):
        if intent_name in self.intents:
            return False
        self.intents[intent_name] = {
            "padroes": patterns or [],
            "respostas": responses or []
        }
        # Atualiza padrões e vetorizador
        for p in self.intents[intent_name]["padroes"]:
            p_lower = p.lower()
            self.patterns.append(p_lower)
            self.pattern_to_intent[p_lower] = intent_name
        if self.patterns:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.patterns)
        return True

    def update_intent_responses(self, intent_name, responses):
        if intent_name not in self.intents:
            return False
        self.intents[intent_name]["respostas"] = responses
        return True

    def save_knowledge(self, json_path=None):
        path = Path(json_path) if json_path else self.data_paths[0]
        to_save = {"intencoes": self.intents, "entidades": self.entities}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(to_save, f, indent=4, ensure_ascii=False)
        return True
