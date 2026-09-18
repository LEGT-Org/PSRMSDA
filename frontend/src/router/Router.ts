import { createRouter, createWebHistory } from 'vue-router';
import routes from './Routes';

import { getCurrentUser } from '@/services/useAuth';


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
            return user.role === 'admin' ? '/admin' : '/dashboard';
        }

        if (to.meta.requiresAdmin) {
            if (!user) return '/';
            if (user.role !== 'admin') return '/dashboard';
        }

        if (to.meta.requiresStaff) {
            if (!user) return '/';
            if (user.role !== 'staff') return user.role === 'admin' ? '/admin' : '/';
        }

        return true;
    }
);


export default router;
