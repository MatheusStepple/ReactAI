# Guia de Contribuição

Obrigado por considerar contribuir com o ReactAI! Este documento fornece diretrizes para contribuições.

## Como Contribuir

### 1. Fork e Clone

1. Faça um fork do repositório
2. Clone seu fork localmente:
   ```bash
   git clone https://github.com/seu-usuario/ReactAI.git
   cd ReactAI
   ```

### 2. Configurar Ambiente

#### Backend (Python)
```bash
cd backend
pip install -r requirements.txt
cp env.example .env
# Configure as variáveis de ambiente no .env
```

#### Frontend (React)
```bash
cd frontend
npm install
```

### 3. Criar Branch

Crie uma branch para sua feature:
```bash
git checkout -b feature/nome-da-feature
```

### 4. Desenvolver

- Siga as convenções de código
- Escreva testes para novas funcionalidades
- Mantenha commits pequenos e descritivos

### 5. Testar

#### Backend
```bash
cd backend
pytest
```

#### Frontend
```bash
cd frontend
npm test
npm run build
```

### 6. Commit e Push

```bash
git add .
git commit -m "feat: adiciona nova funcionalidade"
git push origin feature/nome-da-feature
```

### 7. Pull Request

1. Vá para o repositório original no GitHub
2. Clique em "New Pull Request"
3. Selecione sua branch
4. Preencha o template do PR
5. Aguarde a revisão

## Convenções de Código

### Python (Backend)

- Use **Black** para formatação
- Use **isort** para importações
- Use **flake8** para linting
- Siga **PEP 8**
- Use **type hints**
- Documente funções com **docstrings**

```python
def analyze_emotion(emotion_data: Dict[str, float]) -> Dict[str, Any]:
    """
    Analisa dados de emoção e retorna resultados.
    
    Args:
        emotion_data: Dicionário com probabilidades de emoções
        
    Returns:
        Dicionário com resultados da análise
    """
    # Implementação
    pass
```

### JavaScript/React (Frontend)

- Use **Prettier** para formatação
- Use **ESLint** para linting
- Use **TypeScript** quando possível
- Siga **Airbnb Style Guide**
- Use **JSDoc** para documentação

```javascript
/**
 * Analisa emoção em tempo real
 * @param {Object} emotionData - Dados da emoção
 * @returns {Object} Resultado da análise
 */
const analyzeEmotion = (emotionData) => {
  // Implementação
}
```

### Commits

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Manutenção

### Branches

- `main`: Código de produção
- `develop`: Desenvolvimento
- `feature/*`: Novas funcionalidades
- `bugfix/*`: Correções de bugs
- `hotfix/*`: Correções urgentes

## Estrutura do Projeto

```
ReactAI/
├── backend/                 # API Python/FastAPI
│   ├── app/
│   │   ├── models.py       # Modelos SQLAlchemy
│   │   ├── schemas.py      # Schemas Pydantic
│   │   ├── crud.py         # Operações CRUD
│   │   ├── main.py         # Aplicação FastAPI
│   │   └── services/       # Serviços de negócio
│   ├── requirements.txt    # Dependências Python
│   └── Dockerfile
├── frontend/               # Aplicação React
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── pages/         # Páginas da aplicação
│   │   ├── services/      # Serviços de API
│   │   └── utils/         # Utilitários
│   ├── package.json       # Dependências Node.js
│   └── Dockerfile
├── nginx/                 # Configuração Nginx
├── docs/                  # Documentação
└── tests/                 # Testes integrados
```

## Testes

### Backend

```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend

```bash
cd frontend
npm test -- --coverage
```

### E2E

```bash
npm run test:e2e
```

## Documentação

- Mantenha o README atualizado
- Documente APIs com docstrings
- Use exemplos de código
- Inclua screenshots quando relevante

## Issues

### Reportando Bugs

1. Use o template de bug
2. Inclua passos para reproduzir
3. Descreva o comportamento esperado
4. Inclua logs e screenshots

### Sugerindo Features

1. Use o template de feature
2. Descreva o problema que resolve
3. Proponha uma solução
4. Discuta alternativas

## Revisão de Código

### Checklist

- [ ] Código segue convenções
- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Não quebra funcionalidades existentes
- [ ] Performance adequada
- [ ] Segurança considerada

### Feedback

- Seja construtivo
- Explique o porquê
- Sugira alternativas
- Reconheça boas práticas

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a [MIT License](LICENSE).

## Contato

- **Issues**: [GitHub Issues](https://github.com/matheusstepple/ReactAI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/matheusstepple/ReactAI/discussions)
- **Email**: [matheus.stepple@gmail.com](mailto:matheus.stepple@gmail.com)

## Agradecimentos

Obrigado por contribuir com o ReactAI! Suas contribuições ajudam a tornar o projeto melhor para todos.
