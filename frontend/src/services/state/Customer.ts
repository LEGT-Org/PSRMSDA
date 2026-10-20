import { ref } from "vue";

export interface Customer {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    phone_number: string;
    created_at: string;
}

export interface CustomerListResponse {
    items: Customer[];
    total: number;
    page: number;
    limit: number;
    pages: number;
}

export interface CustomerCreateRequest {
    first_name: string;
    last_name: string;
    email: string;
    phone_number: string;
}

export interface CustomerUpdateRequest {
    first_name: string | null;
    last_name: string | null;
    email: string | null;
    phone_number: string | null;
}


export const Customers = ref<Customer[]>([]);

export const isCreateCustomer = ref<boolean>(false);
export const ShowCreateCustomer = ref<boolean>(false);
export const CustomerError = ref<string | null>(null);

export const CurrentPage = ref<number>(1);
export const CustomerPerPage = ref<number>(10);

export const Total = ref<number>(0);
export const TotalPages = ref<number>(0);

export const IsLoading = ref<boolean>(false);
export const Search = ref<string>('');