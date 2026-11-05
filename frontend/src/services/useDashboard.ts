import Swal from "sweetalert2";
import { ref } from "vue";
import { ApiFetch } from "@/api/Client";
import type {
    ServiceRequestDashboard,
    RecentServiceRequestsResponse,
    RecentActivitiesResponse,
    RecentServiceRequest,
    RecentActivity,
    LowStockCheckResponse,
} from "@/services/state/Dashboard";

export function useDashboard() {

    const statistics = ref<ServiceRequestDashboard | null>(null);

    const totalCustomers = ref(0);
    const totalActiveUsers = ref(0);
    const totalLowStockParts = ref(0);

    const recentRequests = ref<RecentServiceRequest[]>([]);
    const recentActivities = ref<RecentActivity[]>([]);

    const isLoading = ref(false);
    const error = ref<string | null>(null);

    async function fetchDashboard() {

        isLoading.value = true;
        error.value = null;

        try {
            const [
                requestCountsResponse,
                customerCountsResponse,
                userCountsResponse,
                lowStockCountsResponse,
                requestsResponse,
                activitiesResponse,
            ] = await Promise.all([
                ApiFetch("/service-requests/counts"),
                ApiFetch("/customers/counts"),
                ApiFetch("/user/counts"),
                ApiFetch("/spare-parts/counts"),
                ApiFetch("/service-requests/recent"),
                ApiFetch("/procurement-alerts/recent"),
            ]);

            const [
                requestCounts,
                customerCounts,
                userCounts,
                lowStockCounts,
                requestsData,
                activitiesData,
            ] = await Promise.all([
                requestCountsResponse.json() as Promise<ServiceRequestDashboard>,
                customerCountsResponse.json() as Promise<{ total_customers: number }>,
                userCountsResponse.json() as Promise<{ total_active_users: number }>,
                lowStockCountsResponse.json() as Promise<{ total_low_stock_parts: number }>,
                requestsResponse.json() as Promise<RecentServiceRequestsResponse>,
                activitiesResponse.json() as Promise<RecentActivitiesResponse>,
            ]);

            statistics.value = requestCounts;

            totalCustomers.value = customerCounts.total_customers;
            totalActiveUsers.value = userCounts.total_active_users;
            totalLowStockParts.value = lowStockCounts.total_low_stock_parts;

            recentRequests.value = requestsData.items;
            recentActivities.value = activitiesData.items;

        } catch (err) {

            error.value =
                err instanceof Error
                    ? err.message
                    : "Failed to load dashboard data.";

        } finally {

            isLoading.value = false;

        }

    }


    async function CheckLowStock(): Promise<void> {

        const confirmation = await Swal.fire({
            title: "Check Inventory Stock?",
            text: "This will scan all active spare parts with 5 or fewer units remaining.",
            icon: "question",
            showCancelButton: true,
            confirmButtonText: "Yes, Check Stock",
            cancelButtonText: "Cancel",
            customClass: {
                confirmButton: 'success-button',
                cancelButton: 'error-button'
            },
            reverseButtons: true,
        });

        if (!confirmation.isConfirmed) return;

        try {

            Swal.fire({
                title: "Checking Stock...",
                text: "Please wait while we scan the spare parts inventory.",
                allowOutsideClick: false,
                allowEscapeKey: false,
                didOpen: () => {
                    Swal.showLoading();
                },
            });

            const response = await ApiFetch(
                "/procurement-alerts/check-stock",
                {
                    method: "POST",
                }
            );

            const result = await response.json() as LowStockCheckResponse;

            if (!response.ok) {
                throw new Error(
                    (result as unknown as { detail?: string }).detail
                    ?? "Failed to check inventory stock."
                );
            }

            await fetchDashboard();

            await Swal.fire({
                title: result.total_low_stock_parts > 0
                    ? result.alert_created
                        ? "Low-Stock Alert Created!"
                        : "Low-Stock Alert Updated!"
                    : "No Low Stock Found",
                text: result.message,
                icon: result.total_low_stock_parts > 0
                    ? "success"
                    : "info",
                confirmButtonText: "OK",
                customClass: {
                    confirmButton: 'success-button'
                },
            });

        } catch (err) {

            Swal.close();

            await Swal.fire({
                title: "Stock Check Failed",
                text: err instanceof Error
                    ? err.message
                    : "An unexpected error occurred.",
                icon: "error",
                confirmButtonText: "OK",
                customClass: {
                    confirmButton: 'success-button'
                },
            });

        }

    }

    return {
        statistics,
        totalCustomers,
        totalActiveUsers,
        totalLowStockParts,
        recentRequests,
        recentActivities,
        isLoading,
        error,
        fetchDashboard,
        CheckLowStock,
    };

}
