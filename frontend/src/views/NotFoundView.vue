<script setup lang="ts">
    import NotfoundComponent from '@/components/Error/NotfoundComponent.vue';
</script>

<template>
    <main class="Error-Main">
        <section class="Error-Section">
            <div class="Error-Image">
                <img 
                    src="@/assets/Images/LEGT-Logo.png" 
                    alt="LEGT-Logo"
                    class="Error-Logo"
                />
            </div>

            <NotfoundComponent />
        </section>
    </main>
</template>