import { ApiFetch } from "./Client";


export async function getCSRFTokenFromServer() {

    return await ApiFetch('/auth/csrf', { method: 'GET' });

}


export function getCSRFToken(): string | null {

    const match = document.cookie.match(/(?:^|; )csrf_token=([^;]*)/);

    return match?.[1]
        ? decodeURIComponent(match[1])
        : null;

} 