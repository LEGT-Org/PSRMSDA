<script setup lang="ts">
    import { ref } from 'vue';

    const Search = ref<string>('');
</script>

<template>
    <div class="Header-Container">
        <div class="Header-Logo">
            <img 
                src="@/assets/Images/LEGT-Logo.png" 
                alt="Lighyear Electrical Goods Logo"
            />
            <h2>LEGT</h2>
        </div>

        <div class="Header-Search">
            <input 
                v-model="Search"
                type="text"
                placeholder="Search..."    
            />
            <div class="Header-Search-Divider"></div>
            <button>
                <img 
                    src="@/assets/Images/Icons/search.png" 
                    alt="Search"
                />
            </button>
        </div>

        <div class="Header-Notification">
            <img 
                src="@/assets/Images/Icons/notification.png" 
                alt="Notification"
            />
        </div>
    </div>
</template>