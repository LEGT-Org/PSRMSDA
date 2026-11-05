
export interface ServiceRequestDashboard {
    total: number;
    pending: number;
    in_progress: number;
    completed: number;
}

export interface CustomerDashboard {
    total_customers: number;
}

export interface ActiveUsersDashboard {
    total_active_users: number;
}

export interface LowStockDashboard {
    total_low_stock_parts: number;
}

export interface RecentServiceRequest {
    id: number;
    device: string;
    customer: string;
    technician: string;
    status: string;
    created_at: string;
}

export interface RecentServiceRequestsResponse {
    items: RecentServiceRequest[];
}

export interface RecentActivity {
    id: number;
    description: string;
    time: string;
}

export interface RecentActivitiesResponse {
    items: RecentActivity[];
}

export interface LowStockCheckResponse {
    message: string;
    alert_created: boolean;
    total_low_stock_parts: number;
    alert: unknown | null;
}
