<script setup lang="ts">
    import Swal from 'sweetalert2';
    import { onMounted, onUnmounted, ref } from 'vue';
    import { parseFaultDescriptions } from '@/helper/SymptomsParser';
    import { ValidateDiagnosisForm } from '@/helper/ValidateServiceRequestForm';
    import { HandleSuccess } from '@/helper/HandleSuccess';
    

    import { 
        runAIDiagnosis, 
        confirmServiceRequest, 
        cancelServiceRequest, 
        cancelServiceRequestOnUnload
    } from '@/services/useNewServiceRequest';

    import { 
        isDiagnosing,
        isConfirming,
        showDiagnosis,
        diagnosis,
        type DiagnosisRequest,
        type ConfirmServiceRequest,
        type SelectedPart, 
    } from '@/services/state/NewServiceRequest';


    const DeviceType = ref<string>('');
    const DeviceBrand = ref<string>('');
    const DeviceModel = ref<string>('');
    const FaultDescription = ref<string>('');

    const CustomerFirstName = ref<string>('');
    const CustomerLastName = ref<string>('');
    const CustomerEmail = ref<string>('');
    const CustomerPhoneNumber = ref<string>('');

    const TechnicianNotes = ref<string>('');
    const FinalStatus = ref<string>('Pending');
    const SelectedParts = ref<SelectedPart[]>([]);


    const BuildRequestPayload = (): DiagnosisRequest => {

        const payload = {
            llm_diagnosis_request: {
                device_type: DeviceType.value,
                device_brand: DeviceBrand.value,
                device_model: DeviceModel.value,
                fault_descriptions: parseFaultDescriptions(
                    FaultDescription.value
                ),
            },

            customer_data: {
                first_name: CustomerFirstName.value,
                last_name: CustomerLastName.value,
                email: CustomerEmail.value,
                phone_number: CustomerPhoneNumber.value,
            },
        };


        return payload;
    };


    const BuildConfirmRequestPayload = (): ConfirmServiceRequest => {

        const payload = {
            service_request_id: diagnosis.value?.service_request_id ?? null,

            customer_data: {
                first_name: CustomerFirstName.value,
                last_name: CustomerLastName.value,
                email: CustomerEmail.value,
                phone_number: CustomerPhoneNumber.value,
            },

            device_type: DeviceType.value,
            device_brand: DeviceBrand.value,
            device_model: DeviceModel.value,

            fault_descriptions: parseFaultDescriptions(FaultDescription.value),
            diagnosis_verdict: 'Accepted',
            selected_parts: SelectedParts.value,
            final_status: FinalStatus.value,
            technician_notes: TechnicianNotes.value || null,
        };

        return payload;

    };


    const ResetServiceRequest = () => {
        CustomerFirstName.value = '';
        CustomerLastName.value = '';
        CustomerEmail.value = '';
        CustomerPhoneNumber.value = '';

        DeviceType.value = '';
        DeviceBrand.value = '';
        DeviceModel.value = '';
        FaultDescription.value = '';

        TechnicianNotes.value = '';

        FinalStatus.value = 'Pending';
        SelectedParts.value = [];

        diagnosis.value = null;
        showDiagnosis.value = false;
    };

    
    const RunDiagnosis = async () => {

        const isValid = await ValidateDiagnosisForm(
            CustomerFirstName.value,
            CustomerLastName.value,
            CustomerEmail.value,
            CustomerPhoneNumber.value,
            DeviceType.value,
            DeviceBrand.value,
            DeviceModel.value,
            FaultDescription.value
        );

        if (!isValid) {
            return;
        }

        const payload = BuildRequestPayload();
        await runAIDiagnosis(payload);

    }


    const ConfirmRequest = async () => {

        const payload = BuildConfirmRequestPayload();
        const response = await confirmServiceRequest(payload);

        ResetServiceRequest();

        await HandleSuccess(
            'Service request confirmed successfully.',
            'Request Confirmed!'
        )

    };


    const CancelRequest = async () => {

        if (diagnosis.value?.service_request_id == null) {

            return;

        }

        try {

            await cancelServiceRequest(diagnosis.value.service_request_id);
            showDiagnosis.value = false;

        } catch (error) {


            await Swal.fire({
                title: 'Connection Error!',
                text: 'Failed to cancel service request. Please try again later.',
                icon: 'error',
            });

        }
    };


    const HandlePageHide = () => {
        
        const serviceRequestId = diagnosis.value?.service_request_id;

        if (serviceRequestId == null) {

            return;
            
        }

        cancelServiceRequestOnUnload(serviceRequestId);
        
    };


    onMounted(() => {

        window.addEventListener('pagehide', HandlePageHide);

    });

    onUnmounted(() => {

        window.removeEventListener('pagehide', HandlePageHide);

    });

</script>

<template>
    <div class="Service-Request">

        <h1>New Service Request</h1>

        <!-- ============================= -->
        <!-- Request Information            -->
        <!-- ============================= -->

        <div class="Service-Request-Forms">

            <!-- Customer Details -->
            <section class="Service-Request-Card">
                <h2>Customer Details</h2>

                <div class="Service-Request-Fields">

                    <label>
                        First Name:

                        <input
                            v-model="CustomerFirstName"
                            type="text"
                            placeholder="e.g. John"
                        />
                    </label>

                    <label>
                        Last Name:

                        <input
                            v-model="CustomerLastName"
                            type="text"
                            placeholder="e.g. Doe"
                        />
                    </label>

                    <label>
                        Contact:

                        <input
                            v-model="CustomerPhoneNumber"
                            type="text"
                            placeholder="e.g. 09123456789 or +639123456789"
                        />
                    </label>

                    <label>
                        Email:

                        <input
                            v-model="CustomerEmail"
                            type="email"
                            placeholder="e.g. johndoe@gmail.com"
                        />
                    </label>

                </div>
            </section>

            <!-- Device Details -->
            <section class="Service-Request-Card">
                <h2>Device Details</h2>

                <div class="Service-Request-Fields">

                    <label>
                        Type:

                        <input
                            v-model="DeviceType"
                            type="text"
                            placeholder="e.g. Refrigerator"
                        />
                    </label>

                    <label>
                        Brand:

                        <input
                            v-model="DeviceBrand"
                            type="text"
                            placeholder="e.g. Samsung"
                        />
                    </label>

                    <label>
                        Model:

                        <input
                            v-model="DeviceModel"
                            type="text"
                            placeholder="e.g. RT58K7000S"
                        />
                    </label>

                    <label>
                        Fault Description:

                        <textarea
                            v-model="FaultDescription"
                            placeholder="Enter detailed hardware symptoms...

Example:

- Refrigerator is running but not cooling
- Compressor is running continuously
- Freezer is cold but lower compartment is warm
- No unusual noise"
                        ></textarea>
                    </label>

                </div>
            </section>

        </div>

        <!-- ============================= -->
        <!-- Diagnosis Button               -->
        <!-- ============================= -->

        <button
            type="button"
            class="Run-Diagnosis-Button"
            :disabled="isDiagnosing"
            @click="RunDiagnosis"
        >
            {{
                isDiagnosing
                    ? 'Running AI-Diagnosis...'
                    : 'Run AI-Diagnosis'
            }}
        </button>

        <!-- ============================= -->
        <!-- Diagnosis Result               -->
        <!-- ============================= -->

        <section
            v-if="showDiagnosis && diagnosis"
            class="Diagnosis-Container"
        >

            <!-- Diagnosis Header -->
            <div class="Diagnosis-Header">

                <div>
                    <h2>Service Request Diagnostic Analysis</h2>

                    <p>
                        Service Request #{{ diagnosis.service_request_id }}
                        |
                        Diagnosis #{{ diagnosis.diagnosis_id }}
                        |
                        Customer #{{ diagnosis.customer_id }}
                    </p>
                </div>

                <span class="Diagnosis-Status">
                    {{ diagnosis.status }}
                </span>

            </div>

            <!-- Summary + Missing Information -->
            <div class="Diagnosis-Top-Grid">

                <!-- Summary -->
                <section class="Diagnosis-Card Summary-Card">

                    <h3>Summary</h3>

                    <p>
                        {{ diagnosis.diagnosis.summary }}
                    </p>

                    <div class="Diagnosis-Metadata">

                        <span>
                            Confidence:

                            <strong>
                                {{ diagnosis.diagnosis.overall_confidence }}
                            </strong>
                        </span>

                        <span>
                            Model:

                            <strong>
                                {{ diagnosis.diagnosis.llm_model }}
                            </strong>
                        </span>

                    </div>

                </section>

                <!-- Missing Information -->
                <section class="Diagnosis-Card Missing-Card">

                    <h3>Missing Information</h3>

                    <ul>
                        <li
                            v-for="item in diagnosis.diagnosis.missing_information"
                            :key="item"
                        >
                            {{ item }}
                        </li>
                    </ul>

                </section>

            </div>

            <!-- ============================= -->
            <!-- Diagnostic Hypotheses          -->
            <!-- ============================= -->

            <section class="Diagnosis-Card">

                <div class="Diagnosis-Section-Header">
                    <h3>Diagnostic Hypotheses</h3>
                </div>

                <div class="Hypothesis-List">

                    <article
                        v-for="(hypothesis, index) in diagnosis.diagnosis.diagnostic_hypotheses"
                        :key="index"
                        class="Hypothesis"
                    >

                        <div class="Hypothesis-Number">
                            {{ index + 1 }}
                        </div>

                        <div class="Hypothesis-Content">

                            <div class="Hypothesis-Title">

                                <h4>
                                    {{ hypothesis.cause }}
                                </h4>

                                <span
                                    class="Confidence-Badge"
                                    :class="`Confidence-${hypothesis.confidence}`"
                                >
                                    {{ hypothesis.confidence }}
                                </span>

                            </div>

                            <p>
                                <strong>Reasoning:</strong>
                                {{ hypothesis.reasoning }}
                            </p>

                            <p>
                                <strong>Supporting faults:</strong>

                                <span
                                    v-for="fault in hypothesis.supporting_faults"
                                    :key="fault"
                                    class="Fault-Tag"
                                >
                                    {{ fault }}
                                </span>
                            </p>

                        </div>

                    </article>

                </div>

            </section>

            <!-- ============================= -->
            <!-- Recommended Checks             -->
            <!-- ============================= -->

            <section class="Diagnosis-Card Recommended-Checks">

                <h3>Recommended Checks</h3>

                <ol>
                    <li
                        v-for="check in diagnosis.diagnosis.recommended_checks"
                        :key="check"
                    >
                        {{ check }}
                    </li>
                </ol>

            </section>

            <!-- ============================= -->
            <!-- SOP                             -->
            <!-- ============================= -->

            <section class="Diagnosis-Card SOP-Card">

                <h3>
                    {{ diagnosis.diagnosis.standard_operating_procedure.title }}
                </h3>

                <div
                    v-for="step in diagnosis.diagnosis.standard_operating_procedure.steps"
                    :key="step.step"
                    class="SOP-Step"
                >

                    <div class="SOP-Step-Number">
                        {{ step.step }}
                    </div>

                    <div class="SOP-Step-Content">

                        <h4>
                            {{ step.instruction }}
                        </h4>

                        <div class="Safety-Note">
                            <strong>Safety:</strong>
                            {{ step.safety_note }}
                        </div>

                    </div>

                </div>

            </section>

            <!-- ============================= -->
            <!-- Replacement Recommendation     -->
            <!-- ============================= -->

            <section class="Diagnosis-Card Replacement-Card">

                <h3>Replacement Recommendation</h3>

                <div class="Replacement-Content">

                    <div>
                        <strong>Component</strong>

                        <p>
                            {{
                                diagnosis.diagnosis.replacement_recommendation.component
                            }}
                        </p>
                    </div>

                    <div>
                        <strong>Reason</strong>

                        <p>
                            {{
                                diagnosis.diagnosis.replacement_recommendation.reason
                            }}
                        </p>
                    </div>

                    <div>
                        <strong>Compatibility Requirements</strong>

                        <ul>
                            <li
                                v-for="requirement in diagnosis.diagnosis.replacement_recommendation.compatibility_requirements"
                                :key="requirement"
                            >
                                {{ requirement }}
                            </li>
                        </ul>
                    </div>

                </div>

            </section>

            <!-- ============================= -->
            <!-- Recommended Part               -->
            <!-- ============================= -->

            <section class="Diagnosis-Card Part-Card">

                <h3>Recommended Part</h3>

                <div 
                    v-if="diagnosis.llm_recommended_part"
                    class="Recommended-Part"
                >

                    <div>
                        <strong>AI Recommended Component</strong>

                        <p>
                            {{ diagnosis.llm_recommended_part.llm_component }}
                        </p>
                    </div>

                    <div>
                        <strong>Reason</strong>

                        <p>
                            {{ diagnosis.llm_recommended_part.llm_reason }}
                        </p>
                    </div>

                    <div>
                        <strong>Compatibility</strong>

                        <ul>
                            <li
                                v-for="requirement in diagnosis.llm_recommended_part.compatibility_requirements"
                                :key="requirement"
                            >
                                {{ requirement }}
                            </li>
                        </ul>
                    </div>

                </div>

                <!-- Matched Database Part -->
                <div class="Matched-Part">
                    <h4>Matched Parts</h4>

                    <div class="Matched-Part-List">
                        <div
                            v-for="part in diagnosis.matched_parts"
                            :key="part.part_id"
                            class="Matched-Part-Item"
                        >
                            <input
                                type="checkbox"
                                :checked="SelectedParts.some(selected => selected.part_id === part.part_id)"
                                @change="(event) => {
                                    const checked = (event.target as HTMLInputElement).checked;

                                    if (checked) {
                                        SelectedParts.push({
                                            part_id: part.part_id,
                                            part_name: part.part_name,
                                            quantity: 1
                                        });
                                    } else {
                                        const index = SelectedParts.findIndex(selected => selected.part_id === part.part_id);

                                        if (index !== -1) {
                                            SelectedParts.splice(index, 1);
                                        }
                                    }

                                }"
                            />

                            <div>
                                <span>Part Number</span>
                                <strong>{{ part.part_code }}</strong>
                            </div>

                            <div>
                                <span>Name</span>
                                <strong>{{ part.part_name }}</strong>
                            </div>

                            <div>
                                <span>Stock</span>
                                <strong>{{ part.stock_quantity ?? 0 }}</strong>
                            </div>

                            <div v-if="SelectedParts.some(selected => selected.part_id === part.part_id)">
                                <span>Quantity</span>

                                <button
                                    type="button"
                                    @click="SelectedParts.find(
                                        selected => selected.part_id === part.part_id
                                    )!.quantity--"
                                    :disabled="SelectedParts.find(
                                        selected => selected.part_id === part.part_id
                                    )!.quantity <= 1"
                                >
                                    -
                                </button>

                                <strong>
                                    {{ SelectedParts.find(
                                        selected => selected.part_id === part.part_id
                                    )!.quantity }}
                                </strong>

                                <button
                                    type="button"
                                    @click="SelectedParts.find(
                                        selected => selected.part_id === part.part_id
                                    )!.quantity++"
                                    :disabled="
                                        SelectedParts.find(
                                            selected => selected.part_id === part.part_id
                                        )!.quantity >= (part.stock_quantity ?? 0)
                                    "
                                >
                                    +
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

            </section>

        </section>

        <!-- ============================= -->
        <!-- Technician Notes               -->
        <!-- ============================= -->

        <section class="Service-Request-Card Technician-Notes">

            <h2>Technician Notes</h2>

            <div class="Service-Request-Fields">

                <textarea
                    placeholder="Enter technician notes..."
                ></textarea>

            </div>

        </section>

        <!-- ============================= -->
        <!-- Request Actions                -->
        <!-- ============================= -->

        <div class="Service-Request-Actions">

            <select v-model="FinalStatus">
                <option value="Pending">
                    Pending
                </option>

                <option value="In Progress">
                    In Progress
                </option>

                <option value="For Further Inspection">
                    For Further Inspection
                </option>

                <option value="Completed">
                    Completed
                </option>

                <option value="Unsuccessful">
                    Unsuccessful
                </option>
            </select>

            <div class="Service-Request-Action-Buttons">

                <button
                    type="button"
                    class="Confirm-Button"
                    :disabled="isConfirming"
                    @click="ConfirmRequest"
                >
                    {{ 
                        isConfirming
                            ? 'Confirm...'
                            : 'Confirm'
                    }}
                </button>

                <button
                    type="button"
                    class="Cancel-Button"
                    @click="CancelRequest"
                >
                    Cancel
                </button>

            </div>

        </div>

    </div>
</template>