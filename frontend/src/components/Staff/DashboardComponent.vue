<script setup lang="ts">
    import { onMounted } from "vue";
    import { useRouter } from "vue-router";
    import { useDashboard } from "@/services/useDashboard";
    import { FormatDate } from "@/helper/DateFormatter";
import Router from "@/router/Router";

    const router = useRouter();

    const {
        statistics,
        recentRequests,
        isLoading,
        error,
        fetchDashboard,
    } = useDashboard();

    onMounted(fetchDashboard);

    function GoToNewRequest() {
        router.push({ name: "Staff New Service Request" });
    }

    function GoToRequests() {
        router.push({ name: "Staff Service Requests" });
    }

    const GoToServiceRequestDetail = (id: number): void => {
        Router.push({
            name: "Staff Service Request Details",
            params: {
                id: id
            }
        });
    }

    function GoToCustomers() {
        router.push({ name: "Staff Customers Management" });
    }

    function GoToSpareParts() {
        router.push({ name: "Staff Inventory Reference" });
    }

    function GetStatusClass(status: string): string {
        const normalizedStatus = status
            .toLowerCase()
            .replaceAll("_", " ")
            .trim();

        switch (normalizedStatus) {
            case "pending":
                return "Status-Pending";

            case "in progress":
            case "ongoing":
                return "Status-Ongoing";

            case "for further inspection":
                return "Status-Diagnosing";

            case "completed":
                return "Status-Completed";

            case "unsuccessful":
                return "Status-Unsuccessful";

            default:
                return "";
        }
    }

</script>



<template>
    <div class="Staff-Dashboard">
        <!-- Dashboard Header -->
        <section class="Staff-Dashboard-Header">
            <div>
                <h1>Dashboard</h1>
                <p>Overview of your service requests.</p>
            </div>

             <button
                type="button"
                class="View-All-Button"
                :disabled="isLoading"
                @click="fetchDashboard"
            >
                {{ isLoading ? "Refreshing..." : "Refresh" }}
            </button>
        </section>

        <!-- Request Statistics -->
        <section class="Staff-Statistics-Grid">
            <div class="Staff-Statistic-Card">
                <div class="Staff-Statistic-Icon">⏳</div>

                <div class="Staff-Statistic-Content">
                    <span class="Staff-Statistic-Label">
                        Pending Requests
                    </span>

                    <strong class="Staff-Statistic-Value">
                        {{ statistics?.pending ?? "—" }}
                    </strong>
                </div>
            </div>

            <div class="Staff-Statistic-Card">
                <div class="Staff-Statistic-Icon">🔧</div>

                <div class="Staff-Statistic-Content">
                    <span class="Staff-Statistic-Label">
                        Ongoing Requests
                    </span>

                    <strong class="Staff-Statistic-Value">
                        {{ statistics?.in_progress ?? "—" }}
                    </strong>
                </div>
            </div>

            <div class="Staff-Statistic-Card">
                <div class="Staff-Statistic-Icon">✓</div>

                <div class="Staff-Statistic-Content">
                    <span class="Staff-Statistic-Label">
                        Completed Requests
                    </span>

                    <strong class="Staff-Statistic-Value">
                        {{ statistics?.completed ?? "—" }}
                    </strong>
                </div>
            </div>
        </section>

        <!-- Main Content -->
        <section class="Staff-Dashboard-Grid">
            <!-- Recent Requests -->
            <div class="Staff-Dashboard-Card Staff-Recent-Requests">
                <div class="Staff-Card-Header">
                    <div>
                        <h2>Recent Service Requests</h2>
                        <p>Recently assigned service requests.</p>
                    </div>
                </div>

                <div
                    v-if="isLoading"
                    class="Staff-Dashboard-Empty"
                >
                    Loading service requests...
                </div>

                <div
                    v-else-if="error"
                    class="Staff-Dashboard-Empty"
                >
                    <p>{{ error }}</p>

                    <button @click="fetchDashboard">
                        Try Again
                    </button>
                </div>

                <!-- Scrollable Request Table -->
                <div
                    v-else-if="recentRequests.length"
                    class="Staff-Request-Table"
                >
                    <div class="Staff-Table-Header">
                        <span>Request</span>
                        <span>Customer</span>
                        <span>Created</span>
                        <span>Status</span>
                    </div>

                    <div
                        v-for="request in recentRequests"
                        :key="request.id"
                        class="Staff-Table-Row"
                    >
                        <div class="Staff-Request-Cell">
                            <strong>#{{ request.id }}</strong>
                            <small>{{ request.device }}</small>
                        </div>

                        <div class="Staff-Request-Cell">
                            <span>{{ request.customer }}</span>
                        </div>

                        <div class="Staff-Request-Cell">
                            <small>
                                {{ FormatDate(request.created_at).toLocaleString() }}
                            </small>
                        </div>

                        <div class="Staff-Request-Cell Staff-Request-Status-Cell">
                            <span
                                class="Staff-Request-Status"
                                :class="GetStatusClass(request.status)"
                            >
                                {{ request.status }}
                            </span>

                            <button
                                class="Staff-Open-Request-Button"
                                aria-label="Open service request"
                                @click="GoToServiceRequestDetail(request.id)"
                            >
                                →
                            </button>
                        </div>
                    </div>
                </div>

                <div
                    v-else
                    class="Staff-Dashboard-Empty"
                >
                    No recent service requests found.
                </div>
            </div>

            <!-- Quick Actions -->
            <div class="Staff-Dashboard-Card Staff-Quick-Actions">
                <div class="Staff-Card-Header">
                    <div>
                        <h2>Quick Actions</h2>
                        <p>Commonly used actions.</p>
                    </div>
                </div>

                <div class="Staff-Action-List">
                    <button
                        class="Staff-Action-Button"
                        @click="GoToNewRequest"
                    >
                        <span class="Staff-Action-Icon">+</span>
                        <span>New Service Request</span>
                    </button>

                    <button
                        class="Staff-Action-Button"
                        @click="GoToRequests"
                    >
                        <span class="Staff-Action-Icon">🔧</span>
                        <span>Active Requests</span>
                    </button>

                    <button
                        class="Staff-Action-Button"
                        @click="GoToCustomers"
                    >
                        <span class="Staff-Action-Icon">👥</span>
                        <span>Customers</span>
                    </button>

                    <button
                        class="Staff-Action-Button"
                        @click="GoToSpareParts"
                    >
                        <span class="Staff-Action-Icon">📦</span>
                        <span>Spare Parts</span>
                    </button>
                </div>
            </div>
        </section>
    </div>
</template>


