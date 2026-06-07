<script setup lang="ts">
    import LoginComponent from '@/components/Authentication/LoginComponent.vue';
</script>

<template>
    <main class="Login-Main">
        <section class="Login-Section">
            <div class="Login-Image">
                <img 
                    src="@/assets/Images/LEGT-Logo.png" 
                    alt="LEGT-Logo"
                    class="Login-Logo"
                />
            </div>

            <LoginComponent />
        </section>
    </main>
</template>