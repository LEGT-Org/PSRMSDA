import { accessToken } from "@/services/state/Auth";
import { getCSRFToken } from "./CSRF";

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

    const csrfToken = getCSRFToken();

    if (
        csrfToken && ['POST', 'PUT', 'PATCH', 'DELETE'].includes(
            (options.method ?? 'GET').toUpperCase()
        )
    ) {

        headers.set('X-CSRF-Token', csrfToken);
        console.log('CSRF header:', headers.get('X-CSRF-Token'));

    }

    return await fetch(`${API_URL}${endpoint}`, {
        
        ...options,
        headers,
        credentials: 'include'

    });
    
}