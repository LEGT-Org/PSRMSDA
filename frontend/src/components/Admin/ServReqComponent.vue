<script setup lang="ts"></script>

<template>

    <section class="Service-Requests">

        <!-- Header -->
        <header class="Service-Requests-Header">

            <div>
                <h1>Service Requests</h1>

                <p>
                    View and manage service requests.
                </p>
            </div>

            <button class="Create-Request-Button">
                + New Service Request
            </button>

        </header>


        <!-- Filters -->
        <div class="Request-Filters">

            <input
                type="text"
                placeholder="Search requests..."
                class="Request-Search"
            />

            <select class="Request-Filter">
                <option value="">All Status</option>
                <option value="Pending">Pending</option>
                <option value="In Progress">In Progress</option>
                <option value="For Further Inspection">For Further Inspection</option>
                <option value="Completed">Completed</option>
                <option value="Unsuccessful">Unsuccessful</option>
            </select>

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
                        <th>Created</th>
                        <th>Status</th>
                        <th></th>
                    </tr>

                </thead>


                <tbody>

                    <tr>

                        <td>
                            <strong>#128</strong>
                        </td>

                        <td>
                            Juan Dela Cruz
                        </td>

                        <td>
                            <div class="Device-Cell">
                                <strong>Refrigerator</strong>
                                <small>Samsung RT38K553ASL</small>
                            </div>
                        </td>

                        <td>
                            John Smith
                        </td>

                        <td>
                            Oct 5, 2026
                        </td>

                        <td>
                            <span class="Request-Status Status-Ongoing">
                                Ongoing
                            </span>
                        </td>

                        <td>
                            <button class="View-Request-Button">
                                →
                            </button>
                        </td>

                    </tr>


                    <tr>

                        <td>
                            <strong>#127</strong>
                        </td>

                        <td>
                            Maria Santos
                        </td>

                        <td>
                            <div class="Device-Cell">
                                <strong>Air Conditioner</strong>
                                <small>Daikin FTKF35</small>
                            </div>
                        </td>

                        <td>
                            Mark Cruz
                        </td>

                        <td>
                            Oct 4, 2026
                        </td>

                        <td>
                            <span class="Request-Status Status-Pending">
                                Pending
                            </span>
                        </td>

                        <td>
                            <button class="View-Request-Button">
                                →
                            </button>
                        </td>

                    </tr>


                    <tr>

                        <td>
                            <strong>#126</strong>
                        </td>

                        <td>
                            Pedro Reyes
                        </td>

                        <td>
                            <div class="Device-Cell">
                                <strong>Washing Machine</strong>
                                <small>LG T2108</small>
                            </div>
                        </td>

                        <td>
                            John Smith
                        </td>

                        <td>
                            Oct 4, 2026
                        </td>

                        <td>
                            <span class="Request-Status Status-Completed">
                                Completed
                            </span>
                        </td>

                        <td>
                            <button class="View-Request-Button">
                                →
                            </button>
                        </td>

                    </tr>


                    <tr>

                        <td>
                            <strong>#125</strong>
                        </td>

                        <td>
                            Ana Garcia
                        </td>

                        <td>
                            <div class="Device-Cell">
                                <strong>Refrigerator</strong>
                                <small>Panasonic NR-BX</small>
                            </div>
                        </td>

                        <td>
                            Mark Cruz
                        </td>

                        <td>
                            Oct 3, 2026
                        </td>

                        <td>
                            <span class="Request-Status Status-Diagnosing">
                                Diagnosing
                            </span>
                        </td>

                        <td>
                            <button class="View-Request-Button">
                                →
                            </button>
                        </td>

                    </tr>

                </tbody>

            </table>

        </div>


        <!-- Pagination -->
        <div class="Request-Pagination">

            <button disabled>
                ←
            </button>

            <button class="Pagination-Active">
                1
            </button>

            <button>
                2
            </button>

            <button>
                3
            </button>

            <button>
                4
            </button>

            <button>
                5
            </button>

            <button>
                →
            </button>

        </div>

    </section>

</template>