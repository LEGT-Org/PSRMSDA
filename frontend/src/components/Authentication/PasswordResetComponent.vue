<script setup lang="ts">
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';
    
    import { resetPassword } from '@/services/useAuth';
    import { Error, isLoading } from '@/services/state/Auth';
    import { HandleSuccess } from '@/helper/HandleSuccess'; 

    const Email          = ref<string>('');
    const ErrorMessage   = ref<string>('');

    const Router         = useRouter();

    const ResetUserPassword = async () => {

        ErrorMessage.value = '';

        const result = await resetPassword(Email.value);

        if (result.ok) {
            
            await HandleSuccess(
                'Your password has been reset successfully. You can now log in using your new password.',
                'Password Reset Successful!'
            );

            await Router.push('/');

            return;
        }

        ErrorMessage.value = result.message;
    };
    
</script>

<template>

    <div class="Auth-Form">
        <form @submit.prevent="ResetUserPassword">

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

            <div class="Auth-Handler">
                <p v-if="ErrorMessage">{{ ErrorMessage }}</p>
                
                <button type="submit" class="Password-Reset" :disabled="isLoading">
                    {{ isLoading ? 'Password Resetting...' : 'Password Reset' }}
                </button>
            </div>

        </form>
    </div>

</template>