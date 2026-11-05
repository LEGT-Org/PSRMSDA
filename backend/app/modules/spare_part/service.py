import re
from math import ceil
from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.modules.spare_part.interface import ProcurementAlertInterface, CategoryInterface
from app.modules.spare_part.repository import SparePartRepository
from app.modules.spare_part.model import SparePart
from app.modules.spare_part.schema import (
    ProcurementAlertTypePreview,
    ProcurementAlertRequest,
    SparePartCreateRequest,
    SparePartUpdateRequest,
    SparePartListResponse,
    SparePartResponse
)

from app.shared.exception import (
    SparePartPartCodeAlreadyExistError,
    SparePartInsufficientQuantityError,
    SparePartUpdateRequestFailedError,
    SparePartUpdateQuantityError,
    SparePartCreationFailedError,
    SparePartDeletionFailedError,
    SparePartUpdateFailedError,
    SparePartDoesNotExistError,
    CategoryDoesNotExistError
)


class SparePartService:
    
    def __init__(
        self,
        repository: SparePartRepository,
        category_interface: CategoryInterface,
        procurement_alert_interface: ProcurementAlertInterface,
        db: Session
    ):

        self.repository = repository
        self.category_interface = category_interface
        self.procurement_alert_interface = procurement_alert_interface
        self.db = db


    def create_spare_part(
        self,
        request: SparePartCreateRequest,
        user_id: int,
    ) -> SparePartResponse:

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        category = self.category_interface.get_category_by_id(request.category_id)

        if category is None:
            raise CategoryDoesNotExistError()

        spare_part = SparePart(
            part_name=request.part_name,
            part_code=f"TEMP-{uuid4().hex}",
            device_brand=request.device_brand,
            device_model=request.device_model,
            specifications=request.specifications,
            stock_quantity=request.stock_quantity,
            unit_cost=request.unit_cost,
            shelf_location=request.shelf_location,
            image_url=request.image_url,
            category_id=category.id,
            last_modified_by_id=user_id,
            created_at=now,
            updated_at=now,
            deleted_at=None
        )

        try:

            self.repository.create(spare_part)

            spare_part.part_code = f"SP-{spare_part.id:06d}"

            self.db.commit()
            self.db.refresh(spare_part)

            return SparePartResponse(
                id=spare_part.id,
                part_name=spare_part.part_name,
                part_code=spare_part.part_code,
                device_model=spare_part.device_model,
                device_brand=spare_part.device_brand,
                specifications=spare_part.specifications,
                stock_quantity=spare_part.stock_quantity,
                unit_cost=spare_part.unit_cost,
                shelf_location=spare_part.shelf_location,
                image_url=spare_part.image_url,
                category_id=spare_part.category_id,
                category_name=spare_part.categories.name
            )

        except Exception as error:

            self.db.rollback()
            raise SparePartCreationFailedError() from error


    def deduct_spare_part_quantity(
        self,
        part_id: int,
        quantity_used: int
    ) -> int:

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        stored_spare_part = self.repository.get_by_id(part_id)
        new_quantity = stored_spare_part.stock_quantity - quantity_used

        if new_quantity < 0:
            raise SparePartInsufficientQuantityError()

        try:

            self.repository.update_quantity(
                stored_spare_part=stored_spare_part,
                new_quantity=new_quantity,
                now=now
            )

            self.db.flush()

            return new_quantity

        except Exception as error:
            
            raise SparePartUpdateQuantityError() from error


    def add_spare_part_quantity(
        self,
        part_id: int,
        quantity_to_add: int
    ) -> int:

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        stored_spare_part = self.repository.get_by_id(part_id)
        new_quantity = stored_spare_part.stock_quantity + quantity_to_add

        if new_quantity < 0:
            raise SparePartInsufficientQuantityError()

        try:

            self.repository.update_quantity(
                stored_spare_part=stored_spare_part,
                new_quantity=new_quantity,
                now=now
            )

            self.db.flush()

            return new_quantity

        except Exception as error:
            
            raise SparePartUpdateQuantityError() from error


    def update_spare_part(
        self,
        part_id: int,
        actor_id: int,
        request: SparePartUpdateRequest,
    ) -> None:

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        spare_part = self.repository.get_by_id(part_id)

        if spare_part is None:
            raise SparePartDoesNotExistError()

        updates = {
            field: value
            for field, value in request.model_dump(exclude_unset=True).items()
            if value is not None
        }

        if not updates:
            raise SparePartUpdateRequestFailedError()

        # Preserve the existing category if it isn't being updated.
        category_id = spare_part.category_id

        if "category_id" in updates:

            category = self.category_interface.get_category_by_id(
                updates["category_id"]
            )

            if category is None:
                raise CategoryDoesNotExistError()

            category_id = category.id

        try:

            # 1. Update the spare part.
            self.repository.update(
                stored_spare_part=spare_part,
                category_id=category_id,
                approve_by=actor_id,
                updates=updates,
                now=now
            )

            # 2. Synchronize the inventory alert only when stock changes.
            if "stock_quantity" in updates:

                self.procurement_alert_interface.sync_inventory_stock_alert(
                    part_id=spare_part.id,
                    part_name=spare_part.part_name,
                    stock_quantity=spare_part.stock_quantity,
                )

            # 3. Commit both the inventory update and alert together.
            self.db.commit()
            self.db.refresh(spare_part)

        except Exception as error:

            self.db.rollback()

            print(error)

            raise SparePartUpdateFailedError() from error


    def delete_spare_part(
        self,
        part_id: int,
        actor_id: int
    ) -> None:

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        spare_part = self.repository.get_by_id(part_id)

        if spare_part is None:
            raise SparePartDoesNotExistError()

        try:

            self.repository.delete(
                stored_spare_part=spare_part,
                approve_by=actor_id,
                now=now
            )

            self.db.commit()

        except Exception as error:

            self.db.rollback()

            print(error)
            raise SparePartDeletionFailedError() from error


    def search_matched_spare_part(
        self,
        part_name: str,
        device_type: str
    ) -> list[SparePart]:

        keywords = set(re.findall(r"[a-z0-9]+", part_name.lower()))

        matched_parts = {}

        for keyword in keywords:
            spare_parts = self.repository.search_by_name(
                part_name=keyword,
                device_type=device_type
            )

            for spare_part in spare_parts:
                matched_parts[spare_part.id] = spare_part

        # Count matching keywords for each spare part.
        def get_match_score(spare_part: SparePart) -> int:
            part_keywords = set(
                re.findall(r"[a-z0-9]+", spare_part.part_name.lower())
            )

            return len(keywords & part_keywords)

        return sorted(
            matched_parts.values(),
            key=get_match_score,
            reverse=True
        )


    def get_list_of_spare_parts(
        self,
        page: int,
        limit: int,
        search: str | None = None,
        category_id: int | None = None,
        parent_category_id: int | None = None,
    ) -> SparePartListResponse:

        spare_parts, total = self.repository.get_all(
            page=page,
            limit=limit,
            search=search,
            category_id=category_id,
            parent_category_id=parent_category_id
        )

        items = [
            SparePartResponse(
                id=spare_part.id,
                part_name=spare_part.part_name,
                part_code=spare_part.part_code,
                device_model=spare_part.device_model,
                device_brand=spare_part.device_brand,
                specifications=spare_part.specifications,
                stock_quantity=spare_part.stock_quantity,
                unit_cost=spare_part.unit_cost,
                shelf_location=spare_part.shelf_location,
                image_url=spare_part.image_url,
                category_id=spare_part.category_id,
                category_name=spare_part.categories.name,
            )
            for spare_part in spare_parts
        ]

        pages = ceil(total / limit) if total else 0

        return SparePartListResponse(
            items=items,
            total=total,
            page=page,
            limit=limit,
            pages=pages,
        )


    def get_spare_part_specific_details(
        self, 
        part_id: int
    ) -> SparePartResponse:

        spare_part = self.repository.get_by_id(part_id)

        if spare_part is None:
            raise SparePartDoesNotExistError()

        item = SparePartResponse(
            id=spare_part.id,
            part_name=spare_part.part_name,
            part_code=spare_part.part_code,
            device_model=spare_part.device_model,
            device_brand=spare_part.device_brand,
            specifications=spare_part.specifications,
            stock_quantity=spare_part.stock_quantity,
            unit_cost=spare_part.unit_cost,
            shelf_location=spare_part.shelf_location,
            image_url=spare_part.image_url,
            category_id=spare_part.category_id,
            category_name=spare_part.categories.name,
        )

        return item


    def get_low_stock_counts(
        self
    ) -> int:

        return self.repository.count_low_stock_parts()


    def get_low_stock_parts(
        self,
        threshold: int = 5,
    ) -> list[SparePart]:

        return self.repository.get_low_stocks(
            threshold=threshold
        )


    