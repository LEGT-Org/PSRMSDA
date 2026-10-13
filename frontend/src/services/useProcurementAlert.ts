import Swal from "sweetalert2";
import { ApiFetch } from "@/api/Client";
import { HandleApiError } from "@/api/Error";
import { HandleSuccess } from "@/helper/HandleSuccess";
import { 
    CurrentPage,
    IsLoading,
    ProcurementAlerts,
    ProcurementAlertsPerPage,
    ResolvedAlerts,
    Search,
    StatusFilter,
    Total,
    TotalAlerts,
    TotalPages,
    TypeFilter,
    UnresolvedAlerts,
    type ProcurementAlertPageListResponse,
    type ProcurementAlertResolution,
} from "./state/ProcurementAlert";


export const ApplyProcurementAlertFilters = async (): Promise<void> => {
    
    CurrentPage.value = 1;

    await GetProcurementAlerts(
        CurrentPage.value,
        ProcurementAlertsPerPage.value,
        Search.value,
        StatusFilter.value,
        TypeFilter.value
    );

};


let SearchTimeout: ReturnType<typeof setTimeout> | null = null;

export const HandleSearch = (): void => {

    if (SearchTimeout !== null) {

        clearTimeout(SearchTimeout);

    }

    SearchTimeout = setTimeout(() => {

        ApplyProcurementAlertFilters();
        
    }, 400);
};


export const GetProcurementAlerts = async (
    page: number = 1,
    limit: number = 10,
    search: string = '',
    resolution: ProcurementAlertResolution = 'all',
    alert_type: string = 'all',
): Promise<ProcurementAlertPageListResponse | null> => {
    IsLoading.value = true;

    try {
        const params = new URLSearchParams();

        params.set('page', String(page));
        params.set('limit', String(limit));
        params.set('resolution', resolution);

        if (search.trim()) {
            params.set('search', search.trim());
        }

        if (alert_type !== 'all') {
            params.set('alert_type', alert_type);
        }

        const Response = await ApiFetch(`/procurement-alerts/list?${params.toString()}`,
            {
                method: 'GET',
            },
        );

        if (!Response.ok) {
            await HandleApiError(
                Response,
                'Failed to retrieve procurement alerts.',
            );

            return null;
        }

        const Data: ProcurementAlertPageListResponse =
            await Response.json();

        ProcurementAlerts.value = Data.items;
        Total.value = Data.total;
        TotalPages.value = Data.pages;
        CurrentPage.value = Data.page;

        TotalAlerts.value = Data.total_alerts;
        UnresolvedAlerts.value = Data.unresolved_alerts;
        ResolvedAlerts.value = Data.resolved_alerts;

        return Data;

    } catch (error) {
        
        await Swal.fire({
            title: 'Connection Error!',
            text: 'Unable to connect to the server. Please try again later.',
            icon: 'error',
        });

        return null;

    } finally {

        IsLoading.value = false;

    }

};


/*  

    Marking the procurement alert as resolved

*/

export const UpdateProcurementAlertResolution = async (
    alertId: number,
    isResolved: boolean,
): Promise<boolean> => {

    IsLoading.value = true;
    
    try {

        const Response = await ApiFetch(`/procurement-alerts/${alertId}/resolution`,
            {
                method: 'PATCH',
                body: JSON.stringify(
                    {
                        is_resolved: isResolved,
                    }
                ),
            },
        );

        if (!Response.ok) {
            await HandleApiError(
                Response,
                'Failed to update procurement alert.'
            )

            return false;
        }
        
        const data: { message: string } = await Response.json();

        await HandleSuccess(data.message);

        return true;

    } catch (error) {

        await Swal.fire({
            title: 'Connection Error!',
            text: 'Unable to connect to the server. Please try again later.',
            icon: 'error',
        });

        return false;

    } finally {

        IsLoading.value = false;

    }

};


