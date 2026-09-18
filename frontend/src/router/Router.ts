import { createRouter, createWebHistory } from 'vue-router';
import routes from './Routes';

interface User {
    id: number
    first_name: string
    last_name: string
    email: string
    role: string
}


async function getCurrentUser(): Promise<User | null> {
    const token = localStorage.getItem('xx-do-you-know-it');

    if (!token) {
        return null;
    }

    const res = await fetch('http://127.0.0.1:8000/auth/me', {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })

    if (!res.ok) {
        return null;
    }

    return await res.json();
}


// Router

const router = createRouter(
    {
        history: createWebHistory(import.meta.env.BASE_URL),
        routes,
    }
);


// Middleware

router.beforeEach( async (to) => 
    {
        const defaultTitle = 'Lightyear Electrical Goods Trading';

        document.title = to.meta?.title || defaultTitle;

        const user = await getCurrentUser();

        if (to.meta.requiresAuth && !user) {
            return '/';
        }

        if (to.meta.requiresGuest && user) {
            return '/dashboard';
        }

        return true;
    }
);


export default router;
