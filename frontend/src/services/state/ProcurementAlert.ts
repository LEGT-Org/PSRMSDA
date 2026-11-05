import { ref } from "vue";

export type ProcurementAlertResolution =
    | 'all'
    | 'unresolved'
    | 'resolved';

interface LowStockPart {
    part_id: number;
    part_name: string;
    stock_quantity: number;
}

export interface ProcurementAlert {
    id: number;
    request_id: number;
    part_id: number | null;
    part_name_snapshot: string | null;
    low_stock_parts_snapshot: LowStockPart[] | null;
    alert_type: string;
    alert_message: string | null;
    is_resolved: boolean;
    created_at: string;
}

export interface ProcurementAlertPageListResponse {
    pages: number;
    resolved_alerts: any;
    unresolved_alerts: any;
    total_alerts: any;
    items: ProcurementAlert[];
    total: number;
    page: number;
    limit: number;
    total_pages: number;
}


export const ProcurementAlerts = ref<ProcurementAlert[]>([]);

export const CurrentPage = ref(1);
export const ProcurementAlertsPerPage = ref(10);
export const Total = ref(0);
export const TotalPages = ref(0);

export const IsLoading = ref(false);
export const Search = ref('');
export const StatusFilter = ref<ProcurementAlertResolution>('unresolved');
export const TypeFilter = ref<string>('all');

export const TotalAlerts = ref(0);
export const UnresolvedAlerts = ref(0);
export const ResolvedAlerts = ref(0);
