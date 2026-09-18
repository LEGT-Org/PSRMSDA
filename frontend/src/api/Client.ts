const API_URL = import.meta.env.VITE_API_URL;


export async function ApiFetch<T>(
    endpoint: string,
    options: RequestInit = {}
): Promise<Response> {

    const token = localStorage.getItem(`${import.meta.env.VITE_ACCESS_TOKEN}`);

    return await fetch(`${API_URL}${endpoint}`, {
        
        ...options,

        headers: {

            'Content-Type': 'application/json',
            'Accept': 'application/json',
            
            ...(token
                ? { Authorization: `Bearer ${token}` }
                : {}
            ),

            ...options.headers

        }

    });
    
}