import hashlib
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models, schemas

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