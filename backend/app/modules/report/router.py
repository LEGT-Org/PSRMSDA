from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Query, Request
from datetime import date
from io import BytesIO

from app.shared.rate_limiter import limiter

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

    Low Stock Spare Parts Report Generation Endpoints

"""

@router.get("/low-stock-spare-parts/csv")
@limiter.limit("15/minute")
def export_low_stock_parts_csv(
    request: Request,
    service: ReportService,
    current_user: AdminUser,
    threshold: int = Query(default=5, ge=0),
):
    csv_content, filename = service.export_low_stock_parts_csv(
        threshold=threshold,
    )

    return StreamingResponse(
        iter([csv_content.encode("utf-8-sig")]),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )


@router.get("/low-stock-spare-parts/excel")
@limiter.limit("15/minute")
def export_low_stock_parts_excel(
    request: Request,
    service: ReportService,
    current_user: AdminUser,
    threshold: int = Query(default=5, ge=0),
):
    excel_file, filename = service.export_low_stock_parts_excel(
        threshold=threshold,
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


@router.get("/low-stock-spare-parts/pdf")
@limiter.limit("15/minute")
def export_low_stock_parts_pdf(
    request: Request,
    service: ReportService,
    current_user: AdminUser,
    threshold: int = Query(default=5, ge=0),
):
    pdf_file, filename = service.export_low_stock_parts_pdf(
        threshold=threshold,
    )

    return StreamingResponse(
        pdf_file,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )


"""  

    Spare Parts Report Generation Endpoint

"""

@router.get("/spare-parts/csv")
@limiter.limit("15/minute")
def export_spare_parts_csv(
    request: Request,
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
@limiter.limit("15/minute")
def export_spare_parts_excel(
    request: Request,
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
@limiter.limit("15/minute")
def export_spare_parts_pdf(
    request: Request,
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
@limiter.limit("15/minute")
def export_service_requests_csv(
    request: Request,
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
@limiter.limit("15/minute")
def export_service_requests_excel(
    request: Request,
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
@limiter.limit("15/minute")
def export_service_requests_pdf(
    request: Request,
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
