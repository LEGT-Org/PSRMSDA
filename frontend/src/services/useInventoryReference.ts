import Swal from 'sweetalert2';

import { ApiFetch } from '@/api/Client';
import { HandleApiError } from '@/api/Error';

import {
    SpareParts,
    CurrentPage,
    SparePartsPerPage,
    Total,
    TotalPages,
    IsLoading,
    Search,
    ParentCategoryFilter,
    CategoryFilter,
    isCreateSparePart,
    ParentCategories,
    Categories,
    SparePartError,
    type SparePartListResponse,
    type CategoryResponse,
    type SparePartCreateRequest,
    type SparePart,
    type SparePartUpdateRequest,
    type CreateCategory,
    type ChildCategory,
    isCreateCategory,
    CategoryError
} from '@/services/state/InventoryReference';
import { HandleSuccess } from '@/helper/HandleSuccess';


// Import HandleApiError using the same path as your
// existing useProcurementAlert.ts file.

export const ApplySparePartFilters = async (): Promise<void> => {

    CurrentPage.value = 1;

    await GetSpareParts(
        CurrentPage.value,
        SparePartsPerPage.value,
        Search.value,
        CategoryFilter.value,
        ParentCategoryFilter.value
    );
};


let SearchTimeout: ReturnType<typeof setTimeout> | null = null;

export const HandleSparePartSearch = (): void => {

    if (SearchTimeout !== null) {
        clearTimeout(SearchTimeout);
    }

    SearchTimeout = setTimeout(() => {
        void ApplySparePartFilters();
    }, 400);
};


export async function GetCategories(): Promise<CategoryResponse | null> {

    try {

        const Response = await ApiFetch('/categories/list', { method: 'GET' });

        if (!Response.ok) {
            await HandleApiError(
                Response,
                'Failed to retrieve categories.',
            );

            return null;
        }

        const Data: CategoryResponse = await Response.json();

        Categories.value = Data.category;
        ParentCategories.value = Data.parent;

        return Data;

    } catch (error) {

        await Swal.fire({
            title: 'Connection Error!',
            text: 'Unable to retrieve categories.',
            icon: 'error',
        });

        return null;

    }
}


export const CreateNewCategory = async (
    payload: CreateCategory
): Promise<ChildCategory | null> => {

    isCreateCategory.value = true;
    CategoryError.value = null;

    try {

        const response = await ApiFetch('/categories/create', {

            method: 'POST',
            body: JSON.stringify(payload),

        });

        const data = await response.json();
        
        if (!response.ok) {
            
            CategoryError.value = data.detail ?? 'Failed to create new category record.';
            return null;
        }
        
        Categories.value.push(data);

        await HandleSuccess(
            `Category ${data.id} record has been created.`,
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

        isCreateCategory.value = false;

    }
};


export const GetSpareParts = async (
    page: number = 1,
    limit: number = 10,
    search: string = '',
    category_id: number | null = null,
    parent_category_id: number | null = null
): Promise<SparePartListResponse | null> => {

    IsLoading.value = true;

    try {

        const params = new URLSearchParams();

        params.set('page', String(page));
        params.set('limit', String(limit));

        if (search.trim()) {
            params.set('search', search.trim());
        }

        if (category_id !== null) {
            params.set('category_id', String(category_id));
        }

        if (parent_category_id !== null) {
            params.set('parent_category_id', String(parent_category_id),);
        }

        const Response = await ApiFetch(`/spare-parts/list?${params.toString()}`,
            {
                method: 'GET',
            },
        );

        if (!Response.ok) {
            await HandleApiError(
                Response,
                'Failed to retrieve spare parts.',
            );

            return null;
        }

        const Data: SparePartListResponse = await Response.json();

        SpareParts.value = Data.items;
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
};


export const GetSparePart = async (
    partId: number,
): Promise<SparePart | null> => {

    try {

        const Response = await ApiFetch(`/spare-parts/${partId}/details`,
            {
                method: 'GET',
            },
        );

        const Data = await Response.json().catch(() => null);

        if (!Response.ok) {
            throw new Error(
                typeof Data?.detail === 'string'
                    ? Data.detail
                    : 'Failed to load spare part.',
            );
        }

        return Data as SparePart;

    } catch (error) {

        await Swal.fire({
            title: 'Connection Error!',
            text: 'Unable to connect to the server. Please try again later.',
            icon: 'error',
        });

        return null;

    }
};


export const CreateSparePart = async (
    payload: SparePartCreateRequest
): Promise<SparePart | null> => {

    isCreateSparePart.value = true;
    SparePartError.value = null;

    try {

        const response = await ApiFetch('/spare-parts/create', {

            method: 'POST',
            body: JSON.stringify(payload),

        });

        const data = await response.json();
        
        if (!response.ok) {
            
            SparePartError.value = data.detail ?? 'Failed to create spare part record.';
            return null;
        }
        
        SpareParts.value.push(data);

        await HandleSuccess(
            `Spare part ${data.id} record has been created.`,
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

        isCreateSparePart.value = false;

    }
};


export const UpdateSparePart = async (
    SparePartID: number, 
    payload: SparePartUpdateRequest
): Promise<boolean> => {

    try {

        const Response = await ApiFetch(`/spare-parts/${SparePartID}/update`,
            {
                method: 'PATCH',
                body: JSON.stringify(payload)
            }
        );
        
        if (!Response.ok) {
            
            await HandleApiError(
                Response,
                'Failed to update spare part record.'
            );
            return false;

        }

        const data = await Response.json();
        await GetSparePart(data.id);

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


export const DeleteSparePart = async (
    SparePartID: number
): Promise<boolean> => {

    try {

        const Response = await ApiFetch(`/spare-parts/${SparePartID}/delete`,
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

};


