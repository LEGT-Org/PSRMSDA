declare module 'vue-router' {
    interface RouteMeta {
        title?:         string;
        requiresAuth?:  boolean;
    }
}


// Routes

const routes = [
    
    /* 
        Authentication View
    */
    
    {
        path: '/',
        name: 'Login',
        component: () => import('@/views/LoginView.vue'),
        meta: {
            title: 'Lightyear Electrical Goods Trading'
        }
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
                component: () => import('@/components/Staff/DashboardComponent.vue'),
                meta: {
                    requiresAuth: true,
                    title: 'Dashboard'
                }
            },
            {
                path: '/requests',
                name: 'Staff Service Requests',
                component: () => import('@/components/Staff/ServReqComponent.vue'),
                meta: {
                    requiresAuth: true,
                    title: 'Service Request'
                }
            },
            {
                path: '/request/new',
                name: 'Staff New Service Request',
                component: () => import('@/components/Staff/NewServReqComponent.vue'),
                meta: {
                    requiresAuth: true,
                    title: 'New Service Request'
                }
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
                component: () => import('@/components/Admin/DashboardComponent.vue'),
                meta: {
                    requiresAuth: true,
                    title: 'Dashboard'
                }
            },
            {
                path: 'requests',
                name: 'Admin Service Request',
                component: () => import('@/components/Admin/ServReqComponent.vue'),
                meta: {
                    requiresAuth: true,
                    title: 'Service Request'
                }
            },
            {
                path: 'request/new',
                name: 'Admin New Service Request',
                component: () => import('@/components/Admin/NewServReqComponent.vue'),
                meta: {
                    requiresAuth: true,
                    title: 'New Service Request'
                }
            },
            {
                path: 'diagnostics',
                name: 'Admin Diagnostic Rules',
                component: () => import('@/components/Admin/DiagRulesComponent.vue'),
                meta: {
                    requiresAuth: true,
                    title: 'Diagnostic Rules'
                }
            },
            {
                path: 'sops',
                name: 'Admin Standard Operational Procedure',
                component: () => import('@/components/Admin/StanOpeProdComponent.vue'),
                meta: {
                    requiresAuth: true,
                    title: 'Standard Operational Procedure'
                }
            },
            {
                path: 'alerts',
                name: 'Admin Procurement Alerts',
                component: () => import('@/components/Admin/AlertsComponent.vue'),
                meta: {
                    requiresAuth: true,
                    title: 'Procurement Alerts'
                }
            },
            {
                path: 'inventory',
                name: 'Admin Inventory Reference',
                component: () => import('@/components/Admin/InvRefComponent.vue'),
                meta: {
                    requiresAuth: true,
                    title: 'Inventory Reference'
                }
            },
            {
                path: 'reports',
                name: 'Admin Reports',
                component: () => import('@/components/Admin/ReportsComponent.vue'),
                meta: {
                    requiresAuth: true,
                    title: 'Reports'
                }
            },
            {
                path: 'users',
                name: 'Admin Users',
                component: () => import('@/components/Admin/UsersComponent.vue'),
                meta: {
                    requiresAuth: true,
                    title: 'Users'
                }
            },
        ]
    }
];

export default routes;