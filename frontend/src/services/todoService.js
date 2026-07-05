import Apis, { endpoints } from "../configs/Apis";

export function getTodos(params) {
    return Apis.get(endpoints.todos, { params });
}

export function createTodo(payload) {
    return Apis.post(endpoints.todos, payload);
}

export function updateTodo(id, payload) {
    return Apis.put(endpoints.todoDetail(id), payload);
}

export function toggleTodo(id) {
    return Apis.patch(endpoints.toggleTodo(id));
}

export function deleteTodo(id) {
    return Apis.delete(endpoints.todoDetail(id));
}
