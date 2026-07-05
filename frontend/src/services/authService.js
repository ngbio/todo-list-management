import Apis, { endpoints } from "../configs/Apis";

export function login(payload) {
    return Apis.post(endpoints.login, payload);
}

export function register(payload) {
    return Apis.post(endpoints.register, payload);
}

export function logout() {
    return Apis.post(endpoints.logout);
}

export function getProfile() {
    return Apis.get(endpoints.profile);
}
