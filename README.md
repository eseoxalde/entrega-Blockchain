# entrega-Blockchain

Ejercicio 4 de la práctica 3

## Autor

- **Nombre:** Ese
- **Apellido:** Oxalde
- **Legajo:** 05947/0

# Lista de Tareas con Prioridad (ToDoList)

## Descripción

Este proyecto implementa un **contrato inteligente en Solidity** (`ToDoList`) que permite a cada usuario:

- Agregar tareas con título y prioridad (1 a 5).
- Actualizar tareas (título y prioridad).
- Cambiar el estado de la tarea: `Pending`, `InProgress` o `Completed`.
- Eliminar tareas.
- Consultar tareas de forma **paginada** con filtros opcionales por prioridad y estado.
- Escuchar eventos: `TaskAdded`, `TaskUpdated`, `TaskDeleted`, `TaskStatusChanged`.

El proyecto incluye un script Python (`todo_list_interact.py`) que interactúa con el contrato usando **Web3.py**, permitiendo ejecutar todas las operaciones mencionadas desde Python.

---

## Contenido del repositorio

- `ToDoList.sol` – Contrato inteligente en Solidity.
- `ToDoList.json` – ABI generado al compilar el contrato (desde Remix o Hardhat/Truffle).
- `todo_list_interact.py` – Script Python para interactuar con el contrato.
- `.gitignore` – Ignora archivos sensibles como `.env`.
- `README.md` – Este archivo.

---

## Configuración del archivo `.env`

Para conectar el script Python al contrato desplegado y usar tu cuenta local, crea un archivo `.env` en la raíz del proyecto con estas variables:

NODE=http://127.0.0.1:8545
CONTRACT_ADDRESS=0xTU_CONTRATO_DESPLEGADO
PRIVATE_KEY=0xTU_CLAVE_PRIVADA

**Notas importantes:**

- Cada persona que reciba el proyecto debe crear su propio `.env` con sus datos de prueba.
- La variable `PRIVATE_KEY` debe corresponder a una cuenta con fondos de prueba si usás testnets como Sepolia o Ganache.

## Uso del script Python

1. Activar entorno virtual:
   source venv/bin/activate

2. Instalar dependencias:
   pip install -r requirements.txt
   (Debe incluir al menos web3 y python-dotenv)

3. Configurar .env como se indicó arriba.

4. Ejecutar el script:
   python3 todo_list_interact.py

## El script realiza:

- Listado inicial de tareas (getTasks).
- Agrega una tarea de ejemplo.
- Actualiza la tarea.
- Cambia su estado a Completed.
- Elimina otra tarea de ejemplo.
- Muestra en consola cada acción con su hash de transacción.

## Ejemplo de salida

Conectado al nodo: http://127.0.0.1:8545
Dirección del contrato cargada: 0x821db3e14be1C77cA8abAbe58f69c6CC2150b90F
Cuenta: 0x5be1808b9c7C7Ac767666a7a29D1fFb555B67840
Tareas paginadas: []
Tarea 'Estudiar Blockchain' agregada, TX: 0xcc799f...
Tarea 1 actualizada, TX: 0xfbf410...
Estado tarea 1 cambiado a Completed, TX: 0xd8f150...
Tarea 2 eliminada, TX: 0xc58fc1..

## Despliegue y pruebas en Remix

Abrir Remix
Crear un nuevo archivo ToDoList.sol y pegar el código del contrato.
Seleccionar Solidity Compiler, versión ^0.8.20 y compilar el contrato.
Ir a Deploy & Run Transactions:
Elegir el ambiente JavaScript VM para pruebas locales o Injected Web3 para red de prueba.
Desplegar el contrato.
El contrato desplegado genera una dirección y un ABI, que se exporta como ToDoList.json.
Con el ABI y la dirección, se puede conectar desde Python (todo_list_interact.py) usando Web3.py.
Se pueden ejecutr las funciones de lectura y escritura y verificar los eventos.

Nota: Para pruebas, se recomienda usar cuentas locales de Ganache o Sepolia. La dirección del contrato y la clave privada se configuran en .env.

## Consideraciones

getTasks soporta 4 parámetros: offset, limit, priorityFilter, statusFilter.
La interacción con Web3.py 6+ requiere usar signed.raw_transaction al enviar transacciones.
La paginación permite consultar lotes de tareas y aplicar filtros sin descargar toda la lista del usuario.
El script Python incluye flujo completo: agregar, actualizar, cambiar estado y eliminar tareas, mostrando los resultados en consola.
