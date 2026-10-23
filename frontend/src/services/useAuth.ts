import { ApiFetch } from "@/api/Client";
import { HandleApiError } from "@/api/Error";

import { 
    currentUser, 
    accessToken, 
    isLoading, 
    isFetched, 
    Error,

    type User 
} from "./state/Auth";
import Swal from "sweetalert2";
import { HandleSuccess } from "@/helper/HandleSuccess";


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

        const res = await ApiFetch('/user/me', { method: 'GET' });

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

    } catch(error) {

        await Swal.fire({
            title: 'Connection Error!',
            text: 'Unable to connect to the server. Please try again later.',
            icon: 'error',
        });

        return;

    } finally {

        isLoading.value = false;
    
    }
}


// Reset User Password

export async function resetPassword(
    Email: string
): Promise<{ ok: true } | { ok: false; message: string }> {

    isLoading.value = true;
    Error.value = '';

    try {

        const res = await ApiFetch('/auth/reset-password', {
            method: 'POST',
            body: JSON.stringify(
                {
                    reset_password_email: Email.trim()
                }
            )

        });

        const data = await res.json()

        if (!res.ok) { 
            
            const message = data.detail ?? 'Invalid email or password';
            Error.value = message;
            
            return { ok: false, message };

        }

        return { ok: true };

    } catch(error) {

        await Swal.fire({
            title: 'Connection Error!',
            text: 'Unable to connect to the server. Please try again later.',
            icon: 'error',
        });

        return { ok: false, message: 'Connection error' };

    } finally {

        isLoading.value = false;

    }

}


// Registration Set My Password

export async function setPassword(
    Token: string | null,
    Password: string,
    ConfirmPassword: string
) {

    isLoading.value = true;

    try {

        if (Password !== ConfirmPassword) {

            Error.value = 'Passwords do not match';
            return Error.value;

        }

        const res = await ApiFetch('/auth/set-password', {

            method: 'POST',
            body: JSON.stringify(
                {
                    token: Token,
                    password: Password,
                    confirm_password: ConfirmPassword,
                }
            ),

        });

        const data = await res.json();

        if (!res.ok) {

            Error.value = data.detail ?? 'Unable to set password';
            return Error.value;

        }

        return null;

    } catch (error) {

        await Swal.fire({
            title: 'Connection Error!',
            text: 'Unable to connect to the server. Please try again later.',
            icon: 'error',
        });

        return;

    } finally {

        isLoading.value = false;

    }
}


// This is for Refresh Token

let RefreshTimer: ReturnType<typeof setTimeout> | null = null;

const ScheduleTokenRefresh = (): void => {
    if (RefreshTimer !== null) {
        clearTimeout(RefreshTimer);
    }

    RefreshTimer = setTimeout(async () => {
        const success = await RestoreSession();

        if (!success) {
            return;
        }

        ScheduleTokenRefresh();
    }, 15 * 60 * 1000);
};

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

        ScheduleTokenRefresh();

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

            await HandleApiError(
                res,
                'Failed to logout'
            );

        }

    } finally {

        await ClearAuthCache();

    }

}

