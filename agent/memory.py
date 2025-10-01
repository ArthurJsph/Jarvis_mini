import redis
import json
import logging
from typing import List, Dict, Optional
from config.config import REDIS_URL

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class MemoryManager:
    def __init__(self, session_key: str = "jarvis_memory", redis_url: Optional[str] = None):
        """
        Inicializa a conexão com Redis e define a chave de sessão para armazenar histórico.
        
        Args:
            session_key (str): chave para armazenar o histórico no Redis.
            redis_url (str|None): URL para conexão com Redis, se None usa REDIS_URL do config.
        """
        redis_url = redis_url or REDIS_URL
        try:
            self.client = redis.from_url(redis_url)
            self.session_key = session_key
            logger.info(f"Conectado ao Redis em {redis_url}, usando chave '{session_key}'.")
        except Exception as e:
            logger.error(f"Falha ao conectar ao Redis: {e}")
            self.client = None

    def load_history(self) -> List[Dict]:
        """
        Carrega o histórico de interações armazenadas no Redis.

        Returns:
            Lista de dicionários com as interações. Lista vazia se não há histórico ou erro.
        """
        if not self.client:
            logger.warning("Cliente Redis não está inicializado.")
            return []
        try:
            history_json = self.client.get(self.session_key)
            if history_json:
                return json.loads(history_json)
        except Exception as e:
            logger.error(f"Erro ao carregar histórico do Redis: {e}")
        return []

    def save_interaction(self, user_input: str, agent_response: str, limit: int = 50) -> None:
        """
        Salva uma nova interação adicionando ao histórico, respeitando limite máximo.

        Args:
            user_input (str): Mensagem do usuário.
            agent_response (str): Resposta do agente.
            limit (int): Máximo de interações a manter no histórico.
        """
        if not self.client:
            logger.warning("Cliente Redis não está inicializado. Interação não salva.")
            return

        history = self.load_history()
        history.append({"user": user_input, "agent": agent_response})
        if len(history) > limit:
            history = history[-limit:]

        try:
            self.client.set(self.session_key, json.dumps(history))
            logger.debug(f"Interação salva. Histórico atual com {len(history)} interações.")
        except Exception as e:
            logger.error(f"Erro ao salvar histórico no Redis: {e}")

    def clear_history(self) -> bool:
        """
        Limpa todo o histórico armazenado.

        Returns:
            bool: True se a limpeza foi bem sucedida, False caso contrário.
        """
        if not self.client:
            logger.warning("Cliente Redis não está inicializado. Não foi possível limpar histórico.")
            return False

        try:
            deleted = self.client.delete(self.session_key)
            logger.info(f"Histórico apagado com sucesso, entradas removidas: {deleted}.")
            return True
        except Exception as e:
            logger.error(f"Erro ao apagar histórico do Redis: {e}")
            return False

    def get_memory_size(self) -> int:
        """
        Retorna o número atual de interações salvas na memória.

        Returns:
            int: quantidade de interações. Zero se não houver memória ou erro.
        """
        history = self.load_history()
        return len(history)

if __name__ == "__main__":
    mm = MemoryManager()
    print(f"Memória atual tem {mm.get_memory_size()} interações.")
    mm.save_interaction("Teste do usuário", "Resposta do Jarvis")
    print(f"Memória atualizada tem {mm.get_memory_size()} interações.")
