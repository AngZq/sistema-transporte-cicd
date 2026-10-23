import hashlib
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import engine, Base, get_db
from backend import models, schemas

# Crear las tablas en Python si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API EXPORTRONIC S.A.C.")

# Función para comparar la contraseña encriptada (SHA-256)
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

@app.post("/login", response_model=schemas.TokenResponse)
def login(credenciales: schemas.LoginRequest, db: Session = Depends(get_db)):
    # Buscar al usuario en la base de datos de EXPORTRONIC
    usuario = db.query(models.Usuario).filter(models.Usuario.correo == credenciales.correo).first()
    
    # Validar si el usuario existe y la contraseña es correcta
    if not usuario or usuario.contrasena_hash != hash_password(credenciales.contrasena):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    
    if not usuario.estado:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    return {"mensaje": "Login exitoso", "rol": usuario.rol, "usuario": usuario.nombre_usuario}

#
@app.post("/clientes", response_model=schemas.ClienteResponse)
def registrar_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    # Verificar si el RUC/DNI ya existe
    cliente_existente = db.query(models.Cliente).filter(models.Cliente.ruc_dni == cliente.ruc_dni).first()
    if cliente_existente:
        raise HTTPException(status_code=400, detail="El RUC o DNI ya está registrado en el sistema")
    
    # Guardar en base de datos
    nuevo_cliente = models.Cliente(**cliente.model_dump())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente

@app.get("/clientes", response_model=list[schemas.ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    # Devolver todos los clientes
    return db.query(models.Cliente).all()

@app.delete("/clientes/{id_cliente}")
def eliminar_cliente(id_cliente: int, db: Session = Depends(get_db)):
    # Buscar y eliminar
    cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    db.delete(cliente)
    db.commit()
    return {"mensaje": f"Cliente {cliente.razon_social} eliminado correctamente"}

##
@app.post("/servicios", response_model=schemas.ServicioResponse)
def registrar_servicio(servicio: schemas.ServicioCreate, db: Session = Depends(get_db)):
    # 1. Verificar que el cliente al que se le asigna el viaje realmente exista
    cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == servicio.id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Error: El cliente especificado no existe")
    
    # 2. Guardar el nuevo servicio en la base de datos
    nuevo_servicio = models.ServicioTransporte(**servicio.model_dump())
    db.add(nuevo_servicio)
    db.commit()
    db.refresh(nuevo_servicio)
    return nuevo_servicio

@app.get("/servicios", response_model=list[schemas.ServicioResponse])
def listar_servicios(db: Session = Depends(get_db)):
    # Devolver todo el historial de viajes
    return db.query(models.ServicioTransporte).all()

##
@app.get("/dashboard", response_model=schemas.DashboardResponse)
def obtener_estadisticas(db: Session = Depends(get_db)):
    # Realizamos consultas optimizadas para contar registros según su estado
    total = db.query(models.ServicioTransporte).count()
    pendientes = db.query(models.ServicioTransporte).filter(models.ServicioTransporte.estado == "Pendiente").count()
    en_proceso = db.query(models.ServicioTransporte).filter(models.ServicioTransporte.estado == "En Proceso").count()
    completados = db.query(models.ServicioTransporte).filter(models.ServicioTransporte.estado == "Completado").count()
    
    return {
        "total_servicios": total,
        "pendientes": pendientes,
        "en_proceso": en_proceso,
        "completados": completados
    }