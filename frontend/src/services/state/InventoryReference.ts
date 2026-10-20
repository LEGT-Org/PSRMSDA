import { ref } from 'vue';

export interface SparePart {
    id: number;
    part_name: string;
    part_code: string;
    device_model: string | null;
    device_brand: string | null;
    specifications: string | null;
    stock_quantity: number | null;
    unit_cost: number | string | null;
    shelf_location: string;
    image_url: string | null;
    category_id: number;
    category_name: string;
}

export interface SparePartListResponse {
    items: SparePart[];
    total: number;
    page: number;
    limit: number;
    pages: number;
}

export interface SparePartCreateRequest {
    part_name: string;
    device_model: string | null;
    device_brand: string | null;
    specifications: string | null;
    stock_quantity: number | null;
    unit_cost: number | null;
    shelf_location: string;
    image_url: string | null;
    category_id: number | null;
}

export interface SparePartUpdateRequest {
    part_name: string | null;
    device_model: string | null;
    device_brand: string | null;
    specifications: string | null;
    stock_quantity: number | null;
    unit_cost: number | null;
    shelf_location: string | null;
    image_url: string | null;
    category_id: number | null;
}

export interface CreateCategory {
    parent_category_id: number | null;
    name: string;
    description: string;
}

export interface ChildCategory {
    id: number;
    name: string;
    parent_category_id: number;
}

export interface ParentCategory {
    id: number;
    name: string;
}

export interface CategoryResponse {
    category: ChildCategory[];
    parent: ParentCategory[];
}

export const Categories = ref<ChildCategory[]>([]);
export const ParentCategories = ref<ParentCategory[]>([]);
export const SpareParts = ref<SparePart[]>([]);

export const isCreateSparePart = ref<boolean>(false);
export const ShowCreateSparePart = ref<boolean>(false);
export const SparePartError = ref<string | null>(null);

export const isCreateCategory = ref<boolean>(false);
export const ShowCreateCategory = ref<boolean>(false);
export const CategoryError = ref<string | null>(null);

export const CurrentPage = ref<number>(1);
export const SparePartsPerPage = ref<number>(10);

export const Total = ref<number>(0);
export const TotalPages = ref<number>(0);

export const IsLoading = ref<boolean>(false);
export const Search = ref<string>('');
export const CategoryFilter = ref<number | null>(null);
export const ParentCategoryFilter = ref<number | null>(null);