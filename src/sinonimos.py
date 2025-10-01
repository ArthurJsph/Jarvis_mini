# src/sinonimos.py

from nltk.corpus import wordnet
import nltk
import logging

# Configuração básica de logging para feedback ao usuário
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Baixe o WordNet se ainda não tiver feito.
# Isso precisa ser feito apenas uma vez.
try:
    wordnet.ensure_loaded()
except LookupError:
    logging.info("Recursos do WordNet não encontrados. Baixando...")
    nltk.download('wordnet', quiet=True)
    logging.info("Download do WordNet concluído.")

def synonyms(word, lang='por'):
    """
    Retorna uma lista de sinônimos para a palavra dada.

    Args:
        word (str): A palavra para a qual buscar sinônimos.
        lang (str): O idioma (por padrão, 'por' para português).
    
    Returns:
        list: Uma lista de sinônimos únicos em minúsculas.
    """
    syns = set()
    for synset in wordnet.synsets(word.lower(), lang=lang):
        for lema in synset.lemmas(lang=lang):
            # Adiciona o sinônimo, substituindo underscores por espaços
            syns.add(lema.name().replace('_', ' '))
    return list(syns)

# Exemplo de uso
if __name__ == '__main__':
    palavra = "casa"
    lista_sinonimos = synonyms(palavra)
    print(f"Sinônimos para '{palavra}': {lista_sinonimos}")

    palavra2 = "triste"
    lista_sinonimos2 = synonyms(palavra2)
    print(f"Sinônimos para '{palavra2}': {lista_sinonimos2}")