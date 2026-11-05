from typing import Protocol

from app.modules.procurement_alert.schema import ProcurementAlertSchema
from app.modules.procurement_alert.model import ProcurementAlert
from app.modules.category.model import Category


class CategoryInterface(Protocol):

    def get_category_by_id(
        self,
        category_id: str
    ) -> Category:

        pass


class ProcurementAlertInterface(Protocol):

    def create_procurement_alert(
        self,
        data: ProcurementAlertSchema
    ) -> ProcurementAlert:

        pass

    def sync_inventory_stock_alert(
        self,
        part_id: int,
        part_name: str,
        stock_quantity: int,
    ) -> None:
    
        pass

    def cancel_by_request(
        self,
        part_id: int,
        alert_message: str
    ) -> ProcurementAlert:

        pass