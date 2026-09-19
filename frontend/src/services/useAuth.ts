import { ApiFetch } from "@/api/Client";

import { 
    currentUser, 
    accessToken, 
    isLoading, 
    isFetched, 
    Error,

    type User 
} from "./state/Auth";


// Fetching the User

export async function getCurrentUser(force: boolean = false): Promise<User | null> {

    if (!accessToken.value) {

        currentUser.value = null;
        isFetched.value = true;
        return null;

    }

    if (isFetched.value && !force) {

        return currentUser.value;

    }

    try {

        const res = await ApiFetch('/auth/me', { method: 'GET' });

        if (!res.ok) {

            accessToken.value = null;
            currentUser.value = null;
            return null;

        } 
        
        currentUser.value = await res.json();

    } catch(error) {

        currentUser.value = null;

    } finally {

        isFetched.value = true;

    }

    return currentUser.value;

}


// Login Logic

export async function login(Email: string, Password: string) {

    isLoading.value = true;

    try {

        const res = await ApiFetch('/auth/login', {

            method: 'POST',
            body: JSON.stringify(
                {
                    email: Email.trim(),
                    password: Password
                }
            )

        });

        const data = await res.json();

        if (!res.ok) { 

            Error.value = data.detail ?? 'Invalid email or password';
            return Error.value;
        }

        accessToken.value = data.access_token;
        await getCurrentUser(true);

        return true;

    } catch(err) {

        console.error('Login error', err);
        alert('Unable to connect to the server. Please try again later');

    } finally {

        isLoading.value = false;
    
    }
}


// This is for Refresh Token

export async function RestoreSession() {
    
    try {

        const res = await ApiFetch('/auth/refresh', { method: 'POST' });
        const data = await res.json();

        if (!res.ok) {

            currentUser.value = null;
            accessToken.value = null;
            isFetched.value = true;

            return false;

        }

        accessToken.value = data.access_token;

        await getCurrentUser(true);

        return true;
        
    } catch {

        currentUser.value = null;
        accessToken.value = null;
        isFetched.value = true;
        return false;

    }

}


// Clear The User Cache (Mostly use for logout)

export async function ClearAuthCache() {

    currentUser.value = null;
    accessToken.value = null;
    isFetched.value = false;

}


// This is for logout and revoking refresh_token

export async function logout() {

    try {

        const res = await ApiFetch('/auth/revoke', { method: 'POST' });
        const data = await res.json();

        if (!res.ok) {

            alert(data.detail);

        }

    } finally {

        await ClearAuthCache();

    }

}

