from sqlalchemy import Column, Integer, String, Boolean, Text, Date, ForeignKey, Enum
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contrasena_hash = Column(String(255), nullable=False)
    rol = Column(String(50), default="Operador")
    estado = Column(Boolean, default=True)

class Cliente(Base):
    __tablename__ = "clientes"
    id_cliente = Column(Integer, primary_key=True, index=True)
    ruc_dni = Column(String(11), unique=True, nullable=False)
    razon_social = Column(String(150), nullable=False)
    telefono = Column(String(20))
    correo = Column(String(100))
    direccion = Column(String(255))

class ServicioTransporte(Base):
    __tablename__ = "servicios_transporte"
    id_servicio = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    origen = Column(String(150), nullable=False)
    destino = Column(String(150), nullable=False)
    descripcion_carga = Column(Text, nullable=False)
    estado = Column(Enum('Pendiente', 'En Proceso', 'Completado'), default='Pendiente')
    fecha_programada = Column(Date, nullable=False)