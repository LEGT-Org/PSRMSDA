<script setup lang="ts">
    import { ref } from 'vue';
    import { login } from '@/services/useAuth';
    import { useRouter } from 'vue-router';

    const Email         = ref<string>('');
    const Password      = ref<string>('');
    const ErrorMessage  = ref<string | null>(null);

    const Router        = useRouter();
    
    const Login = async () => {

        const LoginResult   = await login(Email.value, Password.value);
        
        if (LoginResult.success) {
            window.location.reload();
        }

        if (!LoginResult.success) {
            ErrorMessage.value = LoginResult.error;
        }

    }
 
</script>

<template>
    <div class="Login-Form">
        <form @submit.prevent="Login">
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
                <p v-if="ErrorMessage">{{ ErrorMessage }}</p>
                <button type="submit">Login</button>
            </div>
        </form>
    </div>
</template>