declare module 'vue-router' {
    interface RouteMeta {
        title?:         string;
        requiresAuth?:  boolean;
        requiresGuest?: boolean;
        requiresAdmin?: boolean;
        requiresStaff?: boolean;
        requiresToken?: boolean;
    }
}


// Routes

const routes = [
    
    /* 
        Authentication View
    */
    
    {
        path: '/',
        name: 'Authentication',
        component: () => import('@/views/AuthenticationView.vue'),
        children: [
            {
                path: '',
                name: 'Login View',
                component: () => import('@/components/Authentication/LoginComponent.vue'),
                meta: {
                    requiresGuest: true,
                    requiresToken: false,
                    requiresAuth: false,
                    requiresAdmin: false,
                    requiresStaff: false,
                    title: 'Lightyear Electrical Goods Trading'
                }
            },
            {
                path: 'password/set',
                name: 'Set Password View',
                component: () => import('@/components/Authentication/SetPasswordComponent.vue'),
                meta: {
                    requiresGuest: true,
                    requiresToken: true,
                    requiresAuth: false,
                    requiresAdmin: false,
                    requiresStaff: false,
                    title: 'Set My Password'
                }
            },
            {
                path: 'password/reset',
                name: 'Reset Password View',
                component: () => import('@/components/Authentication/PasswordResetComponent.vue'),
                meta: {
                    requiresGuest: true,
                    requiresToken: false,
                    requiresAuth: false,
                    requiresAdmin: false,
                    requiresStaff: false,
                    title: 'Reset My Password'
                }
            }
        ]
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
                    requiresToken: false,
                    requiresAdmin: false,
                    requiresStaff: true,
                    title: 'Dashboard'
                }
            },
            {
                path: '/request/new',
                name: 'Staff New Service Request',
                component: () => import('@/components/Staff/NewServReqComponent.vue'),
                meta: {
                    requiresAuth: true,
                    requiresToken: false,
                    requiresAdmin: false,
                    requiresStaff: true,
                    title: 'New Service Request'
                }
            },
            {
                path: '/requests',
                name: 'Staff Service Requests',
                component: () => import('@/components/Staff/ServReqComponent.vue'),
                meta: {
                    requiresAuth: true,
                    requiresToken: false,
                    requiresAdmin: false,
                    requiresStaff: true,
                    title: 'Service Request Management'
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
                    requiresToken: false,
                    requiresAdmin: true,
                    requiresStaff: false,
                    title: 'Dashboard'
                }
            },
            {
                path: 'request/new',
                name: 'Admin New Service Request',
                component: () => import('@/components/Admin/NewServReqComponent.vue'),
                meta: {
                    requiresAuth: true,
                    requiresToken: false,
                    requiresAdmin: true,
                    requiresStaff: false,
                    title: 'New Service Request'
                }
            },
            {
                path: 'requests',
                name: 'Admin Service Request',
                component: () => import('@/components/Admin/ServReqComponent.vue'),
                meta: {
                    requiresAuth: true,
                    requiresToken: false,
                    requiresAdmin: true,
                    requiresStaff: false,
                    title: 'Service Request Management'
                }
            },
            {
                path: 'sops',
                name: 'Admin Standard Operational Procedure',
                component: () => import('@/components/Admin/StanOpeProdComponent.vue'),
                meta: {
                    requiresAuth: true,
                    requiresToken: false,
                    requiresAdmin: true,
                    requiresStaff: false,
                    title: 'Standard Operational Procedure Management'
                }
            },
            {
                path: 'alerts',
                name: 'Admin Procurement Alerts',
                component: () => import('@/components/Admin/AlertsComponent.vue'),
                meta: {
                    requiresAuth: true,
                    requiresToken: false,
                    requiresAdmin: true,
                    requiresStaff: false,
                    title: 'Procurement Alerts Management'
                }
            },
            {
                path: 'inventory',
                name: 'Admin Inventory Reference',
                component: () => import('@/components/Admin/InvRefComponent.vue'),
                meta: {
                    requiresAuth: true,
                    requiresToken: false,
                    requiresAdmin: true,
                    requiresStaff: false,
                    title: 'Inventory Reference Management'
                }
            },
            {
                path: 'reports',
                name: 'Admin Reports',
                component: () => import('@/components/Admin/ReportsComponent.vue'),
                meta: {
                    requiresAuth: true,
                    requiresToken: false,
                    requiresAdmin: true,
                    requiresStaff: false,
                    title: 'Reports Management'
                }
            },
            {
                path: 'customers',
                name: 'Admin Customers Management',
                component: () => import('@/components/Admin/CustomerComponent.vue'),
                meta: {
                    requiresAuth: true,
                    requiresToken: false,
                    requiresAdmin: true,
                    requiresStaff: false,
                    title: 'Customers Management'
                }
            },
            {
                path: 'users',
                name: 'Admin Users Management',
                component: () => import('@/components/Admin/UsersComponent.vue'),
                meta: {
                    requiresAuth: true,
                    requiresToken: false,
                    requiresAdmin: true,
                    requiresStaff: false,
                    title: 'Users Management'
                }
            },
        ]
    },

    // Error Handler for Pages that does not included

    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('@/views/NotFoundView.vue')
    }
];

export default routes;