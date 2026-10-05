<script setup lang="ts">
import { ref } from 'vue';


interface ServiceRequest {
    id: number;
    device: string;
    customer: string;
    status: string;
    created_at: string;
}


const PendingRequests = ref<number>(12);
const OngoingRequests = ref<number>(5);
const CompletedRequests = ref<number>(28);


const RecentRequests = ref<ServiceRequest[]>([
    {
        id: 102,
        device: 'Samsung Refrigerator',
        customer: 'Juan Dela Cruz',
        status: 'Pending',
        created_at: '10 minutes ago'
    },
    {
        id: 101,
        device: 'LG Air Conditioner',
        customer: 'Maria Santos',
        status: 'Diagnosing',
        created_at: '35 minutes ago'
    },
    {
        id: 100,
        device: 'Panasonic Television',
        customer: 'Pedro Reyes',
        status: 'Completed',
        created_at: '1 hour ago'
    },
    {
        id: 99,
        device: 'Samsung Washing Machine',
        customer: 'Ana Reyes',
        status: 'Ongoing',
        created_at: '2 hours ago'
    }
]);


const GetStatusClass = (status: string): string => {

    switch (status) {

        case 'Pending':
            return 'Status-Pending';

        case 'Diagnosing':
            return 'Status-Diagnosing';

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

    <div class="Dashboard">

        <!-- =========================================
             Dashboard Header
        ========================================== -->

        <section class="Dashboard-Header">

            <div>

                <h1>
                    Dashboard
                </h1>

                <p>
                    Overview of your service requests.
                </p>

            </div>


            <button class="Create-Request-Button">
                + New Service Request
            </button>

        </section>



        <!-- =========================================
             Request Statistics
        ========================================== -->

        <section class="Statistics-Grid">

            <!-- Pending -->

            <div class="Statistic-Card">

                <div class="Statistic-Icon">
                    <img src="@/assets/Images/Dashboard-icons/pending.png" alt="Pending Logo">
                </div>

                <div class="Statistic-Content">

                    <span class="Statistic-Label">
                        Pending Requests
                    </span>

                    <strong class="Statistic-Value">
                        {{ PendingRequests }}
                    </strong>

                </div>

            </div>


            <!-- Ongoing -->

            <div class="Statistic-Card">

                <div class="Statistic-Icon">
                    🔧
                </div>

                <div class="Statistic-Content">

                    <span class="Statistic-Label">
                        Ongoing Requests
                    </span>

                    <strong class="Statistic-Value">
                        {{ OngoingRequests }}
                    </strong>

                </div>

            </div>


            <!-- Completed -->

            <div class="Statistic-Card">

                <div class="Statistic-Icon">
                    ✓
                </div>

                <div class="Statistic-Content">

                    <span class="Statistic-Label">
                        Completed Requests
                    </span>

                    <strong class="Statistic-Value">
                        {{ CompletedRequests }}
                    </strong>

                </div>

            </div>

        </section>



        <!-- =========================================
             Main Content
        ========================================== -->

        <section class="Dashboard-Grid">


            <!-- =====================================
                 Recent Requests
            ====================================== -->

            <div class="Dashboard-Card Recent-Requests">

                <div class="Card-Header">

                    <div>

                        <h2>
                            Recent Service Requests
                        </h2>

                        <p>
                            Recently created service requests.
                        </p>

                    </div>


                    <button class="View-All-Button">
                        View All
                    </button>

                </div>



                <!-- Request List -->

                <div class="Request-List">

                    <div
                        v-for="request in RecentRequests"
                        :key="request.id"
                        class="Request-Item"
                    >

                        <!-- Request Information -->

                        <div class="Request-Information">

                            <div class="Request-Number">
                                #{{ request.id }}
                            </div>


                            <div class="Request-Details">

                                <strong>
                                    {{ request.device }}
                                </strong>

                                <span>
                                    {{ request.customer }}
                                </span>

                                <small>
                                    {{ request.created_at }}
                                </small>

                            </div>

                        </div>



                        <!-- Request Status -->

                        <div class="Request-Action">

                            <span
                                class="Request-Status"
                                :class="GetStatusClass(request.status)"
                            >
                                {{ request.status }}
                            </span>


                            <button class="Open-Request-Button">
                                →
                            </button>

                        </div>

                    </div>

                </div>

            </div>



            <!-- =====================================
                 Quick Actions
            ====================================== -->

            <div class="Dashboard-Card Quick-Actions">

                <div class="Card-Header">

                    <div>

                        <h2>
                            Quick Actions
                        </h2>

                        <p>
                            Commonly used actions.
                        </p>

                    </div>

                </div>



                <div class="Action-List">

                    <button class="Action-Button">

                        <span class="Action-Icon">
                            +
                        </span>

                        <span>
                            New Service Request
                        </span>

                    </button>


                    <button class="Action-Button">

                        <span class="Action-Icon">
                            🔧
                        </span>

                        <span>
                            Active Requests
                        </span>

                    </button>


                    <button class="Action-Button">

                        <span class="Action-Icon">
                            👥
                        </span>

                        <span>
                            Customers
                        </span>

                    </button>


                    <button class="Action-Button">

                        <span class="Action-Icon">
                            📦
                        </span>

                        <span>
                            Spare Parts
                        </span>

                    </button>

                </div>

            </div>

        </section>



        <!-- =========================================
             AI Diagnosis
        ========================================== -->

        <section class="Dashboard-Card AI-Overview">

            <div class="Card-Header">

                <div>

                    <h2>
                        AI Diagnosis
                    </h2>

                    <p>
                        Overview of recent AI-assisted diagnostics.
                    </p>

                </div>


                <span class="AI-Badge">
                    AI Powered
                </span>

            </div>



            <div class="AI-Statistics">


                <div class="AI-Statistic">

                    <span>
                        Diagnoses Generated
                    </span>

                    <strong>
                        36
                    </strong>

                </div>


                <div class="AI-Statistic">

                    <span>
                        Pending Review
                    </span>

                    <strong>
                        4
                    </strong>

                </div>


                <div class="AI-Statistic">

                    <span>
                        Recommended Parts
                    </span>

                    <strong>
                        18
                    </strong>

                </div>


            </div>

        </section>

    </div>

</template>