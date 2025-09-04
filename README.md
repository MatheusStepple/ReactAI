# ReactAI - Análise de Emoções em Tempo Real

[![Deploy Status](https://img.shields.io/badge/Live%20Demo-Online-brightgreen)](https://matheusstepple.github.io/ReactAI)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Online-brightgreen)](https://matheusstepple.github.io/ReactAI)

> Sistema de visão computacional que analisa expressões faciais em tempo real para medir aprovação e interesse do público.

## 🚀 Demo Online

**[Acesse o site funcionando](https://matheusstepple.github.io/ReactAI)**

## 🎯 O que faz

- 🎥 **Captura em tempo real** via webcam
- 🧠 **IA para análise** de expressões faciais
- 📊 **Métricas instantâneas** de aprovação e interesse
- 💾 **Armazenamento** de dados e relatórios
- 📈 **Dashboard** com visualizações

## 🛠️ Tecnologias

**Frontend:** React, Tailwind CSS, TensorFlow.js, Teachable Machine  
**Backend:** FastAPI, PostgreSQL, scikit-learn, pandas  
**Deploy:** Docker, GitHub Actions, GitHub Pages

## 📖 Como usar

1. **Acesse** o site
2. **Permita** acesso à webcam
3. **Configure** nome do produto e duração
4. **Inicie** a análise
5. **Veja** os resultados em tempo real

## ⚡ Início Rápido

```bash
# Clone o projeto
git clone https://github.com/MatheusStepple/ReactAI.git
cd ReactAI

# Instale dependências
make install

# Inicie o desenvolvimento
make dev
```

## 🏗️ Estrutura

```
ReactAI/
├── apps/
│   ├── backend/     # API FastAPI
│   └── frontend/    # Interface React
├── infrastructure/  # Docker e deploy
└── docs/           # Documentação
```

## 📊 API

- **Docs:** http://localhost:8000/docs
- **Health:** http://localhost:8000/health
- **Endpoints:** `/api/v1/`

## 🧪 Desenvolvimento

```bash
# Comandos úteis
make dev          # Iniciar desenvolvimento
make test         # Executar testes
make docker-up    # Subir com Docker
make clean        # Limpar arquivos
```

## 👨‍💻 Autor

**Matheus Stepple**  
Desenvolvido no curso de IA da UFPE com supervisão do professor Cléber Zanchettin.

---

⭐ **Se foi útil, dê uma estrela!**
