# backend/app/modules/gerador_quesitos/v1/esquemas.py
from pydantic import BaseModel, Field

class RespostaQuesitos(BaseModel):
    """Schema para a resposta contendo os quesitos gerados."""
    quesitos_texto: str = Field(..., description="O texto formatado contendo os quesitos gerados pela IA.")

class GerarQuesitosComDocIdPayload(BaseModel):
    document_id: int
    beneficio: str
    profissao: str
    modelo_nome: str

# Add other relevant schemas for this module later if needed