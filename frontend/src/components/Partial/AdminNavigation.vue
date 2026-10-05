<script setup lang="ts">
    import { ref } from 'vue';

    import { logout } from '@/services/useAuth';
    import { currentUser } from '@/services/state/Auth';
    import { capitalizeFirstLetter } from '@/helper/Capitalize';
    
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
    <div class="Admin-Navigation-Container">

        <div class="Admin-Navigation">
            <!-- <button>
                <img 
                    src="@/assets/Images/Icons/menu.png" 
                    alt="Menu" 
                />
            </button> -->

            <p>Main Operations</p>

            <RouterLink to="/admin">
                <img 
                    src="@/assets/Images/Icons/White/dashboard-white.png" 
                    alt=" Dashboard"
                />
                <span>Dashboard</span>
            </RouterLink>

            

            <RouterLink to="/admin/request/new">
                <img 
                    src="@/assets/Images/Icons/White/new-service-request-white.png" 
                    alt="New Request"
                />
                <span>New Request</span>
            </RouterLink>

            <p>Management</p>

            <RouterLink to="/admin/requests">
                <img 
                    src="@/assets/Images/Icons/White/request-white.png" 
                    alt="Service Request"
                />
                <span>Service Request</span>
            </RouterLink>

            <RouterLink to="/admin/sops">
                <img 
                    src="@/assets/Images/Icons/sop.png" 
                    alt="Standard Operational Procedure"
                />
                <span>SOP</span>
            </RouterLink>

            <RouterLink to="/admin/inventory">
                <img 
                    src="@/assets/Images/Icons/inventory.png" 
                    alt="Inventory Reference"
                />
                <span>Inventory Reference</span>
            </RouterLink>

            <RouterLink to="/admin/reports">
                <img 
                    src="@/assets/Images/Icons/report.png" 
                    alt="Reports"
                />
                <span>Reports</span>
            </RouterLink>

            <RouterLink to="/admin/users">
                <img 
                    src="@/assets/Images/Icons/user.png" 
                    alt="Users"
                />
                <span>Users</span>
            </RouterLink>
        </div>

        <div class="Admin-Profile-Wrapper">
            
            <button type="button" class="Admin-Profile" @click="ToggleProfileMenu">
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

            <div v-if="showProfileMenu" class="Admin-Profile-Menu">
                <!-- <RouterLink to="/settings" @click="showProfileMenu = false">
                    Settings
                </RouterLink> -->

                <button type="button" @click="Logout">Logout</button>
            </div>

        </div>
    </div>
</template>