#!/bin/bash

# ReactAI - Script de Inicialização Rápida
# Este script inicia o backend e frontend do ReactAI

echo "🚀 ReactAI - Inicializando Sistema..."
echo "======================================"

# Verificar se estamos no diretório correto
if [ ! -f "README.md" ]; then
    echo "❌ Execute este script no diretório raiz do projeto"
    exit 1
fi

# Função para verificar se um comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar pré-requisitos
echo "🔍 Verificando pré-requisitos..."

if ! command_exists python3; then
    echo "❌ Python 3 não encontrado"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js não encontrado"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm não encontrado"
    exit 1
fi

echo "✅ Pré-requisitos verificados"

# Verificar se o backend está configurado
if [ ! -d "backend" ]; then
    echo "❌ Diretório backend não encontrado"
    exit 1
fi

if [ ! -d "frontend" ]; then
    echo "❌ Diretório frontend não encontrado"
    exit 1
fi

# Função para iniciar o backend
start_backend() {
    echo "🔧 Iniciando backend..."
    cd backend
    
    # Verificar se as dependências estão instaladas
    if [ ! -d "venv" ] && [ ! -d "__pycache__" ]; then
        echo "📦 Instalando dependências do backend..."
        pip install -r requirements.txt
    fi
    
    # Verificar se o arquivo .env existe
    if [ ! -f ".env" ]; then
        if [ -f "env.example" ]; then
            echo "📝 Criando arquivo .env..."
            cp env.example .env
            echo "⚠️  Configure as variáveis de ambiente no arquivo .env"
        fi
    fi
    
    # Iniciar o servidor backend
    echo "🚀 Iniciando servidor backend na porta 8000..."
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
    BACKEND_PID=$!
    cd ..
}

# Função para iniciar o frontend
start_frontend() {
    echo "🎨 Iniciando frontend..."
    cd frontend
    
    # Verificar se as dependências estão instaladas
    if [ ! -d "node_modules" ]; then
        echo "📦 Instalando dependências do frontend..."
        npm install
    fi
    
    # Iniciar o servidor frontend
    echo "🚀 Iniciando servidor frontend na porta 3000..."
    npm start &
    FRONTEND_PID=$!
    cd ..
}

# Função para limpar processos ao sair
cleanup() {
    echo ""
    echo "🛑 Parando serviços..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    echo "✅ Serviços parados"
    exit 0
}

# Capturar Ctrl+C para limpeza
trap cleanup SIGINT

# Iniciar serviços
start_backend
sleep 3  # Aguardar backend inicializar

start_frontend
sleep 5  # Aguardar frontend inicializar

echo ""
echo "✅ ReactAI iniciado com sucesso!"
echo ""
echo "📱 Acesse a aplicação:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   Documentação: http://localhost:8000/docs"
echo ""
echo "🛑 Pressione Ctrl+C para parar os serviços"
echo ""

# Aguardar indefinidamente
wait
