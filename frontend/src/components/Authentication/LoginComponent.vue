<script setup lang="ts">
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';

    import { login } from '@/services/useAuth';
    import { Error, currentUser } from '@/services/state/Auth';

    const Email         = ref<string>('');
    const Password      = ref<string>('');
    const ErrorMessage  = ref<string>('');

    const Router = useRouter();
    
    const Login = async () => {

        const loginResult = await login(Email.value, Password.value);

        console.log('LOGIN RESULT:', loginResult);
        console.log('CURRENT USER:', currentUser.value);

        if (loginResult) {

            await Router.push(currentUser.value?.role === 'admin' ? '/admin' : '/dashboard');

        }

        ErrorMessage.value = Error.value;

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