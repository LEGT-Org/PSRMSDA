<script setup lang="ts">
import { ref } from 'vue';


interface RecentRequest {
    id: number;
    customer: string;
    device: string;
    technician: string;
    status: string;
    created_at: string;
}


interface RecentActivity {
    id: number;
    description: string;
    time: string;
}


const TotalRequests = ref<number>(128);
const PendingRequests = ref<number>(23);
const OngoingRequests = ref<number>(14);
const CompletedRequests = ref<number>(91);

const TotalCustomers = ref<number>(84);
const TotalUsers = ref<number>(17);
const LowStockParts = ref<number>(6);

const TotalDiagnoses = ref<number>(36);
const PendingDiagnoses = ref<number>(4);
const RecommendedParts = ref<number>(18);


const RecentRequests = ref<RecentRequest[]>([
    {
        id: 128,
        customer: 'Juan Dela Cruz',
        device: 'Samsung Refrigerator',
        technician: 'Mark Santos',
        status: 'Pending',
        created_at: '10 minutes ago'
    },
    {
        id: 127,
        customer: 'Maria Santos',
        device: 'LG Air Conditioner',
        technician: 'John Reyes',
        status: 'Ongoing',
        created_at: '35 minutes ago'
    },
    {
        id: 126,
        customer: 'Pedro Reyes',
        device: 'Panasonic Television',
        technician: 'Mark Santos',
        status: 'Completed',
        created_at: '1 hour ago'
    },
    {
        id: 125,
        customer: 'Ana Cruz',
        device: 'Samsung Washing Machine',
        technician: 'Michael Tan',
        status: 'Completed',
        created_at: '2 hours ago'
    }
]);


const RecentActivities = ref<RecentActivity[]>([
    {
        id: 1,
        description: 'Service Request #128 was created',
        time: '10 minutes ago'
    },
    {
        id: 2,
        description: 'AI diagnosis generated for Request #127',
        time: '35 minutes ago'
    },
    {
        id: 3,
        description: 'Service Request #126 was completed',
        time: '1 hour ago'
    },
    {
        id: 4,
        description: 'New staff account was created',
        time: '2 hours ago'
    }
]);


const GetStatusClass = (status: string): string => {

    switch (status) {

        case 'Pending':
            return 'Status-Pending';

        case 'Ongoing':
            return 'Status-Ongoing';

        case 'Completed':
            return 'Status-Completed';

        default:
            return '';
    }
};
</script>


<template>

    <div class="Admin-Dashboard">

        <!-- =========================================
             Header
        ========================================== -->

        <section class="Dashboard-Header">

            <div>

                <h1>
                    Admin Dashboard
                </h1>

                <p>
                    System-wide overview and management.
                </p>

            </div>

        </section>



        <!-- =========================================
             Main Statistics
        ========================================== -->

        <section class="Statistics-Grid">

            <div class="Statistic-Card">

                <div class="Statistic-Icon">
                    📋
                </div>

                <div class="Statistic-Content">

                    <span class="Statistic-Label">
                        Total Requests
                    </span>

                    <strong class="Statistic-Value">
                        {{ TotalRequests }}
                    </strong>

                </div>

            </div>


            <div class="Statistic-Card">

                <div class="Statistic-Icon">
                    ⏳
                </div>

                <div class="Statistic-Content">

                    <span class="Statistic-Label">
                        Pending
                    </span>

                    <strong class="Statistic-Value">
                        {{ PendingRequests }}
                    </strong>

                </div>

            </div>


            <div class="Statistic-Card">

                <div class="Statistic-Icon">
                    🔧
                </div>

                <div class="Statistic-Content">

                    <span class="Statistic-Label">
                        Ongoing
                    </span>

                    <strong class="Statistic-Value">
                        {{ OngoingRequests }}
                    </strong>

                </div>

            </div>


            <div class="Statistic-Card">

                <div class="Statistic-Icon">
                    ✓
                </div>

                <div class="Statistic-Content">

                    <span class="Statistic-Label">
                        Completed
                    </span>

                    <strong class="Statistic-Value">
                        {{ CompletedRequests }}
                    </strong>

                </div>

            </div>

        </section>



        <!-- =========================================
             System Overview
        ========================================== -->

        <section class="Overview-Grid">

            <div class="Overview-Card">

                <span class="Overview-Label">
                    Customers
                </span>

                <strong>
                    {{ TotalCustomers }}
                </strong>

                <small>
                    Registered customers
                </small>

            </div>


            <div class="Overview-Card">

                <span class="Overview-Label">
                    System Users
                </span>

                <strong>
                    {{ TotalUsers }}
                </strong>

                <small>
                    Active staff and administrators
                </small>

            </div>


            <div class="Overview-Card">

                <span class="Overview-Label">
                    Low Stock
                </span>

                <strong>
                    {{ LowStockParts }}
                </strong>

                <small>
                    Parts requiring attention
                </small>

            </div>

        </section>



        <!-- =========================================
             Main Dashboard Grid
        ========================================== -->

        <section class="Dashboard-Grid">


            <!-- =====================================
                 Recent Requests
            ====================================== -->

            <div class="Dashboard-Card">

                <div class="Card-Header">

                    <div>

                        <h2>
                            Recent Service Requests
                        </h2>

                        <p>
                            Latest activity across the system.
                        </p>

                    </div>


                    <button class="View-All-Button">
                        View All
                    </button>

                </div>



                <div class="Request-Table">

                    <!-- Table Header -->

                    <div class="Table-Header">

                        <span>
                            Request
                        </span>

                        <span>
                            Customer
                        </span>

                        <span>
                            Technician
                        </span>

                        <span>
                            Status
                        </span>

                    </div>



                    <!-- Table Rows -->

                    <div
                        v-for="request in RecentRequests"
                        :key="request.id"
                        class="Table-Row"
                    >

                        <div class="Request-Cell">

                            <strong>
                                #{{ request.id }}
                            </strong>

                            <small>
                                {{ request.device }}
                            </small>

                        </div>


                        <span>
                            {{ request.customer }}
                        </span>


                        <span>
                            {{ request.technician }}
                        </span>


                        <span
                            class="Request-Status"
                            :class="GetStatusClass(request.status)"
                        >
                            {{ request.status }}
                        </span>

                    </div>

                </div>

            </div>



            <!-- =====================================
                 Recent Activity
            ====================================== -->

            <div class="Dashboard-Card">

                <div class="Card-Header">

                    <div>

                        <h2>
                            Recent Activity
                        </h2>

                        <p>
                            Latest system activity.
                        </p>

                    </div>

                </div>


                <div class="Activity-List">

                    <div
                        v-for="activity in RecentActivities"
                        :key="activity.id"
                        class="Activity-Item"
                    >

                        <div class="Activity-Dot"></div>

                        <div class="Activity-Content">

                            <span>
                                {{ activity.description }}
                            </span>

                            <small>
                                {{ activity.time }}
                            </small>

                        </div>

                    </div>

                </div>

            </div>

        </section>



        <!-- =========================================
             AI + Inventory
        ========================================== -->

        <section class="Bottom-Grid">


            <!-- AI Diagnosis -->

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



            <!-- Inventory -->

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

        </section>

    </div>

</template>