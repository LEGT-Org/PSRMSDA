<script setup lang="ts">
    import { ref } from 'vue';
    import { useRoute } from 'vue-router';

    import { logout } from '@/services/useAuth';
    import { currentUser } from '@/services/state/Auth';
    import { capitalizeFirstLetter } from '@/helper/Capitalize';

    import DashboardBlue from '@/assets/Images/Icons/Blue/dashboard-blue.png';
    import DashboardWhite from '@/assets/Images/Icons/White/dashboard-white.png';
    import RequestBlue from '@/assets/Images/Icons/Blue/service-request-blue.png';
    import RequestWhite from '@/assets/Images/Icons/White/service-request-white.png';
    import NewServiceRequestBlue from '@/assets/Images/Icons/Blue/new-service-request-blue.png';
    import NewServiceRequestWhite from '@/assets/Images/Icons/White/new-service-request-white.png';
    import SOPBlue from '@/assets/Images/Icons/Blue/sop-blue.png';
    import SOPWhite from '@/assets/Images/Icons/White/sop-white.png';
    import InventoryBlue from '@/assets/Images/Icons/Blue/inventory-reference-blue.png';
    import InventoryWhite from '@/assets/Images/Icons/White/inventory-reference-white.png';
    import ReportBlue from '@/assets/Images/Icons/Blue/reports-blue.png';
    import ReportWhite from '@/assets/Images/Icons/White/reports-white.png';
    import CustomerBlue from '@/assets/Images/Icons/Blue/customers-management-blue.png';
    import CustomerWhite from '@/assets/Images/Icons/White/customers-management-white.png';
    import UserBlue from '@/assets/Images/Icons/Blue/user-management-blue.png';
    import UserWhite from '@/assets/Images/Icons/White/user-management-white.png';
    

    const Route           = useRoute(); 
    const showProfileMenu = ref<boolean>(false);

    const ToggleProfileMenu = () => {

        showProfileMenu.value = !showProfileMenu.value
        
    }

    const Logout = async () => {

        await logout();
        showProfileMenu.value = false
        window.location.reload();

    }
</script>

<template>
    <div class="Sidebar-Navigation-Container">

        <div class="Sidebar-Navigation">
            <!-- <button>
                <img 
                    src="@/assets/Images/Icons/menu.png" 
                    alt="Menu" 
                />
            </button> -->

            <p>Main Operations</p>

            <RouterLink 
                to="/admin"
                class="Navigation-Link"
                exact-active-class="Navigation-Link-Active"
            >
                <img 
                    :src="Route.path === '/admin'
                        ? DashboardBlue
                        : DashboardWhite
                    "
                    alt=" Dashboard"
                />
                <span>Dashboard</span>
            </RouterLink>

            

            <RouterLink 
                to="/admin/request/new"
                class="Navigation-Link"
                exact-active-class="Navigation-Link-Active"    
            >
                <img 
                    :src="Route.path === '/admin/request/new'
                        ? NewServiceRequestBlue
                        : NewServiceRequestWhite
                    "  
                    alt="New Request"
                />
                <span>New Request</span>
            </RouterLink>

            <p>Management</p>

            <RouterLink 
                to="/admin/requests"
                class="Navigation-Link"
                exact-active-class="Navigation-Link-Active"
            >
                <img 
                    :src="Route.path === '/admin/requests'
                        ? RequestBlue
                        : RequestWhite
                    "  
                    alt="Service Request"
                />
                <span>Service Request</span>
            </RouterLink>

            <RouterLink 
                to="/admin/sops"
                class="Navigation-Link"
                exact-active-class="Navigation-Link-Active"
            >
                <img 
                    :src="Route.path === '/admin/sops'
                        ? SOPBlue
                        : SOPWhite
                    " 
                    alt="Standard Operational Procedure"
                />
                <span>SOP</span>
            </RouterLink>

            <RouterLink 
                to="/admin/inventory"
                class="Navigation-Link"
                exact-active-class="Navigation-Link-Active"
            >
                <img 
                    :src="Route.path === '/admin/inventory'
                        ? InventoryBlue
                        : InventoryWhite
                    " 
                    alt="Inventory Reference"
                />
                <span>Inventory Reference</span>
            </RouterLink>

            <RouterLink 
                to="/admin/reports"
                class="Navigation-Link"
                exact-active-class="Navigation-Link-Active"
            >
                <img 
                    :src="Route.path === '/admin/reports'
                        ? ReportBlue
                        : ReportWhite
                    " 
                    alt="Reports"
                />
                <span>Reports</span>
            </RouterLink>

            <RouterLink 
                to="/admin/customers"
                class="Navigation-Link"
                exact-active-class="Navigation-Link-Active"    
            >
                <img 
                    :src="Route.path === '/admin/customers'
                        ? CustomerBlue
                        : CustomerWhite
                    "  
                    alt="Customers"
                />
                <span>Customers</span>
            </RouterLink>

            <RouterLink 
                to="/admin/users"
                class="Navigation-Link"
                exact-active-class="Navigation-Link-Active"    
            >
                <img 
                    :src="Route.path === '/admin/users'
                        ? UserBlue
                        : UserWhite
                    "  
                    alt="Users"
                />
                <span>Users</span>
            </RouterLink>
        </div>

        <div class="Sidebar-Profile-Wrapper">
            
            <button type="button" class="Sidebar-Profile" @click="ToggleProfileMenu">
                <img src="@/assets/Images/Icons/user.png" alt="Profile">
                <div v-if="currentUser">
                    <h4>{{ capitalizeFirstLetter(currentUser.first_name) }} {{ capitalizeFirstLetter(currentUser.last_name) }}</h4>
                    <p>{{ currentUser.email }}</p>
                    <p>{{ capitalizeFirstLetter(currentUser.role) }}</p>
                </div>

                <div v-else>
                    <h4>Loading...</h4>
                </div>
            </button>

            <div v-if="showProfileMenu" class="Sidebar-Profile-Menu">
                <!-- <RouterLink to="/settings" @click="showProfileMenu = false">
                    Settings
                </RouterLink> -->

                <button type="button" @click="Logout">Logout</button>
            </div>

        </div>
    </div>
</template>