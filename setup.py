#!/usr/bin/env python3
"""
Script de setup automatizado para o ReactAI
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Executa um comando e retorna o resultado"""
    try:
        result = subprocess.run(command, cwd=cwd, shell=shell, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Erro ao executar: {command}")
            print(f"Erro: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Erro ao executar: {command}")
        print(f"Exceção: {e}")
        return False

def check_requirements():
    """Verifica se os pré-requisitos estão instalados"""
    print("🔍 Verificando pré-requisitos...")
    
    # Verificar Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ é necessário")
        return False
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Verificar Node.js
    if not run_command("node --version", shell=True):
        print("❌ Node.js é necessário")
        return False
    
    # Verificar npm
    if not run_command("npm --version", shell=True):
        print("❌ npm é necessário")
        return False
    
    # Verificar PostgreSQL
    if not run_command("psql --version", shell=True):
        print("⚠️  PostgreSQL não encontrado. Certifique-se de que está instalado.")
    
    print("✅ Pré-requisitos verificados")
    return True

def setup_backend():
    """Configura o backend"""
    print("\n🔧 Configurando backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Diretório backend não encontrado")
        return False
    
    # Instalar dependências Python
    print("📦 Instalando dependências Python...")
    if not run_command("pip install -r requirements.txt", cwd=backend_dir):
        return False
    
    # Criar arquivo .env se não existir
    env_file = backend_dir / ".env"
    env_example = backend_dir / "env.example"
    
    if not env_file.exists() and env_example.exists():
        print("📝 Criando arquivo .env...")
        run_command(f"cp env.example .env", cwd=backend_dir)
        print("⚠️  Configure as variáveis de ambiente no arquivo .env")
    
    print("✅ Backend configurado")
    return True

def setup_frontend():
    """Configura o frontend"""
    print("\n🎨 Configurando frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Diretório frontend não encontrado")
        return False
    
    # Instalar dependências Node.js
    print("📦 Instalando dependências Node.js...")
    if not run_command("npm install", cwd=frontend_dir):
        return False
    
    print("✅ Frontend configurado")
    return True

def create_database():
    """Cria o banco de dados"""
    print("\n🗄️  Configurando banco de dados...")
    
    # Tentar criar banco de dados
    if run_command("createdb reactai_db", shell=True):
        print("✅ Banco de dados criado")
    else:
        print("⚠️  Não foi possível criar o banco de dados automaticamente")
        print("   Execute manualmente: createdb reactai_db")
    
    return True

def main():
    """Função principal"""
    print("🚀 ReactAI - Setup Automatizado")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not Path("README.md").exists():
        print("❌ Execute este script no diretório raiz do projeto")
        return
    
    # Verificar pré-requisitos
    if not check_requirements():
        print("\n❌ Setup falhou. Verifique os pré-requisitos.")
        return
    
    # Setup backend
    if not setup_backend():
        print("\n❌ Setup do backend falhou.")
        return
    
    # Setup frontend
    if not setup_frontend():
        print("\n❌ Setup do frontend falhou.")
        return
    
    # Setup banco de dados
    create_database()
    
    print("\n" + "=" * 50)
    print("✅ Setup concluído com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Configure as variáveis de ambiente em backend/.env")
    print("2. Inicie o backend: cd backend && uvicorn app.main:app --reload")
    print("3. Inicie o frontend: cd frontend && npm start")
    print("4. Acesse: http://localhost:3000")
    print("\n📚 Documentação: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
