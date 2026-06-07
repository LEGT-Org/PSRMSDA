const routes = [
    
    /* 
        Authentication View
    */
    
    {
        path: '/',
        name: 'Login',
        component: () => import('@/views/LoginView.vue')
    }
];

export default routes;