import { ref } from "vue";

export interface LLMDiagnosisRequest {
    device_type: string;
    device_brand: string;
    device_model: string;
    fault_descriptions: string[];
}

export interface CustomerData {
    first_name: string;
    last_name: string;
    email: string;
    phone_number: string;
}

export interface DiagnosisRequest {
    llm_diagnosis_request: LLMDiagnosisRequest;
    customer_data: CustomerData;
}

export interface DiagnosisResponse {
    detail: string | undefined;
    service_request_id: number;
    diagnosis_id: number;
    customer_id: number;
    status: string;

    diagnosis: {
        summary: string;
        llm_model: string;

        diagnostic_hypotheses: {
            cause: string;
            supporting_faults: number[];
            reasoning: string;
            confidence: string;
        }[];

        missing_information: string[];
        recommended_checks: string[];

        standard_operating_procedure: {
            title: string;
            steps: {
                step: number;
                instruction: string;
                safety_note: string;
            }[];
        };

        replacement_recommendation: {
            component: string;
            reason: string;
            compatibility_requirements: string[];
        };

        overall_confidence: string;
    };

    confidence: string;
    model: string;

    llm_recommended_part: {
        llm_component: string;
        llm_reason: string;
        compatibility_requirements: string[];
    } | null;

    matched_parts: {
        part_id: number;
        part_name: string;
        part_code: string;
        device_model: string | null;
        device_brand: string | null;
        specifications: string | null;
        unit_cost: string | null;
        stock_quantity: number | null;
        shelf_location: string;
        image_url: string | null;
        category_name: string;
        is_available: boolean;
    }[];

    created_at: string;
}

export interface SelectedPart {
    part_id: number;
    part_name: string;
    quantity: number;
}

export interface ConfirmServiceRequest {
    service_request_id: number | null;
    customer_data: CustomerData;
    device_type: string;
    device_brand: string;
    device_model: string;
    fault_descriptions: string[];
    diagnosis_verdict: string | null;
    selected_parts: SelectedPart[];
    final_status: string;
    technician_notes: string | null;
}


// Run AI Diagnosis State

export const isDiagnosing = ref<boolean>(false)
export const showDiagnosis = ref<boolean>(false)
export const diagnosis = ref<DiagnosisResponse | null>(null)


// Confirm Service Request State

export const isConfirming = ref<boolean>(false)


