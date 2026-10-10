<script setup lang="ts">
    import { computed, onMounted, ref } from 'vue';
    import { useRoute } from 'vue-router';
    import { ApiFetch } from '@/api/Client';
    
    import type { 
        ServiceRequestDetail, 
        ServiceRequestStatus 
    } from '@/services/state/ServiceRequest';
    import { capitalizeFirstLetter } from '@/helper/Capitalize';


    const Route = useRoute();
    const SelectedStatus = ref<ServiceRequestStatus>('Pending');
    const PartsUsed = ref<boolean | null>(null);

    const ServiceRequestId = computed<number>(() =>
        Number(Route.params.id)
    );

    const IsLoading = ref<boolean>(true);
    const ErrorMessage = ref<string | null>(null);

    const ServiceRequest = ref<ServiceRequestDetail | null>(null);

    const IsRequestClosed = computed<boolean>(() =>
        ['Completed', 'Unsuccessful'].includes(
            ServiceRequest.value?.status ?? ''
        )
    );

    const UpdateServiceRequestStatus = async () => {
        // Call your API to update the service request status.
    }

    const UpdatePartsUsage = async (used: boolean) => {
        // Call your API to record whether requested parts were used.
    }

    const FetchServiceRequest = async (value: number): Promise<void> => {

        IsLoading.value = true;
        ErrorMessage.value = null;

        try {

            const Response = await ApiFetch(`/service-requests/${ServiceRequestId.value}/detail`, { method: 'GET' });

            if (!Response.ok) {
                const ErrorData = await Response.json();

                ErrorMessage.value =
                    typeof ErrorData.detail === 'string'
                        ? ErrorData.detail
                        : 'Failed to load service request.';

                return;
            }

            ServiceRequest.value =
                await Response.json() as ServiceRequestDetail;

            SelectedStatus.value = ServiceRequest.value.status;

        } catch (Error) {

            ErrorMessage.value = 'Unable to connect to the server.';
            console.error('Failed to fetch service request:', Error);

        } finally {

            IsLoading.value = false;

        }
    };

    onMounted(async () => { 
        await FetchServiceRequest(ServiceRequestId.value)
    });
    
</script>

<template>

    <section class="Service-Request-Details">

        <p v-if="IsLoading">
            Loading service request...
        </p>

        <p v-else-if="ErrorMessage">
            {{ ErrorMessage }}
        </p>

        <template v-else-if="ServiceRequest">
            <!-- Header -->
            <header class="Request-Header-Details">
                <h1>Service Request #{{ ServiceRequest.id }}</h1>
                <p>Status: 
                    <span 
                        class="Status-Badge"
                        :class="{
                            'Status-Pending': ServiceRequest.status === 'Pending',
                            'Status-In-Progress': ServiceRequest.status === 'In Progress',
                            'Status-For-Further-Inspection': ServiceRequest.status === 'For Further Inspection',
                            'Status-Completed': ServiceRequest.status === 'Completed',
                            'Status-Unsuccessful': ServiceRequest.status === 'Unsuccessful'
                        }"
                    >
                        {{ ServiceRequest.status }}
                    </span>
                </p>
            </header>

            <!-- Device Information -->
            <section class="Device-Information-Details">
                <h2>Device Information</h2>
                <p>Device Type: {{ ServiceRequest.device_type }}</p>
                <p>Brand: {{ ServiceRequest.device_brand }}</p>
                <p>Model: {{ ServiceRequest.device_model }}</p>
            </section>

            <!-- Customer Information -->
            <section class="Customer-Information-Details">
                <h2>Customer</h2>
                <p>{{ ServiceRequest.customer.name }}</p>
                <p>Customer ID: {{ ServiceRequest.customer.id }}</p>
            </section>

            <!-- Technician Information -->
            <section class="Technician-Information-Details">
                <h2>Assigned Technician</h2>
                <p>{{ ServiceRequest.technician.name }}</p>
                <p>Technician ID: {{ ServiceRequest.technician.id }}</p>
            </section>

            <!-- Reported Faults -->
            <section class="Fault-Descriptions-Details">
                <h2>Reported Faults</h2>

                <ul>
                    <li
                        v-for="(fault, index) in ServiceRequest.fault_descriptions"
                        :key="index"
                    >
                        {{ fault }}
                    </li>
                </ul>
            </section>

            <!-- AI Diagnosis -->
            <section class="AI-Diagnosis-Details">
                <h2>AI Diagnosis</h2>

                <p>{{ ServiceRequest.diagnosis.summary }}</p>

                <p>
                    <strong>Model:</strong>
                    {{ ServiceRequest.diagnosis.llm_model }}
                </p>

                <p>
                    <strong>Overall Confidence:</strong>
                    <span 
                        class="Overall-Confidence"
                        :class="{
                            'Confidence-Low': capitalizeFirstLetter(ServiceRequest.diagnosis.overall_confidence) === 'Low',
                            'Confidence-Moderate': capitalizeFirstLetter(ServiceRequest.diagnosis.overall_confidence) === 'Moderate',
                            'Confidence-High': capitalizeFirstLetter(ServiceRequest.diagnosis.overall_confidence) === 'High',
                        }"
                    >
                        {{ capitalizeFirstLetter(ServiceRequest.diagnosis.overall_confidence) }}
                    </span>
                </p>

                <!-- Diagnostic Hypotheses -->
                <div class="Diagnostic-Hypotheses-Details">
                    <h3>Possible Causes</h3>

                    <article
                        v-for="(hypothesis, index) in ServiceRequest.diagnosis.diagnostic_hypotheses"
                        :key="index"
                    >
                        <h4>{{ hypothesis.cause }}</h4>
                        <p>{{ hypothesis.reasoning }}</p>

                        <p>
                            <strong>Confidence:</strong>
                            {{ hypothesis.confidence }}
                        </p>

                        <p>
                            <strong>Supporting Fault Numbers:</strong>
                            <span class="Supporting-Faults">
                                <span
                                    v-for="fault in hypothesis.supporting_faults"
                                    :key="fault"
                                    class="Fault-Badge"
                                >
                                    {{ fault }}
                                </span>
                            </span>
                        </p>
                    </article>
                </div>

                <!-- Missing Information -->
                <div class="Missing-Information-Details">
                    <h3>Additional Information Needed</h3>

                    <ul>
                        <li
                            v-for="(item, index) in ServiceRequest.diagnosis.missing_information"
                            :key="index"
                        >
                            {{ item }}
                        </li>
                    </ul>
                </div>

                <!-- Recommended Checks -->
                <div class="Recommended-Checks-Details">
                    <h3>Recommended Checks</h3>

                    <ol>
                        <li
                            v-for="(check, index) in ServiceRequest.diagnosis.recommended_checks"
                            :key="index"
                        >
                            {{ check }}
                        </li>
                    </ol>
                </div>
            </section>

            <!-- Standard Operating Procedure -->
            <section class="Standard-Operating-Procedure-Details">
                <h2>Standard Operating Procedure</h2>

                <h3>
                    {{ ServiceRequest.diagnosis.standard_operating_procedure.title }}
                </h3>

                <ol>
                    <li
                        v-for="step in ServiceRequest.diagnosis.standard_operating_procedure.steps"
                        :key="step.step"
                    >
                        <p>
                            <strong>Step {{ step.step }}:</strong>
                            {{ step.instruction }}
                        </p>

                        <p v-if="step.safety_note">
                            <strong>Safety Note:</strong>
                            {{ step.safety_note }}
                        </p>
                    </li>
                </ol>
            </section>

            <!-- Replacement Recommendation -->
            <section class="Replacement-Recommendation-Details">
                <h2>Replacement Recommendation</h2>

                <p>
                    <strong>Recommended Component:</strong>
                    {{ ServiceRequest.diagnosis.replacement_recommendation.component }}
                </p>

                <p>
                    <strong>Reason:</strong>
                    {{ ServiceRequest.diagnosis.replacement_recommendation.reason }}
                </p>

                <h3>Compatibility Requirements</h3>

                <ul>
                    <li
                        v-for="(requirement, index) in ServiceRequest.diagnosis.replacement_recommendation.compatibility_requirements"
                        :key="index"
                    >
                        {{ requirement }}
                    </li>
                </ul>
            </section>

            <!-- Requested Parts -->
            <section class="Requested-Parts-Details">
                <h2>Requested Parts</h2>

                <p v-if="ServiceRequest.requested_part.length === 0">
                    No parts have been requested.
                </p>

                <ul v-else>
                    <li
                        v-for="(part, index) in ServiceRequest.requested_part"
                        :key="part.id ?? index"
                    >
                        {{ part.part_name }}

                        <span v-if="part.quantity">
                            — Quantity: {{ part.quantity }}
                        </span>
                    </li>
                </ul>
            </section>

            <!-- Service Request Actions -->
            <section
                v-if="IsRequestClosed"
                class="Request-Closed-Details"
            >
                <p>
                    This service request is closed and can no longer be edited.
                </p>
            </section>

            <div v-else class="Service-Request-Actions-Details">
                <!-- Update Service Request Status -->
                <div class="Status-Control-Details">
                    <label for="service-status">
                        Update Status
                    </label>

                    <select
                        id="service-status"
                        v-model="SelectedStatus"
                    >
                        <option value="Pending">Pending</option>
                        <option value="In Progress">In Progress</option>
                        <option value="For Further Inspection">
                            For Further Inspection
                        </option>
                        <option value="Completed">Completed</option>
                        <option value="Unsuccessful">Unsuccessful</option>
                    </select>

                    <button
                        type="button"
                        @click="UpdateServiceRequestStatus"
                        :disabled="SelectedStatus === ServiceRequest.status"
                    >
                        Update Status
                    </button>
                </div>

                <!-- Requested Parts Usage -->
                <div
                    v-if="PartsUsed === null" 
                    class="Requested-Parts-Control-Details"
                >
                    <p>Were the requested parts used?</p>

                    <button
                        type="button"
                        @click="UpdatePartsUsage(true)"
                    >
                        Yes, parts were used
                    </button>

                    <button
                        type="button"
                        @click="UpdatePartsUsage(false)"
                    >
                        No parts were used
                    </button>
                </div>

                <p v-else>
                    Parts usage:
                    {{ PartsUsed ? 'Parts were used' : 'No parts were used' }}
                </p>
            </div>
        </template>
    </section>

</template>