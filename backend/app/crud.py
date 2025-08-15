from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timedelta
import pandas as pd

from . import models, schemas

# CRUD para User
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

# CRUD para Session
def create_session(db: Session, session: schemas.SessionCreate) -> models.Session:
    db_session = models.Session(
        user_id=session.user_id,
        product_name=session.product_name,
        duration_seconds=session.duration_seconds
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_session(db: Session, session_id: int) -> Optional[models.Session]:
    return db.query(models.Session).filter(models.Session.id == session_id).first()

def get_sessions_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Session]:
    return db.query(models.Session).filter(models.Session.user_id == user_id).offset(skip).limit(limit).all()

def get_all_sessions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Session]:
    return db.query(models.Session).order_by(desc(models.Session.created_at)).offset(skip).limit(limit).all()

# CRUD para EmotionData
def create_emotion_data(db: Session, emotion_data: schemas.EmotionDataCreate) -> models.EmotionData:
    db_emotion = models.EmotionData(
        session_id=emotion_data.session_id,
        satisfaction_prob=emotion_data.satisfaction_prob,
        dissatisfaction_prob=emotion_data.dissatisfaction_prob,
        background_prob=emotion_data.background_prob,
        predicted_class=emotion_data.predicted_class,
        confidence=emotion_data.confidence
    )
    db.add(db_emotion)
    db.commit()
    db.refresh(db_emotion)
    return db_emotion

def get_emotion_data_by_session(db: Session, session_id: int) -> List[models.EmotionData]:
    return db.query(models.EmotionData).filter(models.EmotionData.session_id == session_id).all()

def get_emotion_data_stats(db: Session, session_id: int) -> dict:
    """Obtém estatísticas dos dados de emoção de uma sessão"""
    emotions = get_emotion_data_by_session(db, session_id)
    
    if not emotions:
        return {
            'total_frames': 0,
            'emotion_frames': 0,
            'satisfaction_frames': 0,
            'dissatisfaction_frames': 0,
            'background_frames': 0,
            'avg_confidence': 0.0
        }
    
    total_frames = len(emotions)
    emotion_frames = len([e for e in emotions if e.predicted_class != 'background'])
    satisfaction_frames = len([e for e in emotions if e.predicted_class == 'satisfaction'])
    dissatisfaction_frames = len([e for e in emotions if e.predicted_class == 'dissatisfaction'])
    background_frames = len([e for e in emotions if e.predicted_class == 'background'])
    avg_confidence = sum(e.confidence for e in emotions) / total_frames
    
    return {
        'total_frames': total_frames,
        'emotion_frames': emotion_frames,
        'satisfaction_frames': satisfaction_frames,
        'dissatisfaction_frames': dissatisfaction_frames,
        'background_frames': background_frames,
        'avg_confidence': round(avg_confidence, 3)
    }

# CRUD para AnalysisResult
def create_analysis_result(db: Session, analysis_result: schemas.AnalysisResultCreate) -> models.AnalysisResult:
    db_result = models.AnalysisResult(
        session_id=analysis_result.session_id,
        approval_rate=analysis_result.approval_rate,
        interest_rate=analysis_result.interest_rate,
        total_frames=analysis_result.total_frames,
        emotion_frames=analysis_result.emotion_frames
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

def get_analysis_result_by_session(db: Session, session_id: int) -> Optional[models.AnalysisResult]:
    return db.query(models.AnalysisResult).filter(models.AnalysisResult.session_id == session_id).first()

def get_all_analysis_results(db: Session, skip: int = 0, limit: int = 100) -> List[models.AnalysisResult]:
    return db.query(models.AnalysisResult).order_by(desc(models.AnalysisResult.created_at)).offset(skip).limit(limit).all()

# Funções de análise e relatórios
def get_analytics_summary(db: Session, days: int = 30) -> dict:
    """Obtém resumo analítico dos últimos N dias"""
    start_date = datetime.now() - timedelta(days=days)
    
    # Estatísticas gerais
    total_sessions = db.query(models.Session).filter(
        models.Session.created_at >= start_date
    ).count()
    
    total_emotions = db.query(models.EmotionData).join(models.Session).filter(
        models.Session.created_at >= start_date
    ).count()
    
    # Médias de aprovação e interesse
    avg_approval = db.query(func.avg(models.AnalysisResult.approval_rate)).join(models.Session).filter(
        models.Session.created_at >= start_date
    ).scalar() or 0.0
    
    avg_interest = db.query(func.avg(models.AnalysisResult.interest_rate)).join(models.Session).filter(
        models.Session.created_at >= start_date
    ).scalar() or 0.0
    
    # Produtos mais analisados
    product_counts = db.query(
        models.Session.product_name,
        func.count(models.Session.id).label('count')
    ).filter(
        models.Session.created_at >= start_date
    ).group_by(models.Session.product_name).order_by(desc('count')).limit(10).all()
    
    sessions_by_product = {product: count for product, count in product_counts}
    
    return {
        'total_sessions': total_sessions,
        'total_emotions_analyzed': total_emotions,
        'average_approval_rate': round(avg_approval, 2),
        'average_interest_rate': round(avg_interest, 2),
        'sessions_by_product': sessions_by_product,
        'period_days': days
    }

def get_time_series_data(db: Session, days: int = 30) -> List[dict]:
    """Obtém dados de série temporal para visualizações"""
    start_date = datetime.now() - timedelta(days=days)
    
    # Agrupar por dia
    daily_stats = db.query(
        func.date(models.Session.created_at).label('date'),
        func.count(models.Session.id).label('sessions'),
        func.avg(models.AnalysisResult.approval_rate).label('avg_approval'),
        func.avg(models.AnalysisResult.interest_rate).label('avg_interest')
    ).join(models.AnalysisResult).filter(
        models.Session.created_at >= start_date
    ).group_by(func.date(models.Session.created_at)).order_by('date').all()
    
    return [
        {
            'date': str(stat.date),
            'sessions': stat.sessions,
            'avg_approval': round(stat.avg_approval or 0, 2),
            'avg_interest': round(stat.avg_interest or 0, 2)
        }
        for stat in daily_stats
    ]

def export_session_data(db: Session, session_id: int) -> pd.DataFrame:
    """Exporta dados de uma sessão para DataFrame"""
    emotions = get_emotion_data_by_session(db, session_id)
    session = get_session(db, session_id)
    
    if not session or not emotions:
        return pd.DataFrame()
    
    data = []
    for emotion in emotions:
        data.append({
            'timestamp': emotion.timestamp,
            'satisfaction_prob': emotion.satisfaction_prob,
            'dissatisfaction_prob': emotion.dissatisfaction_prob,
            'background_prob': emotion.background_prob,
            'predicted_class': emotion.predicted_class,
            'confidence': emotion.confidence
        })
    
    df = pd.DataFrame(data)
    df['session_id'] = session_id
    df['product_name'] = session.product_name
    df['duration_seconds'] = session.duration_seconds
    
    return df
