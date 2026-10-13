import { ApiFetch } from "@/api/Client";
import { HandleApiError } from "@/api/Error";
import Swal from "sweetalert2";
import { 
    CurrentPage, 
    isLoadingServiceRequests, 
    ServiceRequestError, 
    ServiceRequests, 
    ServiceRequestsPerPage, 
    TotalPages, 
    TotalServiceRequests,
    Search,
    StatusFilter,
    CreatedDate, 
    type ServiceRequestListResponse, 
    type ServiceRequestListResponseData, 
    type ServiceRequestFinalizePayload,
    type ServiceRequestStatus,
    type ServiceRequestDetail
} from "./state/ServiceRequest";



export const ApplyServiceRequestFilters = async (): Promise<void> => {
    
    CurrentPage.value = 1;

    await GetServiceRequests(
        1,
        ServiceRequestsPerPage.value,
        Search.value,
        StatusFilter.value,
        CreatedDate.value
    );

};


let SearchTimeout: ReturnType<typeof setTimeout> | null = null;

export const HandleSearch = (): void => {

    if (SearchTimeout !== null) {

        clearTimeout(SearchTimeout);

    }

    SearchTimeout = setTimeout(() => {

        ApplyServiceRequestFilters();
        
    }, 400);
};


export const GetServiceRequests = async (
    page: number = 1,
    limit: number = 10,
    search: string = '',
    status: string = '',
    createdDate: string = ''
): Promise<ServiceRequestListResponse[]> => {

    isLoadingServiceRequests.value = true;
    ServiceRequestError.value = null;

    try {
        const params = new URLSearchParams();

        params.set('page', String(page));
        params.set('limit', String(limit));

        if (search.trim()) {
            params.set('search', search.trim());
        }

        if (status) {
            params.set('status', status);
        }

        if (createdDate) {
            params.set('created_date', createdDate);
        }

        const response = await ApiFetch(
            `/service-requests/list?${params.toString()}`,
            {
                method: 'GET',
            }
        );

        if (!response.ok) {
            await HandleApiError(
                response,
                'Failed to load service requests.'
            );
        }

        const data: ServiceRequestListResponseData = await response.json();

        ServiceRequests.value = data.items;

        CurrentPage.value = data.page;
        ServiceRequestsPerPage.value = data.limit;
        TotalServiceRequests.value = data.total;
        TotalPages.value = data.pages;

        return data.items;

    } catch (error) {

        await Swal.fire({
            title: 'Connection Error!',
            text: 'Unable to connect to the server. Please try again later.',
            icon: 'error',
        });

        return [];

    } finally {

        isLoadingServiceRequests.value = false;

    }
};


export const GetServiceRequestDetail = async (
    serviceRequestId: number,
): Promise<ServiceRequestDetail> => {

    const Response = await ApiFetch(`/service-requests/${serviceRequestId}/detail`,
        {
            method: 'GET',
        },
    );

    const Data = await Response.json().catch(() => null);

    if (!Response.ok) {
        throw new Error(
            typeof Data?.detail === 'string'
                ? Data.detail
                : 'Failed to load service request.',
        );
    }

    return Data as ServiceRequestDetail;
};


export const FinalizeServiceRequest = async (
    serviceRequestId: number,
    payload: ServiceRequestFinalizePayload,
): Promise<boolean> => {

    try {
        const response = await ApiFetch(`/service-requests/${serviceRequestId}/final-confirmation`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            },
        );

        if (!response.ok) {
            await HandleApiError(
                response,
                'Failed to finalize service request.',
            );

            return false;
        }

        return true;

    } catch (error) {

        await Swal.fire({
            title: 'Connection Error!',
            text: 'Unable to connect to the server. Please try again later.',
            icon: 'error',
        });

        return false;
    }
};


export const RegularStatusUpdate = async (
    serviceRequestId: number,
    status: ServiceRequestStatus,
): Promise<boolean> => {
    try {
        const Response = await ApiFetch(
            `/service-requests/${serviceRequestId}/status`,
            {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    status,
                }),
            },
        );

        if (!Response.ok) {
            const ErrorData = await Response.json().catch(() => null);

            const Message =
                typeof ErrorData?.detail === 'string'
                    ? ErrorData.detail
                    : 'Failed to update the service request.';

            await Swal.fire({
                title: 'Update Failed!',
                text: Message,
                icon: 'error',
            });

            return false;
        }

        return true;

    } catch (error) {

        await Swal.fire({
            title: 'Connection Error!',
            text: 'Unable to connect to the server. Please try again later.',
            icon: 'error',
        });

        return false;
    }
};