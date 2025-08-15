# ReactAI - Sistema de Visão Computacional para Análise de Reação do Público em Tempo Real

---

## 🚀 Descrição

O **ReactAI** é um sistema inovador de visão computacional que mede, em tempo real, o nível de interesse e aprovação do público em relação a um produto, a partir da análise de expressões faciais. Desenvolvido durante o curso de extensão **Inteligência Artificial para Automação Industrial**, ministrado pelo professor Cleber Zanchettin no Centro de Informática da UFPE, o projeto teve como objetivo aplicar IA de forma prática em cenários reais de automação industrial.

Usando o **Teachable Machine**, do Google, foi criado um modelo personalizado de reconhecimento de imagens treinado com expressões faciais para classificar reações como:  
- 😄 **Satisfação**  
- 😒 **Desaprovação** 
- 🌫️ **Fundo/Sem rosto**

Este sistema simula a coleta e análise automática do feedback visual do público, semelhante ao comportamento de consumidores avaliando produtos em lojas ou eventos.

---

## ✨ Novas Funcionalidades

### 🔧 Backend Avançado
- **FastAPI**: API REST moderna e rápida
- **PostgreSQL**: Banco de dados robusto para armazenamento de dados
- **SQLAlchemy**: ORM para gerenciamento de banco de dados
- **Pydantic**: Validação de dados e serialização

### 🤖 Machine Learning Aprimorado
- **scikit-learn**: Modelos de ML mais sofisticados
- **pandas & NumPy**: Manipulação e análise de dados
- **matplotlib**: Visualizações avançadas
- **Modelo híbrido**: Combina Teachable Machine com scikit-learn

### 📊 Dashboard Interativo
- **React**: Interface moderna e responsiva
- **Tailwind CSS**: Design system consistente
- **Recharts**: Gráficos interativos
- **Real-time updates**: Atualizações em tempo real

### 📈 Analytics Avançados
- **Relatórios detalhados**: Métricas de aprovação e interesse
- **Séries temporais**: Análise de tendências
- **Exportação de dados**: CSV, JSON e visualizações
- **Visualizações**: Gráficos e dashboards interativos

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**: Linguagem principal
- **FastAPI**: Framework web moderno
- **PostgreSQL**: Banco de dados relacional
- **SQLAlchemy**: ORM para Python
- **Pydantic**: Validação de dados
- **scikit-learn**: Machine Learning
- **pandas & NumPy**: Análise de dados
- **matplotlib**: Visualizações

### Frontend
- **React 18**: Biblioteca JavaScript
- **Tailwind CSS**: Framework CSS
- **Recharts**: Biblioteca de gráficos
- **React Webcam**: Captura de vídeo
- **TensorFlow.js**: ML no navegador
- **Teachable Machine**: Modelo de IA

### DevOps
- **Docker**: Containerização
- **Git**: Controle de versão
- **GitHub Actions**: CI/CD

---

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Node.js 16 ou superior
- PostgreSQL 12 ou superior
- Git

---

## 🚀 Instalação e Configuração

### 🌐 Demo Online
**Acesse a aplicação funcionando:** https://matheusstepple.github.io/ReactAI/

> **Nota:** O demo online mostra apenas o frontend. Para funcionalidade completa com backend, execute localmente.

### 1. Clone o repositório
```bash
git clone https://github.com/matheusstepple/ReactAI.git
cd ReactAI
```

### 2. Configurar Backend

#### Instalar dependências Python
```bash
cd backend
pip install -r requirements.txt
```

#### Configurar banco de dados PostgreSQL
```bash
# Criar banco de dados
createdb reactai_db

# Configurar variáveis de ambiente
cp env.example .env
# Editar .env com suas configurações
```

#### Executar migrações
```bash
# Criar tabelas
python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(engine)"
```

#### Iniciar servidor backend
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Configurar Frontend

#### Instalar dependências Node.js
```bash
cd frontend
npm install
```

#### Iniciar servidor de desenvolvimento
```bash
npm start
```

### 4. Acessar a aplicação
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentação API: http://localhost:8000/docs

---

## 📖 Como Usar

### 1. Configuração Inicial
1. Acesse http://localhost:3000
2. Configure o nome do produto e duração da análise
3. Permita acesso à webcam

### 2. Análise em Tempo Real
1. Clique em "Iniciar Análise"
2. O sistema capturará e analisará expressões faciais
3. Visualize os resultados em tempo real

### 3. Visualização de Dados
1. Acesse o Dashboard para ver métricas gerais
2. Consulte relatórios detalhados
3. Exporte dados em diferentes formatos

---

## 📊 Funcionalidades Principais

### 🎯 Análise em Tempo Real
- Captura de vídeo via webcam
- Processamento de frames em tempo real
- Classificação de emoções instantânea
- Feedback visual imediato

### 📈 Dashboard Analytics
- Métricas de aprovação e interesse
- Gráficos interativos
- Séries temporais
- Comparação entre produtos

### 💾 Armazenamento de Dados
- Sessões de análise
- Dados de emoções
- Resultados consolidados
- Histórico completo

### 📤 Exportação
- CSV para análise externa
- JSON para integração
- Visualizações em PNG
- Relatórios detalhados

---

## 🔧 Configuração Avançada

### Variáveis de Ambiente

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/reactai_db
SECRET_KEY=your-secret-key
DEBUG=True
```

#### Frontend
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_MODEL_URL=https://teachablemachine.withgoogle.com/models/YwDSlSEVp/
```

### Personalização do Modelo

1. Acesse [Teachable Machine](https://teachablemachine.withgoogle.com/)
2. Treine seu próprio modelo com suas expressões
3. Atualize a URL do modelo no frontend
4. Retreine o modelo scikit-learn se necessário

---

## 📚 API Documentation

### Endpoints Principais

#### Sessões
- `POST /sessions/` - Criar nova sessão
- `GET /sessions/` - Listar sessões
- `GET /sessions/{id}` - Obter sessão específica

#### Emoções
- `POST /emotions/` - Registrar emoção
- `GET /sessions/{id}/emotions/` - Dados de emoção da sessão

#### Análise
- `POST /analysis/` - Salvar resultado de análise
- `GET /sessions/{id}/analysis/` - Resultado da análise

#### Relatórios
- `GET /analytics/summary/` - Resumo analítico
- `GET /analytics/timeseries/` - Dados de série temporal

#### Exportação
- `GET /sessions/{id}/export/csv/` - Exportar CSV
- `GET /sessions/{id}/export/json/` - Exportar JSON

---

## 🧪 Testes

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm test
```

---

## 🚀 Deploy

### Docker
```bash
# Build das imagens
docker-compose build

# Executar
docker-compose up -d
```

### Produção
1. Configure variáveis de ambiente para produção
2. Use um servidor WSGI (Gunicorn)
3. Configure um proxy reverso (Nginx)
4. Configure SSL/TLS

---

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Matheus Stepple**
- LinkedIn: [matheus-stepple](https://www.linkedin.com/in/matheus-stepple/)
- GitHub: [matheusstepple](https://github.com/matheusstepple)

---

## 🙏 Agradecimentos

- **Prof. Cleber Zanchettin** - UFPE Centro de Informática
- **Google Teachable Machine** - Plataforma de ML
- **Comunidade open source** - Bibliotecas e ferramentas

---

## 📞 Suporte

Para dúvidas, sugestões ou problemas:
- Abra uma [issue](https://github.com/matheusstepple/ReactAI/issues)
- Entre em contato via [LinkedIn](https://www.linkedin.com/in/matheus-stepple/)

---

## 🔗 Links Úteis

- [Demo Online](https://matheusstepple.github.io/ReactAI/)
- [Vídeo Demonstrativo](https://lnkd.in/dAQqBye5)
- [Documentação da API](http://localhost:8000/docs)
- [Teachable Machine](https://teachablemachine.withgoogle.com/)
