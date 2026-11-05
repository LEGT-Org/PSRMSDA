from datetime import date, datetime, time, timedelta

from sqlalchemy.orm import Session, selectinload, joinedload
from sqlalchemy import or_, select

from app.modules.spare_part.model import SparePart
from app.modules.category.model import Category

from app.modules.service_request.model import ServiceRequest
from app.modules.llm_diagnosis.model import LLMDiagnosis
from app.modules.customer.model import Customer
from app.modules.user.model import User
from app.modules.service_request.schema import (
    LLMDiagnosisStatusPreview,
    ServiceRequestStatus,
)


class ReportRepository:

    def __init__(
        self, 
        db: Session
    ):
        self.db = db


    def get_low_stock_parts(
        self,
        threshold: int = 5,
    ) -> list[SparePart]:

        statement = (
            select(SparePart)
            .where(
                SparePart.deleted_at.is_(None),
                SparePart.stock_quantity <= threshold,
            )
            .order_by(SparePart.part_name.asc())
        )

        return list(self.db.scalars(statement).all())


    def get_spare_parts(
        self,
        search: str | None = None,
        category_id: int | None = None,
    ) -> list[SparePart]:

        statement = (
            select(SparePart)
            .where(SparePart.deleted_at.is_(None))
        )

        if search:
            search_value = f"%{search.strip()}%"

            statement = (
                statement
                .join(SparePart.categories)
                .where(
                    or_(
                        SparePart.part_name.ilike(search_value),
                        SparePart.part_code.ilike(search_value),
                        SparePart.device_model.ilike(search_value),
                        SparePart.device_brand.ilike(search_value),
                        SparePart.specifications.ilike(search_value),
                        SparePart.shelf_location.ilike(search_value),
                        Category.name.ilike(search_value),
                    )
                )
            )

        if category_id is not None:
            statement = statement.where(
                SparePart.category_id == category_id
            )

        statement = (
            statement
            .options(selectinload(SparePart.categories))
            .order_by(SparePart.created_at.desc())
        )

        return list(self.db.scalars(statement).all())


    def get_service_requests(
        self,
        search: str | None = None,
        status: ServiceRequestStatus | None = None,
        created_date: date | None = None,
    ) -> list[ServiceRequest]:

        statement = (
            select(ServiceRequest)
            .join(ServiceRequest.customers)
            .join(ServiceRequest.users)
            .outerjoin(ServiceRequest.llm_diagnosis)
            .options(
                joinedload(ServiceRequest.customers),
                joinedload(ServiceRequest.users),
                joinedload(ServiceRequest.llm_diagnosis),
                joinedload(ServiceRequest.request_parts),
            )
            .where(
                ServiceRequest.deleted_at.is_(None),
                or_(
                    LLMDiagnosis.id.is_(None),
                    (
                        LLMDiagnosis.status.isnot(None)
                        & (
                            LLMDiagnosis.status
                            != LLMDiagnosisStatusPreview.DRAFT
                        )
                    ),
                ),
            )
        )

        if search:
            search_value = f"%{search.strip()}%"

            statement = statement.where(
                or_(
                    ServiceRequest.device_type.ilike(search_value),
                    ServiceRequest.device_brand.ilike(search_value),
                    ServiceRequest.device_model.ilike(search_value),
                    ServiceRequest.fault_description.ilike(search_value),
                    ServiceRequest.customers.has(
                        or_(
                            Customer.first_name.ilike(search_value),
                            Customer.last_name.ilike(search_value),
                        )
                    ),
                    ServiceRequest.users.has(
                        or_(
                            User.first_name.ilike(search_value),
                            User.last_name.ilike(search_value),
                        )
                    ),
                )
            )

        if status is not None:
            statement = statement.where(
                ServiceRequest.status == status
            )

        if created_date is not None:
            start_date = datetime.combine(created_date, time.min)
            end_date = start_date + timedelta(days=1)

            statement = statement.where(
                ServiceRequest.created_at >= start_date,
                ServiceRequest.created_at < end_date,
            )

        statement = statement.order_by(
            ServiceRequest.created_at.desc()
        )

        return list(
            self.db.scalars(statement).unique().all()
        )
