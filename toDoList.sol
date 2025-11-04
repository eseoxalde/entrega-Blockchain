// SPDX-License-Identifier: MIT

// Nombre: [Ese]
// Apellido: [Oxalde]
// Legajo: [05947/0]
// Actividad 3 - Ejercicio 4: Lista de Tareas con Prioridad

pragma solidity ^0.8.20;

contract ToDoList {
    enum TaskStatus { Pending, InProgress, Completed }

    struct Task {
        uint id;
        string title;
        uint8 priority; // 1 a 5
        TaskStatus status;
        uint createdAt;
    }

    // Cada usuario tiene su propia lista de tareas
    mapping(address => Task[]) private userTasks;

    // Contador de IDs por usuario
    mapping(address => uint) private userTaskCount;

    // Eventos
    event TaskAdded(address indexed user, uint id, string title, uint8 priority);
    event TaskUpdated(address indexed user, uint id, string newTitle, uint8 newPriority);
    event TaskDeleted(address indexed user, uint id);
    event TaskStatusChanged(address indexed user, uint id, TaskStatus newStatus);

    // Agregar nueva tarea
    function addTask(string memory _title, uint8 _priority) public {
        require(_priority >= 1 && _priority <= 5, "Prioridad debe ser 1 a 5");

        uint newId = ++userTaskCount[msg.sender];
        userTasks[msg.sender].push(Task({
            id: newId,
            title: _title,
            priority: _priority,
            status: TaskStatus.Pending,
            createdAt: block.timestamp
        }));

        emit TaskAdded(msg.sender, newId, _title, _priority);
    }

    // Actualizar título o prioridad
    function updateTask(uint _id, string memory _newTitle, uint8 _newPriority) public {
        require(_newPriority >= 1 && _newPriority <= 5, "Prioridad debe ser 1 a 5");

        Task[] storage tasks = userTasks[msg.sender];
        for (uint i = 0; i < tasks.length; i++) {
            if (tasks[i].id == _id) {
                tasks[i].title = _newTitle;
                tasks[i].priority = _newPriority;
                emit TaskUpdated(msg.sender, _id, _newTitle, _newPriority);
                return;
            }
        }
        revert("Tarea no encontrada");
    }

    // Cambiar estado
    function changeStatus(uint _id, TaskStatus _newStatus) public {
        Task[] storage tasks = userTasks[msg.sender];
        for (uint i = 0; i < tasks.length; i++) {
            if (tasks[i].id == _id) {
                tasks[i].status = _newStatus;
                emit TaskStatusChanged(msg.sender, _id, _newStatus);
                return;
            }
        }
        revert("Tarea no encontrada");
    }

    // Eliminar tarea
    function deleteTask(uint _id) public {
        Task[] storage tasks = userTasks[msg.sender];
        for (uint i = 0; i < tasks.length; i++) {
            if (tasks[i].id == _id) {
                // Mover la última tarea al lugar de la eliminada para no dejar huecos
                tasks[i] = tasks[tasks.length - 1];
                tasks.pop();
                emit TaskDeleted(msg.sender, _id);
                return;
            }
        }
        revert("Tarea no encontrada");
    }

    // Listar tareas con filtros y paginación
    function getTasks(uint offset, uint limit, uint8 priorityFilter, TaskStatus statusFilter)
        public view returns (Task[] memory)
    {
        Task[] storage allTasks = userTasks[msg.sender];
        uint total = allTasks.length;
        uint end = offset + limit;
        if (end > total) end = total;

        // Contar cuántas cumplen el filtro
        uint count = 0;
        for (uint i = offset; i < end; i++) {
            if (
                (priorityFilter == 0 || allTasks[i].priority == priorityFilter) &&
                (uint(statusFilter) == 0 || allTasks[i].status == statusFilter)
            ) {
                count++;
            }
        }

        // Armar el array con las filtradas
        Task[] memory filtered = new Task[](count);
        uint j = 0;
        for (uint i = offset; i < end; i++) {
            if (
                (priorityFilter == 0 || allTasks[i].priority == priorityFilter) &&
                (uint(statusFilter) == 0 || allTasks[i].status == statusFilter)
            ) {
                filtered[j] = allTasks[i];
                j++;
            }
        }

        return filtered;
    }
}
