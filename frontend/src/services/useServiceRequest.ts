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
    type ServiceRequestListResponseData 
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