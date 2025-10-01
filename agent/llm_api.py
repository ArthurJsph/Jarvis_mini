import logging

class LLMAPI:
    def __init__(self):
        logging.info("LLMAPI inicializada (modo placeholder). Sem conexão com LLM externa.")

    def call_llm(self, prompt, context=None):
        """
        Simula uma chamada para a LLM externa.
        
        Args:
            prompt (str): Texto a ser enviado para a LLM.
            context (list|None): Histórico ou contexto da conversa (opcional).
        
        Returns:
            str: Mensagem padrão informando que a LLM não está configurada.
        """
        logging.info("call_llm chamado, mas LLM não está configurada.")
        return "LLM não configurada ainda. Por favor, aguarde."

    def test_connection(self):
        """
        Simula teste de conexão com a LLM.

        Returns:
            bool: True sempre, já que não existe conexão real.
        """
        logging.info("Teste de conexão com LLM (placeholder) executado com sucesso.")
        return True

    def get_status(self):
        """
        Retorna status atual do serviço LLM.

        Returns:
            dict: Estado do serviço, indicando que está em modo placeholder.
        """
        return {
            "status": "placeholder",
            "description": "LLMAPI não conectada a nenhum serviço externo."
        }
