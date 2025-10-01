# src/augment_data.py

import json
import os
import random
import glob
from sinonimos import synonyms

# Palavras de parada comuns em português
STOP_WORDS = set([
    'a', 'o', 'as', 'os', 'um', 'uma', 'de', 'da', 'do', 'das', 'dos', 'em', 'no', 'na', 
    'nos', 'nas', 'por', 'para', 'com', 'sem', 'sob', 'sobre', 'se', 'ser', 'sendo',
    'ter', 'tem', 'tendo', 'que', 'qual', 'quem', 'como', 'onde', 'quando', 'porque',
    'eu', 'você', 'ele', 'ela', 'nós', 'vocês', 'eles', 'elas', 'me', 'te', 'lhe'
])

def synonym_replacement(sentence, n=1):
    """Substitui 'n' palavras na frase por seus sinônimos."""
    words = sentence.split()
    new_words = words.copy()
    
    # Encontra palavras que não são de parada e que têm sinônimos
    replaceable_words_indices = [i for i, word in enumerate(words) if word.lower() not in STOP_WORDS and synonyms(word)]
    
    if not replaceable_words_indices:
        return None

    # Escolhe 'n' palavras aleatórias para substituir
    words_to_replace_indices = random.sample(replaceable_words_indices, min(n, len(replaceable_words_indices)))
    
    for index in words_to_replace_indices:
        word_to_replace = words[index]
        syns = synonyms(word_to_replace)
        if syns:
            synonym = random.choice(syns)
            new_words[index] = synonym
            
    return ' '.join(new_words)

def augment_data(input_dir, output_file, augment_factor=2):
    """
    Lê todos os JSONs de um diretório, aumenta os dados e salva em um único arquivo.
    
    Args:
        input_dir (str): Diretório contendo os arquivos JSON originais.
        output_file (str): Arquivo JSON de saída com os dados aumentados.
        augment_factor (int): Quantas novas frases gerar para cada frase original.
    """
    json_files = glob.glob(os.path.join(input_dir, '*.json'))
    if not json_files:
        print(f"Nenhum arquivo JSON encontrado em '{input_dir}'")
        return

    augmented_data = {"content": {"intencoes": {}}}

    for file_path in json_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        intents = data.get("content", {}).get("intencoes", {})
        for intent, details in intents.items():
            patterns = details.get("padroes", [])
            
            # Garante que a intenção exista no novo JSON
            if intent not in augmented_data["content"]["intencoes"]:
                augmented_data["content"]["intencoes"][intent] = {"padroes": []}
            
            new_patterns = set(patterns) # Usa um set para evitar duplicatas

            # Adiciona os padrões originais
            for pattern in patterns:
                new_patterns.add(pattern)
                
                # Gera novas frases a partir do padrão original
                for _ in range(augment_factor):
                    new_sentence = synonym_replacement(pattern, n=1) # Troca 1 palavra
                    if new_sentence and new_sentence != pattern:
                        new_patterns.add(new_sentence)

            augmented_data["content"]["intencoes"][intent]["padroes"].extend(list(new_patterns))

    # Salva o arquivo JSON aumentado
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(augmented_data, f, ensure_ascii=False, indent=2)
        
    print(f"Dados aumentados e salvos em '{output_file}'")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    
    # Define o arquivo de saída para os dados aumentados
    augmented_file_path = os.path.join(data_dir, 'augmented_knowledge.json')
    
    # Executa o aumento de dados
    augment_data(input_dir=data_dir, output_file=augmented_file_path, augment_factor=3)