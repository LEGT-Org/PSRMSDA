<script setup lang="ts">
    import Header from '@/components/Partial/Header.vue';
    import Navigation from '@/components/Partial/StaffNavigation.vue';

</script>

<template>
    <header>
        <Header />
    </header>

    <div class="Staff-Main">

        <nav>
            <Navigation />
        </nav>

        <main>
            <section class="Main-Content">
                <RouterView />
            </section>
        </main>
        
    </div>
</template>