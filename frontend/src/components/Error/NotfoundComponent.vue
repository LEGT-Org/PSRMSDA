<script setup lang="ts">
    import { useRouter } from 'vue-router';
    
    const Router = useRouter();
    const GoBack = () => {
        Router.push('/dashboard');
    }
    
</script>

<template>
    <div class="Error-Div">
        <h2>404</h2>
        <p>Not Found</p>

        <button @click="GoBack">Go Back</button>
    </div>
</template>