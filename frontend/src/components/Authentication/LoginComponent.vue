<script setup lang="ts">
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';

    const Email     = ref<string>('');
    const Password  = ref<string>('');
    const Error     = ref<string>('');

    const Router    = useRouter()

    async function login() {
        const res = await fetch('http://127.0.0.1:8000/auth/login',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(
                    {
                        email: Email.value,
                        password: Password.value
                    }
                )
            }
        )

        const data = await res.json()

        if (!res.ok) { 
            Error.value = data.detail ?? 'Login failed' 
            return 
        }

        localStorage.setItem('xx-do-you-know-it', data.access_token)
        await Router.push('/dashboard')
        
    }

</script>

<template>
    <div class="Login-Form">
        <form @submit.prevent="login">
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
                <button type="submit">Login</button>
            </div>
        </form>
    </div>
</template>