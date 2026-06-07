<script setup lang="ts">
    import { ref } from 'vue';

    const Name  = ref<string>('John Doe Example');
    const Email = ref<string>('johndoe@example.com');
    const Role  = ref<string>('Admin');
</script>

<template>
    <div class="Admin-Navigation-Container">

        <div class="Admin-Navigation">
            <button>
                <img 
                    src="@/assets/Images/Icons/menu.png" 
                    alt="Menu" 
                />
            </button>

            <RouterLink to="/admin">
                <img 
                    src="@/assets/Images/Icons/dashboard.png" 
                    alt=" Dashboard"
                />
                <span>Dashboard</span>
            </RouterLink>

            <RouterLink to="/admin/requests">
                <img 
                    src="@/assets/Images/Icons/request.png" 
                    alt="Service Request"
                />
                <span>Requests</span>
            </RouterLink>

            <RouterLink to="/admin/request/new">
                <img 
                    src="@/assets/Images/Icons/create.png" 
                    alt="New Request"
                />
                <span>New Request</span>
            </RouterLink>

            <RouterLink to="/admin/diagnostic">
                <img 
                    src="@/assets/Images/Icons/diagnostic.png" 
                    alt="Diagnostic Rules"
                />
                <span>Diagnostic Rules</span>
            </RouterLink>

            <RouterLink to="/admin/sop">
                <img 
                    src="@/assets/Images/Icons/sop.png" 
                    alt="Standard Operational Procedure"
                />
                <span>Standard Operational Procedure</span>
            </RouterLink>

            <RouterLink to="/admin/alerts">
                <img 
                    src="@/assets/Images/Icons/danger.png" 
                    alt="Alerts"
                />
                <span>Alerts</span>
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

        <div class="Admin-Profile">
            <img src="@/assets/Images/Icons/user.png" alt="Lighyear Electrical Godds Trading Profile">
            <div>
                <h4>{{ Name }}</h4>
                <p>{{ Email }}</p>
                <p>{{ Role }}</p>
            </div>
        </div>
    </div>
</template>