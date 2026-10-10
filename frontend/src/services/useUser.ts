import { ApiFetch } from '@/api/Client';
import { HandleApiError } from '@/api/Error.ts';
import { HandleSuccess } from "@/helper/HandleSuccess";
import Swal from 'sweetalert2';
import {
    Users,
    isRegisteringUser,
    isLoadingUsers,
    UserError,
    CurrentPage,
    UsersPerPage,
    TotalUsers,
    TotalPages,
    Search,
    RoleFilter,
    StatusFilter,
    type RegisterUserRequest,
    type User,
    type UserPageListResponse,
} from './state/User.ts';


// Register a User

export const RegisterUser = async (payload: RegisterUserRequest): Promise<User | null> => {

    isRegisteringUser.value = true;
    UserError.value = null;

    try {

        const response = await ApiFetch('/user/admin/register', {

            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),

        });

        const data = await response.json();
        
        if (!response.ok) {
            
            UserError.value = data.detail ?? 'Failed to register user.';
            return null;
        }
        
        Users.value.push(data);

        await HandleSuccess(
            `User ${data.email} has been created.`,
            'Registration Successful!'
        );

        return data;

    } catch (error) {

        await Swal.fire({
            title: 'Connection Error!',
            text: 'Unable to connect to the server. Please try again later.',
            icon: 'error',
        });

        return null;

    } finally {

        isRegisteringUser.value = false;

    }
};


export const ApplyUserFilters = async (): Promise<void> => {

    CurrentPage.value = 1;

    await GetUsers(
        1,
        UsersPerPage.value,
        Search.value,
        RoleFilter.value,
        StatusFilter.value
    );
};


let SearchTimeout: ReturnType<typeof setTimeout> | null = null;

export const HandleSearch = (): void => {

    if (SearchTimeout !== null) {
        clearTimeout(SearchTimeout);
    }

    SearchTimeout = setTimeout(() => {
        ApplyUserFilters();
    }, 400);
};



// Get List of Users

export const GetUsers = async (
    page: number = 1,
    limit: number = 10,
    search: string = '',
    role: string = 'all',
    status: string = 'all'
): Promise<UserPageListResponse | null> => {

    isLoadingUsers.value = true;
    UserError.value = null;

    try {

        const params = new URLSearchParams();

        params.set('page', String(page));
        params.set('limit', String(limit));

        if (search.trim()) {
            params.set('search', search.trim());
        }

        if (role !== 'all') {
            params.set('role', role);
        }

        if (status !== 'all') {
            params.set('status', status);
        }

        const response = await ApiFetch(`/user/list?${params.toString()}`,
            {
                method: 'GET',
            }
        );

        
        if (!response.ok) {
            
            await HandleApiError(
                response,
                'Failed to load users table.'
            );
            
            return null;
            
        }
        
        const data = await response.json();
        const pageData: UserPageListResponse = data;

        Users.value = pageData.items;
        CurrentPage.value = pageData.page;
        UsersPerPage.value = pageData.limit;
        TotalUsers.value = pageData.total;
        TotalPages.value = pageData.pages;

        return pageData;

    } catch (error) {

        await Swal.fire({
            title: 'Connection Error!',
            text: 'Unable to connect to the server. Please try again later.',
            icon: 'error',
        });

        return null;

    } finally {

        isLoadingUsers.value = false;

    }

};


// Promote a User

export const PromoteUser = async (userId: number): Promise<boolean> => {

    try {

        const response = await ApiFetch(`/user/admin/${userId}/promote`, { method: 'PATCH' });
        
        if (!response.ok) {
            
            await HandleApiError(
                response,
                'Failed to promote user.'
            );
            
            return false;
            
        }
        
        const data = await response.json();
        await GetUsers();

        await HandleSuccess(data.message);

        return true;

    } catch (error) {

        await Swal.fire({
            title: 'Connection Error!',
            text: 'Unable to connect to the server. Please try again later.',
            icon: 'error',
        });

        return false;

    }
};


// Demote a User

export const DemoteUser = async (userId: number): Promise<boolean> => {

    try {

        const response = await ApiFetch(`/user/admin/${userId}/demote`, { method: 'PATCH' });
        
        if (!response.ok) {
            
            await HandleApiError(
                response,
                'Failed to demote user.'
            );
            
            return false;
            
        }
        
        const data = await response.json();
        await GetUsers();

        await HandleSuccess(data.message);

        return true;

    } catch (error) {

        await Swal.fire({
            title: 'Connection Error!',
            text: 'Unable to connect to the server. Please try again later.',
            icon: 'error',
        });

        return false;

    }
};


// Disable a User

export const DisableUser = async (userId: number): Promise<boolean> => {

    try {

        const response = await ApiFetch(`/user/admin/${userId}/disable`, { method: 'PATCH' });
        
        if (!response.ok) {
            
            await HandleApiError(
                response,
                'Failed to disable user.'
            );

            return false;

        }
        
        const data = await response.json();
        await GetUsers();

        await HandleSuccess(data.message);

        return true;

    } catch (error) {

        await Swal.fire({
            title: 'Connection Error!',
            text: 'Unable to connect to the server. Please try again later.',
            icon: 'error',
        });

        return false;

    }
};


// Enable a User

export const EnableUser = async (userId: number): Promise<boolean> => {

    try {

        const response = await ApiFetch(`/user/admin/${userId}/enable`,{ method: 'PATCH' });
        
        if (!response.ok) {
            
            await HandleApiError(
                response,
                'Failed to enable user.'
            );
            
            return false;
            
        }
        
        const data = await response.json();
        await GetUsers();

        await HandleSuccess(data.message);

        return true;

    } catch (error) {

        await Swal.fire({
            title: 'Connection Error!',
            text: 'Unable to connect to the server. Please try again later.',
            icon: 'error',
        });

        return false;

    }
};