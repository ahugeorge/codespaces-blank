from fastapi.testclient import TestClient
from main import app

cliente = TestClient(app)


def test_crear_y_listar():
    respuesta = cliente.post("/tareas", json={"titulo": "Estudiar FastAPI"})
    assert respuesta.status_code == 201
    tarea = respuesta.json()
    assert tarea["titulo"] == "Estudiar FastAPI"
    assert tarea["hecha"] is False
    lista = cliente.get("/tareas").json()
    assert tarea in lista


def test_obtener_tarea_existente():
    creada = cliente.post("/tareas", json={"titulo": "Leer documentación"}).json()

    respuesta = cliente.get(f"/tareas/{creada['id']}")

    assert respuesta.status_code == 200
    assert respuesta.json() == creada


def test_obtener_tarea_inexistente():
    respuesta = cliente.get("/tareas/-1")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Tarea no encontrada"}
