<script setup lang="ts">
    import Swal from 'sweetalert2'; 
    import { onMounted, ref } from 'vue';
    import Router from '@/router/Router';

    import { FormatDate } from '@/helper/DateFormatter';
    import {
        Customers,
        CurrentPage,
        CustomerPerPage,
        TotalPages,
        IsLoading,
        Search,
        isCreateCustomer,
        ShowCreateCustomer,
        CustomerError,
        type CustomerCreateRequest,
    } from '@/services/state/Customer';

    import {
        CreateCustomer,
        GetCustomers,
        HandleCustomerSearch,
    } from '@/services/useCustomer';


    const FirstName = ref<string>('');
    const LastName = ref<string>('');
    const Email = ref<string>('');
    const PhoneNumber = ref<string>('');

    
    const ResetCreateCustomer = () => {
        FirstName.value = ''
        LastName.value = ''
        Email.value = ''
        PhoneNumber.value = ''
    }


    const CloseCreateCustomerModal = () => {
        if (isCreateCustomer.value) return;

        ShowCreateCustomer.value = false;
        ResetCreateCustomer();
    }


    const SubmitCreateCustomer = async () => {

        const Confirmation = await Swal.fire({
            title: 'Create this record?',
            text: `Double-check the details below. You can go back and edit if anything looks wrong.`,
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'Create record',
            cancelButtonText: 'Go back and edit',
            customClass: {
                confirmButton: 'success-button',
                cancelButton: 'error-button'
            },
            reverseButtons: true,
            focusCancel: true,
        });

        if (!Confirmation.isConfirmed) return;
        

        const payload: CustomerCreateRequest = {
            first_name: FirstName.value,
            last_name: LastName.value,
            email: Email.value,
            phone_number: PhoneNumber.value
        }

        const customers = await CreateCustomer(payload);

        if (!customers) return;

        CloseCreateCustomerModal()
    }


    const FetchPage = async (): Promise<void> => {
        await GetCustomers(
            CurrentPage.value,
            CustomerPerPage.value,
            Search.value,
        );
    };


    const GoToNextPage = async (): Promise<void> => {
        if (CurrentPage.value >= TotalPages.value) {
            return;
        }

        await GetCustomers(
            CurrentPage.value + 1,
            CustomerPerPage.value,
            Search.value,
        );
    };


    const GoToPreviousPage = async (): Promise<void> => {
        if (CurrentPage.value <= 1) {
            return;
        }

        await GetCustomers(
            CurrentPage.value - 1,
            CustomerPerPage.value,
            Search.value,
        );
    };


    const GoToCustomerDetail = async (id: number): Promise<void> => {
        await Router.push(`/customer/${id}`);
    }


    onMounted(async () => {
        await Promise.all([
            FetchPage()
        ]);
    });
</script>

<template>
    
    <section class="Customer-Management">
        <!-- Header -->
        <div class="Customer-Title">

            <div>
                <h1>Customer Management</h1>
                <p>View and manage customers.</p>
            </div>

            <div class="Customer-Action-Buttons">
                <button
                    type="button"
                    class="Create-Customer-Button"
                    @click="ShowCreateCustomer = true"
                >
                    Create Customer
                </button>
            </div>

        </div>

        <!-- Create New Spare Part -->
        <Transition name="form-transition">

            <div
                v-if="ShowCreateCustomer"
                class="Form-Panel"
            >

                <div class="Modal-Header">

                    <div>
                        <h2>Add New Customer</h2>

                        <p>
                            Create a new customer record.
                        </p>
                    </div>

                    <button
                        type="button"
                        class="Modal-Close"
                        :disabled="isCreateCustomer"
                        @click="CloseCreateCustomerModal"
                    >
                        ×
                    </button>

                </div>


                <form @submit.prevent="SubmitCreateCustomer">

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
                            autocomplete="family-name"
                            required
                        />

                    </div>

                    <div class="Form-Field">

                        <label for="phone-number">
                            Phone Number
                        </label>

                        <input
                            id="phone-number"
                            v-model="PhoneNumber"
                            type="tel"
                            placeholder="e.g  09123456789 or +639123456789"
                            autocomplete="family-name"
                            required
                        />

                    </div>

                    <p
                        v-if="CustomerError"
                        class="Form-Error"
                    >
                        {{ CustomerError }}
                    </p>


                    <div class="Modal-Actions">

                        <button
                            type="button"
                            class="Modal-Cancel-Button"
                            :disabled="isCreateCustomer"
                            @click="CloseCreateCustomerModal"
                        >
                            Cancel
                        </button>

                        <button
                            type="submit"
                            class="Modal-Confirm-Button"
                            :disabled="isCreateCustomer"
                        >
                            {{
                                isCreateCustomer
                                    ? 'Adding Customer...'
                                    : 'Add New Customer'
                            }}
                        </button>

                    </div>

                </form>

            </div>

        </Transition>

        <!-- Filters -->
        <div class="Customer-Filters">

            <div class="Search-Field">
                <label for="customer-search">
                    Search
                </label>

                <input
                    id="customer-search"
                    v-model="Search"
                    class="Customer-Search"
                    type="search"
                    placeholder="Search customers..."
                    @input="HandleCustomerSearch"
                />
            </div>

        </div>

        <!-- Spare Parts Table -->
        <div class="Customer-Table-Container">
            <table class="Customer-Table">
                <thead>
                    <tr>
                        <th>Customer</th>
                        <th>Email</th>
                        <th>Phone Number</th>
                        <th>Created Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>

                <tbody>
                    <tr
                        v-for="Customer in Customers"
                        :key="Customer.id"
                    >
                        <td>
                            <strong>{{ Customer.first_name }} {{ Customer.last_name }}</strong>
                            <span>ID: {{ Customer.id }}</span>
                        </td>
                        <td>{{ Customer.email }}</td>
                        <td>{{ Customer.phone_number }}</td>
                        <td>{{ FormatDate(Customer.created_at).toLocaleString() }}</td>

                        <td>
                            <button
                                type="button"
                                class="View-Request-Button"
                                @click="GoToCustomerDetail(Customer.id)"
                            >
                                →
                            </button>
                        </td>

                    </tr>

                    <tr v-if="Customers.length === 0">
                        <td colspan="8">
                            <div class="Customer-Empty-State">
                                <h3>No spare parts found</h3>
                                <p>
                                    No spare parts record match
                                    your current search or filter.
                                </p>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Pagination -->
        <div class="Pagination">
            <button
                type="button"
                :disabled="CurrentPage <= 1 || IsLoading"
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
                    IsLoading ||
                    TotalPages === 0
                "
                @click="GoToNextPage"
            >
                Next
            </button>
        </div>

    </section>
</template>