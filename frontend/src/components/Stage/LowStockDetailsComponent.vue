<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { ApiFetch } from "@/api/Client";
import { FormatDate } from "@/helper/DateFormatter";

interface LowStockPart {
    part_id: number;
    part_name: string;
    stock_quantity: number;
}

interface LowStockAlert {
    id: number;
    request_id: number | null;
    part_id: number | null;
    part_name_snapshot: string | null;
    low_stock_parts_snapshot: LowStockPart[] | null;
    alert_type: string;
    alert_message: string | null;
    is_resolved: boolean;
    created_at: string;
}

const route = useRoute();
const router = useRouter();

const alert = ref<LowStockAlert | null>(null);
const isLoading = ref<boolean>(false);
const error = ref<string | null>(null);

const lowStockParts = computed(() => {
    return alert.value?.low_stock_parts_snapshot ?? [];
});

const totalLowStockParts = computed(() => {
    return lowStockParts.value.length;
});

const totalRemainingStock = computed(() => {
    return lowStockParts.value.reduce(
        (total, part) => total + part.stock_quantity,
        0
    );
});

async function FetchLowStockAlert(): Promise<void> {
    isLoading.value = true;
    error.value = null;

    try {
        const alertId = Number(route.params.id);

        if (!Number.isInteger(alertId) || alertId <= 0) {
            throw new Error("Invalid procurement alert ID.");
        }

        const response = await ApiFetch(
            `/procurement-alerts/${alertId}`
        );

        const result = await response.json() as
            LowStockAlert & { detail?: string };

        console.log("API STATUS:", response.status);
        console.log("API RESPONSE:", result);
        console.log("ALERT TYPE:", result.alert_type);

        if (!response.ok) {
            throw new Error(
                result.detail ?? "Failed to retrieve procurement alert."
            );
        }

        if (result.alert_type !== "Insufficient Stock") {
            throw new Error(
                "The selected procurement alert is not an insufficient-stock alert."
            );
        }

        alert.value = result;

    } catch (err) {
        error.value = err instanceof Error
            ? err.message
            : "An unexpected error occurred.";

    } finally {
        isLoading.value = false;
    }
}

function GoBack(): void {
    router.push({
        name: "Admin Procurement Alert Management"
    });
}

onMounted(FetchLowStockAlert);
</script>

<template>
    <div class="Low-Stock-Details-Page">

        <!-- Page Header -->

        <div class="Page-Header">
            <div>
                <h1>Low Stock Details</h1>
                <p>
                    Review spare parts that require inventory attention.
                </p>
            </div>

            <button
                type="button"
                class="Back-Button"
                @click="GoBack"
            >
                ← Back to Alerts
            </button>
        </div>

        <!-- Loading State -->

        <div
            v-if="isLoading"
            class="Loading-State"
        >
            <p>Loading low-stock details...</p>
        </div>

        <!-- Error State -->

        <div
            v-else-if="error"
            class="Error-State"
        >
            <h3>Unable to Load Low Stock Details</h3>
            <p>{{ error }}</p>

            <button
                type="button"
                class="Retry-Button"
                @click="FetchLowStockAlert"
            >
                Try Again
            </button>
        </div>

        <!-- Alert Details -->

        <template v-else-if="alert">

            <!-- Summary -->

            <div class="Low-Stock-Summary">

                <div class="Low-Stock-Summary-Card">
                    <span>Low-Stock Spare Parts</span>
                    <strong>{{ totalLowStockParts }}</strong>
                    <small>Parts requiring attention</small>
                </div>

                <div class="Low-Stock-Summary-Card">
                    <span>Total Remaining Stock</span>
                    <strong>{{ totalRemainingStock }}</strong>
                    <small>Units across affected spare parts</small>
                </div>

                <div class="Low-Stock-Summary-Card">
                    <span>Alert Status</span>

                    <strong
                        :class="alert.is_resolved
                            ? 'Status-Resolved'
                            : 'Status-Unresolved'"
                    >
                        {{ alert.is_resolved ? "Resolved" : "Unresolved" }}
                    </strong>

                    <small>Procurement alert #{{ alert.id }}</small>
                </div>

            </div>

            <!-- Alert Information -->

            <section class="Alert-Information">
                <h2>Alert Information</h2>

                <p>
                    {{ alert.alert_message }}
                </p>

                <small>
                    Date Created: {{ FormatDate(alert.created_at) }}
                </small>
            </section>

            <!-- Spare Parts Table -->

            <section class="Low-Stock-List">

                <div class="List-Header">
                    <div>
                        <h2>Affected Spare Parts</h2>
                        <p>
                            Spare parts included in this procurement alert.
                        </p>
                    </div>
                </div>

                <div
                    v-if="lowStockParts.length === 0"
                    class="Empty-State"
                >
                    <h3>No Spare Parts Found</h3>
                    <p>
                        This alert does not contain any spare part records.
                    </p>
                </div>

                <div
                    v-else
                    class="Table-Wrapper"
                >
                    <table class="Low-Stock-Table">

                        <thead>
                            <tr>
                                <th>Part ID</th>
                                <th>Spare Part Name</th>
                                <th>Remaining Stock</th>
                                <th>Stock Condition</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr
                                v-for="part in lowStockParts"
                                :key="part.part_id"
                            >
                                <td>#{{ part.part_id }}</td>

                                <td class="Part-Name">
                                    {{ part.part_name }}
                                </td>

                                <td>
                                    <strong>
                                        {{ part.stock_quantity }}
                                    </strong>
                                </td>

                                <td>
                                    <span :class="
                                        part.stock_quantity === 0
                                            ? 'Insufficient-Stock-Badge'
                                            : 'Low-Stock-Badge'
                                    ">
                                        {{
                                            part.stock_quantity === 0
                                                ? 'Out Of Stock'
                                                : 'Insufficient Stock'
                                        }}
                                    </span>
                                </td>
                            </tr>
                        </tbody>

                    </table>
                </div>

            </section>

        </template>

    </div>
</template>