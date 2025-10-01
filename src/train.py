import json
import pickle
import os
import glob
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_training_data_from_json(file_path):
    """
    Carrega e processa os dados de treinamento de um único arquivo JSON.
    """
    texts, labels = [], []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        intents = data.get("content", {}).get("intencoes", {})
        for intent, details in intents.items():
            patterns = details.get("padroes", [])
            if not patterns:
                logging.warning(f"Intenção '{intent}' no arquivo '{os.path.basename(file_path)}' não tem padrões.")
                continue
            for pattern in patterns:
                texts.append(pattern.lower())
                labels.append(intent)
        
        return texts, labels

    except json.JSONDecodeError:
        logging.error(f"O arquivo '{file_path}' não é um JSON válido.")
        return [], []
    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado ao ler '{file_path}': {e}")
        return [], []

def train_and_save_model():
    """
    Orquestra o processo de carregamento de dados de um arquivo aumentado, 
    treinamento e salvamento do modelo.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    models_dir = os.path.join(script_dir, '..', 'models')

    # --- PONTO DE ALTERAÇÃO ---
    # O script agora procura pelo arquivo gerado pelo augment_data.py
    augmented_json_file = os.path.join(data_dir, 'augmented_knowledge.json')
    
    if not os.path.exists(augmented_json_file):
        logging.error(f"Arquivo de dados aumentado '{augmented_json_file}' não encontrado.")
        logging.error("--> Execute 'python src/augment_data.py' primeiro para gerar os dados de treino.")
        return

    logging.info(f"Carregando dados do arquivo aumentado: '{os.path.basename(augmented_json_file)}'...")
    all_texts, all_labels = load_training_data_from_json(augmented_json_file)
    # --- FIM DA ALTERAÇÃO ---

    if not all_texts or not all_labels:
        logging.error("Nenhum dado de treinamento foi carregado. Verifique o arquivo JSON aumentado.")
        return

    unique_labels = sorted(list(set(all_labels)))
    logging.info(f"Total de dados carregados: {len(all_texts)} exemplos de {len(unique_labels)} intenções.")
    
    # Vetorização e treinamento
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
    X = vectorizer.fit_transform(all_texts)

    X_train, X_test, y_train, y_test = train_test_split(
        X, all_labels, test_size=0.25, random_state=42, stratify=all_labels
    )
    
    logging.info("Iniciando treinamento do modelo SVC...")
    clf = SVC(kernel="linear", probability=True, random_state=42, class_weight='balanced')
    clf.fit(X_train, y_train)
    logging.info("Treinamento concluído.")

    # Avaliação detalhada do modelo
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logging.info(f"Acurácia do modelo no conjunto de teste: {accuracy:.3f}")
    
    print("\n" + "="*50)
    print("Relatório de Classificação:")
    print(classification_report(y_test, y_pred, target_names=unique_labels, zero_division=0))
    
    print("\n" + "="*50)
    logging.info("Matriz de confusão:")
    print(confusion_matrix(y_test, y_pred, labels=unique_labels))
    print("="*50 + "\n")

    # Cria o diretório de modelos se não existir
    os.makedirs(models_dir, exist_ok=True)

    # Salva os modelos
    vectorizer_path = os.path.join(models_dir, "vectorizer.pkl")
    model_path = os.path.join(models_dir, "model.pkl")

    with open(vectorizer_path, "wb") as f:
        pickle.dump(vectorizer, f)
    
    with open(model_path, "wb") as f:
        pickle.dump(clf, f)

    logging.info("Modelos treinados e salvos com sucesso.")

if __name__ == "__main__":
    train_and_save_model()