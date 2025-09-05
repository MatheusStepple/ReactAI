import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Brain, 
  Camera, 
  BarChart3, 
  Zap, 
  Users, 
  Target,
  TrendingUp,
  Shield,
  ArrowRight,
  Play,
  BookOpen,
  Github
} from 'lucide-react';

const HomePage = () => {
  const features = [
    {
      icon: Brain,
      title: 'IA Avançada',
      description: 'Modelo de machine learning treinado com scikit-learn para análise precisa de emoções',
      color: 'text-primary-400'
    },
    {
      icon: Camera,
      title: 'Visão Computacional',
      description: 'Captura e análise em tempo real de expressões faciais via webcam',
      color: 'text-secondary-400'
    },
    {
      icon: BarChart3,
      title: 'Analytics em Tempo Real',
      description: 'Dashboard interativo com métricas de aprovação e interesse do público',
      color: 'text-green-400'
    },
    {
      icon: Zap,
      title: 'Processamento Rápido',
      description: 'Análise instantânea com feedback visual imediato',
      color: 'text-yellow-400'
    }
  ];

  const benefits = [
    {
      icon: Users,
      title: 'Compreensão do Público',
      description: 'Entenda as reações espontâneas do seu público-alvo'
    },
    {
      icon: Target,
      title: 'Decisões Estratégicas',
      description: 'Suporte para marketing, design de produto e pesquisa de mercado'
    },
    {
      icon: TrendingUp,
      title: 'Insights Valiosos',
      description: 'Dados quantitativos sobre a recepção de produtos e serviços'
    },
    {
      icon: Shield,
      title: 'Privacidade Garantida',
      description: 'Processamento local sem armazenamento de imagens pessoais'
    }
  ];

  const techStack = [
    { name: 'Python', category: 'Backend' },
    { name: 'FastAPI', category: 'API' },
    { name: 'PostgreSQL', category: 'Database' },
    { name: 'React', category: 'Frontend' },
    { name: 'scikit-learn', category: 'ML' },
    { name: 'pandas', category: 'Data' },
    { name: 'NumPy', category: 'Data' },
    { name: 'matplotlib', category: 'Visualization' },
    { name: 'TensorFlow.js', category: 'ML' },
    { name: 'Teachable Machine', category: 'ML' }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="text-center py-20 fade-in">
        <div className="max-w-4xl mx-auto px-4">
          <div className="flex justify-center mb-6">
            <div className="relative">
              <Brain className="h-20 w-20 text-primary-400" />
              <Zap className="h-8 w-8 text-secondary-400 absolute -top-2 -right-2" />
            </div>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            <span className="gradient-text">ReactAI</span>
          </h1>
          
          <p className="text-xl md:text-2xl text-dark-300 mb-8 max-w-3xl mx-auto">
            Sistema inovador de visão computacional que mede, em tempo real, 
            o nível de interesse e aprovação do público através da análise de expressões faciais
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/analysis"
              className="btn-primary flex items-center justify-center space-x-2"
            >
              <Play className="h-5 w-5" />
              <span>Começar Análise</span>
            </Link>
            
            <Link
              to="/dashboard"
              className="btn-secondary flex items-center justify-center space-x-2"
            >
              <BarChart3 className="h-5 w-5" />
              <span>Ver Dashboard</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-dark-800/50">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Tecnologias Avançadas
            </h2>
            <p className="text-dark-300 text-lg max-w-2xl mx-auto">
              Combinamos as melhores tecnologias de IA e visão computacional 
              para criar uma solução poderosa e acessível
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div key={index} className="card p-6 text-center fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                  <div className={`${feature.color} mb-4 flex justify-center`}>
                    <Icon className="h-12 w-12" />
                  </div>
                  <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                  <p className="text-dark-300">{feature.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Benefícios para seu Negócio
            </h2>
            <p className="text-dark-300 text-lg max-w-2xl mx-auto">
              Transforme a forma como você entende e interage com seu público
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            {benefits.map((benefit, index) => {
              const Icon = benefit.icon;
              return (
                <div key={index} className="card p-6 slide-in" style={{ animationDelay: `${index * 0.1}s` }}>
                  <div className="flex items-start space-x-4">
                    <div className="text-primary-400">
                      <Icon className="h-8 w-8" />
                    </div>
                    <div>
                      <h3 className="text-xl font-semibold mb-2">{benefit.title}</h3>
                      <p className="text-dark-300">{benefit.description}</p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Tech Stack Section */}
      <section className="py-20 bg-dark-800/50">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Stack Tecnológico
            </h2>
            <p className="text-dark-300 text-lg max-w-2xl mx-auto">
              Desenvolvido com as melhores ferramentas e frameworks disponíveis
            </p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {techStack.map((tech, index) => (
              <div key={index} className="card p-4 text-center fade-in" style={{ animationDelay: `${index * 0.05}s` }}>
                <div className="text-sm text-primary-400 mb-1">{tech.category}</div>
                <div className="font-semibold">{tech.name}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Pronto para revolucionar sua análise de público?
          </h2>
          <p className="text-dark-300 text-lg mb-8 max-w-2xl mx-auto">
            Comece agora mesmo e descubra insights valiosos sobre as reações do seu público
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/analysis"
              className="btn-primary flex items-center justify-center space-x-2"
            >
              <Camera className="h-5 w-5" />
              <span>Iniciar Análise</span>
              <ArrowRight className="h-4 w-4" />
            </Link>
            
            <a
              href="https://github.com/matheusstepple/ReactAI"
              target="_blank"
              rel="noopener noreferrer"
              className="btn-secondary flex items-center justify-center space-x-2"
            >
              <Github className="h-5 w-5" />
              <span>Ver no GitHub</span>
            </a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-dark-700">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <div className="flex justify-center items-center space-x-2 mb-4">
            <Brain className="h-6 w-6 text-primary-400" />
            <span className="text-xl font-bold gradient-text">ReactAI</span>
          </div>
          
          <p className="text-dark-400 mb-4">
            Sistema de Visão Computacional para Análise de Reação do Público em Tempo Real
          </p>
          
          <div className="flex justify-center space-x-6 text-sm text-dark-400">
            <span>Desenvolvido por Matheus Stepple</span>
            <span>•</span>
            <span>UFPE - Centro de Informática</span>
            <span>•</span>
            <span>Prof. Cleber Zanchettin</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
