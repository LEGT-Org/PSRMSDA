import { ref } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';

import routes from './Routes';
import { RestoreSession, getCurrentUser } from '@/services/useAuth';
import { currentUser, isFetched, isCSRFInitialized } from '@/services/state/Auth';
import { getCSRFTokenFromServer } from '@/api/CSRF';


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
        
        // CSRF Middleware

        if (!isCSRFInitialized.value) {

            const csrfResponse = await getCSRFTokenFromServer();

            if (!csrfResponse.ok) {

                const data = await csrfResponse.json();
                alert(data.detail);
                return;

            }

            isCSRFInitialized.value = true;
            
        }


        // Refresh Token Middleware

        if (!isFetched.value) {

            await RestoreSession();

        }

        console.log({
            path: to.path,
            matchedRoute: to.matched.length,
            routeName: to.name,
            role: currentUser.value?.role,
            requiresStaff: to.meta.requiresStaff,
        });
                
        
        // Allowed Routes Middleware
        
        const user = currentUser.value;

        if (to.meta.requiresToken) {
            const token = to.query.token;

            if (!token || typeof token !== 'string') {
                return { name: "NotFound" };
            }

            return true  
        }

        
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
            if (user.role !== 'user') return user.role === 'admin' ? '/admin' : '/';

        }

        return true;
    }
);


export default router;
