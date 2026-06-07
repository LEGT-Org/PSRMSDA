const routes = [
    
    /* 
        Authentication View
    */
    
    {
        path: '/',
        name: 'Login',
        component: () => import('@/views/LoginView.vue')
    },

    /* 
        Core Staff View and Components
    */

    {
        path: '/dashboard',
        name: 'Staff View',
        component: () => import('@/views/StaffView.vue'),
        children: [
            {
                path: '',
                name: 'Staff Dashboard',
                component: () => import('@/components/Staff/DashboardComponent.vue')
            },
            {
                path: '/requests',
                name: 'Staff Service Requests',
                component: () => import('@/components/Staff/ServReqComponent.vue')
            },
            {
                path: '/request/new',
                name: 'Staff New Service Request',
                component: () => import('@/components/Staff/NewServReqComponent.vue')
            },
        ]
    }
];

export default routes;