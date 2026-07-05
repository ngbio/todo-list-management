import axios from "axios";

export const endpoints = {
    todos: "/todos",
    todoDetail: id => `/todos/${id}`,
    toggleTodo: id => `/todos/${id}/toggle`,
    health: "/health",
    login: "/login",
    logout: "/logout",
    register: "/register",
    profile: "/profile",
};

export default axios.create({
    baseURL: process.env.REACT_APP_API_BASE_URL || "http://localhost:5000/api",
    withCredentials: true,
});
