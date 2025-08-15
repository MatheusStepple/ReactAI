# ReactAI - Makefile
# Comandos úteis para desenvolvimento

.PHONY: help install setup start stop test clean docker-build docker-run docker-stop

# Variáveis
PYTHON = python3
PIP = pip3
NODE = node
NPM = npm
DOCKER = docker
DOCKER_COMPOSE = docker-compose

# Cores para output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

help: ## Mostra esta ajuda
	@echo "$(BLUE)ReactAI - Comandos Disponíveis$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Instala todas as dependências
	@echo "$(YELLOW)Instalando dependências...$(NC)"
	@echo "$(BLUE)Backend (Python)...$(NC)"
	cd backend && $(PIP) install -r requirements.txt
	@echo "$(BLUE)Frontend (Node.js)...$(NC)"
	cd frontend && $(NPM) install
	@echo "$(GREEN)✅ Dependências instaladas!$(NC)"

setup: ## Configura o ambiente de desenvolvimento
	@echo "$(YELLOW)Configurando ambiente...$(NC)"
	@if [ ! -f backend/.env ]; then \
		echo "$(BLUE)Criando arquivo .env...$(NC)"; \
		cp backend/env.example backend/.env; \
		echo "$(YELLOW)⚠️  Configure as variáveis de ambiente em backend/.env$(NC)"; \
	fi
	@echo "$(GREEN)✅ Ambiente configurado!$(NC)"

start: ## Inicia o sistema completo
	@echo "$(YELLOW)Iniciando ReactAI...$(NC)"
	@echo "$(BLUE)Backend na porta 8000...$(NC)"
	cd backend && $(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
	@echo "$(BLUE)Frontend na porta 3000...$(NC)"
	cd frontend && $(NPM) start &
	@echo "$(GREEN)✅ ReactAI iniciado!$(NC)"
	@echo "$(BLUE)Frontend: http://localhost:3000$(NC)"
	@echo "$(BLUE)Backend API: http://localhost:8000$(NC)"
	@echo "$(BLUE)Documentação: http://localhost:8000/docs$(NC)"

stop: ## Para todos os serviços
	@echo "$(YELLOW)Parando serviços...$(NC)"
	@pkill -f "uvicorn app.main:app" || true
	@pkill -f "npm start" || true
	@echo "$(GREEN)✅ Serviços parados!$(NC)"

test: ## Executa todos os testes
	@echo "$(YELLOW)Executando testes...$(NC)"
	@echo "$(BLUE)Testes do Backend...$(NC)"
	cd backend && $(PYTHON) -m pytest -v
	@echo "$(BLUE)Testes do Frontend...$(NC)"
	cd frontend && $(NPM) test -- --watchAll=false
	@echo "$(GREEN)✅ Testes concluídos!$(NC)"

test-backend: ## Executa apenas testes do backend
	@echo "$(YELLOW)Executando testes do backend...$(NC)"
	cd backend && $(PYTHON) -m pytest -v

test-frontend: ## Executa apenas testes do frontend
	@echo "$(YELLOW)Executando testes do frontend...$(NC)"
	cd frontend && $(NPM) test -- --watchAll=false

lint: ## Executa linters
	@echo "$(YELLOW)Executando linters...$(NC)"
	@echo "$(BLUE)Backend (flake8)...$(NC)"
	cd backend && flake8 app/ --max-line-length=88 --ignore=E203,W503
	@echo "$(BLUE)Frontend (ESLint)...$(NC)"
	cd frontend && $(NPM) run lint
	@echo "$(GREEN)✅ Linting concluído!$(NC)"

format: ## Formata o código
	@echo "$(YELLOW)Formatando código...$(NC)"
	@echo "$(BLUE)Backend (Black)...$(NC)"
	cd backend && black app/
	@echo "$(BLUE)Frontend (Prettier)...$(NC)"
	cd frontend && $(NPM) run format
	@echo "$(GREEN)✅ Código formatado!$(NC)"

clean: ## Limpa arquivos temporários
	@echo "$(YELLOW)Limpando arquivos temporários...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	@echo "$(GREEN)✅ Limpeza concluída!$(NC)"

docker-build: ## Constrói as imagens Docker
	@echo "$(YELLOW)Construindo imagens Docker...$(NC)"
	$(DOCKER_COMPOSE) build
	@echo "$(GREEN)✅ Imagens construídas!$(NC)"

docker-run: ## Executa com Docker Compose
	@echo "$(YELLOW)Iniciando com Docker...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)✅ ReactAI iniciado com Docker!$(NC)"
	@echo "$(BLUE)Frontend: http://localhost:3000$(NC)"
	@echo "$(BLUE)Backend API: http://localhost:8000$(NC)"

docker-stop: ## Para os containers Docker
	@echo "$(YELLOW)Parando containers Docker...$(NC)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)✅ Containers parados!$(NC)"

docker-logs: ## Mostra logs dos containers
	$(DOCKER_COMPOSE) logs -f

db-create: ## Cria o banco de dados
	@echo "$(YELLOW)Criando banco de dados...$(NC)"
	createdb reactai_db || echo "$(YELLOW)Banco já existe ou erro na criação$(NC)"
	@echo "$(GREEN)✅ Banco de dados criado!$(NC)"

db-migrate: ## Executa migrações do banco
	@echo "$(YELLOW)Executando migrações...$(NC)"
	cd backend && $(PYTHON) -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(engine)"
	@echo "$(GREEN)✅ Migrações executadas!$(NC)"

build: ## Constrói para produção
	@echo "$(YELLOW)Construindo para produção...$(NC)"
	cd frontend && $(NPM) run build
	@echo "$(GREEN)✅ Build concluído!$(NC)"

deploy: ## Deploy para produção
	@echo "$(YELLOW)Fazendo deploy...$(NC)"
	$(MAKE) build
	$(MAKE) docker-build
	$(MAKE) docker-run
	@echo "$(GREEN)✅ Deploy concluído!$(NC)"

security-check: ## Verifica vulnerabilidades de segurança
	@echo "$(YELLOW)Verificando segurança...$(NC)"
	cd backend && safety check
	cd frontend && $(NPM) audit
	@echo "$(GREEN)✅ Verificação de segurança concluída!$(NC)"

docs: ## Gera documentação
	@echo "$(YELLOW)Gerando documentação...$(NC)"
	cd backend && $(PYTHON) -m pydoc -w app
	@echo "$(GREEN)✅ Documentação gerada!$(NC)"

backup: ## Faz backup do banco de dados
	@echo "$(YELLOW)Fazendo backup...$(NC)"
	pg_dump reactai_db > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✅ Backup concluído!$(NC)"

restore: ## Restaura backup do banco de dados
	@echo "$(YELLOW)Restaurando backup...$(NC)"
	@read -p "Nome do arquivo de backup: " file; \
	psql reactai_db < $$file
	@echo "$(GREEN)✅ Restauração concluída!$(NC)"

monitor: ## Monitora recursos do sistema
	@echo "$(YELLOW)Monitorando recursos...$(NC)"
	@echo "$(BLUE)CPU e Memória:$(NC)"
	top -bn1 | head -20
	@echo "$(BLUE)Portas em uso:$(NC)"
	netstat -tulpn | grep -E ':(3000|8000|5432)'

# Comandos de desenvolvimento rápido
dev: install setup start ## Instala, configura e inicia (desenvolvimento)
prod: docker-build docker-run ## Constrói e executa com Docker (produção)
quick: start ## Inicia rapidamente (assume dependências instaladas)
