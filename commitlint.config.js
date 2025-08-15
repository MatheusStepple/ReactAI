module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',     // Nova funcionalidade
        'fix',      // Correção de bug
        'docs',     // Documentação
        'style',    // Formatação
        'refactor', // Refatoração
        'perf',     // Melhoria de performance
        'test',     // Testes
        'build',    // Build system
        'ci',       // CI/CD
        'chore',    // Manutenção
        'revert',   // Reverter commit
        'wip',      // Work in progress
        'hotfix',   // Correção urgente
        'security', // Segurança
        'deps',     // Dependências
        'config',   // Configuração
        'init',     // Inicialização
        'release',  // Release
        'breaking', // Breaking changes
      ],
    ],
    'type-case': [2, 'always', 'lower'],
    'type-empty': [2, 'never'],
    'subject-case': [2, 'always', 'lower'],
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],
    'subject-max-length': [2, 'always', 72],
    'body-leading-blank': [2, 'always'],
    'body-max-line-length': [2, 'always', 100],
    'footer-leading-blank': [2, 'always'],
    'footer-max-line-length': [2, 'always', 100],
  },
  prompt: {
    questions: {
      type: {
        description: 'Selecione o tipo de mudança que você está fazendo:',
        enum: {
          feat: {
            description: '✨ Nova funcionalidade',
            title: 'Features',
            emoji: '✨',
          },
          fix: {
            description: '🐛 Correção de bug',
            title: 'Bug Fixes',
            emoji: '🐛',
          },
          docs: {
            description: '📝 Documentação',
            title: 'Documentation',
            emoji: '📝',
          },
          style: {
            description: '💄 Formatação',
            title: 'Styles',
            emoji: '💄',
          },
          refactor: {
            description: '♻️ Refatoração',
            title: 'Code Refactoring',
            emoji: '♻️',
          },
          perf: {
            description: '⚡ Performance',
            title: 'Performance Improvements',
            emoji: '⚡',
          },
          test: {
            description: '🚨 Testes',
            title: 'Tests',
            emoji: '🚨',
          },
          build: {
            description: '📦 Build',
            title: 'Builds',
            emoji: '📦',
          },
          ci: {
            description: '👷 CI/CD',
            title: 'Continuous Integrations',
            emoji: '👷',
          },
          chore: {
            description: '🔧 Manutenção',
            title: 'Chores',
            emoji: '🔧',
          },
          revert: {
            description: '⏪ Reverter',
            title: 'Reverts',
            emoji: '⏪',
          },
          wip: {
            description: '🚧 Work in progress',
            title: 'Work in Progress',
            emoji: '🚧',
          },
          hotfix: {
            description: '🚑 Correção urgente',
            title: 'Hotfixes',
            emoji: '🚑',
          },
          security: {
            description: '🔒 Segurança',
            title: 'Security',
            emoji: '🔒',
          },
          deps: {
            description: '📦 Dependências',
            title: 'Dependencies',
            emoji: '📦',
          },
          config: {
            description: '⚙️ Configuração',
            title: 'Configuration',
            emoji: '⚙️',
          },
          init: {
            description: '🎉 Inicialização',
            title: 'Initialization',
            emoji: '🎉',
          },
          release: {
            description: '🚀 Release',
            title: 'Releases',
            emoji: '🚀',
          },
          breaking: {
            description: '💥 Breaking changes',
            title: 'Breaking Changes',
            emoji: '💥',
          },
        },
      },
      scope: {
        description: 'Indique o escopo desta mudança (opcional):',
      },
      subject: {
        description: 'Escreva uma descrição curta e imperativa da mudança:',
      },
      body: {
        description: 'Forneça uma descrição mais detalhada da mudança (opcional):',
      },
      isBreaking: {
        description: 'Há mudanças que quebram a compatibilidade?',
      },
      breakingBody: {
        description: 'Uma descrição das mudanças que quebram a compatibilidade:',
      },
      breaking: {
        description: 'Descreva as mudanças que quebram a compatibilidade:',
      },
      isIssueAffected: {
        description: 'Esta mudança afeta algum issue aberto?',
      },
      issuesBody: {
        description: 'Se os issues são fechados, a chave de fechamento é necessária:',
      },
      issues: {
        description: 'Adicione referências de issues (ex: "fix #123", "re #123"):',
      },
    },
  },
};
