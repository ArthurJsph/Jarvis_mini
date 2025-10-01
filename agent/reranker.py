import logging
from sentence_transformers import SentenceTransformer, util
import torch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Reranker:
    def __init__(self, model_name: str = 'paraphrase-MiniLM-L6-v2'):
        """
        Inicializa o modelo de reranking baseado em embeddings.

        Args:
            model_name (str): nome do modelo Sentence Transformers para embeddings.
        """
        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"Modelo '{model_name}' carregado com sucesso para reranking.")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo para reranking: {e}")
            self.model = None

    def rank_best_response(self, question: str, responses: list) -> str:
        """
        Dado uma pergunta e uma lista de respostas candidatas, retorna a resposta
        mais semanticamente similar usando embeddings e similaridade do cosseno.

        Args:
            question (str): texto da pergunta do usuário.
            responses (list[str]): lista de respostas candidatas.

        Returns:
            str: resposta mais relevante segundo o modelo; None se inválido.
        """
        if not self.model:
            logger.warning("Modelo de reranking não inicializado. Retornando resposta aleatória.")
            return responses[0] if responses else None

        if not responses:
            logger.warning("Lista de respostas vazia para reranking.")
            return None

        try:
            question_emb = self.model.encode(question, convert_to_tensor=True)
            responses_emb = self.model.encode(responses, convert_to_tensor=True)
            scores = util.pytorch_cos_sim(question_emb, responses_emb)[0]
            best_idx = torch.argmax(scores).item()
            best_score = scores[best_idx].item()
            logger.info(f"Melhor score reranking: {best_score:.4f} para resposta índice {best_idx}")
            return responses[best_idx]
        except Exception as e:
            logger.error(f"Erro durante reranking: {e}")
            return responses[0]  # fallback simples

if __name__ == "__main__":
    reranker = Reranker()

    pergunta_teste = "Qual a previsão do tempo para hoje?"
    respostas_teste = [
        "Está previsto sol com poucas nuvens.",
        "Vai chover bastante esta noite.",
        "Não tenho essa informação agora."
    ]

    melhor_resposta = reranker.rank_best_response(pergunta_teste, respostas_teste)
    print(f"Pergunta: {pergunta_teste}")
    print(f"Melhor resposta escolhida: {melhor_resposta}")
