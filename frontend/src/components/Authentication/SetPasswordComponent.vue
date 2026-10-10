<script setup lang="ts">
    import { ref, onMounted } from 'vue';
    import { useRoute, useRouter } from 'vue-router';

    import { setPassword } from '@/services/useAuth';
    import { Error, isLoading } from '@/services/state/Auth';
    import { HandleSuccess } from '@/helper/HandleSuccess';

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

        await HandleSuccess(
            'Your new password has been set. You may login now.',
            'Set New Password Successful!'
        )

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
                <label for="Password">Password</label>
                <input 
                    v-model="Password" 
                    type="password"
                    id="Password" 
                    placeholder="Password..." 
                    required 
                />
            </div>

            <div class="Auth-Input">
                <label for="Confirm-Password">Confirm Password</label>
                <input 
                    v-model="ConfirmPassword" 
                    type="password"
                    id="Confirm-Password" 
                    placeholder="Confirm Password..." 
                    required 
                />
            </div>

            <div class="Auth-Handler">
                <p v-if="ErrorMessage">{{ ErrorMessage }}</p>
                
                <button type="submit" :disabled="isLoading">
                    {{ isLoading ? 'Setting Password...' : 'Set Password' }}
                </button>
            </div>
        </form>
    </div>

</template>