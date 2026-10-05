import { ApiFetch } from "@/api/Client";
import { 
    showDiagnosis,
    isDiagnosing,
    diagnosis, 
    type DiagnosisRequest,
    type DiagnosisResponse
} from "./state/NewServiceRequest";


export const runAIDiagnosis = async (payload: DiagnosisRequest): Promise<void> => {

    isDiagnosing.value = true;

    try {

        const response = await ApiFetch('/service-requests/diagnose', 
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            }
        );
        
        
        if (!response.ok) {

            if (!response.ok) {
            const errorData = await response.json();

            console.error('Backend Error:', errorData);

            if (Array.isArray(errorData.detail)) {

                const messages = errorData.detail
                    .map((error: { msg?: string }) => error.msg)
                    .filter(Boolean);

                throw new Error(messages.join('\n'));
                
            }

            throw new Error(errorData.detail ?? 'Failed to generate diagnosis.');
        }

        }
        
        const data: DiagnosisResponse = await response.json();

        diagnosis.value = data;
        showDiagnosis.value = true;

    } catch (error) {
        
        console.error('AI Diagnosis Error:', error);

        alert(
            error instanceof Error
                ? error.message
                : 'Something went wrong while generating the diagnosis.'
        );

    } finally {

        isDiagnosing.value = false;

    }
};