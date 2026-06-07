<script setup lang="ts">
    import { ref } from 'vue';

    const Name  = ref<string>('John Doe Example');
    const Email = ref<string>('johndoe@example.com');
    const Role  = ref<string>('Staff');
</script>

<template>
    <div class="Staff-Dashboard">

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

        <div class="Staff-Profile"  >
            <img src="@/assets/Images/Icons/user.png" alt="Profile">
            <div>
                <h4>{{ Name }}</h4>
                <p>{{ Email }}</p>
                <p>{{ Role }}</p>
            </div>
        </div>
    </div>
</template>