######################################################################
# Nombre: [Ese]
# Apellido: [Oxalde]
# Legajo: [05947/0]
#####################################################################
# 4- Lista de Tareas con Prioridad
# Requerimientos:
# a) Leer: obtener todas las tareas o filtrarlas por prioridad o estado.
# b) Escribir: agregar, actualizar o eliminar tareas.
# c) Escuchar eventos de tareas (TaskAdded, TaskUpdated, TaskDeleted,
# TaskStatusChanged).
# d) Implementar la consulta paginada con parámetros offset y limit.
######################################################################

###################################################################
# todo_list_interact.py
# Interacción con el contrato ToDoList
###################################################################
from web3 import Web3
from enum import IntEnum
import json, os, time
from dotenv import load_dotenv

load_dotenv()

# -----------------------
# Conexión al nodo
# -----------------------
NODE = os.getenv("NODE", "http://127.0.0.1:8545")  # Sepolia o Ganache
w3 = Web3(Web3.HTTPProvider(NODE))
assert w3.is_connected(), "No se pudo conectar al nodo"
print("Conectado al nodo:", NODE)

# -----------------------
# Cargar ABI y dirección del contrato
# -----------------------
with open("ToDoList.json") as f:
    contract_data = json.load(f)

abi = contract_data.get("abi", contract_data)
contract_address = os.getenv("CONTRACT_ADDRESS", "0xTU_CONTRATO_DESPLEGADO")
print("Dirección del contrato cargada:", contract_address)

contract = w3.eth.contract(address=contract_address, abi=abi)

# -----------------------
# Cuenta local (owner)
# -----------------------
private_key = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(private_key)
print("Cuenta:", account.address)


# -----------------------
# Enumeración TaskStatus
# -----------------------
class TaskStatus(IntEnum):
    Pending = 0
    InProgress = 1
    Completed = 2


# -----------------------
# Funciones de lectura
# -----------------------
def obtener_tareas(offset=0, limit=10, prioridad=None, estado=None):
    """
    Devuelve tareas filtradas por prioridad, estado y paginadas.
    """
    prioridad_filter = prioridad if prioridad is not None else 0
    estado_filter = estado if estado is not None else 0  # 0 = ignorar filtro

    tareas = contract.functions.getTasks(
        offset, limit, prioridad_filter, estado_filter
    ).call()

    filtradas = []
    for t in tareas:
        t_id, t_title, t_priority, t_status, t_createdAt = t
        filtradas.append(
            {
                "id": t_id,
                "nombre": t_title,
                "prioridad": t_priority,
                "estado": TaskStatus(t_status).name,
                "creada": t_createdAt,
            }
        )
    return filtradas


# -----------------------
# Funciones de escritura
# -----------------------
def enviar_tx(tx):
    """
    Firma y envía la transacción, devuelve el hash.
    """
    signed = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    return w3.to_hex(tx_hash)


def agregar_tarea(nombre, prioridad):
    tx = contract.functions.addTask(nombre, prioridad).build_transaction(
        {
            "from": account.address,
            "gas": 200000,
            "gasPrice": w3.eth.gas_price,
            "nonce": w3.eth.get_transaction_count(account.address),
        }
    )
    tx_hash = enviar_tx(tx)
    print(f"Tarea '{nombre}' agregada, TX:", tx_hash)


def actualizar_tarea(task_id, nombre=None, prioridad=None):
    tx = contract.functions.updateTask(
        task_id, nombre or "", prioridad or 1  # prioridad mínima 1
    ).build_transaction(
        {
            "from": account.address,
            "gas": 200000,
            "gasPrice": w3.eth.gas_price,
            "nonce": w3.eth.get_transaction_count(account.address),
        }
    )
    tx_hash = enviar_tx(tx)
    print(f"Tarea {task_id} actualizada, TX:", tx_hash)


def eliminar_tarea(task_id):
    tx = contract.functions.deleteTask(task_id).build_transaction(
        {
            "from": account.address,
            "gas": 200000,
            "gasPrice": w3.eth.gas_price,
            "nonce": w3.eth.get_transaction_count(account.address),
        }
    )
    tx_hash = enviar_tx(tx)
    print(f"Tarea {task_id} eliminada, TX:", tx_hash)


def cambiar_estado(task_id, nuevo_estado):
    """
    nuevo_estado: puede ser TaskStatus.Pending/InProgress/Completed o int 0/1/2
    """
    if isinstance(nuevo_estado, TaskStatus):
        estado_val = int(nuevo_estado)
    else:
        estado_val = int(nuevo_estado)

    tx = contract.functions.changeStatus(task_id, estado_val).build_transaction(
        {
            "from": account.address,
            "gas": 200000,
            "gasPrice": w3.eth.gas_price,
            "nonce": w3.eth.get_transaction_count(account.address),
        }
    )
    tx_hash = enviar_tx(tx)
    print(
        f"Estado tarea {task_id} cambiado a {TaskStatus(estado_val).name}, TX:", tx_hash
    )


# -----------------------
# Escuchar eventos
# -----------------------
def escuchar_eventos():
    filters = [
        contract.events.TaskAdded.createFilter(fromBlock="latest"),
        contract.events.TaskUpdated.createFilter(fromBlock="latest"),
        contract.events.TaskDeleted.createFilter(fromBlock="latest"),
        contract.events.TaskStatusChanged.createFilter(fromBlock="latest"),
    ]
    print("Escuchando eventos de tareas...")
    while True:
        for f in filters:
            for event in f.get_new_entries():
                print("Evento:", event.event, event.args)
        time.sleep(2)


# -----------------------
# Ejemplo de uso
# -----------------------
if __name__ == "__main__":
    print("\n--- Estado inicial de tareas ---")
    tareas = obtener_tareas(offset=0, limit=10)
    for t in tareas:
        print(t)

    # Agregar tarea
    print("\n--- Agregando tarea 'Estudiar', prioridad 2 ---")
    agregar_tarea("Estudiar ", 2)

    print("\n--- Estado de tareas después de agregar ---")
    tareas = obtener_tareas(offset=0, limit=10)
    for t in tareas:
        print(t)

    # Actualizar tarea
    print("\n--- Actualizando tarea 1 ---")
    actualizar_tarea(1, nombre="Estudiar Python", prioridad=3)

    print("\n--- Estado de tareas después de actualizar ---")
    tareas = obtener_tareas(offset=0, limit=10)
    for t in tareas:
        print(t)

    # Cambiar estado a completada
    print("\n--- Cambiando estado de tarea 1 a Completed ---")
    cambiar_estado(1, TaskStatus.Completed)

    print("\n--- Estado de tareas después de cambiar estado ---")
    tareas = obtener_tareas(offset=0, limit=10)
    for t in tareas:
        print(t)

    # Agregar otra tarea para probar eliminación
    print("\n--- Agregando tarea 'Hacer ejercicio', prioridad 1 ---")
    agregar_tarea("Hacer ejercicio", 1)

    print("\n--- Estado de tareas antes de eliminar ---")
    tareas = obtener_tareas(offset=0, limit=10)
    for t in tareas:
        print(t)

    # Eliminar tarea 2
    print("\n--- Eliminando tarea 2 ---")
    eliminar_tarea(2)

    print("\n--- Estado de tareas después de eliminar ---")
    tareas = obtener_tareas(offset=0, limit=10)
    for t in tareas:
        print(t)
