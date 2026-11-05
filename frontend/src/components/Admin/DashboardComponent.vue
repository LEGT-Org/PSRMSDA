<script setup lang="ts">
    import { onMounted } from "vue";
    import { useDashboard } from "@/services/useDashboard";
    import { FormatDate } from "@/helper/DateFormatter";
    import Router from "@/router/Router";

    const {
        statistics,
        totalCustomers,
        totalActiveUsers,
        totalLowStockParts,
        recentRequests,
        recentActivities,
        isLoading,
        error,
        fetchDashboard,
        CheckLowStock,
    } = useDashboard();

    onMounted(fetchDashboard);

    function GetStatusClass(status: string): string {
        const normalized = status.toLowerCase().replaceAll(" ", "-");

        const classes: Record<string, string> = {
            pending: "Status-Pending",
            diagnosing: "Status-Diagnosing",
            "in-progress": "Status-Ongoing",
            ongoing: "Status-Ongoing",
            "for-further-inspection": "Status-Diagnosing",
            completed: "Status-Completed",
        };

        return classes[normalized] ?? "";
    }

    const GoToServiceRequestDetail = (id: number): void => {
        Router.push({
            name: "Admin Service Request Details",
            params: {
                id: id
            }
        });
    }

</script>



<template>
    <div class="Admin-Dashboard">
        <section class="Dashboard-Header">
            <div>
                <h1>Admin Dashboard</h1>
                <p>System-wide overview and management.</p>
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

        <p v-if="error" class="Dashboard-Error" role="alert">
            {{ error }}
        </p>

        <!-- Main Statistics -->
        <section class="Statistics-Grid">
            <div class="Statistic-Card">
                <div class="Statistic-Icon">📋</div>
                <div class="Statistic-Content">
                    <span class="Statistic-Label">Total Requests</span>
                    <strong class="Statistic-Value">
                        {{ statistics?.total ?? "—" }}
                    </strong>
                </div>
            </div>

            <div class="Statistic-Card">
                <div class="Statistic-Icon">⏳</div>
                <div class="Statistic-Content">
                    <span class="Statistic-Label">Pending</span>
                    <strong class="Statistic-Value">
                        {{ statistics?.pending ?? "—" }}
                    </strong>
                </div>
            </div>

            <div class="Statistic-Card">
                <div class="Statistic-Icon">🔧</div>
                <div class="Statistic-Content">
                    <span class="Statistic-Label">Ongoing</span>
                    <strong class="Statistic-Value">
                        {{ statistics?.in_progress ?? "—" }}
                    </strong>
                </div>
            </div>

            <div class="Statistic-Card">
                <div class="Statistic-Icon">✓</div>
                <div class="Statistic-Content">
                    <span class="Statistic-Label">Completed</span>
                    <strong class="Statistic-Value">
                        {{ statistics?.completed ?? "—" }}
                    </strong>
                </div>
            </div>
        </section>

        <!-- System Overview -->
        <section class="Overview-Grid">
            <div class="Overview-Card">
                <span class="Overview-Label">Customers</span>
                <strong>{{ totalCustomers }}</strong>
                <small>Registered customers</small>
            </div>

            <div class="Overview-Card">
                <span class="Overview-Label">System Users</span>
                <strong>{{ totalActiveUsers }}</strong>
                <small>Active staff and administrators</small>
            </div>

            <div class="Overview-Card">
                <span class="Overview-Label">Low Stock</span>

                <strong>{{ totalLowStockParts }}</strong>

                <small>Parts requiring attention</small>

                <button
                    type="button"
                    class="Check-Stock-Button"
                    @click="CheckLowStock"
                >
                    Check Stock
                </button>
            </div>
        </section>

        <!-- Main Dashboard Grid -->
        <section class="Dashboard-Grid">
            <!-- Recent Service Requests -->
            <div class="Dashboard-Card">
                <div class="Card-Header">
                    <div>
                        <h2>Recent Service Requests</h2>
                        <p>Latest service requests across the system.</p>
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

                <div 
                    v-else-if="recentRequests.length"
                    class="Request-Table"
                >
                    <div class="Table-Header">
                        <span>Request</span>
                        <span>Customer</span>
                        <span>Technician</span>
                        <span>Status</span>
                    </div>

                    <div
                        v-if="isLoading && recentRequests.length === 0"
                        class="Dashboard-Empty"
                    >
                        Loading service requests...
                    </div>

                    <div
                        v-else-if="recentRequests.length === 0"
                        class="Dashboard-Empty"
                    >
                        No recent service requests found.
                    </div>

                    <div
                        v-for="request in recentRequests"
                        :key="request.id"
                        class="Table-Row"
                    >
                        <div class="Request-Cell">
                            <strong>#{{ request.id }}</strong>
                            <small>{{ request.device }}</small>
                        </div>

                        <span>{{ request.customer }}</span>

                        <span>{{ request.technician }}</span>

                        <span
                            class="Request-Status"
                            :class="GetStatusClass(request.status)"
                        >
                            {{ request.status }}
                        </span>

                        <span>
                            <button
                                class="Staff-Open-Request-Button"
                                aria-label="Open service request"
                                @click="GoToServiceRequestDetail(request.id)"
                            >
                                →
                            </button>
                            
                        </span>

                    </div>
                    
                </div>

            </div>


            <!-- Recent Activity -->
            <div class="Dashboard-Card">
                <div class="Card-Header">
                    <div>
                        <h2>Recent Activity</h2>
                        <p>Latest procurement alerts.</p>
                    </div>
                </div>

                <div
                    v-if="isLoading && recentActivities.length === 0"
                    class="Dashboard-Empty"
                >
                    Loading activities...
                </div>

                <div
                    v-else-if="recentActivities.length === 0"
                    class="Dashboard-Empty"
                >
                    No recent activities found.
                </div>

                <div v-else class="Activity-List">
                    <div
                        v-for="activity in recentActivities"
                        :key="activity.id"
                        class="Activity-Item"
                    >
                        <div class="Activity-Dot"></div>

                        <div class="Activity-Content">
                            <span>{{ activity.description }}</span>

                            <small>
                                {{ FormatDate(activity.time).toLocaleString() }}
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>




        <!-- =========================================
             AI + Inventory
        ========================================== -->

        <!-- <section class="Bottom-Grid">

            <div class="Dashboard-Card">

                <div class="Card-Header">

                    <div>

                        <h2>
                            AI Diagnosis
                        </h2>

                        <p>
                            AI-assisted diagnostic activity.
                        </p>

                    </div>


                    <span class="AI-Badge">
                        AI Powered
                    </span>

                </div>


                <div class="AI-Statistics">

                    <div>

                        <span>
                            Diagnoses Generated
                        </span>

                        <strong>
                            {{ TotalDiagnoses }}
                        </strong>

                    </div>


                    <div>

                        <span>
                            Pending Review
                        </span>

                        <strong>
                            {{ PendingDiagnoses }}
                        </strong>

                    </div>


                    <div>

                        <span>
                            Recommended Parts
                        </span>

                        <strong>
                            {{ RecommendedParts }}
                        </strong>

                    </div>

                </div>

            </div>

            <div class="Dashboard-Card">

                <div class="Card-Header">

                    <div>

                        <h2>
                            Inventory
                        </h2>

                        <p>
                            Spare-part inventory status.
                        </p>

                    </div>

                </div>


                <div class="Inventory-Overview">

                    <div class="Inventory-Number">

                        <strong>
                            {{ LowStockParts }}
                        </strong>

                        <span>
                            Low-stock parts
                        </span>

                    </div>


                    <button class="Inventory-Button">
                        Manage Inventory
                    </button>

                </div>

            </div>

        </section> -->