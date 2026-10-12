import { ref } from 'vue';

export interface ServiceRequestListResponse {
    id: number;
    customer_name: string;
    device_type: string;
    device_brand: string;
    device_model: string;
    technician_name: string;
    created_at: string;
    status: string;
}

export interface ServiceRequestListResponseData {
    items: ServiceRequestListResponse[];
    page: number;
    limit: number;
    total: number;
    pages: number;
}


export const ServiceRequests = ref<ServiceRequestListResponse[]>([]);

export const Search = ref<string>('');
export const StatusFilter = ref<string>('');
export const CreatedDate = ref<string>('');

export const CurrentPage = ref<number>(1);
export const ServiceRequestsPerPage = ref<number>(10);
export const TotalServiceRequests = ref<number>(0);
export const TotalPages = ref<number>(0);

export const isLoadingServiceRequests = ref<boolean>(false);

export const ServiceRequestError = ref<string | null>(null);


/*  

    Service Request Detail State

*/

export type ServiceRequestStatus =
    | 'Pending'
    | 'In Progress'
    | 'For Further Inspection'
    | 'Completed'
    | 'Unsuccessful';

export interface CustomerDetails {
    id: number;
    name: string;
}

export interface TechnicianDetails {
    id: number;
    name: string;
}

export interface FaultHypothesis {
    cause: string;
    supporting_faults: number[];
    reasoning: string;
    confidence: string;
}

export interface ProcedureStep {
    step: number;
    instruction: string;
    safety_note: string;
}

export interface RequestedPart {
    id?: number;
    part_name: string;
    quantity?: number;
}

export interface ServiceRequestDetail {
    id: number;
    status: ServiceRequestStatus;
    device_type: string;
    device_brand: string;
    device_model: string;
    fault_descriptions: string[];

    diagnosis: {
        summary: string;
        llm_model: string;
        diagnostic_hypotheses: FaultHypothesis[];
        missing_information: string[];
        recommended_checks: string[];

        standard_operating_procedure: {
            title: string;
            steps: ProcedureStep[];
        };

        replacement_recommendation: {
            component: string;
            reason: string;
            compatibility_requirements: string[];
        };

        overall_confidence: string;
    };

    customer: CustomerDetails;
    technician: TechnicianDetails;
    requested_part: RequestedPart[];
}


/*  

    Service Request Detail Update (Status + Quantity)

*/

export type FinalServiceRequestStatus =
    | 'Completed'
    | 'Unsuccessful';

export interface PartUsagePayload {
    request_part_id: number;
    parts_used: boolean;
    quantity_used: number;
}

export interface ServiceRequestFinalizePayload {
    status: FinalServiceRequestStatus;
    parts_usage: PartUsagePayload[];
}
