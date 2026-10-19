<script setup lang="ts">
    import Swal from 'sweetalert2';
    import { computed, onMounted, ref } from 'vue';
    import { useRoute } from 'vue-router';
    
    import { FinalizeServiceRequest, GetServiceRequestDetail, RegularStatusUpdate } from '@/services/useServiceRequest';
    import { capitalizeFirstLetter } from '@/helper/Capitalize';
    import { currentUser } from '@/services/state/Auth';
    import type { 
        FinalServiceRequestStatus,
        PartUsagePayload,
        ServiceRequestDetail, 
        ServiceRequestFinalizePayload, 
        ServiceRequestStatus 
    } from '@/services/state/ServiceRequest';


    const Route = useRoute();
    const SelectedStatus = ref<ServiceRequestStatus>('Pending');

    const ServiceRequestId = computed<number>(() =>
        Number(Route.params.id)
    );

    const IsLoading = ref<boolean>(true);
    const IsStatusLoading = ref<boolean>(false);
    const ErrorMessage = ref<string | null>(null);

    const ServiceRequest = ref<ServiceRequestDetail | null>(null);

    const IsRequestFinalized = computed<boolean>(() => {
        return ['Completed', 'Unsuccessful'].includes(
            ServiceRequest.value?.status ?? ''
        );
    });

    const IsAdmin = computed<boolean>(() => {
        return currentUser.value?.role === 'admin';
    });

    const IsRequestClosed = computed<boolean>(() => {
        return IsRequestFinalized.value && !IsAdmin.value;
    });

    const CanReopenRequest = computed<boolean>(() => {
        return IsRequestFinalized.value && IsAdmin.value;
    });


    const ReopenRequest = async (
        Status: ServiceRequestStatus
    ): Promise<void> => {

        SelectedStatus.value = Status;
        await UpdateServiceRequestStatus();

    };


    const UpdateServiceRequestStatus = async (): Promise<void> => {

        IsStatusLoading.value = true;

        if (!ServiceRequest.value) return;

        const PreviousStatus = ServiceRequest.value.status;
        const Status = SelectedStatus.value;
        
        if (Status === ServiceRequest.value.status) return;

        const IsFinalStatus =
            Status === 'Completed' ||
            Status === 'Unsuccessful';

        try {

            const IsReopeningRequest =
                ['Completed', 'Unsuccessful'].includes(PreviousStatus) &&
                ['In Progress', 'For Further Inspection'].includes(Status);

            if (IsReopeningRequest) {
                const Confirmation = await Swal.fire({
                    title: 'Reopen Service Request?',
                    text: `Service Request No. ${ServiceRequestId.value} is already finalized. Do you want to reopen it?`,
                    icon: 'question',
                    showCancelButton: true,
                    confirmButtonText: 'Yes, reopen request',
                    cancelButtonText: 'Cancel',
                    customClass: {
                        confirmButton: 'success-button',
                        cancelButton: 'error-button'
                    },
                    reverseButtons: true,
                    focusCancel: true,
                });

                if (!Confirmation.isConfirmed) {
                    SelectedStatus.value = PreviousStatus;
                    return;
                }
            }

            if (IsFinalStatus) {
                
                // 1. Ask the technician to confirm parts usage.
                const PartsUsage = await ConfirmPartsUsage(Status);

                if (PartsUsage === null) {
                    SelectedStatus.value = ServiceRequest.value.status;
                    return;
                }

                // 2. Call your existing finalization API function.
                const Payload: ServiceRequestFinalizePayload = {
                    status: Status,
                    parts_usage: PartsUsage,
                };

                const Success = await FinalizeServiceRequest(
                    ServiceRequestId.value,
                    Payload,
                );

                // FinalizeServiceRequest already handles API errors.
                if (!Success) {
                    SelectedStatus.value = ServiceRequest.value.status;
                    return;
                }

            } else {

                if (!IsReopeningRequest) {

                    const Confirmation = await Swal.fire({
                        title: 'Update Service Request?',
                        text: `Do you want to update the status of 
                            Service Request No. ${ServiceRequestId.value} into ${Status} status?`,
                        icon: 'question',
                        showCancelButton: true,
                        confirmButtonText: 'Yes, update request',
                        cancelButtonText: 'Cancel',
                        customClass: {
                            confirmButton: 'success-button',
                            cancelButton: 'error-button'
                        },
                        reverseButtons: true,
                        focusCancel: true,
                    });

                    if (!Confirmation.isConfirmed) {
                        return;
                    }

                }

                // 3. Ordinary statuses use the regular status endpoint.
                const Success = await RegularStatusUpdate(
                    ServiceRequestId.value,
                    Status,
                );

                if (!Success) {
                    SelectedStatus.value = ServiceRequest.value.status;
                    return;
                }
            }

            // 4. Both workflows succeeded.
            await Swal.fire({
                title: 'Success!',
                text: IsFinalStatus
                    ? 'Service request has been finalized.'
                    : 'Service request status updated successfully.',
                icon: 'success',
                confirmButtonText: 'OK',
                customClass: {
                    confirmButton: 'success-button'
                }
            });

            // 5. Refresh the displayed request.
            await FetchServiceRequest(ServiceRequestId.value);

        } catch (error) {

            await Swal.fire({
                title: 'Error!',
                text: error instanceof Error
                    ? error.message
                    : 'Unable to complete the operation.',
                icon: 'error',
            });

            SelectedStatus.value = ServiceRequest.value?.status ?? 'Pending';

        } finally {

            IsStatusLoading.value = false;

        }
    };


    const ConfirmPartsUsage = async (
        Status: FinalServiceRequestStatus,
    ): Promise<PartUsagePayload[] | null> => {
        
        const Parts = ServiceRequest.value?.requested_part ?? [];

        if (Parts.some(Part => Part.id == null)) {

            throw new Error('A requested part is missing its request-part ID.');

        }

        const EscapeHtml = (Value: string): string => {
            const Characters: Record<string, string> = {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#39;',
            };

            return Value.replace(/[&<>"']/g, Char => Characters[Char] ?? Char);
        };

        const PartsHtml = Parts.length > 0
            ? Parts.map(Part => `
                <div style="display:flex; align-items:center; gap:12px; margin:12px 0;">
                    <label style="flex:1; text-align:left;">
                        <input
                            type="checkbox"
                            id="part-used-${Part.id}"
                        />
                        ${EscapeHtml(Part.part_name)}
                        (Requested: ${Part.quantity ?? 'N/A'})
                    </label>

                    <input
                        type="number"
                        id="quantity-used-${Part.id}"
                        min="1"
                        step="1"
                        value="${Math.max(1, Part.quantity ?? 1)}"
                        disabled
                        style="width:90px;"
                    />
                </div>
            `).join('')
            : '<p>No requested parts were recorded.</p>';

        const Result = await Swal.fire<PartUsagePayload[]>({
            title: `Finalize as ${Status}?`,
            html: `
                <p>Confirm which parts were actually used.</p>
                ${PartsHtml}
            `,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Confirm Finalization',
            cancelButtonText: 'Cancel',
            customClass: {
                confirmButton: 'success-button',
                cancelButton: 'error-button'
            },
            reverseButtons: true,
            focusCancel: true,

            didOpen: () => {
                for (const Part of Parts) {
                    const Checkbox = document.getElementById(
                        `part-used-${Part.id}`,
                    ) as HTMLInputElement | null;

                    const QuantityInput = document.getElementById(
                        `quantity-used-${Part.id}`,
                    ) as HTMLInputElement | null;

                    Checkbox?.addEventListener('change', () => {
                        if (!Checkbox || !QuantityInput) return;

                        QuantityInput.disabled = !Checkbox.checked;

                        QuantityInput.value = Checkbox.checked
                            ? String(Math.max(1, Part.quantity ?? 1))
                            : '0';
                    });
                }
            },

            preConfirm: () => {
                const PartsUsage: PartUsagePayload[] = [];

                for (const Part of Parts) {

                    if (Part.id == null) {

                        Swal.showValidationMessage('A requested part is missing its ID.',);
                        return false;

                    }

                    const Checkbox = document.getElementById(`part-used-${Part.id}`,) as HTMLInputElement | null;
                    const QuantityInput = document.getElementById(`quantity-used-${Part.id}`,) as HTMLInputElement | null;

                    if (!Checkbox || !QuantityInput) {

                        Swal.showValidationMessage('Unable to read the parts usage.',);
                        return false;

                    }

                    const PartsWereUsed = Checkbox.checked;
                    const QuantityUsed = PartsWereUsed
                        ? Number(QuantityInput.value)
                        : 0;

                    if (
                        PartsWereUsed &&
                        (!Number.isInteger(QuantityUsed) || QuantityUsed <= 0)
                    ) {

                        Swal.showValidationMessage('Enter a positive whole-number quantity for every part used.',);
                        return false;

                    }

                    PartsUsage.push(
                        {
                            request_part_id: Part.id,
                            part_used: PartsWereUsed,
                            quantity_used: QuantityUsed,
                        }
                    );
                }

                return PartsUsage;
            },
        });

        return Result.isConfirmed
            ? Result.value ?? null
            : null;
    };


    const FetchServiceRequest = async (serviceRequestId: number): Promise<void> => {
        IsLoading.value = true;
        ErrorMessage.value = null;

        try {
            console.log('Fetching service request:', serviceRequestId);

            ServiceRequest.value = await GetServiceRequestDetail(serviceRequestId);
            SelectedStatus.value = ServiceRequest.value.status;

            console.log('Service request received:', ServiceRequest);

        } catch (error) {
            
            await Swal.fire({
                title: 'Error!',
                text: error instanceof Error
                    ? error.message
                    : 'Unable to load service request detail.',
                icon: 'error',
            });

            ErrorMessage.value =
                error instanceof Error
                    ? error.message
                    : 'Unable to load service request detail.';

            console.error('Failed to fetch service request:', error);

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

        <!-- Error -->
        <div
            v-else-if="ErrorMessage"
            class="Service-Request-Details-Error"
        >
            <h2>Unable to Load Service Request.</h2>
            <p>{{ ErrorMessage }}</p>
        </div>

        <template v-else-if="ServiceRequest">
            <!-- Header -->
            <header class="Request-Header-Details">
                <h1>Service Request No. {{ ServiceRequest.id }}</h1>
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
                <h2>Technician</h2>
                <p>{{ ServiceRequest.technician.name }}</p>
                <p>Technician ID: {{ ServiceRequest.technician.id }}</p>

                <div
                    v-if="ServiceRequest.technician_notes !== null" 
                    class="Diagnostic-Hypotheses-Details"
                >
                    <h3>Technician Notes: </h3>
                    
                    <article>
                        <p>{{ ServiceRequest.technician_notes }}</p>
                    </article>
                </div>
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


            <template v-if="ServiceRequest.diagnosis">

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
                                <span
                                    class="Overall-Confidence"
                                    :class="{
                                        'Confidence-Low': capitalizeFirstLetter(hypothesis.confidence) === 'Low',
                                        'Confidence-Moderate': capitalizeFirstLetter(hypothesis.confidence) === 'Moderate',
                                        'Confidence-High': capitalizeFirstLetter(hypothesis.confidence) === 'High',
                                    }"
                                >
                                    {{ capitalizeFirstLetter(hypothesis.confidence) }}</span>
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

            </template>

            <section v-else class="AI-Diagnosis-Details">
                <h2>AI Diagnosis</h2>
                <p>
                    No AI diagnosis was performed for this service request.
                </p>
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

            <section
                v-else-if="CanReopenRequest"
                class="Request-Closed-Details"
            >
                <p>
                    This request has been finalized. You can reopen it if further
                    work or inspection is required.
                </p>

                <button
                    type="button"
                    @click="ReopenRequest('In Progress')"
                >
                    Reopen Service Request
                </button>

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
                        :disabled="SelectedStatus === ServiceRequest.status || IsStatusLoading"
                    >
                        {{
                            IsStatusLoading
                                ? 'Updating Status...'
                                : 'Update Status'
                        }}
                    </button>
                </div>
                
            </div>
        </template>
    </section>

</template>