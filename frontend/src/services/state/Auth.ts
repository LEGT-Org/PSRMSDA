import { ref } from "vue"


export interface User {
    id: number
    first_name: string
    last_name: string
    email: string
    role: string
}


export const isLoading = ref<boolean>(false);
export const isFetched   = ref(false);
export const Error       = ref<string>('');
export const currentUser = ref<User | null>(null);
export const accessToken = ref<string | null>(null);