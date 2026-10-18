<script setup lang="ts">
    import Swal from 'sweetalert2';
    import { computed, onMounted, ref, watch } from 'vue';
    import { useRoute, useRouter } from 'vue-router';

    import { currentUser } from '@/services/state/Auth';
    import { DeleteSparePart, GetCategories, GetSparePart, UpdateSparePart } from '@/services/useInventoryReference';
    import { FormatCurrency } from '@/helper/CurrencyFormatter';
    import { HandleSuccess } from '@/helper/HandleSuccess';
    import { 
        Categories,
        ParentCategoryFilter,
        SparePartError,
        type SparePart as SparePartType, 
        type SparePartUpdateRequest
    } from '@/services/state/InventoryReference';


    const Route = useRoute();
    const Router = useRouter();

    const IsLoading = ref<boolean>(true);
    const ErrorMessage = ref<string | null>(null);

    const SparePart = ref<SparePartType | null>(null);

    const IsEditing = ref<boolean>(false);
    const IsUpdating = ref<boolean>(false);

    const SparePartId = computed<number>(() =>
        Number(Route.params.id)
    );

    const EditForm = ref<SparePartUpdateRequest>({
        part_name: null,
        device_model: null,
        device_brand: null,
        specifications: null,
        stock_quantity: null,
        unit_cost: null,
        shelf_location: null,
        image_url: null,
        category_id: null
    });


    const FetchCategories = async (): Promise<void> => {
        await GetCategories();
    };


    const StartEditing = (): void => {
        if (!SparePart.value) return;

        EditForm.value = {
            part_name: SparePart.value.part_name,
            device_model: SparePart.value.device_model,
            device_brand: SparePart.value.device_brand,
            specifications: SparePart.value.specifications,
            stock_quantity: SparePart.value.stock_quantity,
            unit_cost: SparePart.value.unit_cost === null
                ? null
                : Number(SparePart.value.unit_cost),
            shelf_location: SparePart.value.shelf_location,
            image_url: SparePart.value.image_url,
            category_id: SparePart.value.category_id,
        };

        IsEditing.value = true;
    };


    const FilteredCategories = computed(() => {
        if (ParentCategoryFilter.value === null) {
            return Categories.value;
        }

        return Categories.value.filter(
            Category => Category.parent_category_id === ParentCategoryFilter.value
        );
    });


    const SaveChanges = async (): Promise<void> => {

        if (!SparePart.value || IsUpdating.value) return;

        const Confirmation = await Swal.fire({
            title: 'Update Spare Part?',
            text: `Are you sure you want to update ${SparePart.value.part_name} (${SparePart.value.part_code})?`,
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'Yes, update it',
            cancelButtonText: 'Cancel',
            customClass: {
                confirmButton: 'success-button',
                cancelButton: 'error-button'
            },
            reverseButtons: true,
        });

        if (!Confirmation.isConfirmed) return;

        IsUpdating.value = true;

        try {
            
            const Success = await UpdateSparePart(
                SparePart.value.id,
                EditForm.value,
            );

            if (!Success) return;

            IsEditing.value = false;

            await FetchSparePartDetails(SparePart.value.id);

        } finally {

            IsUpdating.value = false;

        }
    };


    const DeleteCurrentSparePart = async (): Promise<void> => {
        if (!SparePart.value) return;

        const Confirmation = await Swal.fire({
            title: 'Delete Spare Part?',
            text: `Are you sure you want to delete ${SparePart.value.part_name} (${SparePart.value.part_code})?`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, delete it',
            cancelButtonText: 'Cancel',
            customClass: {
                confirmButton: 'error-button',
                cancelButton: 'success-button'
            },
            reverseButtons: true,
        });

        if (!Confirmation.isConfirmed) return;

        const Success = await DeleteSparePart(SparePart.value.id);

        if (!Success) return;

        await HandleSuccess(
            'Spare part record has been successfully deleted.',
            'Record Delete Successful!'
        );

        Router.back();
    };


    const FetchSparePartDetails = async (
        partId: number,
    ): Promise<void> => {

        IsLoading.value = true;
        ErrorMessage.value = null;
        SparePart.value = null;

        try {
            if (!Number.isInteger(partId) || partId <= 0) {
                ErrorMessage.value = 'Invalid spare part ID.';
                return;
            }

            const Result = await GetSparePart(partId);

            if (Result === null) {
                ErrorMessage.value = 'Unable to load spare part details.';
                return;
            }

            SparePart.value = Result;

        } catch (error) {
            console.error('Failed to fetch spare part details:', error);

            ErrorMessage.value =
                error instanceof Error
                    ? error.message
                    : 'Unable to load spare part details.';

        } finally {
            IsLoading.value = false;
        }
    };


    const IsAdmin = computed<boolean>(() => {
        return currentUser.value?.role === 'admin';
    });


    onMounted(async () => {
        await FetchCategories();
    });

    watch(
        SparePartId,
        async (id) => {
            await FetchSparePartDetails(id);
        },
        { immediate: true }
    );
    </script>

<template>
    <section class="Spare-Part-Details">

        <!-- Loading -->
        <p v-if="IsLoading">
            Loading spare part details...
        </p>

        <!-- Error -->
        <div
            v-else-if="ErrorMessage"
            class="Spare-Part-Details-Error"
        >
            <h2>Unable to Load Spare Part.</h2>

            <p>{{ ErrorMessage }}</p>

        </div>

        <!-- Details -->
        <template v-else-if="SparePart">

            <!-- Header -->
            <header class="Spare-Part-Details-Header">
                <div>
                    <h1>{{ SparePart.part_name }}</h1>

                    <p>
                        Part Code:
                        <strong>{{ SparePart.part_code }}</strong>
                    </p>
                </div>


                <!-- Spare Part Actions -->
                <div class="Spare-Part-Details-Actions">

                    <button
                        type="button"
                        class="Update-Spare-Part-Button"
                        @click="StartEditing"
                    >
                        Update Spare Part
                    </button>

                    <button
                        v-if="IsAdmin"
                        type="button"
                        class="Delete-Spare-Part-Button"
                        @click="DeleteCurrentSparePart"
                    >
                        Delete Spare Part
                    </button>
                    
                </div>
            </header>

            <!-- Create New Spare Part -->
            <Transition name="form-transition">

                <div
                    v-if="IsEditing"
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
                            :disabled="IsUpdating"
                            @click="IsEditing = false"
                        >
                            ×
                        </button>

                    </div>


                    <form @submit.prevent="SaveChanges">

                        <div class="Form-Field">

                            <label for="part-name">
                                Part Name
                            </label>

                            <input
                                id="part-name"
                                v-model="EditForm.part_name"
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
                                v-model="EditForm.device_model"
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
                                v-model="EditForm.device_brand"
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
                                v-model="EditForm.specifications"
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
                                v-model="EditForm.stock_quantity"
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
                                v-model="EditForm.unit_cost"
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
                                v-model="EditForm.shelf_location"
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
                                v-model="EditForm.image_url"
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
                                v-model="EditForm.category_id"
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
                                :disabled="IsUpdating"
                                @click="IsEditing = false"
                            >
                                Cancel
                            </button>

                            <button
                                type="submit"
                                class="Modal-Confirm-Button"
                                :disabled="IsUpdating"
                            >
                                {{
                                    IsUpdating
                                        ? 'Updating Spare Part...'
                                        : 'Update Spare Part'
                                }}
                            </button>

                        </div>

                    </form>

                </div>

            </Transition>

            <!-- Image -->
            <section class="Spare-Part-Image-Details">
                <h2>Spare Part Image</h2>

                <img
                    v-if="SparePart.image_url"
                    :src="SparePart.image_url"
                    :alt="SparePart.part_name"
                    @error="($event.target as HTMLImageElement).style.display = 'none'"
                />

                <p v-else>
                    No image available.
                </p>
            </section>

            <!-- General Information -->
            <section class="Spare-Part-Information-Details">
                <h2>Spare Part Information</h2>

                <dl>
                    <div>
                        <dt>Part Name</dt>
                        <dd>{{ SparePart.part_name }}</dd>
                    </div>

                    <div>
                        <dt>Part Code</dt>
                        <dd>{{ SparePart.part_code }}</dd>
                    </div>

                    <div>
                        <dt>Category</dt>
                        <dd>{{ SparePart.category_name }}</dd>
                    </div>

                    <div>
                        <dt>Category ID</dt>
                        <dd>{{ SparePart.category_id }}</dd>
                    </div>

                    <div>
                        <dt>Shelf Location</dt>
                        <dd>{{ SparePart.shelf_location }}</dd>
                    </div>
                </dl>
            </section>

            <!-- Device Compatibility -->
            <section class="Spare-Part-Compatibility-Details">
                <h2>Device Compatibility</h2>

                <dl>
                    <div>
                        <dt>Device Brand</dt>
                        <dd>{{ SparePart.device_brand ?? '—' }}</dd>
                    </div>

                    <div>
                        <dt>Device Model</dt>
                        <dd>{{ SparePart.device_model ?? '—' }}</dd>
                    </div>

                    <div>
                        <dt>Specifications</dt>
                        <dd>
                            {{ SparePart.specifications ?? '—' }}
                        </dd>
                    </div>
                </dl>
            </section>

            <!-- Inventory Information -->
            <section class="Spare-Part-Stock-Details">
                <h2>Inventory Information</h2>

                <dl>
                    <div>
                        <dt>Stock Quantity</dt>
                        <dd>{{ SparePart.stock_quantity ?? 'Unknown' }}</dd>
                    </div>

                    <div>
                        <dt>Unit Cost</dt>
                        <dd>{{ FormatCurrency(SparePart.unit_cost) }}</dd>
                    </div>
                </dl>
            </section>

        </template>

    </section>
</template>