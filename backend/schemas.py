from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

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
##
class ServicioBase(BaseModel):
    id_cliente: int
    origen: str
    destino: str
    descripcion_carga: str
    estado: str = "Pendiente"
    fecha_programada: date

class ServicioCreate(ServicioBase):
    pass

class ServicioResponse(ServicioBase):
    id_servicio: int

    class Config:
        from_attributes = True

##
class DashboardResponse(BaseModel):
    total_servicios: int
    pendientes: int
    en_proceso: int
    completados: int