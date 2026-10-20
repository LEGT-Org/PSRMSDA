
import { ref } from "vue";
import { ApiFetch } from "@/api/Client";
import type {
    ServiceRequestDashboard,
    RecentServiceRequestsResponse,
    RecentActivitiesResponse,
    RecentServiceRequest,
    RecentActivity,
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
    };
}
