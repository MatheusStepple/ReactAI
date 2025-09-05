import React, { useState, useRef, useEffect, useCallback } from 'react';
import Webcam from 'react-webcam';
import { 
  Play, 
  Square, 
  Camera, 
  BarChart3, 
  Download, 
  Settings,
  AlertCircle,
  CheckCircle,
  Clock,
  Brain,
  Zap
} from 'lucide-react';
import toast from 'react-hot-toast';
import axios from 'axios';

const AnalysisPage = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [model, setModel] = useState(null);
  const [predictions, setPredictions] = useState([]);
  const [currentEmotion, setCurrentEmotion] = useState(null);
  const [sessionData, setSessionData] = useState({
    productName: '',
    duration: 10,
    userId: 1 // Default user for demo
  });
  const [timer, setTimer] = useState(0);
  const [isModelLoading, setIsModelLoading] = useState(true);
  const [isWebcamReady, setIsWebcamReady] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [emotionData, setEmotionData] = useState([]);
  
  const webcamRef = useRef(null);
  const intervalRef = useRef(null);
  const predictionIntervalRef = useRef(null);

  // Teachable Machine model URL
  const MODEL_URL = "https://teachablemachine.withgoogle.com/models/YwDSlSEVp/";

  // Load TensorFlow.js and Teachable Machine
  useEffect(() => {
    const loadModel = async () => {
      try {
        // Load TensorFlow.js
        const tf = await import('@tensorflow/tfjs');
        const tmImage = await import('@teachablemachine/image');
        
        // Load the model
        const loadedModel = await tmImage.load(MODEL_URL + "model.json", MODEL_URL + "metadata.json");
        setModel(loadedModel);
        setIsModelLoading(false);
        toast.success('Modelo carregado com sucesso!');
      } catch (error) {
        console.error('Erro ao carregar modelo:', error);
        setIsModelLoading(false);
        toast.error('Erro ao carregar modelo. Verifique sua conexão.');
      }
    };

    loadModel();
  }, []);

  // Prediction function
  const predict = useCallback(async () => {
    if (!model || !webcamRef.current || !isRunning) return;

    try {
      const canvas = document.createElement('canvas');
      canvas.width = 224;
      canvas.height = 224;
      const ctx = canvas.getContext('2d');
      
      // Capture frame from webcam
      ctx.drawImage(webcamRef.current.video, 0, 0, canvas.width, canvas.height);
      
      // Make prediction
      const prediction = await model.predict(canvas);
      
      // Process prediction
      const emotionData = {
        satisfaction_prob: 0,
        dissatisfaction_prob: 0,
        background_prob: 0,
        predicted_class: '',
        confidence: 0,
        timestamp: new Date().toISOString()
      };

      prediction.forEach((p) => {
        if (p.className === 'Gostou') {
          emotionData.satisfaction_prob = p.probability;
        } else if (p.className === 'Não gostou') {
          emotionData.dissatisfaction_prob = p.probability;
        } else if (p.className === 'FUNDO') {
          emotionData.background_prob = p.probability;
        }
      });

      // Determine predicted class
      const maxProb = Math.max(emotionData.satisfaction_prob, emotionData.dissatisfaction_prob, emotionData.background_prob);
      emotionData.confidence = maxProb;
      
      if (maxProb === emotionData.satisfaction_prob) {
        emotionData.predicted_class = 'satisfaction';
      } else if (maxProb === emotionData.dissatisfaction_prob) {
        emotionData.predicted_class = 'dissatisfaction';
      } else {
        emotionData.predicted_class = 'background';
      }

      setCurrentEmotion(emotionData);
      setEmotionData(prev => [...prev, emotionData]);

      // Send to backend if session is active
      if (sessionId) {
        try {
          await axios.post('/emotions/', {
            session_id: sessionId,
            ...emotionData
          });
        } catch (error) {
          console.error('Erro ao enviar dados para backend:', error);
        }
      }

    } catch (error) {
      console.error('Erro na predição:', error);
    }
  }, [model, isRunning, sessionId]);

  // Start prediction loop
  useEffect(() => {
    if (isRunning && model) {
      predictionIntervalRef.current = setInterval(predict, 100); // 10 FPS
    } else {
      if (predictionIntervalRef.current) {
        clearInterval(predictionIntervalRef.current);
      }
    }

    return () => {
      if (predictionIntervalRef.current) {
        clearInterval(predictionIntervalRef.current);
      }
    };
  }, [isRunning, model, predict]);

  // Timer effect
  useEffect(() => {
    if (isRunning && timer < sessionData.duration) {
      intervalRef.current = setInterval(() => {
        setTimer(prev => prev + 1);
      }, 1000);
    } else if (timer >= sessionData.duration) {
      stopAnalysis();
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isRunning, timer, sessionData.duration]);

  const startAnalysis = async () => {
    if (!sessionData.productName.trim()) {
      toast.error('Por favor, insira o nome do produto');
      return;
    }

    if (sessionData.duration < 5 || sessionData.duration > 300) {
      toast.error('Duração deve estar entre 5 e 300 segundos');
      return;
    }

    try {
      // Create session in backend
      const sessionResponse = await axios.post('/sessions/', {
        user_id: sessionData.userId,
        product_name: sessionData.productName,
        duration_seconds: sessionData.duration
      });

      setSessionId(sessionResponse.data.id);
      setIsRunning(true);
      setTimer(0);
      setEmotionData([]);
      setPredictions([]);
      toast.success('Análise iniciada!');
    } catch (error) {
      console.error('Erro ao iniciar sessão:', error);
      toast.error('Erro ao iniciar análise. Tente novamente.');
    }
  };

  const stopAnalysis = async () => {
    setIsRunning(false);
    
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    
    if (predictionIntervalRef.current) {
      clearInterval(predictionIntervalRef.current);
    }

    if (sessionId && emotionData.length > 0) {
      try {
        // Calculate results
        const totalFrames = emotionData.length;
        const emotionFrames = emotionData.filter(e => e.predicted_class !== 'background').length;
        const satisfactionFrames = emotionData.filter(e => e.predicted_class === 'satisfaction').length;
        const dissatisfactionFrames = emotionData.filter(e => e.predicted_class === 'dissatisfaction').length;
        
        const approvalRate = emotionFrames > 0 ? (satisfactionFrames / (satisfactionFrames + dissatisfactionFrames)) * 100 : 0;
        const interestRate = (emotionFrames / totalFrames) * 100;

        // Save analysis result
        await axios.post('/analysis/', {
          session_id: sessionId,
          approval_rate: approvalRate,
          interest_rate: interestRate,
          total_frames: totalFrames,
          emotion_frames: emotionFrames
        });

        setPredictions([{
          product: sessionData.productName,
          duration: sessionData.duration,
          approval: approvalRate.toFixed(2),
          interest: interestRate.toFixed(2)
        }]);

        toast.success('Análise concluída!');
      } catch (error) {
        console.error('Erro ao salvar resultados:', error);
        toast.error('Erro ao salvar resultados.');
      }
    }

    setSessionId(null);
    setTimer(0);
  };

  const exportResults = async () => {
    if (!sessionId) {
      toast.error('Nenhuma sessão para exportar');
      return;
    }

    try {
      const response = await axios.get(`/sessions/${sessionId}/export/csv/`, {
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `reactai_analysis_${sessionData.productName}_${new Date().toISOString().split('T')[0]}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      toast.success('Dados exportados com sucesso!');
    } catch (error) {
      console.error('Erro ao exportar:', error);
      toast.error('Erro ao exportar dados.');
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const getEmotionEmoji = (emotion) => {
    if (!emotion) return '🤔';
    switch (emotion.predicted_class) {
      case 'satisfaction': return '😊';
      case 'dissatisfaction': return '😔';
      case 'background': return '🌫️';
      default: return '🤔';
    }
  };

  const getEmotionColor = (emotion) => {
    if (!emotion) return 'text-gray-400';
    switch (emotion.predicted_class) {
      case 'satisfaction': return 'text-green-400';
      case 'dissatisfaction': return 'text-red-400';
      case 'background': return 'text-gray-400';
      default: return 'text-gray-400';
    }
  };

  return (
    <div className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-4">
            <span className="gradient-text">Análise de Emoções</span>
          </h1>
          <p className="text-dark-300 text-lg">
            Analise as reações do público em tempo real usando visão computacional
          </p>
        </div>

        {/* Configuration Panel */}
        <div className="card p-6 mb-8">
          <div className="flex items-center space-x-2 mb-4">
            <Settings className="h-5 w-5 text-primary-400" />
            <h2 className="text-xl font-semibold">Configuração da Análise</h2>
          </div>
          
          <div className="grid md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Nome do Produto</label>
              <input
                type="text"
                value={sessionData.productName}
                onChange={(e) => setSessionData(prev => ({ ...prev, productName: e.target.value }))}
                placeholder="Ex: Coca-Cola, iPhone 15..."
                className="input-field w-full"
                disabled={isRunning}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2">Duração (segundos)</label>
              <input
                type="number"
                value={sessionData.duration}
                onChange={(e) => setSessionData(prev => ({ ...prev, duration: parseInt(e.target.value) || 10 }))}
                min="5"
                max="300"
                className="input-field w-full"
                disabled={isRunning}
              />
            </div>
            
            <div className="flex items-end">
              <button
                onClick={isRunning ? stopAnalysis : startAnalysis}
                disabled={isModelLoading || !isWebcamReady}
                className={`flex-1 flex items-center justify-center space-x-2 py-3 px-6 rounded-lg font-semibold transition-all ${
                  isRunning
                    ? 'bg-red-500 hover:bg-red-600 text-white'
                    : 'btn-primary'
                } ${(isModelLoading || !isWebcamReady) ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                {isRunning ? (
                  <>
                    <Square className="h-5 w-5" />
                    <span>Parar Análise</span>
                  </>
                ) : (
                  <>
                    <Play className="h-5 w-5" />
                    <span>Iniciar Análise</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Status Indicators */}
        <div className="grid md:grid-cols-4 gap-4 mb-8">
          <div className="card p-4 text-center">
            <div className="flex items-center justify-center space-x-2 mb-2">
              <div className={`status-indicator ${isModelLoading ? 'status-offline' : 'status-online'}`}></div>
              <span className="text-sm font-medium">Modelo IA</span>
            </div>
            <p className="text-xs text-dark-400">
              {isModelLoading ? 'Carregando...' : 'Pronto'}
            </p>
          </div>
          
          <div className="card p-4 text-center">
            <div className="flex items-center justify-center space-x-2 mb-2">
              <div className={`status-indicator ${isWebcamReady ? 'status-online' : 'status-offline'}`}></div>
              <span className="text-sm font-medium">Webcam</span>
            </div>
            <p className="text-xs text-dark-400">
              {isWebcamReady ? 'Conectada' : 'Desconectada'}
            </p>
          </div>
          
          <div className="card p-4 text-center">
            <div className="flex items-center justify-center space-x-2 mb-2">
              <div className={`status-indicator ${isRunning ? 'status-processing' : 'status-offline'}`}></div>
              <span className="text-sm font-medium">Análise</span>
            </div>
            <p className="text-xs text-dark-400">
              {isRunning ? 'Em andamento' : 'Parada'}
            </p>
          </div>
          
          <div className="card p-4 text-center">
            <div className="flex items-center justify-center space-x-2 mb-2">
              <Clock className="h-4 w-4 text-primary-400" />
              <span className="text-sm font-medium">Tempo</span>
            </div>
            <p className="text-xs text-dark-400">
              {formatTime(timer)} / {formatTime(sessionData.duration)}
            </p>
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Webcam and Real-time Analysis */}
          <div className="space-y-6">
            <div className="card p-6">
              <div className="flex items-center space-x-2 mb-4">
                <Camera className="h-5 w-5 text-primary-400" />
                <h3 className="text-lg font-semibold">Câmera</h3>
              </div>
              
              <div className="webcam-container">
                <Webcam
                  ref={webcamRef}
                  audio={false}
                  width="100%"
                  height="auto"
                  onUserMedia={() => setIsWebcamReady(true)}
                  onUserMediaError={() => {
                    setIsWebcamReady(false);
                    toast.error('Erro ao acessar webcam. Verifique as permissões.');
                  }}
                  className="rounded-lg"
                />
              </div>
            </div>

            {/* Current Emotion Display */}
            <div className="card p-6">
              <div className="flex items-center space-x-2 mb-4">
                <Brain className="h-5 w-5 text-primary-400" />
                <h3 className="text-lg font-semibold">Emoção Atual</h3>
              </div>
              
              {currentEmotion ? (
                <div className="text-center">
                  <div className="text-6xl mb-4">
                    {getEmotionEmoji(currentEmotion)}
                  </div>
                  <div className={`text-2xl font-bold mb-2 ${getEmotionColor(currentEmotion)}`}>
                    {currentEmotion.predicted_class === 'satisfaction' && 'Satisfação'}
                    {currentEmotion.predicted_class === 'dissatisfaction' && 'Insatisfação'}
                    {currentEmotion.predicted_class === 'background' && 'Fundo'}
                  </div>
                  <div className="text-sm text-dark-400">
                    Confiança: {(currentEmotion.confidence * 100).toFixed(1)}%
                  </div>
                </div>
              ) : (
                <div className="text-center text-dark-400">
                  <div className="text-4xl mb-2">🤔</div>
                  <p>Aguardando análise...</p>
                </div>
              )}
            </div>
          </div>

          {/* Results and Controls */}
          <div className="space-y-6">
            {/* Progress Bars */}
            <div className="card p-6">
              <div className="flex items-center space-x-2 mb-4">
                <BarChart3 className="h-5 w-5 text-primary-400" />
                <h3 className="text-lg font-semibold">Feedback em Tempo Real</h3>
              </div>
              
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>😊 Satisfação</span>
                    <span>{currentEmotion ? (currentEmotion.satisfaction_prob * 100).toFixed(1) : 0}%</span>
                  </div>
                  <div className="w-full bg-dark-700 rounded-full h-3">
                    <div 
                      className="progress-bar progress-bar-satisfaction h-3 rounded-full"
                      style={{ width: `${currentEmotion ? currentEmotion.satisfaction_prob * 100 : 0}%` }}
                    ></div>
                  </div>
                </div>
                
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>😔 Insatisfação</span>
                    <span>{currentEmotion ? (currentEmotion.dissatisfaction_prob * 100).toFixed(1) : 0}%</span>
                  </div>
                  <div className="w-full bg-dark-700 rounded-full h-3">
                    <div 
                      className="progress-bar progress-bar-dissatisfaction h-3 rounded-full"
                      style={{ width: `${currentEmotion ? currentEmotion.dissatisfaction_prob * 100 : 0}%` }}
                    ></div>
                  </div>
                </div>
                
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>🌫️ Fundo</span>
                    <span>{currentEmotion ? (currentEmotion.background_prob * 100).toFixed(1) : 0}%</span>
                  </div>
                  <div className="w-full bg-dark-700 rounded-full h-3">
                    <div 
                      className="progress-bar progress-bar-background h-3 rounded-full"
                      style={{ width: `${currentEmotion ? currentEmotion.background_prob * 100 : 0}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Session Results */}
            {predictions.length > 0 && (
              <div className="card p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold">Resultados da Sessão</h3>
                  <button
                    onClick={exportResults}
                    className="btn-secondary flex items-center space-x-2"
                  >
                    <Download className="h-4 w-4" />
                    <span>Exportar</span>
                  </button>
                </div>
                
                <div className="space-y-4">
                  {predictions.map((prediction, index) => (
                    <div key={index} className="bg-dark-700 rounded-lg p-4">
                      <div className="grid grid-cols-2 gap-4 text-center">
                        <div>
                          <div className="text-2xl font-bold text-green-400">{prediction.approval}%</div>
                          <div className="text-sm text-dark-400">Aprovação</div>
                        </div>
                        <div>
                          <div className="text-2xl font-bold text-blue-400">{prediction.interest}%</div>
                          <div className="text-sm text-dark-400">Interesse</div>
                        </div>
                      </div>
                      <div className="mt-3 pt-3 border-t border-dark-600 text-center">
                        <div className="text-sm text-dark-300">
                          {prediction.product} • {prediction.duration}s
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Statistics */}
            <div className="card p-6">
              <h3 className="text-lg font-semibold mb-4">Estatísticas da Sessão</h3>
              
              <div className="grid grid-cols-2 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-primary-400">{emotionData.length}</div>
                  <div className="text-sm text-dark-400">Frames Analisados</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-secondary-400">
                    {emotionData.filter(e => e.predicted_class !== 'background').length}
                  </div>
                  <div className="text-sm text-dark-400">Frames com Emoção</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisPage;
