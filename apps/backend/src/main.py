from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Para funcionar sem display
import matplotlib.pyplot as plt

from . import crud, models, schemas
from .database import engine, get_db
from .services.emotion_analyzer import EmotionAnalyzer

# Criar tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ReactAI API",
    description="Sistema de Visão Computacional para Análise de Reação do Público em Tempo Real",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instanciar analisador de emoções
emotion_analyzer = EmotionAnalyzer()

@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "ReactAI API - Sistema de Análise de Emoções",
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde da API"""
    return {"status": "healthy", "service": "ReactAI API"}

# Rotas para Users
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Criar novo usuário"""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email já registrado"
        )
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar usuários"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Obter usuário por ID"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user

# Rotas para Sessions
@app.post("/sessions/", response_model=schemas.Session)
def create_session(session: schemas.SessionCreate, db: Session = Depends(get_db)):
    """Criar nova sessão de análise"""
    return crud.create_session(db=db, session=session)

@app.get("/sessions/", response_model=List[schemas.Session])
def read_sessions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar sessões"""
    sessions = crud.get_all_sessions(db, skip=skip, limit=limit)
    return sessions

@app.get("/sessions/{session_id}", response_model=schemas.Session)
def read_session(session_id: int, db: Session = Depends(get_db)):
    """Obter sessão por ID"""
    db_session = crud.get_session(db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    return db_session

@app.get("/users/{user_id}/sessions/", response_model=List[schemas.Session])
def read_user_sessions(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar sessões de um usuário específico"""
    sessions = crud.get_sessions_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return sessions

# Rotas para EmotionData
@app.post("/emotions/", response_model=schemas.EmotionData)
def create_emotion_data(emotion_data: schemas.EmotionDataCreate, db: Session = Depends(get_db)):
    """Criar novo registro de emoção"""
    return crud.create_emotion_data(db=db, emotion_data=emotion_data)

@app.get("/sessions/{session_id}/emotions/", response_model=List[schemas.EmotionData])
def read_session_emotions(session_id: int, db: Session = Depends(get_db)):
    """Obter dados de emoção de uma sessão"""
    emotions = crud.get_emotion_data_by_session(db, session_id=session_id)
    return emotions

@app.get("/sessions/{session_id}/emotions/stats/")
def get_emotion_stats(session_id: int, db: Session = Depends(get_db)):
    """Obter estatísticas dos dados de emoção de uma sessão"""
    stats = crud.get_emotion_data_stats(db, session_id=session_id)
    return stats

# Rotas para AnalysisResult
@app.post("/analysis/", response_model=schemas.AnalysisResult)
def create_analysis_result(analysis_result: schemas.AnalysisResultCreate, db: Session = Depends(get_db)):
    """Criar novo resultado de análise"""
    return crud.create_analysis_result(db=db, analysis_result=analysis_result)

@app.get("/sessions/{session_id}/analysis/", response_model=schemas.AnalysisResult)
def read_session_analysis(session_id: int, db: Session = Depends(get_db)):
    """Obter resultado de análise de uma sessão"""
    analysis = crud.get_analysis_result_by_session(db, session_id=session_id)
    if analysis is None:
        raise HTTPException(status_code=404, detail="Análise não encontrada")
    return analysis

# Rotas para análise em tempo real
@app.post("/analyze/emotion/")
def analyze_emotion(emotion_data: schemas.RealTimeEmotion):
    """Analisar emoção em tempo real usando o modelo treinado"""
    try:
        # Converter para formato do analisador
        data_dict = {
            'satisfaction_prob': emotion_data.satisfaction_prob,
            'dissatisfaction_prob': emotion_data.dissatisfaction_prob,
            'background_prob': emotion_data.background_prob,
            'predicted_class': emotion_data.predicted_class,
            'confidence': emotion_data.confidence
        }
        
        # Fazer análise
        result = emotion_analyzer.predict_emotion(data_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na análise: {str(e)}")

@app.post("/analyze/session/{session_id}/")
def analyze_session_data(session_id: int, db: Session = Depends(get_db)):
    """Analisar dados completos de uma sessão"""
    try:
        # Obter dados da sessão
        emotions = crud.get_emotion_data_by_session(db, session_id=session_id)
        
        if not emotions:
            raise HTTPException(status_code=404, detail="Nenhum dado de emoção encontrado para esta sessão")
        
        # Converter para formato do analisador
        emotion_data = []
        for emotion in emotions:
            emotion_data.append({
                'satisfaction_prob': emotion.satisfaction_prob,
                'dissatisfaction_prob': emotion.dissatisfaction_prob,
                'background_prob': emotion.background_prob,
                'predicted_class': emotion.predicted_class,
                'confidence': emotion.confidence
            })
        
        # Fazer análise
        result = emotion_analyzer.analyze_session_data(emotion_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na análise: {str(e)}")

# Rotas para relatórios e analytics
@app.get("/analytics/summary/")
def get_analytics_summary(days: int = 30, db: Session = Depends(get_db)):
    """Obter resumo analítico dos últimos N dias"""
    try:
        summary = crud.get_analytics_summary(db, days=days)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar resumo: {str(e)}")

@app.get("/analytics/timeseries/")
def get_time_series_data(days: int = 30, db: Session = Depends(get_db)):
    """Obter dados de série temporal para visualizações"""
    try:
        time_series = crud.get_time_series_data(db, days=days)
        return time_series
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar série temporal: {str(e)}")

@app.get("/sessions/{session_id}/visualization/")
def generate_session_visualization(session_id: int, db: Session = Depends(get_db)):
    """Gerar visualização dos dados de uma sessão"""
    try:
        # Obter dados da sessão
        emotions = crud.get_emotion_data_by_session(db, session_id=session_id)
        
        if not emotions:
            raise HTTPException(status_code=404, detail="Nenhum dado de emoção encontrado para esta sessão")
        
        # Converter para formato do analisador
        emotion_data = []
        for emotion in emotions:
            emotion_data.append({
                'satisfaction_prob': emotion.satisfaction_prob,
                'dissatisfaction_prob': emotion.dissatisfaction_prob,
                'background_prob': emotion.background_prob,
                'predicted_class': emotion.predicted_class,
                'confidence': emotion.confidence
            })
        
        # Gerar visualização
        fig = emotion_analyzer.generate_visualizations(emotion_data)
        
        if fig is None:
            raise HTTPException(status_code=500, detail="Erro ao gerar visualização")
        
        # Salvar figura em buffer
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        
        # Converter para base64
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        plt.close(fig)  # Fechar figura para liberar memória
        
        return {
            "image_base64": img_base64,
            "session_id": session_id,
            "total_frames": len(emotion_data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar visualização: {str(e)}")

# Rotas para exportação de dados
@app.get("/sessions/{session_id}/export/csv/")
def export_session_csv(session_id: int, db: Session = Depends(get_db)):
    """Exportar dados de uma sessão em formato CSV"""
    try:
        df = crud.export_session_data(db, session_id=session_id)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para esta sessão")
        
        # Salvar DataFrame em buffer
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        # Criar resposta de arquivo
        response = FileResponse(
            io.BytesIO(csv_buffer.getvalue().encode()),
            media_type="text/csv",
            filename=f"session_{session_id}_data.csv"
        )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao exportar dados: {str(e)}")

@app.get("/sessions/{session_id}/export/json/")
def export_session_json(session_id: int, db: Session = Depends(get_db)):
    """Exportar dados de uma sessão em formato JSON"""
    try:
        emotions = crud.get_emotion_data_by_session(db, session_id=session_id)
        session = crud.get_session(db, session_id=session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Sessão não encontrada")
        
        # Converter para formato JSON
        data = {
            "session": {
                "id": session.id,
                "product_name": session.product_name,
                "duration_seconds": session.duration_seconds,
                "created_at": session.created_at.isoformat()
            },
            "emotions": [
                {
                    "timestamp": emotion.timestamp.isoformat(),
                    "satisfaction_prob": emotion.satisfaction_prob,
                    "dissatisfaction_prob": emotion.dissatisfaction_prob,
                    "background_prob": emotion.background_prob,
                    "predicted_class": emotion.predicted_class,
                    "confidence": emotion.confidence
                }
                for emotion in emotions
            ]
        }
        
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao exportar dados: {str(e)}")

# Rota para treinar modelo
@app.post("/train/model/")
def train_model(emotion_data: List[dict], labels: List[str]):
    """Treinar modelo de análise de emoções"""
    try:
        if len(emotion_data) != len(labels):
            raise HTTPException(status_code=400, detail="Número de dados e labels deve ser igual")
        
        result = emotion_analyzer.train_model(emotion_data, labels)
        return {
            "message": "Modelo treinado com sucesso",
            "accuracy": result['accuracy'],
            "classification_report": result['classification_report']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao treinar modelo: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
