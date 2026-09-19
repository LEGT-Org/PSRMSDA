import { accessToken } from "@/services/state/Auth";

const API_URL = import.meta.env.VITE_API_URL;


export async function ApiFetch<T>(
    endpoint: string,
    options: RequestInit = {}
): Promise<Response> {

    const headers = new Headers(options.headers);

    headers.set('Content-Type', 'application/json');
    headers.set('Accept', 'application/json');

    if (accessToken.value) {

        headers.set('Authorization', `Bearer ${accessToken.value}`);

    }

    return await fetch(`${API_URL}${endpoint}`, {
        
        ...options,
        headers,
        credentials: 'include'

    });
    
}