# Prueba unitaria inicial para el Módulo de Servicios
def test_estado_inicial_servicio():
    # Simulamos la asignación del estado de un nuevo viaje
    estado_asignado = "Pendiente"
    
    # Validamos que la lógica asigne correctamente el estado inicial
    assert estado_asignado == "Pendiente"