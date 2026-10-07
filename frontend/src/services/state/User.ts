import { ref } from 'vue';

export interface User {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    role: string;
    is_active: boolean;
    email_verified: boolean;
}

export interface RegisterUserRequest {
    first_name: string;
    last_name: string;
    email: string;
}

export interface UserPageListResponse {
    items: User[];
    page: number;
    limit: number;
    total: number;
    pages: number;
}


// For user essential state

export const Users = ref<User[]>([]);
export const isLoadingUsers = ref<boolean>(false);
export const isRegisteringUser = ref<boolean>(false);
export const UserError = ref<string | null>(null);


// For pagination state

export const Search = ref<string>('');
export const RoleFilter = ref<string>('all');
export const StatusFilter = ref<string>('all');
export const ShowRegisterUser = ref<boolean>(false);


export const CurrentPage = ref<number>(1);
export const UsersPerPage = ref<number>(10);
export const TotalUsers = ref<number>(0);
export const TotalPages = ref<number>(0);