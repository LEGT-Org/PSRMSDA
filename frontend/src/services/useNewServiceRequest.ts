import { ApiFetch } from "@/api/Client";
import { ParseApiError } from "@/api/Error";
import { 
    showDiagnosis,
    isDiagnosing,
    diagnosis,
    type DiagnosisRequest,
    type DiagnosisResponse,
    type ConfirmServiceRequest 
} from "./state/NewServiceRequest";


// Run an AI Diagnosis

export const runAIDiagnosis = async (payload: DiagnosisRequest): Promise<void> => {

    isDiagnosing.value = true;

    try {

        const response = await ApiFetch('/service-requests/diagnose',
            {
                method: 'POST',
                body: JSON.stringify(payload),
            }
        );

        if (!response.ok) {
            throw new Error(
                await ParseApiError(
                    response,
                    'Failed to generate diagnosis.'
                )
            );
        }

        const data: DiagnosisResponse = await response.json();

        diagnosis.value = data;
        showDiagnosis.value = true;

    } catch (error) {

        alert(
            error instanceof Error
                ? error.message
                : 'Something went wrong while generating the diagnosis.'
        );

    } finally {

        isDiagnosing.value = false;

    }
};


// Confirm the Service Request

export const confirmServiceRequest = async (payload: ConfirmServiceRequest): Promise<DiagnosisResponse> => {

    const response = await ApiFetch('/service-requests/confirm',
        {

            method: 'POST',
            body: JSON.stringify(payload),

        }
    );

    if (!response.ok) {
        throw new Error(
            await ParseApiError(
                response,
                'Failed to confirm service request.'
            )
        );
    }

    return await response.json();

};


// Cancel the Service Request

export const cancelServiceRequest = async (serviceRequestId: number): Promise<void> => {

    const response = await ApiFetch(`/service-requests/cancel`,
        {

            method: 'POST',
            body: JSON.stringify(
                {
                    "service_request_id": serviceRequestId
                }
            )
        }
    );

    if (!response.ok) {
        throw new Error(
            await ParseApiError(
                response,
                'Failed to cancel service request.'
            )
        );
    }

    return await response.json();
};