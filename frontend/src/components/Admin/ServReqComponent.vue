<script setup lang="ts">
    import { ref, onMounted } from 'vue';
    import { useRouter } from 'vue-router';

    import { FormatDate } from '@/helper/DateFormatter';
    import { 
        GetServiceRequests, 
        ApplyServiceRequestFilters,
        HandleSearch
    } from '@/services/useServiceRequest';

    import {
        ServiceRequests,
        CurrentPage,
        ServiceRequestsPerPage,
        TotalPages,
        isLoadingServiceRequests,
        Search,
        StatusFilter,
        CreatedDate
    } from '@/services/state/ServiceRequest';


    const Router = useRouter();

    const GoToNextPage = async (): Promise<void> => {

        if (CurrentPage.value >= TotalPages.value) {
            return;
        }

        await GetServiceRequests(
            CurrentPage.value + 1,
            ServiceRequestsPerPage.value,
            Search.value,
            StatusFilter.value,
            CreatedDate.value
        );
        
    };


    const GoToPreviousPage = async (): Promise<void> => {

        if (CurrentPage.value <= 1) {
            return;
        }

        await GetServiceRequests(
            CurrentPage.value - 1,
            ServiceRequestsPerPage.value,
            Search.value,
            StatusFilter.value,
            CreatedDate.value
        );
        
    };


    const GoToNewServiceRequest = async (): Promise<void> => {
        await Router.push('/admin/request/new');
    };

    const GoToServiceRequestDetail = async (id: number): Promise<void> => {
        await Router.push(`/admin/request/${id}`);
    }


    onMounted(async () => {

        await GetServiceRequests(
            CurrentPage.value,
            ServiceRequestsPerPage.value,
            Search.value,
            StatusFilter.value,
            CreatedDate.value
        );

    });

</script>

<template>
    <section class="Service-Requests">

        <!-- Title -->
        <div class="Service-Requests-Title">
            <div>
                <h1>Service Request Management</h1>
                <p>
                    View and manage service requests.
                </p>
            </div>

            <button
                type="button"
                class="Create-Request-Button"   
                @click="GoToNewServiceRequest"
            >
                + New Service Request
            </button>
        </div>

        <!-- Filters -->
        <div class="Request-Filters">

            <div class="Search-Field">
                <label for="request-search">
                    Search
                </label>

                <input
                    id="request-search"
                    v-model="Search"
                    type="text"
                    placeholder="Search requests..."
                    @input="HandleSearch"
                />
            </div>

            <div class="Filter-Field">
                <label for="request-status-filter">
                    Status
                </label>

                <select
                    id="request-status-filter"
                    v-model="StatusFilter"
                    @change="ApplyServiceRequestFilters"
                >
                    <option value="">
                        All Status
                    </option>

                    <option value="Pending">
                        Pending
                    </option>

                    <option value="In Progress">
                        In Progress
                    </option>

                    <option value="For Further Inspection">
                        For Further Inspection
                    </option>

                    <option value="Completed">
                        Completed
                    </option>

                    <option value="Unsuccessful">
                        Unsuccessful
                    </option>
                </select>
            </div>

            <div class="Filter-Field">

                <label for="request-date-filter">
                    Date
                </label>

                <input
                    id="request-date-filter"
                    v-model="CreatedDate"
                    type="date"
                    class="Request-Filter"
                    @change="ApplyServiceRequestFilters"
                />
            </div>
        </div>

        <!-- Table -->
        <div class="Request-Table-Container">

            <table class="Request-Table">

                <thead>
                    <tr>
                        <th>Request</th>
                        <th>Customer</th>
                        <th>Device</th>
                        <th>Technician</th>
                        <th>Created Date</th>
                        <th>Status</th>
                        <th></th>
                    </tr>
                </thead>

                <tbody>
                    <tr
                        v-for="serviceRequest in ServiceRequests"
                        :key="serviceRequest.id"
                    >
                        <td>
                            <strong>SR-{{ serviceRequest.id }}</strong>
                        </td>

                        <td>
                            {{ serviceRequest.customer_name }}
                        </td>

                        <td>
                            <div class="Device-Cell">
                                <strong>
                                    {{ serviceRequest.device_type }}
                                </strong>

                                <small>
                                    {{ serviceRequest.device_brand }}
                                    {{ serviceRequest.device_model }}
                                </small>
                            </div>
                        </td>

                        <td>
                            {{ serviceRequest.technician_name }}
                        </td>

                        <td>
                            {{ FormatDate(serviceRequest.created_at) }}
                        </td>

                        <td>
                            <span
                                class="Request-Status"
                                :class="{
                                    'Status-Pending': serviceRequest.status === 'Pending',
                                    'Status-Diagnosed': serviceRequest.status === 'For Further Inspection',
                                    'Status-Ingoing': serviceRequest.status === 'In Progress',
                                    'Status-Completed': serviceRequest.status === 'Completed',
                                    'Status-Unsuccessful': serviceRequest.status === 'Unsuccessful'
                                }"
                            >
                                {{ serviceRequest.status }}
                            </span>
                        </td>

                        <td>
                            <button
                                type="button"
                                class="View-Request-Button"
                                @click="GoToServiceRequestDetail(serviceRequest.id)"
                            >
                                →
                            </button>
                        </td>
                    </tr>

                    <tr v-if="ServiceRequests.length === 0">
                        <td colspan="6">
                            <div class="Request-Empty-State">
                                <h3>No service requests found</h3>
                                <p>
                                    No service requests match your
                                    current search or filter.
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
                :disabled="
                    CurrentPage <= 1 ||
                    isLoadingServiceRequests
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
                    isLoadingServiceRequests
                "
                @click="GoToNextPage"
            >
                Next
            </button>

        </div>

    </section>
</template>