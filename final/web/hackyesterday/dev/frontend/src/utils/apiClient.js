import axios from 'axios';


const getToken = () => {
    return localStorage.getItem("token");
};

const setToken = (token) => {
    localStorage.setItem("token", token);
};

const removeToken = () => {
    localStorage.removeItem("token");
};

const isLogged = () => {
    try {
        const token = getToken();
        const tokenPayload = JSON.parse(atob(token.split('.')[1]));
        const expirationDate = new Date(tokenPayload.exp * 1000);
    
        return new Date() <= expirationDate;
    } catch (error) {}
    return false;
};

const isAdmin = () => {
    if (!isLogged()) return false;
    try {
        const token = getToken();
        const tokenPayload = JSON.parse(atob(token.split('.')[1]));
        return tokenPayload.is_admin;
    } catch (error) {}
    return false;
};

const apiClient = axios.create({
    baseURL: '/api/',
    headers: {
        'Content-Type': 'application/json',
    },
});

apiClient.interceptors.request.use(
    (config) => {
        const token = getToken();
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);
  

export { apiClient, setToken, removeToken, isLogged, isAdmin };
export default apiClient;