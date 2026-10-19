<script setup lang="ts">
    import Swal from 'sweetalert2';
    import { computed, ref, watch } from 'vue';
    import { useRoute, useRouter } from 'vue-router';

    import { DeleteCustomer, GetCustomer, UpdateCustomer } from '@/services/useCustomer';
    import { currentUser } from '@/services/state/Auth';
    import { HandleSuccess } from '@/helper/HandleSuccess';
    import { FormatDate } from '@/helper/DateFormatter';
    import { 
        type Customer as CustomerType, 
        type CustomerUpdateRequest 
    } from '@/services/state/Customer';

    const Route = useRoute();
    const Router = useRouter();

    const IsLoading = ref<boolean>(true);
    const ErrorMessage = ref<string | null>(null);

    const Customer = ref<CustomerType | null>(null);

    const IsEditing = ref<boolean>(false);
    const IsUpdating = ref<boolean>(false);

    const CustomerId = computed<number>(() =>
        Number(Route.params.id)
    );


    const EditForm = ref<CustomerUpdateRequest>({
        first_name: null,
        last_name: null,
        email: null,
        phone_number: null
    });


    const StartEditing = (): void => {
        if (!Customer.value) return;

        EditForm.value = {
            first_name: Customer.value.first_name,
            last_name: Customer.value.last_name,
            email: Customer.value.email,
            phone_number: Customer.value.phone_number
        }

        IsEditing.value = true;
    }

    
     const SaveChanges = async (): Promise<void> => {

        if (!Customer.value || IsUpdating.value) return;

        const Confirmation = await Swal.fire({
            title: 'Update Customer?',
            text: `Are you sure you want to update ${Customer.value.first_name} ${Customer.value.last_name} (${Customer.value.email})?`,
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'Yes, update it',
            cancelButtonText: 'Cancel',
            customClass: {
                confirmButton: 'success-button',
                cancelButton: 'error-button'
            },
            reverseButtons: true,
        });

        if (!Confirmation.isConfirmed) return;

        IsUpdating.value = true;

        try {
            
            const Success = await UpdateCustomer(
                Customer.value.id,
                EditForm.value,
            );

            if (!Success) return;

            IsEditing.value = false;

            await FetchCustomerDetails(Customer.value.id);

        } finally {

            IsUpdating.value = false;

        }
    };


    const DeleteCurrentCustomer = async (): Promise<void> => {

        IsEditing.value = false;

        if (!Customer.value) return;

        const Confirmation = await Swal.fire({
            title: 'Delete Spare Part?',
            text: `Are you sure you want to delete  ${Customer.value.first_name} ${Customer.value.last_name} (${Customer.value.email})?`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, delete it',
            cancelButtonText: 'Cancel',
            customClass: {
                confirmButton: 'error-button',
                cancelButton: 'success-button'
            },
            reverseButtons: true,
        });

        if (!Confirmation.isConfirmed) return;

        const Success = await DeleteCustomer(Customer.value.id);

        if (!Success) return;

        await HandleSuccess(
            'Customer record has been successfully deleted.',
            'Record Delete Successful!'
        );

        Router.back();

    };



    const FetchCustomerDetails = async (
        customerId: number,
    ): Promise<void> => {

        IsLoading.value = true;
        ErrorMessage.value = null;
        Customer.value = null;

        try {
            if (!Number.isInteger(customerId) || customerId <= 0) {
                ErrorMessage.value = 'Invalid customer ID.';
                return;
            }

            const Result = await GetCustomer(customerId);

            if (Result === null) {
                ErrorMessage.value = 'Unable to load customer details.';
                return;
            }

            Customer.value = Result;

        } catch (error) {
            console.error('Failed to fetch customer details:', error);

            ErrorMessage.value =
                error instanceof Error
                    ? error.message
                    : 'Unable to load customer details.';

        } finally {

            IsLoading.value = false;

        }
    };

    
    const IsAdmin = computed<boolean>(() => {
        return currentUser.value?.role === 'admin';
    });

    watch(
        CustomerId,
        async (id) => {
            await FetchCustomerDetails(id);
        },
        { immediate: true }
    );

</script>

<template>
    <section class="Customer-Details">

        <!-- Loading -->
        <p v-if="IsLoading">
            Loading customer details...
        </p>

        <!-- Error -->
        <div
            v-else-if="ErrorMessage"
            class="Customer-Details-Error"
        >
            <h2>Unable to Load Customer.</h2>
            <p>{{ ErrorMessage }}</p>
        </div>

        <!-- Details -->
        <template v-else-if="Customer">

            <!-- Header -->
            <header class="Customer-Details-Header">
                <div>
                    <h1>
                        {{ Customer.first_name }}
                        {{ Customer.last_name }}
                    </h1>

                    <p>
                        Customer ID:
                        <strong>{{ CustomerId }}</strong>
                    </p>
                </div>

                <!-- Customer Actions -->
                <div class="Customer-Details-Actions">

                    <button
                        type="button"
                        class="Update-Customer-Button"
                        @click="StartEditing"
                    >
                        Update Customer
                    </button>

                    <button
                        v-if="IsAdmin"
                        type="button"
                        class="Delete-Customer-Button"
                        :disabled="IsUpdating"
                        @click="DeleteCurrentCustomer"
                    >
                        Delete Customer
                    </button>

                </div>
            </header>

            <!-- Update Customer Form -->
            <Transition name="form-transition">
                <div
                    v-if="IsEditing"
                    class="Form-Panel"
                >

                    <div class="Modal-Header">
                        <div>
                            <h2>Update Customer</h2>

                            <p>
                                Update the customer's information.
                            </p>
                        </div>

                        <button
                            type="button"
                            class="Modal-Close"
                            :disabled="IsUpdating"
                            @click="IsEditing = false"
                        >
                            ×
                        </button>
                    </div>

                    <form @submit.prevent="SaveChanges">

                        <div class="Form-Field">
                            <label for="customer-first-name">
                                First Name
                            </label>

                            <input
                                id="customer-first-name"
                                v-model="EditForm.first_name"
                                type="text"
                                placeholder="e.g. John"
                                autocomplete="given-name"
                                required
                            />
                        </div>

                        <div class="Form-Field">
                            <label for="customer-last-name">
                                Last Name
                            </label>

                            <input
                                id="customer-last-name"
                                v-model="EditForm.last_name"
                                type="text"
                                placeholder="e.g. Doe"
                                autocomplete="family-name"
                                required
                            />
                        </div>

                        <div class="Form-Field">
                            <label for="customer-email">
                                Email
                            </label>

                            <input
                                id="customer-email"
                                v-model="EditForm.email"
                                type="email"
                                placeholder="e.g. johndoe@gmail.com"
                                autocomplete="email"
                                required
                            />
                        </div>

                        <div class="Form-Field">
                            <label for="customer-phone">
                                Phone Number
                            </label>

                            <input
                                id="customer-phone"
                                v-model="EditForm.phone_number"
                                type="tel"
                                placeholder="e.g. 09123456789"
                                autocomplete="tel"
                                required
                            />
                        </div>

                        <div class="Modal-Actions">

                            <button
                                type="button"
                                class="Modal-Cancel-Button"
                                :disabled="IsUpdating"
                                @click="IsEditing = false"
                            >
                                Cancel
                            </button>

                            <button
                                type="submit"
                                class="Modal-Confirm-Button"
                                :disabled="IsUpdating"
                            >
                                {{
                                    IsUpdating
                                        ? 'Updating Customer...'
                                        : 'Update Customer'
                                }}
                            </button>

                        </div>

                    </form>
                </div>
            </Transition>

            <!-- Customer Information -->
            <section class="Customer-Information-Details">
                <h2>Customer Information</h2>

                <dl>
                    <div>
                        <dt>Customer ID</dt>
                        <dd>{{ CustomerId }}</dd>
                    </div>

                    <div>
                        <dt>First Name</dt>
                        <dd>{{ Customer.first_name }}</dd>
                    </div>

                    <div>
                        <dt>Last Name</dt>
                        <dd>{{ Customer.last_name }}</dd>
                    </div>

                    <div>
                        <dt>Full Name</dt>
                        <dd>
                            {{ Customer.first_name }}
                            {{ Customer.last_name }}
                        </dd>
                    </div>
                </dl>
            </section>

            <!-- Contact Information -->
            <section class="Customer-Contact-Details">
                <h2>Contact Information</h2>

                <dl>
                    <div>
                        <dt>Email Address</dt>
                        <dd>{{ Customer.email }}</dd>
                    </div>

                    <div>
                        <dt>Phone Number</dt>
                        <dd>{{ Customer.phone_number }}</dd>
                    </div>
                </dl>
            </section>

            <!-- Account Information -->
            <section class="Customer-Account-Details">
                <h2>Record Information</h2>

                <dl>
                    <div>
                        <dt>Customer ID</dt>
                        <dd>{{ CustomerId }}</dd>
                    </div>

                    <div>
                        <dt>Created Date</dt>
                        <dd>
                            {{ FormatDate(Customer.created_at).toLocaleString() }}
                        </dd>
                    </div>
                </dl>
            </section>

        </template>

    </section>
</template>