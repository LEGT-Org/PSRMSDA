import { ApiFetch } from '@/api/Client';
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

        return data;

    } catch (error) {

        console.error('Register User Error:', error);
        UserError.value = 'Unable to connect to the server. Please try again later.';
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

        const response = await ApiFetch(
            `/user/list?${params.toString()}`,
            {
                method: 'GET',
            }
        );

        const data = await response.json();

        if (!response.ok) {

            UserError.value = data.detail ?? 'Failed to load users.';
            return null;

        }

        const pageData: UserPageListResponse = data;

        Users.value = pageData.items;
        CurrentPage.value = pageData.page;
        UsersPerPage.value = pageData.limit;
        TotalUsers.value = pageData.total;
        TotalPages.value = pageData.pages;

        return pageData;

    } catch (error) {

        console.error('Get Users Error:', error);
        UserError.value = 'Unable to connect to the server. Please try again later.';
        return null;

    } finally {

        isLoadingUsers.value = false;

    }

};


// Promote a User

export const PromoteUser = async (userId: number): Promise<boolean> => {

    try {

        const response = await ApiFetch(`/user/admin/${userId}/promote`, { method: 'PATCH' });
        const data = await response.json();

        if (!response.ok) {

            UserError.value = data.detail ?? 'Failed to promote user.';
            return false;

        }

        await GetUsers();

        alert(data.message);

        return true;

    } catch (error) {

        console.error('Promote User Error:', error);
        UserError.value = 'Unable to connect to the server.';
        return false;

    }
};


// Demote a User

export const DemoteUser = async (userId: number): Promise<boolean> => {

    try {

        const response = await ApiFetch(`/user/admin/${userId}/demote`, { method: 'PATCH' });
        const data = await response.json();

        if (!response.ok) {

            UserError.value = data.detail ?? 'Failed to demote user.';
            return false;

        }

        await GetUsers();

        alert(data.message);

        return true;

    } catch (error) {

        console.error('Demote User Error:', error);
        UserError.value = 'Unable to connect to the server.';
        return false;

    }
};


// Disable a User

export const DisableUser = async (userId: number): Promise<boolean> => {

    try {

        const response = await ApiFetch(`/user/admin/${userId}/disable`, { method: 'PATCH' });
        const data = await response.json();

        if (!response.ok) {

            UserError.value = data.detail ?? 'Failed to disable user.';
            return false;

        }

        await GetUsers();

        alert(data.message);

        return true;

    } catch (error) {

        console.error('Disable User Error:', error);
        UserError.value = 'Unable to connect to the server.';
        return false;

    }
};


// Enable a User

export const EnableUser = async (userId: number): Promise<boolean> => {

    try {

        const response = await ApiFetch(`/user/admin/${userId}/enable`,{ method: 'PATCH' });
        const data = await response.json();

        if (!response.ok) {

            UserError.value = data.detail ?? 'Failed to enable user.';
            return false;

        }

        await GetUsers();

        alert(data.message);

        return true;

    } catch (error) {

        console.error('Enable User Error:', error);
        UserError.value = 'Unable to connect to the server.';
        return false;

    }
};