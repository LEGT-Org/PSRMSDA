from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Query
from datetime import date
from io import BytesIO

from app.modules.service_request.schema import ServiceRequestStatus
from app.modules.report.dependency import (
    ReportService,
    AdminUser
)


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


"""  

    Spare Parts Report Generation Endpoint

"""

@router.get("/spare-parts/csv")
def export_spare_parts_csv(
    service: ReportService,
    current_user: AdminUser,
    search: str | None = Query(default=None),
    category_id: int | None = Query(default=None, ge=1),
):
    csv_content, filename = service.export_spare_parts_csv(
        search=search,
        category_id=category_id,
    )

    return StreamingResponse(
        iter([csv_content.encode("utf-8-sig")]),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )


@router.get("/spare-parts/excel")
def export_spare_parts_excel(
    service: ReportService,
    current_user: AdminUser,
    search: str | None = Query(default=None),
    category_id: int | None = Query(default=None, ge=1),
):
    excel_file, filename = service.export_spare_parts_excel(
        search=search,
        category_id=category_id,
    )

    return StreamingResponse(
        excel_file,
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )


@router.get("/spare-parts/pdf")
def export_spare_parts_pdf(
    service: ReportService,
    current_user: AdminUser,
    search: str | None = Query(default=None),
    category_id: int | None = Query(default=None, ge=1),
):
    pdf_file, filename = service.export_spare_parts_pdf(
        search=search,
        category_id=category_id,
    )

    return StreamingResponse(
        pdf_file,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )


"""  

    Service Request Reports Generation Endpoint

"""

@router.get("/service-requests/csv")
def export_service_requests_csv(
    service: ReportService,
    current_user: AdminUser,
    search: str | None = Query(default=None),
    status: ServiceRequestStatus | None = Query(default=None),
    created_date: date | None = Query(default=None),
):
    csv_content = service.export_service_requests_csv(
        search=search,
        status=status,
        created_date=created_date,
    )

    return StreamingResponse(
        iter([csv_content.encode("utf-8-sig")]),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": (
                'attachment; filename="service-requests.csv"'
            )
        },
    )


@router.get("/service-requests/excel")
def export_service_requests_excel(
    service: ReportService,
    current_user: AdminUser,
    search: str | None = Query(default=None),
    status: ServiceRequestStatus | None = Query(default=None),
    created_date: date | None = Query(default=None),
):
    excel_content = service.export_service_requests_excel(
        search=search,
        status=status,
        created_date=created_date,
    )

    return StreamingResponse(
        iter([excel_content]),
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition": (
                'attachment; filename="service-requests.xlsx"'
            )
        },
    )


@router.get("/service-requests/pdf")
def export_service_requests_pdf(
    service: ReportService,
    current_user: AdminUser,
    search: str | None = Query(default=None),
    status: ServiceRequestStatus | None = Query(default=None),
    created_date: date | None = Query(default=None),
):
    pdf_content = service.export_service_requests_pdf(
        search=search,
        status=status,
        created_date=created_date,
    )

    return StreamingResponse(
        iter([pdf_content]),
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                'attachment; filename="service-requests.pdf"'
            )
        },
    )
