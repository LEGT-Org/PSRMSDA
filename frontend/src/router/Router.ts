import { createRouter, createWebHistory } from 'vue-router';
import routes from './Routes';


// Router

const router = createRouter(
    {
        history: createWebHistory(import.meta.env.BASE_URL),
        routes,
    }
);


// Middleware

router.beforeEach((to,_from) => 
    {
        const defaultTitle = 'Lightyear Electrical Goods Trading';

        document.title = to.meta?.title || defaultTitle;
    }
);

export default router;
