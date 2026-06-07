<script setup lang="ts">
    import Header from '@/components/Partial/Header.vue';
    import Navigation from '@/components/Partial/Staff/Navigation.vue';
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
            <section>
                <RouterView />
            </section>
        </main>
    </div>
</template>