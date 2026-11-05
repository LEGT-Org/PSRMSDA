<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';

import { FormatAlertType } from '@/helper/SymptomsParser';
import { FormatDate } from '@/helper/DateFormatter';
import {
    GetProcurementAlerts,
    ApplyProcurementAlertFilters,
    HandleSearch,
    UpdateProcurementAlertResolution,
} from '@/services/useProcurementAlert';

import {
    ProcurementAlerts,
    CurrentPage,
    ProcurementAlertsPerPage,
    TotalAlerts,
    UnresolvedAlerts,
    ResolvedAlerts,
    IsLoading,
    TotalPages,
    Total,
    Search,
    StatusFilter,
    TypeFilter,
} from '@/services/state/ProcurementAlert';


const router = useRouter();

// The backend already handles searching and filtering.
const FilteredAlerts = computed(() => ProcurementAlerts.value);


const GetAlerts = async (): Promise<void> => {

    const Response = await GetProcurementAlerts(
        CurrentPage.value,
        ProcurementAlertsPerPage.value,
        Search.value,
        StatusFilter.value,
        TypeFilter.value
    );

    if (!Response) {
        return;
    }

    ProcurementAlerts.value = Response.items;
    Total.value = Response.total;
    TotalPages.value = Response.pages;
    CurrentPage.value = Response.page;

};


const ToggleResolved = async (AlertId: number): Promise<void> => {

    const Alert = ProcurementAlerts.value.find((Item) => Item.id === AlertId);

    if (!Alert) {
        return;
    }

    const Success = await UpdateProcurementAlertResolution(
        AlertId,
        !Alert.is_resolved,
    );

    if (Success) {
        await GetAlerts();
    }

};


const GoToNextPage = async () => {

    if (CurrentPage.value >= TotalPages.value) return;

    await GetProcurementAlerts(
        CurrentPage.value + 1,
        ProcurementAlertsPerPage.value,
        Search.value,
        StatusFilter.value,
        TypeFilter.value
    );

};


const GoToPreviousPage = async () => {

    if (CurrentPage.value <= 1) return;

    await GetProcurementAlerts(
        CurrentPage.value - 1,
        ProcurementAlertsPerPage.value,
        Search.value,
        StatusFilter.value,
        TypeFilter.value
    );

};


const GoToLowStockDetail = (alertId: number)  => {
    router.push({
        name: 'Admin Low Stock Details',
        params: {
            id: alertId
        }
    });
}


onMounted(async () => {
    await GetAlerts();
});

</script>

<template>
    <main class="Procurement-Alert-Page">
        <!-- Page Header -->
        <header class="Page-Header">
            <div>
                <h1>Procurement Alerts</h1>
                <p>
                    Monitor inventory issues and service request
                    notifications.
                </p>
            </div>
        </header>

        <!-- Summary -->
        <section class="Alert-Summary">
            <article class="Summary-Card">
                <span class="Summary-Label">Total Alerts</span>
                <strong>{{ TotalAlerts }}</strong>
                <span class="Summary-Description">
                    All recorded notifications
                </span>
            </article>

            <article class="Summary-Card Unresolved-Summary">
                <span class="Summary-Label">Unresolved</span>
                <strong>{{ UnresolvedAlerts }}</strong>
                <span class="Summary-Description">
                    Requires attention
                </span>
            </article>

            <article class="Summary-Card Resolved-Summary">
                <span class="Summary-Label">Resolved</span>
                <strong>{{ ResolvedAlerts }}</strong>
                <span class="Summary-Description">
                    Already addressed
                </span>
            </article>
        </section>

        <!-- Alert List -->
        <section class="Alert-List-Section">
            <div class="Alert-List-Header">
                <div>
                    <h2>Alert History</h2>
                    <p>Review and manage procurement notifications.</p>
                </div>
            </div>

            <!-- Search and Filters -->
            <div class="Alert-Filters">
                
                <div class="Search-Field">

                    <label for="search-filter">
                        Search
                    </label>

                    <input
                        id="search-filter"
                        v-model="Search"
                        type="search"
                        placeholder="Search alerts, parts, or request ID..."
                        aria-label="Search procurement alerts"
                        class="Alert-Search"
                        @input="HandleSearch"
                    />

                </div>

                <div class="Filter-Field">

                    <label for="type-filter">
                        Type
                    </label>

                    <select
                        id="type-filter"
                        v-model="TypeFilter"
                        class="Alert-Filter-Select"
                        aria-label="Filter alerts by resolution"
                        @change="ApplyProcurementAlertFilters"
                    >
                        <option value="all">All Types</option>
                        <option value="Request Stage">Request Stage</option>
                        <option value="No Part Match">No Part Matched</option>
                        <option value="Part Not Found">Part Not Found</option>
                        <option value="Finalized Request">Finalized Request</option>
                        <option value="Insufficient Stock">Insufficient Stock</option>
                    </select>

                </div>

                <div class="Filter-Field">

                    <label for="status-filter">
                        Status
                    </label>

                    <select
                        id="status-filter"
                        v-model="StatusFilter"
                        class="Alert-Filter-Select"
                        aria-label="Filter alerts by resolution"
                        @change="ApplyProcurementAlertFilters"
                    >
                        <option value="all">All Status</option>
                        <option value="unresolved">Unresolved</option>
                        <option value="resolved">Resolved</option>
                    </select>

                </div>
            </div>

            <!-- Table -->
            <div class="Alert-Table-Wrapper">
                <table class="Alert-Table">
                    <thead>
                        <tr>
                            <th>Alert</th>
                            <th>Type</th>
                            <th>Request</th>
                            <th>Date Created</th>
                            <th>Status</th>
                            <th>Action</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr
                            v-for="Alert in FilteredAlerts"
                            :key="Alert.id"
                        >
                            <td class="Alert-Message-Cell">
                                <strong>
                                    {{
                                        Alert.part_name_snapshot
                                            ? Alert.part_name_snapshot
                                            : Alert.alert_type === 'Finalized Request'
                                                ? 'Service Request Finalization'
                                                : Alert.alert_type === 'Insufficient Stock'
                                                    ? 'Insufficient Stock Alert'
                                                    : Alert.alert_type === 'No Part Match' 
                                                        || Alert.alert_type === 'Part Not Found'
                                                    ? 'Spare Part Unavailable Alert'
                                                    : 'Service Request Update' 
                                    }}
                                </strong>

                                <p>{{ Alert.alert_message }}</p>
                            </td>

                            <td>
                                <span class="Alert-Type">
                                    {{ FormatAlertType(Alert.alert_type) }}
                                </span>
                            </td>

                            <td>
                                <span class="Alert-Request-ID">
                                    {{ 
                                        Alert.request_id 
                                            ? `No. ${Alert.request_id}` 
                                            : 'N/A'
                                    }}
                                </span>
                            </td>

                            <td>
                                <span class="Alert-Date">
                                    {{ FormatDate(Alert.created_at) }}
                                </span>
                            </td>

                            <td>
                                <span
                                    class="Alert-Status"
                                    :class="
                                        Alert.is_resolved
                                            ? 'Status-Resolved'
                                            : 'Status-Unresolved'
                                    "
                                >
                                    {{
                                        Alert.is_resolved
                                            ? 'Resolved'
                                            : 'Unresolved'
                                    }}
                                </span>
                            </td>

                            <td>
                                <div class="Alert-Action-Container">
                                    <button
                                        type="button"
                                        class="Alert-Action-Button"
                                        @click="ToggleResolved(Alert.id)"
                                        :disabled="Alert.is_resolved === true"
                                    >
                                        {{
                                            Alert.alert_type === 'Request Stage'
                                                ? 'Mark as Read'
                                                : 'Mark as Resolve'
                                        }}
                                    </button>

                                    <button
                                        v-if="Alert.alert_type === 'Insufficient Stock'
                                            && Alert.low_stock_parts_snapshot !== null
                                        "
                                        type="button"
                                        class="View-Request-Button"
                                        @click="GoToLowStockDetail(Alert.id)"
                                    >
                                        →
                                    </button>
                                </div>
                            </td>
                        </tr>

                        <tr v-if="FilteredAlerts.length === 0">
                            <td colspan="6">
                                <div class="Alert-Empty-State">
                                    <h3>No alerts found</h3>
                                    <p>
                                        No procurement alerts match your
                                        current search or filter.
                                    </p>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="Pagination">

            <button
                type="button"
                :disabled="
                    CurrentPage <= 1 || IsLoading
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
                    CurrentPage >= TotalPages || IsLoading
                "
                @click="GoToNextPage"
            >
                Next
            </button>

        </div>
        </section>
    </main>
</template>

