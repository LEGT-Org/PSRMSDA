<script setup lang="ts">
    import { ref } from 'vue';

    const Email     = ref<string>('');
    const Password  = ref<string>('');
    const Error     = ref<string>('');
</script>

<template>
    <div class="Login-Form">
        <form>
            <div class="Login-Input">
                <label for="Email">Email</label>
                <input 
                    v-model="Email" 
                    type="email"
                    id="Email" 
                    placeholder="Email..." 
                    required 
                />
            </div>

            <div class="Login-Input">
                <label for="Password">Password</label>
                <input 
                    v-model="Password" 
                    type="password"
                    id="Password" 
                    placeholder="Password..." 
                    required 
                />
            </div>

            <div class="Login-Handler">
                <p v-if="Error">{{ Error }}</p>
                <button>Login</button>
            </div>
        </form>
    </div>
</template>