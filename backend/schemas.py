from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    correo: EmailStr
    contrasena: str

class TokenResponse(BaseModel):
    mensaje: str
    rol: str
    usuario: str
##
class ClienteBase(BaseModel):
    ruc_dni: str
    razon_social: str
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    direccion: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id_cliente: int

    class Config:
        from_attributes = True