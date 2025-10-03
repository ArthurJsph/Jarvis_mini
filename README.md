# 🤖 Jarvis Mini - Assistente de IA Inteligente

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange.svg)

Um assistente de IA conversacional construído com tecnologias modernas de Machine Learning e processamento de linguagem natural. O Jarvis Mini é capaz de entender intenções do usuário e responder de forma contextual e inteligente.

## 🚀 Características Principais

- **🧠 NLP Avançado**: Utiliza modelos de machine learning para classificação de intenções
- **💾 Memória Persistente**: Sistema de memória com Redis para lembrar do contexto da conversa
- **🔌 Arquitetura Modular**: Sistema de plugins extensível para novas funcionalidades
- **📊 Base de Conhecimento**: Sistema inteligente de recuperação de informações
- **🌐 API REST**: Interface via FastAPI para integração com outras aplicações
- **🐳 Docker Ready**: Containerização completa para deploy fácil

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **FastAPI**: Framework web para APIs
- **Scikit-learn**: Machine Learning para classificação de intenções
- **Sentence Transformers**: Embeddings semânticos para reranking
- **Redis**: Banco de dados em memória para sessões
- **Docker**: Containerização da aplicação
- **PyTorch & Transformers**: Modelos de linguagem pré-treinados

## 📁 Estrutura do Projeto

```
jarvis_mini/
├── agent/                  # Núcleo do agente IA
│   ├── core.py            # Lógica principal do agente
│   ├── nlp.py             # Processamento de linguagem natural
│   ├── memory.py          # Sistema de memória
│   ├── knowledge_base.py  # Base de conhecimento
│   ├── llm_api.py         # Interface com LLMs externos
│   └── plugins.py         # Sistema de plugins
├── data/                  # Dados de treinamento
│   ├── knowledge_data.json
│   └── augmented_knowledge.json
├── models/                # Modelos treinados
│   ├── model.pkl
│   └── vectorizer.pkl
├── src/                   # Scripts utilitários
│   ├── train.py          # Treinamento do modelo
│   └── augment_data.py   # Aumento de dados
├── config/               # Configurações
├── logs/                 # Arquivos de log
└── docker-compose.yml   # Configuração Docker
```

## 🔧 Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- Docker e Docker Compose (opcional)
- Redis Server (ou usar Docker)

### 1. Clone o Repositório

```bash
git clone https://github.com/ArthurJsph/Jarvis_mini.git
cd jarvis_mini
```

### 2. Crie um Ambiente Virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite as configurações necessárias
```

**Exemplo de configuração (.env):**
```env
REDIS_URL=redis://localhost:6379
REDIS_DB=0
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### 5. Inicie os Serviços com Docker (Recomendado)

```bash
docker-compose up -d
```

### 6. Treine o Modelo (Primeira Execução)

```bash
# Gere dados aumentados
python src/augment_data.py

# Treine o modelo de classificação
python src/train.py
```

## 🎯 Como Usar

### Modo Interativo (Terminal)

```bash
python main.py
```

### Modo API (Servidor Web)

```bash
# Inicie o servidor FastAPI
uvicorn agent.routes:app --reload --port 8000

# Acesse a documentação em: http://localhost:8000/docs
```

### Exemplo de Conversa

```
Você: oi jarvis
Jarvis: Olá! Como posso te ajudar hoje?

Você: que horas são?
Jarvis: Agora são 14:30.

Você: obrigado
Jarvis: De nada! Sempre à disposição!
```

## 🧮 Funcionalidades Disponíveis

- ✅ **Saudações**: Cumprimentos e despedidas
- ✅ **Consulta de Hora**: Horário atual
- ✅ **Agradecimentos**: Reconhecimento de gratidão
- ✅ **Pedidos de Ajuda**: Assistência geral
- ✅ **Sistema de Comandos**: Executar comandos do sistema
- 🔄 **Mais funcionalidades em desenvolvimento...**

## 🔬 Treinamento e Customização

### Adicionando Novas Intenções

1. **Edite os dados**: Adicione novos padrões em `data/knowledge_data.json`
2. **Regenere dados**: Execute `python src/augment_data.py`
3. **Retreine**: Execute `python src/train.py`
4. **Implemente ação**: Adicione a função correspondente em `agent/plugins.py`

### Exemplo de Nova Intenção

```json
{
  "contar_piada": {
    "padroes": ["conte uma piada", "me faça rir", "diga algo engraçado"],
    "respostas": ["Por que o livro de matemática se suicidou? Porque tinha muitos problemas!"]
  }
}
```

## 📊 Métricas de Performance

O modelo atual alcança:
- **Acurácia**: ~99.9%
- **Precision**: 1.00 (média)
- **Recall**: 0.99 (média)
- **F1-Score**: 0.99 (média)

*Treinado com ~22.000 exemplos de 10 intenções diferentes*

## 🐳 Deploy com Docker

### Desenvolvimento

```bash
docker-compose up -d
```

### Produção

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 🧪 Testes

```bash
# Execute os testes unitários
pytest tests/

# Teste o modelo NLP
python src/train.py --test-only

# Teste a API
python -m pytest tests/test_api.py
```

## 📈 Roadmap

- [ ] 🎯 Integração com LLMs externos (OpenAI, Anthropic)
- [ ] 🗣️ Suporte a áudio (Speech-to-Text / Text-to-Speech)
- [ ] 🌐 Interface web moderna
- [ ] 📱 App mobile
- [ ] 🔐 Sistema de autenticação
- [ ] 📊 Dashboard de analytics
- [ ] 🔌 Mais plugins (clima, notícias, calculadora)

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Arthur Joseph** - [@ArthurJsph](https://github.com/ArthurJsph)

## 🙏 Agradecimentos

- Comunidade Python e Machine Learning
- Desenvolvedores do Scikit-learn e Transformers
- Todos que contribuem com feedback e sugestões

---

⭐ **Se este projeto te ajudou, considere dar uma estrela!** ⭐

## 📞 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique a [documentação](docs/)
2. Procure nas [Issues existentes](https://github.com/ArthurJsph/Jarvis_mini/issues)
3. Abra uma [nova Issue](https://github.com/ArthurJsph/Jarvis_mini/issues/new)

**Status do Projeto**: 🟢 Ativo - Em desenvolvimento contínuo