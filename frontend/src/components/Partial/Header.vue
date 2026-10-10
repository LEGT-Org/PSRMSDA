<script setup lang="ts">
    import { ref } from 'vue';
    import { ToggleNavigation } from '@/services/state/Navigation';

</script>

<template>
    <div class="Header-Container">

        <div class="Header-Logo">

            <button
                type="button"
                class="Mobile-Navigation-Button"
                @click="ToggleNavigation"
            >
                <img
                    src="@/assets/Images/Icons/menu.png"
                    alt="Menu"
                />
            </button>

            <img 
                src="@/assets/Images/LEGT-Logo.png" 
                alt="Lighyear Electrical Goods Logo"
            />
            <h2>LEGT</h2>
        </div>

        <div class="Header-Notification">
            <img 
                src="@/assets/Images/Icons/notification.png" 
                alt="Notification"
            />
        </div>
    </div>
</template>