import json
import random
import os
import re

def gerar_variacoes(frases_base, prefixos=None, sufixos=None, intermediarios=None):
    prefixos = prefixos or [""]
    sufixos = sufixos or [""]
    intermediarios = intermediarios or [""]
    variacoes = set()
    for frase in frases_base:
        for pre in prefixos:
            for intm in intermediarios:
                for suf in sufixos:
                    componentes = [pre, intm, frase, suf]
                    # Remove vazios e junta com espaço
                    frase_composta = ' '.join([c for c in componentes if c]).strip()
                    frase_composta = re.sub(r'\s+', ' ', frase_composta)
                    variacoes.add(frase_composta)
    return list(variacoes)

def gerar_intencoes():
    intencoes_base = {
        "saudacao": {
            "frases_base": ["olá", "oi", "bom dia", "boa tarde", "boa noite", "e aí", "como vai", "tudo bem"],
            "respostas": [
                "Olá! Como posso ajudar hoje?",
                "Oi, tudo bem? Em que posso ser útil?",
                "Saudações! Qual sua dúvida?",
                "Oi! Estou aqui para ajudar."
            ],
            "prefixos": ["", "então", "ei", "hey", "salve", "fala aí", "alô"],
            "intermediarios": ["", "como vai", "tudo bem", "beleza", "meu amigo"],
            "sufixos": ["", "meu amigo", "pessoal", "querido", "galera"]
        },
        "despedida": {
            "frases_base": ["tchau", "adeus", "até mais", "até logo", "fico por aqui", "falou", "até a próxima"],
            "respostas": [
                "Até logo! Volte sempre.",
                "Tchau! Foi um prazer ajudar.",
                "Cuide-se! Espero te ver novamente.",
                "Até mais, tenha um ótimo dia!"
            ],
            "prefixos": ["", "bem", "então", "por enquanto", "bom", "com carinho"],
            "intermediarios": ["", "me cuida", "fica bem", "se cuida"],
            "sufixos": ["", "amigo", "meu chapa", "querido"]
        },
        # Inclua outras intenções similares, com mais prefixos, intermediarios e sufixos
        # ...
    }

    intencoes_geradas = {}
    for intent_name, intent_data in intencoes_base.items():
        padroes = gerar_variacoes(
            intent_data["frases_base"], 
            intent_data.get("prefixos"), 
            intent_data.get("sufixos"),
            intent_data.get("intermediarios")
        )
        respostas = intent_data["respostas"]

        respostas_expandidas = respostas.copy()
        for resp in respostas:
            for suffix in ["", "!", "!!", ".", "...", " rs", " hehehe"]:
                resposta_variada = resp.strip() + suffix
                if resposta_variada not in respostas_expandidas:
                    respostas_expandidas.append(resposta_variada)

        intencoes_geradas[intent_name] = {
            "padroes": padroes,
            "respostas": respostas_expandidas
        }

    entidades = {
        "localizacao": [f"cidade {i}" for i in range(1, 501)],
        "pessoa": [f"usuario{i}" for i in range(1, 201)],
        "tempo": ["hoje", "amanhã", "agora", "semana que vem", "final de semana", "ontem", "sempre", "às vezes", "raramente"],
        "comando": ["abrir", "fechar", "executar", "iniciar", "parar", "cancelar", "reiniciar"],
        "sentimento": ["feliz", "triste", "animado", "cansado", "estressado", "calmo"],
        "numero": [str(i) for i in range(0, 101)],
        "tempo_relativo": ["agora", "depois", "cedo", "tarde", "em breve", "hoje à noite", "amanhã de manhã"]
    }
    return {"content": {"intencoes": intencoes_geradas, "entidades": entidades}}

def get_next_versioned_filename(folder_path, base_name="knowledge_data_large", ext=".json"):
    if not os.path.exists(folder_path):
        return os.path.join(folder_path, f"{base_name}1{ext}")
    files = os.listdir(folder_path)
    pattern = re.compile(rf"{re.escape(base_name)}(\d+){re.escape(ext)}")
    indices = [int(m.group(1)) for f in files if (m := pattern.match(f))]
    next_index = max(indices) + 1 if indices else 1
    return os.path.join(folder_path, f"{base_name}{next_index}{ext}")

def salvar_json_incremental(data, folder="data"):
    os.makedirs(folder, exist_ok=True)
    caminho = get_next_versioned_filename(folder)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Arquivo salvo em: {caminho}")

def main():
    data = gerar_intencoes()
    salvar_json_incremental(data, folder="data")

if __name__ == "__main__":
    main()
