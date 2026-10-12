<script setup lang="ts">
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';

    import { login } from '@/services/useAuth';
    import { Error, currentUser, isLoading } from '@/services/state/Auth';

    const Email         = ref<string>('');
    const Password      = ref<string>('');
    const ErrorMessage  = ref<string>('');

    const Router = useRouter();
    
    const Login = async () => {

        const success = await login(Email.value, Password.value);

        if (success) {

            await Router.push(currentUser.value?.role === 'admin' ? '/admin' : '/dashboard');

        }

        ErrorMessage.value = Error.value;   

    }
 
</script>

<template>
    <div class="Auth-Form">
        <form @submit.prevent="Login">
            <div class="Auth-Input">
                <label for="Email">Email</label>
                <input 
                    v-model="Email" 
                    type="email"
                    id="Email" 
                    placeholder="Email..." 
                    required 
                />
            </div>

            <div class="Auth-Input">
                <label for="Password">Password</label>
                <input 
                    v-model="Password" 
                    type="password"
                    id="Password" 
                    placeholder="Password..." 
                    required 
                />
            </div>

            <div class="Auth-Handler">
                <p v-if="ErrorMessage">{{ ErrorMessage }}</p>

                <div class="Auth-Actions">
                    <a href="/password/reset" class="Forgot-Password">
                        Forgot Password?
                    </a>

                    <button type="submit" :disabled="isLoading">
                        {{ isLoading ? 'Login...' : 'Login' }}
                    </button>
                </div>
            </div>
        </form>
    </div>
</template>