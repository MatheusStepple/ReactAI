from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Schemas para User
class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas para Session
class SessionBase(BaseModel):
    product_name: str
    duration_seconds: int

class SessionCreate(SessionBase):
    user_id: int

class Session(SessionBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas para EmotionData
class EmotionDataBase(BaseModel):
    satisfaction_prob: float
    dissatisfaction_prob: float
    background_prob: float
    predicted_class: str
    confidence: float

class EmotionDataCreate(EmotionDataBase):
    session_id: int

class EmotionData(EmotionDataBase):
    id: int
    session_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Schemas para AnalysisResult
class AnalysisResultBase(BaseModel):
    approval_rate: float
    interest_rate: float
    total_frames: int
    emotion_frames: int

class AnalysisResultCreate(AnalysisResultBase):
    session_id: int

class AnalysisResult(AnalysisResultBase):
    id: int
    session_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas para análise em tempo real
class RealTimeEmotion(BaseModel):
    satisfaction_prob: float
    dissatisfaction_prob: float
    background_prob: float
    predicted_class: str
    confidence: float

class SessionResult(BaseModel):
    session: Session
    analysis_result: AnalysisResult
    emotion_count: int

# Schemas para relatórios
class ReportData(BaseModel):
    total_sessions: int
    average_approval_rate: float
    average_interest_rate: float
    total_emotions_analyzed: int
    sessions_by_product: dict
    time_series_data: List[dict]
