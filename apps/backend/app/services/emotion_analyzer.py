import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt
import seaborn as sns

class EmotionAnalyzer:
    """Serviço para análise avançada de emoções usando scikit-learn"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_path = "models/emotion_classifier.pkl"
        self.scaler_path = "models/scaler.pkl"
        
        # Criar diretório de modelos se não existir
        os.makedirs("models", exist_ok=True)
        
        # Tentar carregar modelo pré-treinado
        self.load_model()
    
    def load_model(self):
        """Carrega modelo pré-treinado se existir"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                self.is_trained = True
                print("Modelo carregado com sucesso!")
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    def save_model(self):
        """Salva o modelo treinado"""
        try:
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            print("Modelo salvo com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar modelo: {e}")
    
    def prepare_features(self, emotion_data: List[Dict]) -> np.ndarray:
        """Prepara features para o modelo de ML"""
        features = []
        for data in emotion_data:
            feature_vector = [
                data['satisfaction_prob'],
                data['dissatisfaction_prob'],
                data['background_prob'],
                data['confidence']
            ]
            features.append(feature_vector)
        return np.array(features)
    
    def train_model(self, emotion_data: List[Dict], labels: List[str]):
        """Treina o modelo com dados de emoções"""
        if len(emotion_data) < 10:
            raise ValueError("Necessário pelo menos 10 amostras para treinar o modelo")
        
        # Preparar features
        X = self.prepare_features(emotion_data)
        y = np.array(labels)
        
        # Dividir dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Normalizar features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Treinar modelo
        self.model.fit(X_train_scaled, y_train)
        
        # Avaliar modelo
        y_pred = self.model.predict(X_test_scaled)
        accuracy = self.model.score(X_test_scaled, y_test)
        
        print(f"Acurácia do modelo: {accuracy:.2f}")
        print("\nRelatório de Classificação:")
        print(classification_report(y_test, y_pred))
        
        self.is_trained = True
        self.save_model()
        
        return {
            'accuracy': accuracy,
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred)
        }
    
    def predict_emotion(self, emotion_data: Dict) -> Dict:
        """Faz predição de emoção usando o modelo treinado"""
        if not self.is_trained:
            # Fallback para predição simples baseada em probabilidades
            return self._simple_prediction(emotion_data)
        
        # Preparar features
        features = self.prepare_features([emotion_data])
        features_scaled = self.scaler.transform(features)
        
        # Fazer predição
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        return {
            'predicted_class': prediction,
            'confidence': max(probabilities),
            'probabilities': dict(zip(self.model.classes_, probabilities))
        }
    
    def _simple_prediction(self, emotion_data: Dict) -> Dict:
        """Predição simples baseada em probabilidades do Teachable Machine"""
        probs = [
            emotion_data['satisfaction_prob'],
            emotion_data['dissatisfaction_prob'],
            emotion_data['background_prob']
        ]
        
        classes = ['satisfaction', 'dissatisfaction', 'background']
        max_idx = np.argmax(probs)
        
        return {
            'predicted_class': classes[max_idx],
            'confidence': probs[max_idx],
            'probabilities': dict(zip(classes, probs))
        }
    
    def analyze_session_data(self, emotion_data: List[Dict]) -> Dict:
        """Analisa dados de uma sessão completa"""
        if not emotion_data:
            return {
                'approval_rate': 0.0,
                'interest_rate': 0.0,
                'total_frames': 0,
                'emotion_frames': 0,
                'emotion_distribution': {},
                'confidence_stats': {}
            }
        
        df = pd.DataFrame(emotion_data)
        
        # Calcular métricas básicas
        total_frames = len(df)
        emotion_frames = len(df[df['predicted_class'] != 'background'])
        
        # Taxa de aprovação (satisfação vs insatisfação)
        satisfaction_frames = len(df[df['predicted_class'] == 'satisfaction'])
        dissatisfaction_frames = len(df[df['predicted_class'] == 'dissatisfation'])
        
        total_emotion_frames = satisfaction_frames + dissatisfaction_frames
        approval_rate = (satisfaction_frames / total_emotion_frames * 100) if total_emotion_frames > 0 else 0
        
        # Taxa de interesse (frames com emoção vs total)
        interest_rate = (emotion_frames / total_frames * 100) if total_frames > 0 else 0
        
        # Distribuição de emoções
        emotion_distribution = df['predicted_class'].value_counts().to_dict()
        
        # Estatísticas de confiança
        confidence_stats = {
            'mean': df['confidence'].mean(),
            'std': df['confidence'].std(),
            'min': df['confidence'].min(),
            'max': df['confidence'].max()
        }
        
        return {
            'approval_rate': round(approval_rate, 2),
            'interest_rate': round(interest_rate, 2),
            'total_frames': total_frames,
            'emotion_frames': emotion_frames,
            'emotion_distribution': emotion_distribution,
            'confidence_stats': confidence_stats
        }
    
    def generate_visualizations(self, emotion_data: List[Dict], save_path: str = None):
        """Gera visualizações dos dados de emoção"""
        if not emotion_data:
            return None
        
        df = pd.DataFrame(emotion_data)
        
        # Configurar estilo
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Análise de Emoções - ReactAI', fontsize=16, fontweight='bold')
        
        # 1. Distribuição de emoções
        emotion_counts = df['predicted_class'].value_counts()
        axes[0, 0].pie(emotion_counts.values, labels=emotion_counts.index, autopct='%1.1f%%')
        axes[0, 0].set_title('Distribuição de Emoções')
        
        # 2. Evolução temporal das probabilidades
        axes[0, 1].plot(df['satisfaction_prob'], label='Satisfação', color='green')
        axes[0, 1].plot(df['dissatisfaction_prob'], label='Insatisfação', color='red')
        axes[0, 1].plot(df['background_prob'], label='Fundo', color='gray')
        axes[0, 1].set_title('Evolução Temporal das Probabilidades')
        axes[0, 1].set_xlabel('Frame')
        axes[0, 1].set_ylabel('Probabilidade')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # 3. Distribuição de confiança
        axes[1, 0].hist(df['confidence'], bins=20, alpha=0.7, color='skyblue')
        axes[1, 0].set_title('Distribuição de Confiança')
        axes[1, 0].set_xlabel('Confiança')
        axes[1, 0].set_ylabel('Frequência')
        
        # 4. Box plot de confiança por emoção
        df.boxplot(column='confidence', by='predicted_class', ax=axes[1, 1])
        axes[1, 1].set_title('Confiança por Tipo de Emoção')
        axes[1, 1].set_xlabel('Emoção')
        axes[1, 1].set_ylabel('Confiança')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Visualização salva em: {save_path}")
        
        return fig
