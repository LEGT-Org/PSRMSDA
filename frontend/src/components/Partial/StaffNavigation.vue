<script setup lang="ts">
    import { ref } from 'vue';
    import { logout } from '@/services/useAuth';
    import { currentUser } from '@/services/state/Auth';
    
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
    <div class="Staff-Navigation-Container">

        <div class="Staff-Navigation">
            <button>
                <img 
                    src="@/assets/Images/Icons/menu.png" 
                    alt="Menu" 
                />
            </button>

            <RouterLink to="/dashboard">
                <img 
                    src="@/assets/Images/Icons/dashboard.png" 
                    alt="Dashboard"
                />
                <span>Dashboard</span>
            </RouterLink>

            <RouterLink to="/requests">
                <img 
                    src="@/assets/Images/Icons/request.png" 
                    alt="Request"
                />
                <span>Requests</span>
            </RouterLink>

            <RouterLink to="/request/new">
                <img 
                    src="@/assets/Images/Icons/create.png" 
                    alt="New Request"
                />
                <span>New Request</span>
            </RouterLink>
        </div>

        <div class="Staff-Profile-Wrapper">

            <button type="button" class="Staff-Profile" @click="ToggleProfileMenu">
                <img src="@/assets/Images/Icons/user.png" alt="Profile">
                <div v-if="currentUser">
                    <h4>{{ currentUser.first_name }} {{ currentUser.last_name }}</h4>
                    <p>{{ currentUser.email }}</p>
                    <p>{{ currentUser.role }}</p>
                </div>
                
                <div v-else>
                    <h4>Loading...</h4>
                </div>
            </button>

            <div v-if="showProfileMenu" class="Staff-Profile-Menu">
                <RouterLink to="/settings" @click="showProfileMenu = false">
                    Settings
                </RouterLink>

                <button type="button" @click="Logout">Logout</button>
            </div>

        </div>
    </div>
</template>