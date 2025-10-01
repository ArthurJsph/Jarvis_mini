import random
import logging
from agent.nlp import NLPProcessor
from agent.llm_api import LLMAPI
from agent.memory import MemoryManager
from agent.plugins.plugins import PluginManager
from agent.knowledge_base import KnowledgeBase
from agent.reranker import Reranker
from config.config import KNOWLEDGE_BASE_PATH, LOG_LEVEL



class AgentCore:
    CONTEXT_LIMIT = 50  # máximo de interações guardadas no contexto

    def __init__(self):
        logging.basicConfig(level=LOG_LEVEL)
        self.nlp = NLPProcessor()
        self.llm = LLMAPI()
        self.memory = MemoryManager()
        self.plugins = PluginManager()
        self.reranker = Reranker()
        self.context = self.load_context()

        self.kb = KnowledgeBase([
            "data/knowledge_data_large.json",
            "data/knowledge_data_large1.json",
            "data/knowledge_data_large2.json",
            "data/knowledge_data_large3.json",
            "data/knowledge_data_large4.json",
            "data/knowledge_data_large5.json",
            "data/knowledge_data_large6.json",
            "data/knowledge_data_large7.json",
            "data/knowledge_data_large8.json",
            "data/knowledge_data_large9.json",
            "data/knowledge_data_large10.json",
            "data/knowledge_data.json"
        ])

    def load_context(self):
        history = self.memory.load_history()
        if len(history) > self.CONTEXT_LIMIT:
            history = history[-self.CONTEXT_LIMIT:]
        return history

    def save_context(self, user_input, agent_response):
        self.context.append({"user": user_input, "agent": agent_response})
        if len(self.context) > self.CONTEXT_LIMIT:
            self.context = self.context[-self.CONTEXT_LIMIT:]
        self.memory.save_interaction(user_input, agent_response)

    def detect_intent(self, text):
        prediction = self.nlp.predict_intent(text, confidence_threshold=0.6)
        if prediction and prediction['intent'] != "desconhecido":
            logging.info(f"Intenção detectada: {prediction['intent']} (Confiança: {prediction['confidence']:.2f})")
            return prediction['intent']
        logging.info("Nenhuma intenção confiável detectada.")
        return None

    def get_response_from_knowledge(self, intent, user_input):
        responses = self.kb.find_responses(intent)
        if responses:
            # Utiliza reranker para melhorar resposta, se possível
            best_response = self.reranker.rank_best_response(user_input, responses)
            return best_response or random.choice(responses)
        return None

    def get_response(self, user_input):
        intent = self.detect_intent(user_input)
        if intent:
            response = self.get_response_from_knowledge(intent, user_input)
            if response:
                self.save_context(user_input, response)
                return response

        similar_pattern = self.kb.find_most_similar_pattern(user_input, threshold=0.5)
        if similar_pattern:
            responses = self.kb.get_response_by_pattern(similar_pattern)
            # Reranking também nas respostas do padrão semelhante
            response = self.reranker.rank_best_response(user_input, responses) if responses else None
            response = response or (random.choice(responses) if responses else None)
            if response:
                self.save_context(user_input, response)
                return response

        # Fallback para LLM (apenas placeholder)
        try:
            response = self.llm.call_llm(user_input, self.context)
        except Exception as e:
            logging.error(f"Erro na chamada da LLM: {e}")
            response = "Desculpe, não consegui processar sua solicitação."

        self.save_context(user_input, response)
        return response

    def execute_plugin(self, command, params=None):
        return self.plugins.execute_command(command, params)

if __name__ == "__main__":
    agent = AgentCore()
    print("Jarvis iniciado. Digite 'sair' para encerrar.")
    while True:
        user_input = input("Você: ").strip()
        if user_input.lower() in ("sair", "exit", "quit"):
            print("Jarvis: Até logo!")
            break
        response = agent.get_response(user_input)
        print("Jarvis:", response)
