import Swal from "sweetalert2";
import { ApiFetch } from "@/api/Client";
import { HandleApiError } from "@/api/Error";
import { 
    CurrentPage,
    CustomerError,
    CustomerPerPage,
    Customers,
    isCreateCustomer,
    IsLoading,
    Search,
    Total, 
    TotalPages, 
    type Customer, 
    type CustomerCreateRequest, 
    type CustomerListResponse, 
    type CustomerUpdateRequest
} from "./state/Customer";
import { HandleSuccess } from "@/helper/HandleSuccess";


export const ApplyCustomerFilters = async (): Promise<void> => {

    CurrentPage.value = 1;

    await GetCustomers(
        CurrentPage.value,
        CustomerPerPage.value,
        Search.value,
    );
};


let SearchTimeout: ReturnType<typeof setTimeout> | null = null;

export const HandleCustomerSearch = (): void => {

    if (SearchTimeout !== null) {
        clearTimeout(SearchTimeout);
    }

    SearchTimeout = setTimeout(() => {
        void ApplyCustomerFilters();
    }, 400);

};


export const GetCustomers = async (
    page: number = 1,
    limit: number = 10,
    search: string = '',
): Promise<CustomerListResponse | null> => {

    IsLoading.value = true;

    try {

        const params = new URLSearchParams();

        params.set('page', String(page));
        params.set('limit', String(limit));

        if (search.trim()) {
            params.set('search', search.trim());
        }

        const Response = await ApiFetch(`/customers/list?${params.toString()}`,
            {
                method: 'GET'
            }
        );

        if (!Response.ok) {
            await HandleApiError(
                Response,
                'Failed to retrieve customers.'
            );

            return null;
        }

        const Data: CustomerListResponse = await Response.json();

        Customers.value = Data.items;
        Total.value = Data.total;
        TotalPages.value = Data.pages;
        CurrentPage.value = Data.page;

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

}


export const GetCustomer = async (
    partId: number,
): Promise<Customer | null> => {

    try {

        const Response = await ApiFetch(`/customers/${partId}/details`,
            {
                method: 'GET',
            },
        );

        const Data = await Response.json().catch(() => null);

        if (!Response.ok) {
            throw new Error(
                typeof Data?.detail === 'string'
                    ? Data.detail
                    : 'Failed to load customer.',
            );
        }

        return Data as Customer;

    } catch (error) {

        await Swal.fire({
            title: 'Connection Error!',
            text: 'Unable to connect to the server. Please try again later.',
            icon: 'error',
        });

        return null;

    }
};


export const CreateCustomer = async (
    payload: CustomerCreateRequest
): Promise<Customer | null> => {

    isCreateCustomer.value = true;
    CustomerError.value = null;

    try {

        const response = await ApiFetch('/customers/create', {

            method: 'POST',
            body: JSON.stringify(payload),

        });

        const data = await response.json();
        
        if (!response.ok) {
            
            CustomerError.value = data.detail ?? 'Failed to create customer record.';
            return null;
        }
        
        Customers.value.push(data);

        await HandleSuccess(
            `Customer ${data.id} record has been created.`,
            'Record Creation Successful!'
        );

        return data;

    } catch (error) {

        await Swal.fire({
            title: 'Connection Error!',
            text: 'Unable to connect to the server. Please try again later.',
            icon: 'error',
        });

        return null;

    } finally {

        isCreateCustomer.value = false;

    }
};


export const UpdateCustomer = async (
    CustomerID: number, 
    payload: CustomerUpdateRequest
): Promise<boolean> => {

    try {

        const Response = await ApiFetch(`/customers/${CustomerID}/update`,
            {
                method: 'PATCH',
                body: JSON.stringify(payload)
            }
        );
        
        if (!Response.ok) {
            
            await HandleApiError(
                Response,
                'Failed to update customer record.'
            );
            return false;

        }

        const data = await Response.json();
        await GetCustomer(data.id);

        await HandleSuccess(
            data.message,
            'Record Update Successful!'
        );

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


export const DeleteCustomer = async (
    CustomerID: number
): Promise<boolean> => {

    try {

        const Response = await ApiFetch(`/customers/${CustomerID}/delete`,
            {
                method: 'DELETE',
            }
        );

        if (!Response.ok) {
            
            await HandleApiError(
                Response,
                'Failed to delete spare part record.'
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

}
