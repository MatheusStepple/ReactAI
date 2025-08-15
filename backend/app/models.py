from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    """Modelo para usuários do sistema"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    sessions = relationship("Session", back_populates="user")

class Session(Base):
    """Modelo para sessões de análise"""
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_name = Column(String)
    duration_seconds = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    user = relationship("User", back_populates="sessions")
    emotions = relationship("EmotionData", back_populates="session")

class EmotionData(Base):
    """Modelo para dados de emoções capturados"""
    __tablename__ = "emotion_data"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    satisfaction_prob = Column(Float)  # Probabilidade de satisfação
    dissatisfaction_prob = Column(Float)  # Probabilidade de insatisfação
    background_prob = Column(Float)  # Probabilidade de fundo/sem rosto
    predicted_class = Column(String)  # Classe prevista (satisfação, insatisfação, fundo)
    confidence = Column(Float)  # Confiança da predição
    
    # Relacionamentos
    session = relationship("Session", back_populates="emotions")

class AnalysisResult(Base):
    """Modelo para resultados consolidados de análise"""
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    approval_rate = Column(Float)  # Taxa de aprovação (%)
    interest_rate = Column(Float)  # Taxa de interesse (%)
    total_frames = Column(Integer)  # Total de frames processados
    emotion_frames = Column(Integer)  # Frames com emoção detectada
    created_at = Column(DateTime(timezone=True), server_default=func.now())
