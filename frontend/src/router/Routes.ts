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
    },

    /* 
        Core Admin Views and Components
    */
    
    {
        path: '/admin',
        name: 'Admin View',
        component: () => import('@/views/AdminView.vue'),
        children: [
            {
                path: '',
                name: 'Admin Dashboard',
                component: () => import('@/components/Admin/DashboardComponent.vue')
            },
            {
                path: 'requests',
                name: 'Admin Service Request',
                component: () => import('@/components/Admin/ServReqComponent.vue')
            },
            {
                path: 'request/new',
                name: 'Admin New Service Request',
                component: () => import('@/components/Admin/NewServReqComponent.vue')
            },
            {
                path: 'diagnostics',
                name: 'Admin Diagnostic Rules',
                component: () => import('@/components/Admin/DiagRulesComponent.vue')
            },
            {
                path: 'sops',
                name: 'Admin Standard Operational Procedure',
                component: () => import('@/components/Admin/StanOpeProdComponent.vue')
            },
            {
                path: 'alerts',
                name: 'Admin Procurement Alerts',
                component: () => import('@/components/Admin/AlertsComponent.vue')
            },
            {
                path: 'inventory',
                name: 'Admin Inventory Reference',
                component: () => import('@/components/Admin/InvRefComponent.vue')
            },
            {
                path: 'reports',
                name: 'Admin Reports',
                component: () => import('@/components/Admin/ReportsComponent.vue')
            },
            {
                path: 'users',
                name: 'Admin Users',
                component: () => import('@/components/Admin/UsersComponent.vue')
            },
        ]
    }
];

export default routes;