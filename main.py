
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Crear la aplicación
app = FastAPI(title="API de tareas")


# Modelo para crear una tarea
class TareaNueva(BaseModel):
    titulo: str
    hecha: bool = False


# Modelo completo de una tarea
class Tarea(TareaNueva):
    id: int


# Almacenar las tareas
tareas: dict[int, Tarea] = {}

# Identificador de la siguiente tarea
siguiente_id = 1


# Consultar todas las tareas
@app.get("/tareas")
def listar() -> list[Tarea]:
    return list(tareas.values())


# Consultar una tarea por su identificador
@app.get("/tareas/{id}")
def obtener(id: int) -> Tarea:
    tarea = tareas.get(id)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    return tarea


# Crear una nueva tarea
@app.post("/tareas", status_code=201)
def crear(datos: TareaNueva) -> Tarea:
    global siguiente_id

    tarea = Tarea(
        id=siguiente_id,
        **datos.model_dump()
    )

    tareas[tarea.id] = tarea

    siguiente_id += 1

    return tarea
