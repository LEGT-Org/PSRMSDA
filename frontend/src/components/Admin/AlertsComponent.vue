<script setup lang="ts">
import { computed, ref } from 'vue';

interface ProcurementAlert {
    id: number;
    request_id: number;
    part_id: number | null;
    part_name_snapshot: string | null;
    alert_type: string;
    alert_message: string;
    is_resolved: boolean;
    created_at: string;
}

type AlertFilter = 'all' | 'unresolved' | 'resolved';

const SearchQuery = ref('');
const SelectedFilter = ref<AlertFilter>('unresolved');

// Temporary demo data. Replace this with your API response.
const ProcurementAlerts = ref<ProcurementAlert[]>([
    {
        id: 1,
        request_id: 9,
        part_id: 3,
        part_name_snapshot: 'Capacitor 35uF',
        alert_type: 'FINALIZED_REQUEST',
        alert_message:
            "Spare part 'Capacitor 35uF' is out of stock after finalizing service request No. 9.",
        is_resolved: false,
        created_at: '2026-10-13T08:30:00',
    },
    {
        id: 2,
        request_id: 12,
        part_id: null,
        part_name_snapshot: null,
        alert_type: 'REQUEST_STAGE',
        alert_message:
            'Service request #12 has been finalized as Completed.',
        is_resolved: false,
        created_at: '2026-10-13T09:00:00',
    },
    {
        id: 3,
        request_id: 7,
        part_id: 5,
        part_name_snapshot: 'Thermostat',
        alert_type: 'FINALIZED_REQUEST',
        alert_message:
            "Spare part 'Thermostat' is out of stock after finalizing service request No. 7.",
        is_resolved: true,
        created_at: '2026-10-12T14:15:00',
    },
]);

const UnresolvedCount = computed(() =>
    ProcurementAlerts.value.filter(
        (Alert) => !Alert.is_resolved
    ).length
);

const ResolvedCount = computed(() =>
    ProcurementAlerts.value.filter(
        (Alert) => Alert.is_resolved
    ).length
);

const FilteredAlerts = computed(() => {
    const Query = SearchQuery.value.trim().toLowerCase();

    return ProcurementAlerts.value
        .filter((Alert) => {
            if (
                SelectedFilter.value === 'unresolved' &&
                Alert.is_resolved
            ) {
                return false;
            }

            if (
                SelectedFilter.value === 'resolved' &&
                !Alert.is_resolved
            ) {
                return false;
            }

            if (!Query) {
                return true;
            }

            return [
                Alert.alert_message,
                Alert.alert_type,
                Alert.part_name_snapshot ?? '',
                String(Alert.request_id),
            ].some((Value) => Value.toLowerCase().includes(Query));
        })
        .sort(
            (A, B) =>
                new Date(B.created_at).getTime() -
                new Date(A.created_at).getTime()
        );
});

const FormatAlertType = (Type: string): string => {
    return Type
        .toLowerCase()
        .split('_')
        .map((Word) => Word.charAt(0).toUpperCase() + Word.slice(1))
        .join(' ');
};

const FormatDate = (DateValue: string): string => {
    return new Date(DateValue).toLocaleString();
};

// Demo interaction only. Connect this to your backend later.
const ToggleResolved = (AlertId: number): void => {
    const Alert = ProcurementAlerts.value.find(
        (Item) => Item.id === AlertId
    );

    if (Alert) {
        Alert.is_resolved = !Alert.is_resolved;
    }
};
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
                <strong>{{ ProcurementAlerts.length }}</strong>
                <span class="Summary-Description">
                    All recorded notifications
                </span>
            </article>

            <article class="Summary-Card Unresolved-Summary">
                <span class="Summary-Label">Unresolved</span>
                <strong>{{ UnresolvedCount }}</strong>
                <span class="Summary-Description">
                    Requires attention
                </span>
            </article>

            <article class="Summary-Card Resolved-Summary">
                <span class="Summary-Label">Resolved</span>
                <strong>{{ ResolvedCount }}</strong>
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
                        v-model="SearchQuery"
                        type="search"
                        placeholder="Search alerts, parts, or request ID..."
                        aria-label="Search procurement alerts"
                        class="Alert-Search"
                    />

                </div>

                <div class="Filter-Field">

                    <label for="status-filter">
                        status
                    </label>

                    <select
                        id="status-filter"
                        v-model="SelectedFilter"
                        class="Alert-Filter-Select"
                        aria-label="Filter alerts by resolution"
                    >
                        <option value="all">All Alerts</option>
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
                                    {{ Alert.part_name_snapshot || 'Service Request Update' }}
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
                                    No. {{ Alert.request_id }}
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
                                <button
                                    type="button"
                                    class="Alert-Action-Button"
                                    :class="
                                        Alert.is_resolved
                                            ? 'Mark-Unresolved'
                                            : 'Mark-Resolved'
                                    "
                                    @click="ToggleResolved(Alert.id)"
                                >
                                    {{
                                        Alert.is_resolved
                                            ? 'Reopen'
                                            : 'Resolve'
                                    }}
                                </button>
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
        </section>
    </main>
</template>

