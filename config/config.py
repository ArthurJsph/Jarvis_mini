import dotenv
import os
import sys
from typing import Optional

dotenv.load_dotenv()

def get_env_var(name: str, default: Optional[str] = None, required: bool = False, var_type: type = str):
    """
    Obtém variável de ambiente convertendo para tipo desejado e validando presença obrigatória.
    
    Args:
        name (str): Nome da variável de ambiente.
        default (str|None): Valor padrão caso variável não exista.
        required (bool): Se True, aborta se variável não definida ou vazia.
        var_type (type): Tipo a converter (str, int, bool, etc).
        
    Returns:
        Valor convertido da variável de ambiente.
    """
    value = os.getenv(name, default)
    if required and (value is None or str(value).strip() == ""):
        print(f"Erro crítico: Variável de ambiente obrigatória '{name}' não definida ou vazia.")
        sys.exit(1)

    # Conversões de tipo comuns
    try:
        if var_type == bool:
            if isinstance(value, str):
                return value.strip().lower() in ("true", "1", "yes", "on")
            return bool(value)
        if var_type == int:
            return int(value)
        if var_type == float:
            return float(value)
        return value
    except Exception as e:
        print(f"Erro ao converter variável '{name}' para {var_type}: {e}")
        sys.exit(1)


# Exemplo de uso com variáveis principais

API_KEY: str = get_env_var("API_KEY", required=True)

REDIS_URL: str = get_env_var("REDIS_URL", required=True)
REDIS_HOST: str = get_env_var("REDIS_HOST", required=True)
REDIS_PORT: int = get_env_var("REDIS_PORT", required=True, var_type=int)
REDIS_USERNAME: str = get_env_var("REDIS_USERNAME", default="")
REDIS_PASSWORD: str = get_env_var("REDIS_PASSWORD", default="")
REDIS_APPENDONLY: str = get_env_var("REDIS_APPENDONLY", default="no")

KNOWLEDGE_BASE_PATH: str = get_env_var("KNOWLEDGE_BASE_PATH", default="data/knowledge_data.json")

LOG_LEVEL: str = get_env_var("LOG_LEVEL", default="INFO")
LOG_FILE_PATH: str = get_env_var("LOG_FILE_PATH", default="logs/jarvis.log")
LOG_FORMAT: str = get_env_var("LOG_FORMAT", default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_DATE_FORMAT: str = get_env_var("LOG_DATE_FORMAT", default="%Y-%m-%d %H:%M:%S")

DEFAULT_LANGUAGE: str = get_env_var("DEFAULT_LANGUAGE", default="pt")

ENABLE_CACHING: bool = get_env_var("ENABLE_CACHING", default="false", var_type=bool)

CACHE_EXPIRATION: int = get_env_var("CACHE_EXPIRATION", default="3600", var_type=int)
