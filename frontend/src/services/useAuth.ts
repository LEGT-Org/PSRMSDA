import { ref } from "vue";
import { ApiFetch } from "@/api/Client";


interface User {
    id: number
    first_name: string
    last_name: string
    email: string
    role: string
}


const Error     = ref<string>('');
const isLoading = ref<boolean>(false);

const currentUser = ref<User | null>(null);
const isFetched   = ref(false);


// Fetching the User

export async function getCurrentUser(force: boolean = false): Promise<User | null> {

    const token = localStorage.getItem(`${import.meta.env.VITE_ACCESS_TOKEN}`);

    if (!token) {

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

            localStorage.removeItem(`${import.meta.env.VITE_ACCESS_TOKEN}`);
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

            return {

                success: false,
                error: Error.value,
                
            };

        }

        localStorage.setItem(`${import.meta.env.VITE_ACCESS_TOKEN}`, data.access_token);

        return {

            success: true,
            error: null,

        }
        
    } catch(err) {

        console.error('Login error', err);
        alert('Unable to connect to the server. Please try again later');

        return {

            success: false,
            error: null,

        };

    } finally {

        isLoading.value = false;
    
    }
}


// Clear The User Cache (Mostly use for logout)

export function clearAuthCache() {

    currentUser.value = null;
    isFetched.value = false;
    localStorage.removeItem(`${import.meta.env.VITE_ACCESS_TOKEN}`);

}

