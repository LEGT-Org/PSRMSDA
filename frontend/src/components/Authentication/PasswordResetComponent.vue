<script setup lang="ts">
    import { ref, onMounted } from 'vue';
    import { useRoute, useRouter } from 'vue-router';

    import { setPassword } from '@/services/useAuth';
    import { Error, isLoading } from '@/services/state/Auth';

    const Route     = useRoute();
    const Router    = useRouter();

    const Token = ref<string | null>(
        typeof Route.query.token === 'string'
            ? Route.query.token
            : null
    );

    const Password          = ref<string>('');
    const ConfirmPassword   = ref<string>('');
    const ErrorMessage      = ref<string>('');


    const SetUserPassword = async () => {

        const error = await setPassword(
            Token.value,
            Password.value,
            ConfirmPassword.value
        );

        ErrorMessage.value = error ?? '';

        if (error) {

            return;
            
        }

        await Router.push('/');

    };

    onMounted(() => {
        if (!Token.value) {

            ErrorMessage.value = "Invalid Password Setup Link";
            return;
        }

        if (Token.value) {

            window.history.replaceState(
                {},
                '',
                Route.path
            );

        }
    })
    
</script>

<template>

    <div class="Auth-Form">
        <form @submit.prevent="SetUserPassword">

            <div class="Auth-Input">
                <label for="Email">Email</label>
                <input 
                    v-model="ConfirmPassword" 
                    type="email"
                    id="Email" 
                    placeholder="Email..." 
                    required 
                />
            </div>

            <div class="Auth-Handler">
                <p v-if="ErrorMessage">{{ ErrorMessage }}</p>
                
                <button type="submit" :disabled="isLoading">
                    {{ isLoading ? 'Password Resetting...' : 'Password Reset' }}
                </button>
            </div>

        </form>
    </div>

</template>