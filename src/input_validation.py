# src/input_validation.py

import re

SAFE_CHARS_PATTERN = re.compile(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚãõÃÕçÇ.,!?\s]')

def sanitize_input(text: str) -> str:
    """
    Sanitiza uma string de entrada para remover caracteres potencialmente maliciosos
    e injecções de código.

    Args:
        text (str): A string de entrada a ser sanitizada.

    Returns:
        str: A string sanitizada em minúsculas. Retorna uma string vazia se
             a entrada não for uma string.
    """
    # Verifica se a entrada é uma string e, se não for, retorna uma string vazia
    if not isinstance(text, str):
        return ""
    
    # Remove espaços em branco extras no início e no fim
    sanitized_text = text.strip()
    
    # Substitui caracteres que não correspondem ao padrão por uma string vazia
    sanitized_text = SAFE_CHARS_PATTERN.sub('', sanitized_text)
    
    # Retorna o texto sanitizado em minúsculas
    return sanitized_text.lower()