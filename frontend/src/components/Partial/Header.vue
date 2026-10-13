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
                aria-label="Toggle navigation"
                @click="ToggleNavigation"
            >
                <img
                    src="@/assets/Images/Icons/menu.png"
                    alt=""
                />
            </button>

            <RouterLink to="/" class="Header-Logo-Link">
                <img
                    src="@/assets/Images/LEGT-Logo.png"
                    alt="Lightyear Electrical Goods Trading"
                />

                <h2>LEGT</h2>
            </RouterLink>
        </div>

    </div>
</template>