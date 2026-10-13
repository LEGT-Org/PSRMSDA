<script setup lang="ts">
    import Swal from 'sweetalert2';
    import { ref, onMounted } from 'vue';

    import { accessToken, currentUser, isFetched } from '@/services/state/Auth';
    import { capitalizeFirstLetter } from '@/helper/Capitalize';
    import { 
        RegisterUser, 
        GetUsers, 
        PromoteUser,
        DemoteUser,
        DisableUser,
        EnableUser,
        HandleSearch,
        ApplyUserFilters,
        DeleteUser
    } from '@/services/useUser.ts';

    import {
        isRegisteringUser,
        isLoadingUsers,
        UserError,
        Users,
        CurrentPage,
        UsersPerPage,
        TotalPages,
        Search,
        RoleFilter,
        StatusFilter,
        ShowRegisterUser,
        type RegisterUserRequest
    } from '@/services/state/User.ts';


    const FirstName = ref('');
    const LastName = ref('');
    const Email = ref('');


    const ResetRegisterForm = () => {
        FirstName.value = '';
        LastName.value = '';
        Email.value = '';
    };


    const CloseRegisterUser = () => {

        if (isRegisteringUser.value) {
            return;
        }

        ShowRegisterUser.value = false;

        ResetRegisterForm();
    };


    const SubmitRegisterUser = async () => {

        const Confirmation = await Swal.fire({
            title: 'Register this user?',
            text: `Double-check the details below. You can go back and edit if anything looks wrong.`,
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'Create account',
            cancelButtonText: 'Go back and edit',
            customClass: {
                confirmButton: 'success-button',
                cancelButton: 'error-button'
            },
            reverseButtons: true,
            focusCancel: true,
        });

        if (!Confirmation.isConfirmed) {
            return;
        }

        const payload: RegisterUserRequest = {
            first_name: FirstName.value,
            last_name: LastName.value,
            email: Email.value,
        };

        const user = await RegisterUser(payload);

        if (!user) {
            return;
        }

        CloseRegisterUser();
    };


    const GoToNextPage = async () => {

        if (CurrentPage.value >= TotalPages.value) return;

        await GetUsers(
            CurrentPage.value + 1,
            UsersPerPage.value,
            Search.value,
            RoleFilter.value,
            StatusFilter.value
        );

    };


    const GoToPreviousPage = async () => {

        if (CurrentPage.value <= 1) return;

        await GetUsers(
            CurrentPage.value - 1,
            UsersPerPage.value,
            Search.value,
            RoleFilter.value,
            StatusFilter.value
        );

    };

    onMounted(async () => {

        if (!currentUser.value || !accessToken.value) return;

        await GetUsers(
            CurrentPage.value,
            UsersPerPage.value,
            Search.value,
            RoleFilter.value,
            StatusFilter.value
        );
        
    });

</script>


<template>

    <section class="Users-Page">

        <!-- Page Header -->

        <div class="Users-Header">

            <div>

                <h1>User Management</h1>

                <p>
                    Manage system users and their accounts.
                </p>

            </div>


            <button
                type="button"
                class="Register-User-Button"
                @click="ShowRegisterUser = true"
            >
                Register User
            </button>

        </div>

        <!-- Register User -->
        <Transition name="register-user">

        <div
            v-if="ShowRegisterUser"
            class="Register-User-Panel"
        >

            <div class="Modal-Header">

                <div>
                    <h2>Register User</h2>

                    <p>
                        Create a new user account.
                    </p>
                </div>

                <button
                    type="button"
                    class="Modal-Close"
                    :disabled="isRegisteringUser"
                    @click="CloseRegisterUser"
                >
                    ×
                </button>

            </div>


            <form @submit.prevent="SubmitRegisterUser">

                <div class="Form-Field">

                    <label for="first-name">
                        First Name
                    </label>

                    <input
                        id="first-name"
                        v-model="FirstName"
                        type="text"
                        placeholder="e.g. John"
                        autocomplete="given-name"
                        required
                    />

                </div>


                <div class="Form-Field">

                    <label for="last-name">
                        Last Name
                    </label>

                    <input
                        id="last-name"
                        v-model="LastName"
                        type="text"
                        placeholder="e.g. Doe"
                        autocomplete="family-name"
                        required
                    />

                </div>


                <div class="Form-Field">

                    <label for="email">
                        Email
                    </label>

                    <input
                        id="email"
                        v-model="Email"
                        type="email"
                        placeholder="e.g johndoe@gmail.com"
                        autocomplete="email"
                        required
                    />

                </div>


                <p
                    v-if="UserError"
                    class="Form-Error"
                >
                    {{ UserError }}
                </p>


                <div class="Modal-Actions">

                    <button
                        type="button"
                        class="Modal-Cancel-Button"
                        :disabled="isRegisteringUser"
                        @click="CloseRegisterUser"
                    >
                        Cancel
                    </button>

                    <button
                        type="submit"
                        class="Modal-Confirm-Button"
                        :disabled="isRegisteringUser"
                    >
                        {{
                            isRegisteringUser
                                ? 'Registering...'
                                : 'Register User'
                        }}
                    </button>

                </div>

            </form>

        </div>

        </Transition>

        <!-- User Controls -->

        <div class="Users-Controls">

            <div class="Search-Field">

                <label for="user-search">
                    Search
                </label>

                <input
                    id="user-search"
                    v-model="Search"
                    type="text"
                    placeholder="Search users..."
                    @input="HandleSearch"
                />

            </div>


            <div class="Filter-Field">

                <label for="role-filter">
                    Role
                </label>

                <select
                    id="role-filter"
                    v-model="RoleFilter"
                    @change="ApplyUserFilters"
                >
                    <option value="all">
                        All Roles
                    </option>

                    <option value="admin">
                        Admin
                    </option>

                    <option value="user">
                        Staff
                    </option>
                </select>

            </div>


            <div class="Filter-Field">

                <label for="status-filter">
                    Status
                </label>

                <select
                    id="status-filter"
                    v-model="StatusFilter"
                    @change="ApplyUserFilters"
                >
                    <option value="all">
                        All Status
                    </option>

                    <option value="active">
                        Active
                    </option>

                    <option value="disabled">
                        Disabled
                    </option>
                </select>

            </div>

        </div>


        <!-- Users -->

        <div class="Users-Card">

            <div class="Users-Table-Header">
                <span>User</span>
                <span>Email</span>
                <span>Role</span>
                <span>Status</span>
                <span>Actions</span>
            </div>

            <div class="Users-List">

                <div
                    v-for="user in Users"
                    :key="user.id"
                    class="User-Row"
                >

                    <!-- User -->

                    <div class="User-Identity">

                        <strong>
                            {{ user.first_name }} {{ user.last_name }}
                        </strong>

                        <span>
                            ID: {{ user.id }}
                        </span>

                    </div>

                    <!-- Email -->

                    <div class="User-Email">
                        {{ user.email }}
                    </div>

                    <!-- Role -->

                    <div>

                        <span class="Role-Badge">
                            {{ capitalizeFirstLetter(user.role) }}
                        </span>

                    </div>

                    <!-- Status -->

                    <div>

                        <span class="Status-Badge">
                            {{ user.is_active ? 'Active' : 'Disabled' }}
                        </span>

                    </div>

                    <!-- Actions -->

                    <div class="User-Actions">

                        <button
                            v-if="user.role === 'admin'"
                            type="button"
                            class="Users-Button-Red-Border"
                            @click="DemoteUser(user.id)"
                        >
                            Demote
                        </button>

                        <button
                            v-else
                            type="button"
                            class="Users-Button-Blue-Border"
                            @click="PromoteUser(user.id)"
                        >
                            Promote
                        </button>

                        <button
                            v-if="user.is_active"
                            type="button"
                            class="Users-Button-Red-Border"
                            @click="DisableUser(user.id)"
                        >
                            Disable
                        </button>

                        <button
                            v-else
                            type="button"
                            class="Users-Button-Blue-Border"
                            @click="EnableUser(user.id)"
                        >
                            Enable
                        </button>

                        <button
                            type="button"
                            class="Users-Button-Red-Border"
                            @click="DeleteUser(user.id)"
                        >
                            Delete
                        </button>

                    </div>

                </div>

            </div>

        </div>

        <div class="Users-Pagination">

            <button
                type="button"
                :disabled="
                    CurrentPage <= 1 ||
                    isLoadingUsers
                "
                @click="GoToPreviousPage"
            >
                Previous
            </button>

            <span>
                Page {{ CurrentPage }} of {{ TotalPages }}
            </span>

            <button
                type="button"
                :disabled="
                    CurrentPage >= TotalPages ||
                    isLoadingUsers
                "
                @click="GoToNextPage"
            >
                Next
            </button>

        </div>

    </section>

</template>