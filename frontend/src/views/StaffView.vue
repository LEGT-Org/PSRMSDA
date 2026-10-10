<script setup lang="ts">
    import { ToggleNavigation } from '@/services/state/Navigation';

    import Header from '@/components/Partial/Header.vue';
    import Navigation from '@/components/Partial/StaffNavigation.vue';

</script>

<template>
    <header>

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