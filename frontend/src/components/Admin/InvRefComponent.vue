<script setup lang="ts">
    import Swal from 'sweetalert2'; 
    import { computed, onMounted, ref } from 'vue';
    import Router from '@/router/Router';

    import { FormatCurrency } from '@/helper/CurrencyFormatter';
    import { currentUser } from '@/services/state/Auth';
    import {
        SpareParts,
        CurrentPage,
        SparePartsPerPage,
        TotalPages,
        IsLoading,
        Search,
        CategoryFilter,
        Categories,
        ParentCategories,
        ParentCategoryFilter,
        isCreateSparePart,
        ShowCreateSparePart,
        SparePartError,
        ShowCreateCategory,
        isCreateCategory,
        CategoryError,
        type SparePartCreateRequest,
        type CreateCategory,
    } from '@/services/state/InventoryReference';

    import {
        ApplySparePartFilters,
        CreateNewCategory,
        CreateSparePart,
        GetCategories,
        GetSpareParts,
        HandleSparePartSearch,
    } from '@/services/useInventoryReference';


    const PartName = ref<string>('');
    const DeviceModel = ref<string>('');
    const DeviceBrand = ref<string>('');
    const Specifications = ref<string>('');
    const StockQuantity = ref<number | null>(null);
    const UnitCost = ref<number | null>(null);
    const ShelfLocation = ref<string>('');
    const ImageURL = ref<string>('');
    const CategoryID = ref<number | null>(null);


    const CategoryName = ref<string>('');
    const CategoryDescription = ref<string>('');
    const ParentCategoryID = ref <number | null>(null);

    
    const ResetCreateSparePart = () => {
        PartName.value = ''
        DeviceModel.value = ''
        DeviceBrand.value = ''
        Specifications.value = ''
        StockQuantity.value = null
        UnitCost.value = null
        ShelfLocation.value = ''
        ImageURL.value = ''
        CategoryID.value = null
    }


    const ResetAddCategory = () => {
        CategoryName.value = ''
        CategoryDescription.value = '',
        ParentCategoryID.value = null
    }


    const CloseCreateSparePartModal = () => {
        if (isCreateSparePart.value) {
            return;
        }

        ShowCreateSparePart.value = false;

        ResetCreateSparePart();
    }

    const CloseAddCategoryModal = () => {
        if (isCreateCategory.value) {
            return;
        }

        ShowCreateCategory.value = false;

        ResetAddCategory();
    }


    const SubmitCreateSparePart = async () => {

        const Confirmation = await Swal.fire({
            title: 'Create this record?',
            text: `Double-check the details below. You can go back and edit if anything looks wrong.`,
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'Create record',
            cancelButtonText: 'Go back and edit',
            customClass: {
                confirmButton: 'success-button',
                cancelButton: 'error-button'
            },
            reverseButtons: true,
            focusCancel: true,
        });

        if (!Confirmation.isConfirmed) return;
        

        const payload: SparePartCreateRequest = {
            part_name: PartName.value,
            device_model: DeviceModel.value,
            device_brand: DeviceBrand.value,
            specifications: Specifications.value,
            stock_quantity: StockQuantity.value,
            unit_cost: UnitCost.value,
            shelf_location: ShelfLocation.value,
            image_url: ImageURL.value,
            category_id: CategoryID.value
        }

        const spare_parts = await CreateSparePart(payload);

        if (!spare_parts) return;

        CloseCreateSparePartModal()
    }


    const SubmitNewCategory = async () => {
        
         const Confirmation = await Swal.fire({
            title: 'Add this record?',
            text: `Double-check the details below. You can go back and edit if anything looks wrong.`,
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'Add record',
            cancelButtonText: 'Go back and edit',
            customClass: {
                confirmButton: 'success-button',
                cancelButton: 'error-button'
            },
            reverseButtons: true,
            focusCancel: true,
        });

        if (!Confirmation.isConfirmed) return;

        const payload: CreateCategory = {
            parent_category_id: ParentCategoryID.value,
            name: CategoryName.value,
            description: CategoryDescription.value
        }
        
        const category = await CreateNewCategory(payload)

        if (!category) return;
        
        CloseAddCategoryModal()
        
    }


    const FilteredCategories = computed(() => {
        if (ParentCategoryFilter.value === null) {
            return Categories.value;
        }

        return Categories.value.filter(
            Category => Category.parent_category_id === ParentCategoryFilter.value
        );
    });


    const HandleParentCategoryChange = async (): Promise<void> => {
        CategoryFilter.value = null;
        await ApplySparePartFilters();
    };
        

    const FetchPage = async (): Promise<void> => {
        await GetSpareParts(
            CurrentPage.value,
            SparePartsPerPage.value,
            Search.value,
            CategoryFilter.value,
            ParentCategoryFilter.value
        );
    };


    const FetchCategories = async (): Promise<void> => {
        await GetCategories();
    };


    const GoToNextPage = async (): Promise<void> => {
        if (CurrentPage.value >= TotalPages.value) {
            return;
        }

        await GetSpareParts(
            CurrentPage.value + 1,
            SparePartsPerPage.value,
            Search.value,
            CategoryFilter.value,
            ParentCategoryFilter.value
        );
    };


    const GoToPreviousPage = async (): Promise<void> => {
        if (CurrentPage.value <= 1) {
            return;
        }

        await GetSpareParts(
            CurrentPage.value - 1,
            SparePartsPerPage.value,
            Search.value,
            CategoryFilter.value,
            ParentCategoryFilter.value
        );
    };


    const GoToSparePartsDetail = async (id: number): Promise<void> => {
        await Router.push(`/admin/inventory/${id}`);
    }

    
    const IsAdmin = computed<boolean>(() => {
        return currentUser.value?.role === 'admin';
    });


    onMounted(async () => {
        await Promise.all([
            FetchCategories(),
            FetchPage()
        ]);
    });
</script>

<template>
    <section class="Inventory-Reference-Management">
        <!-- Header -->
        <div class="Inventory-Reference-Title">

            <div>
                <h1>Inventory Reference Management</h1>
                <p>View and manage spare parts.</p>
            </div>

            <div>
                <button
                    v-if="IsAdmin"
                    type="button"
                    class="Add-New-Category-Button"
                    @click="ShowCreateCategory = true"
                >
                    Add New Category
                </button>

                <button
                    type="button"
                    class="Create-Inventory-Reference-Button"
                    @click="ShowCreateSparePart = true"
                >
                    Create Spare Part
                </button>
            </div>

        </div>

        <!-- Create New Category -->
        <Transition name="form-transition">

            <div
                v-if="ShowCreateCategory"
                class="Form-Panel"
            >

                <div class="Modal-Header">

                    <div>
                        <h2>Add New Category</h2>

                        <p>
                            Create a new category record.
                        </p>
                    </div>

                    <button
                        type="button"
                        class="Modal-Close"
                        :disabled="isCreateCategory"
                        @click="CloseAddCategoryModal"
                    >
                        ×
                    </button>

                </div>


                <form @submit.prevent="SubmitNewCategory">

                    <div class="Form-Field">

                        <label for="category-name">
                            Category Name
                        </label>

                        <input
                            id="category-name"
                            v-model="CategoryName"
                            type="text"
                            placeholder="e.g. Electric Fan"
                            autocomplete="given-name"
                            required
                        />

                    </div>


                    <div class="Form-Field">

                        <label for="category-description">
                            Description
                        </label>

                        <textarea
                            id="category-description"
                            v-model="CategoryDescription"
                            type="text"
                            placeholder="Descriptions..."
                            autocomplete="family-name"
                            required
                        />

                    </div>

                    <div class="Form-Field">

                        <label for="category-id">
                            Parent Category
                        </label>

                        <select
                            id="category-id"
                            v-model="ParentCategoryID"
                            class="Spare-Part-Filter"
                            required
                        >
                            <option value="" disabled hidden>Select a Category</option>

                            <option
                                v-for="Category in  ParentCategories"
                                :key="Category.id"
                                :value="Category.id"
                            >
                                {{ Category.name }}
                            </option>
                        </select>
                        
                    </div>

                    <p
                        v-if="CategoryError"
                        class="Form-Error"
                    >
                        {{ CategoryError }}
                    </p>


                    <div class="Modal-Actions">

                        <button
                            type="button"
                            class="Modal-Cancel-Button"
                            :disabled="isCreateCategory"
                            @click="CloseAddCategoryModal"
                        >
                            Cancel
                        </button>

                        <button
                            type="submit"
                            class="Modal-Confirm-Button"
                            :disabled="isCreateCategory"
                        >
                            {{
                                isCreateSparePart
                                    ? 'Adding new category...'
                                    : 'Add new category'
                            }}
                        </button>

                    </div>

                </form>

            </div>

        </Transition>

        <!-- Create New Spare Part -->
        <Transition name="form-transition">

            <div
                v-if="ShowCreateSparePart"
                class="Form-Panel"
            >

                <div class="Modal-Header">

                    <div>
                        <h2>Create Spare Part</h2>

                        <p>
                            Create a new spare part record.
                        </p>
                    </div>

                    <button
                        type="button"
                        class="Modal-Close"
                        :disabled="isCreateSparePart"
                        @click="CloseCreateSparePartModal"
                    >
                        ×
                    </button>

                </div>


                <form @submit.prevent="SubmitCreateSparePart">

                    <div class="Form-Field">

                        <label for="part-name">
                            Part Name
                        </label>

                        <input
                            id="part-name"
                            v-model="PartName"
                            type="text"
                            placeholder="e.g. Thermal Fuse"
                            autocomplete="given-name"
                            required
                        />

                    </div>


                    <div class="Form-Field">

                        <label for="device-model">
                            Device Model
                        </label>

                        <input
                            id="device-model"
                            v-model="DeviceModel"
                            type="text"
                            placeholder="e.g. TF-130C"
                            autocomplete="family-name"
                            required
                        />

                    </div>


                    <div class="Form-Field">

                        <label for="device-brand">
                            Device Brand
                        </label>

                        <input
                            id="device-brand"
                            v-model="DeviceBrand"
                            type="text"
                            placeholder="e.g Panasonic"
                            autocomplete="family-name"
                            required
                        />

                    </div>

                    <div class="Form-Field">

                        <label for="specifications">
                            Specifications
                        </label>

                        <input
                            id="specifications"
                            v-model="Specifications"
                            type="text"
                            placeholder="e.g 130°C, 2A, 250V"
                            autocomplete="family-name"
                            required
                        />

                    </div>

                    <div class="Form-Field">

                        <label for="stock-quantity">
                            Stock Quantity
                        </label>

                        <input
                            id="stock-quantity"
                            v-model="StockQuantity"
                            type="number"
                            min="0"
                            placeholder="e.g 0"
                            autocomplete="family-name"
                            required
                        />

                    </div>

                    <div class="Form-Field">

                        <label for="unit-cost">
                            Unit Cost
                        </label>

                        <input
                            id="unit-cost"
                            v-model="UnitCost"
                            type="number"
                            min="0"
                            placeholder="e.g 1000"
                            autocomplete="family-name"
                            required
                        />

                    </div>

                    <div class="Form-Field">

                        <label for="shelf-location">
                            Shelf Location
                        </label>

                        <input
                            id="shelf-location"
                            v-model="ShelfLocation"
                            type="text"
                            placeholder="e.g SH-000594"
                            autocomplete="family-name"
                            required
                        />

                    </div>

                    <div class="Form-Field">

                        <label for="image-url">
                            Image URL
                        </label>

                        <input
                            id="image-url"
                            v-model="ImageURL"
                            type="url"
                            placeholder="e.g https://example.com/images"
                            autocomplete="family-name"
                        />

                    </div>

                    <div class="Form-Field">

                        <label for="category-id">
                            Category
                        </label>

                        <select
                            id="category-id"
                            v-model="CategoryID"
                            class="Spare-Part-Filter"
                            required
                        >
                            <option value="" disabled hidden>Select a Category</option>

                            <option
                                v-for="Category in  FilteredCategories"
                                :key="Category.id"
                                :value="Category.id"
                            >
                                {{ Category.name }}
                            </option>
                        </select>
                        
                    </div>

                    <p
                        v-if="SparePartError"
                        class="Form-Error"
                    >
                        {{ SparePartError }}
                    </p>


                    <div class="Modal-Actions">

                        <button
                            type="button"
                            class="Modal-Cancel-Button"
                            :disabled="isCreateSparePart"
                            @click="CloseCreateSparePartModal"
                        >
                            Cancel
                        </button>

                        <button
                            type="submit"
                            class="Modal-Confirm-Button"
                            :disabled="isCreateSparePart"
                        >
                            {{
                                isCreateSparePart
                                    ? 'Creating Spare Part...'
                                    : 'Create Spare Part'
                            }}
                        </button>

                    </div>

                </form>

            </div>

        </Transition>

        <!-- Filters -->
        <div class="Spare-Part-Filters">

            <div class="Search-Field">
                <label for="spare-part-search">
                    Search
                </label>

                <input
                    id="spare-part-search"
                    v-model="Search"
                    class="Spare-Part-Search"
                    type="search"
                    placeholder="Search spare parts..."
                    @input="HandleSparePartSearch"
                />
            </div>

            <div class="Filter-Field">
                <label for="spare-part-type">
                    Type
                </label>

                <select
                    id="spare-part-type"
                    v-model="CategoryFilter"
                    class="Spare-Part-Filter"
                    @change="ApplySparePartFilters"
                >
                    <option :value="null">All Types</option>

                    <option
                        v-for="Category in  FilteredCategories"
                        :key="Category.id"
                        :value="Category.id"
                    >
                        {{ Category.name }}
                    </option>
                </select>
            </div>

            <div class="Filter-Field">
                <label for="spare-part-category">
                    Categoty
                </label>

                <select
                    id="spare-part-category"
                    v-model="ParentCategoryFilter"
                    class="Spare-Part-Filter"
                    @change="HandleParentCategoryChange"
                >
                    <option :value="null">All Categories</option>

                    <option
                        v-for="Parent in ParentCategories"
                        :key="Parent.id"
                        :value="Parent.id"
                    >
                        {{ Parent.name }}
                    </option>
                </select>
            </div>
        </div>

        <!-- Loading -->
        <p v-if="IsLoading">
            Loading spare parts...
        </p>

        <template v-else>
            <!-- Spare Parts Table -->
            <div class="Spare-Part-Table-Container">
                <table class="Spare-Part-Table">
                    <thead>
                        <tr>
                            <th>Part Code</th>
                            <th>Part Name</th>
                            <th>Type</th>
                            <th>Brand</th>
                            <th>Model</th>
                            <th>Quantity</th>
                            <th>Unit Cost</th>
                            <th>Shelf Location</th>
                            <th>Actions</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr
                            v-for="Part in SpareParts"
                            :key="Part.id"
                        >
                            <td>
                                <strong>{{ Part.part_code }}</strong>
                            </td>
                            <td>{{ Part.part_name }}</td>
                            <td>{{ Part.category_name }}</td>
                            <td>{{ Part.device_brand ?? '—' }}</td>
                            <td>{{ Part.device_model ?? '—' }}</td>
                            <td>{{ Part.stock_quantity ?? '—' }}</td>
                            <td>{{ FormatCurrency(Part.unit_cost) }}</td>
                            <td>{{ Part.shelf_location }}</td>

                            <td>
                                <button
                                    type="button"
                                    class="View-Request-Button"
                                    @click="GoToSparePartsDetail(Part.id)"
                                >
                                    →
                                </button>
                            </td>

                        </tr>

                        <tr v-if="SpareParts.length === 0">
                            <td colspan="8">
                                <div class="Spare-Part-Empty-State">
                                    <h3>No spare parts found</h3>
                                    <p>
                                        No spare parts record match
                                        your current search or filter.
                                    </p>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Pagination -->
            <div class="Pagination">
                <button
                    type="button"
                    :disabled="CurrentPage <= 1 || IsLoading"
                    @click="GoToPreviousPage"
                >
                    Previous
                </button>

                <span>
                    Page {{ CurrentPage }} of {{ TotalPages }}
                </span>

                <button
                    type="button"
                    :disabled="
                        CurrentPage >= TotalPages ||
                        IsLoading ||
                        TotalPages === 0
                    "
                    @click="GoToNextPage"
                >
                    Next
                </button>
            </div>
        </template>
    </section>
</template>