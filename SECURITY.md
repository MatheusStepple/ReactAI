# Política de Segurança

## Versões Suportadas

Use esta seção para informar às pessoas sobre quais versões do seu projeto estão atualmente sendo suportadas com atualizações de segurança.

| Versão | Suportada          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reportando uma Vulnerabilidade

Se você descobrir uma vulnerabilidade de segurança, por favor, siga estas etapas:

1. **NÃO** abra um issue público no GitHub
2. Envie um email para [matheus.stepple@gmail.com](mailto:matheus.stepple@gmail.com) com o assunto "[SECURITY] Vulnerabilidade no ReactAI"
3. Inclua detalhes sobre a vulnerabilidade, incluindo:
   - Descrição da vulnerabilidade
   - Passos para reproduzir
   - Possível impacto
   - Sugestões de correção (se houver)

### O que esperar

- Você receberá uma confirmação em até 48 horas
- Uma análise será realizada e você será informado sobre o progresso
- Uma correção será desenvolvida e testada
- Uma nova versão será lançada com a correção
- Você será creditado na seção de agradecimentos (se desejar)

## Boas Práticas de Segurança

### Para Desenvolvedores

1. **Mantenha as dependências atualizadas**
   - Execute regularmente `npm audit` e `pip audit`
   - Configure o Dependabot para atualizações automáticas

2. **Validação de Entrada**
   - Sempre valide dados de entrada no backend
   - Use Pydantic para validação de schemas
   - Implemente rate limiting para APIs

3. **Autenticação e Autorização**
   - Use tokens JWT seguros
   - Implemente autenticação de dois fatores quando possível
   - Valide permissões em todas as rotas

4. **Criptografia**
   - Use HTTPS em produção
   - Criptografe dados sensíveis
   - Use variáveis de ambiente para secrets

### Para Usuários

1. **Mantenha o sistema atualizado**
2. **Use senhas fortes**
3. **Não compartilhe credenciais**
4. **Monitore logs de acesso**
5. **Faça backup regular dos dados**

## Histórico de Vulnerabilidades

### 2024-01-XX
- **CVE-XXXX-XXXX**: Descrição da vulnerabilidade
- **Status**: Corrigido na versão 1.0.1
- **Impacto**: Baixo/Médio/Alto
- **Solução**: Atualizar para versão 1.0.1 ou superior

## Contato

Para questões de segurança, entre em contato:

- **Email**: [matheus.stepple@gmail.com](mailto:matheus.stepple@gmail.com)
- **LinkedIn**: [matheus-stepple](https://www.linkedin.com/in/matheus-stepple/)
- **GitHub**: [matheusstepple](https://github.com/matheusstepple)

## Agradecimentos

Agradecemos a todos os pesquisadores de segurança que contribuem para manter o ReactAI seguro:

- [Nome do pesquisador] - CVE-XXXX-XXXX
- [Nome do pesquisador] - CVE-XXXX-XXXX
