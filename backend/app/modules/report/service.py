import csv
from xml.sax.saxutils import escape
from io import StringIO, BytesIO
from datetime import date
from pathlib import Path

from sqlalchemy.orm import Session

from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl import Workbook

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from app.modules.service_request.schema import ServiceRequestStatus
from app.modules.report.repository import ReportRepository


class ReportService:

    def __init__(
        self, 
        repository: ReportRepository,
        db: Session
    ):

        self.repository = repository
        self.db = db


    """  
    
        Spare Parts Reports Generation Service
    
    """

    def export_spare_parts_csv(
        self,
        search: str | None = None,
        category_id: int | None = None,
    ) -> tuple[str, str]:

        spare_parts = self.repository.get_spare_parts(
            search=search,
            category_id=category_id,
        )

        output = StringIO()
        writer = csv.writer(output)

        writer.writerow([
            "ID",
            "Part Code",
            "Part Name",
            "Device Brand",
            "Device Model",
            "Category",
            "Specifications",
            "Stock Quantity",
            "Unit Cost",
            "Shelf Location",
        ])

        for part in spare_parts:
            writer.writerow([
                part.id,
                part.part_code,
                part.part_name,
                part.device_brand,
                part.device_model,
                part.categories.name if part.categories else "",
                part.specifications,
                part.stock_quantity,
                part.unit_cost,
                part.shelf_location,
            ])

        return output.getvalue(), "spare-parts.csv"


    def export_spare_parts_excel(
        self,
        search: str | None = None,
        category_id: int | None = None,
    ) -> tuple[BytesIO, str]:

        spare_parts = self.repository.get_spare_parts(
            search=search,
            category_id=category_id,
        )

        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Spare Parts"

        headers = [
            "ID",
            "Part Code",
            "Part Name",
            "Device Brand",
            "Device Model",
            "Category",
            "Specifications",
            "Stock Quantity",
            "Unit Cost",
            "Shelf Location",
        ]

        worksheet.append(headers)

        for part in spare_parts:
            worksheet.append([
                part.id,
                part.part_code,
                part.part_name,
                part.device_brand,
                part.device_model,
                part.categories.name if part.categories else "",
                part.specifications,
                part.stock_quantity,
                float(part.unit_cost) if part.unit_cost is not None else None,
                part.shelf_location,
            ])

        # Format the header row.
        for cell in worksheet[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(
                fill_type="solid",
                fgColor="1F4E78",
            )
            cell.alignment = Alignment(horizontal="center")

        # Adjust each column width based on its contents.
        for column in worksheet.columns:
            max_length = max(
                len(str(cell.value))
                if cell.value is not None
                else 0
                for cell in column
            )

            column_letter = get_column_letter(column[0].column)
            worksheet.column_dimensions[column_letter].width = min(
                max_length + 2,
                50,
            )

        # Keep headers visible while scrolling.
        worksheet.freeze_panes = "A2"

        # Enable filtering on all populated columns.
        worksheet.auto_filter.ref = worksheet.dimensions

        # Format unit cost as a currency-like number.
        for cell in worksheet["I"][1:]:
            cell.number_format = '#,##0.00'

        output = BytesIO()
        workbook.save(output)
        output.seek(0)

        return output, "spare-parts.xlsx"


    def export_spare_parts_pdf(
        self,
        search: str | None = None,
        category_id: int | None = None,
    ) -> tuple[BytesIO, str]:

        from xml.sax.saxutils import escape

        spare_parts = self.repository.get_spare_parts(
            search=search,
            category_id=category_id,
        )

        output = BytesIO()

        document = SimpleDocTemplate(
            output,
            pagesize=landscape(A4),
            rightMargin=10 * mm,
            leftMargin=10 * mm,
            topMargin=12 * mm,
            bottomMargin=12 * mm,
            title="Spare Parts Inventory Report",
        )

        styles = getSampleStyleSheet()

        title_style = styles["Title"]

        cell_style = ParagraphStyle(
            "TableCell",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=6.5,
            leading=8,
            wordWrap="CJK",
        )

        header_style = ParagraphStyle(
            "TableHeader",
            parent=cell_style,
            fontName="Helvetica-Bold",
            textColor=colors.white,
        )

        elements = [
            Paragraph(
                "Spare Parts Inventory Report",
                title_style,
            ),
            Spacer(1, 5 * mm),
            Paragraph(
                f"Total records: {len(spare_parts)}",
                styles["Normal"],
            ),
            Spacer(1, 5 * mm),
        ]

        headers = [
            "ID",
            "Part Code",
            "Part Name",
            "Brand",
            "Model",
            "Category",
            "Specifications",
            "Stock",
            "Unit Cost",
            "Shelf",
        ]

        table_data = [
            [
                Paragraph(escape(header), header_style)
                for header in headers
            ]
        ]

        for part in spare_parts:
            values = [
                part.id,
                part.part_code,
                part.part_name,
                part.device_brand,
                part.device_model,
                (
                    part.categories.name
                    if part.categories
                    else ""
                ),
                part.specifications,
                part.stock_quantity,
                (
                    f"{part.unit_cost:,.2f}"
                    if part.unit_cost is not None
                    else ""
                ),
                part.shelf_location,
            ]

            row = []

            for value in values:
                text = escape(
                    str(value) if value is not None else ""
                ).replace("\n", "<br/>")

                row.append(
                    Paragraph(text, cell_style)
                )

            table_data.append(row)

        table = Table(
            table_data,
            colWidths=[
                9 * mm,    # ID
                22 * mm,   # Part Code
                28 * mm,   # Part Name
                20 * mm,   # Brand
                22 * mm,   # Model
                23 * mm,   # Category
                39 * mm,   # Specifications
                12 * mm,   # Stock
                19 * mm,   # Unit Cost
                18 * mm,   # Shelf
            ],
            repeatRows=1,
            hAlign="LEFT",
        )

        table.setStyle(TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#1F4E78"),
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white,
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP",
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.4,
                colors.grey,
            ),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [
                    colors.white,
                    colors.HexColor("#F2F6FA"),
                ],
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                3,
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                3,
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                4,
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                4,
            ),
        ]))

        elements.append(table)

        document.build(elements)

        output.seek(0)

        return output, "spare-parts.pdf"


    """  
    
        Service Request Reports Generation Service
    
    """

    
    def export_service_requests_csv(
        self,
        search: str | None = None,
        status: ServiceRequestStatus | None = None,
        created_date: date | None = None,
    ) -> str:
        service_requests = self.repository.get_service_requests(
            search=search,
            status=status,
            created_date=created_date,
        )

        output = StringIO()
        writer = csv.writer(output)

        writer.writerow([
            "Request ID",
            "Created At",
            "Device Type",
            "Device Brand",
            "Device Model",
            "Customer",
            "Technician",
            "Fault Description",
            "Status",
            "AI Diagnosis",
            "Requested Parts",
        ])

        for request in service_requests:
            customer = request.customers
            technician = request.users
            diagnosis = request.llm_diagnosis

            # Convert fault descriptions into readable text.
            fault_descriptions = request.fault_description or []

            if isinstance(fault_descriptions, list):
                fault_descriptions = "\n".join(
                    str(fault).strip()
                    for fault in fault_descriptions
                    if fault
                )
            else:
                fault_descriptions = str(fault_descriptions)

            # Extract only the diagnosis summary.
            diagnosis_summary = ""

            if diagnosis and diagnosis.response:
                response = diagnosis.response

                if isinstance(response, dict):
                    diagnosis_summary = response.get("summary", "")
                elif isinstance(response, str):
                    diagnosis_summary = response
                else:
                    diagnosis_summary = getattr(
                        response,
                        "summary",
                        "",
                    )

            # Combine requested parts into readable text.
            requested_parts = "; ".join(
                f"{part.part_name_snapshot} (Qty: {part.quantity})"
                for part in request.request_parts
            )

            writer.writerow([
                request.id,
                request.created_at,
                request.device_type,
                request.device_brand,
                request.device_model,
                (
                    f"{customer.first_name} {customer.last_name}"
                    if customer else ""
                ),
                (
                    f"{technician.first_name} {technician.last_name}"
                    if technician else ""
                ),
                fault_descriptions,
                (
                    request.status.value
                    if hasattr(request.status, "value")
                    else request.status
                ),
                diagnosis_summary,
                requested_parts,
            ])

        return output.getvalue()

    
    def export_service_requests_excel(
        self,
        search: str | None = None,
        status: ServiceRequestStatus | None = None,
        created_date: date | None = None,
    ) -> bytes:
        service_requests = self.repository.get_service_requests(
            search=search,
            status=status,
            created_date=created_date,
        )

        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Service Requests"

        headers = [
            "Request ID",
            "Created At",
            "Device Type",
            "Device Brand",
            "Device Model",
            "Customer",
            "Technician",
            "Fault Description",
            "Status",
            "AI Diagnosis",
            "Requested Parts",
        ]

        worksheet.append(headers)

        for request in service_requests:
            customer = request.customers
            technician = request.users
            diagnosis = request.llm_diagnosis

            # Convert the fault descriptions list into readable text.
            fault_descriptions = request.fault_description or []

            if isinstance(fault_descriptions, list):
                fault_descriptions = "\n".join(
                    str(fault).strip()
                    for fault in fault_descriptions
                    if fault
                )
            else:
                fault_descriptions = str(fault_descriptions)

            # Extract the diagnosis summary instead of exporting
            # the entire diagnosis object.
            diagnosis_summary = ""

            if diagnosis and diagnosis.response:
                response = diagnosis.response

                if isinstance(response, dict):
                    diagnosis_summary = response.get("summary", "")
                elif isinstance(response, str):
                    diagnosis_summary = response
                else:
                    diagnosis_summary = getattr(
                        response,
                        "summary",
                        "",
                    )

            # Combine requested parts into a single readable cell.
            requested_parts = "\n".join(
                f"{part.part_name_snapshot} (Qty: {part.quantity})"
                for part in request.request_parts
            )

            worksheet.append([
                request.id,
                request.created_at,
                request.device_type,
                request.device_brand,
                request.device_model,
                (
                    f"{customer.first_name} {customer.last_name}"
                    if customer else ""
                ),
                (
                    f"{technician.first_name} {technician.last_name}"
                    if technician else ""
                ),
                fault_descriptions,
                (
                    request.status.value
                    if hasattr(request.status, "value")
                    else request.status
                ),
                diagnosis_summary,
                requested_parts,
            ])

        # Style the header.
        header_fill = PatternFill(
            fill_type="solid",
            fgColor="1F4E78",
        )

        for cell in worksheet[1]:
            cell.font = Font(
                bold=True,
                color="FFFFFF",
            )
            cell.fill = header_fill
            cell.alignment = Alignment(
                horizontal="center",
                vertical="center",
                wrap_text=True,
            )

        # Set readable column widths.
        column_widths = [
            12, 22, 20, 20, 20, 25,
            25, 45, 24, 60, 45,
        ]

        for index, width in enumerate(column_widths, start=1):
            worksheet.column_dimensions[
                get_column_letter(index)
            ].width = width

        # Wrap text and align data to the top.
        for row in worksheet.iter_rows(min_row=2):
            for cell in row:
                cell.alignment = Alignment(
                    vertical="top",
                    wrap_text=True,
                )

        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions
        worksheet.row_dimensions[1].height = 30

        output = BytesIO()
        workbook.save(output)

        return output.getvalue()


    def export_service_requests_pdf(
        self,
        search: str | None = None,
        status: ServiceRequestStatus | None = None,
        created_date: date | None = None,
    ) -> bytes:
        service_requests = self.repository.get_service_requests(
            search=search,
            status=status,
            created_date=created_date,
        )
        
        # Locate Unicode font files.
        font_directory = Path("/usr/share/fonts/truetype/dejavu")
        regular_font = font_directory / "DejaVuSans.ttf"
        bold_font = font_directory / "DejaVuSans-Bold.ttf"

        if not regular_font.exists() or not bold_font.exists():
            raise RuntimeError(
                "DejaVu Sans fonts were not found. "
                "Install the DejaVu fonts or configure their paths."
            )

        # Register fonts only once.
        if "DejaVu" not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(
                TTFont("DejaVu", str(regular_font))
            )

        if "DejaVu-Bold" not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(
                TTFont("DejaVu-Bold", str(bold_font))
            )

        output = BytesIO()

        document = SimpleDocTemplate(
            output,
            pagesize=landscape(A4),
            rightMargin=8 * mm,
            leftMargin=8 * mm,
            topMargin=10 * mm,
            bottomMargin=10 * mm,
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            fontName="DejaVu-Bold",
            fontSize=16,
            leading=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1F4E78"),
            spaceAfter=4 * mm,
        )

        subtitle_style = ParagraphStyle(
            "ReportSubtitle",
            parent=styles["Normal"],
            fontName="DejaVu",
            fontSize=8,
            leading=11,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#555555"),
            spaceAfter=5 * mm,
        )

        header_style = ParagraphStyle(
            "TableHeader",
            parent=styles["Normal"],
            fontName="DejaVu-Bold",
            fontSize=6.5,
            leading=8,
            textColor=colors.white,
            alignment=TA_LEFT,
            wordWrap="CJK",
        )

        cell_style = ParagraphStyle(
            "TableCell",
            parent=styles["Normal"],
            fontName="DejaVu",
            fontSize=6.5,
            leading=8,
            alignment=TA_LEFT,
            wordWrap="CJK",
        )

        def make_cell(value, style=cell_style):
            text = "" if value is None else str(value)

            # Remove unsupported control characters while preserving
            # newlines and tabs.
            text = "".join(
                char
                for char in text
                if char in "\n\t" or ord(char) >= 32
            )

            # Escape content so user-provided text is not interpreted
            # as ReportLab paragraph markup.
            text = escape(text)
            text = text.replace("\n", "<br/>")
            text = text.replace("\t", "    ")

            return Paragraph(text, style)

        story = [
            Paragraph("Service Request Report", title_style),
            Paragraph(
                f"Total service requests: {len(service_requests)}",
                subtitle_style,
            ),
        ]

        headers = [
            "Request ID",
            "Created At",
            "Device",
            "Brand / Model",
            "Customer",
            "Technician",
            "Fault Description",
            "Status",
            "AI Diagnosis",
            "Requested Parts",
        ]

        data = [
            [make_cell(header, header_style) for header in headers]
        ]

        for request in service_requests:
            customer = request.customers
            technician = request.users
            diagnosis = request.llm_diagnosis

            fault_descriptions = request.fault_description or []

            if isinstance(fault_descriptions, list):
                fault_descriptions = "\n".join(
                    str(fault).strip()
                    for fault in fault_descriptions
                    if fault
                )
            else:
                fault_descriptions = str(fault_descriptions)

            diagnosis_summary = ""

            if diagnosis and diagnosis.response:
                response = diagnosis.response

                if isinstance(response, dict):
                    diagnosis_summary = response.get("summary", "")
                elif isinstance(response, str):
                    diagnosis_summary = response
                else:
                    diagnosis_summary = getattr(
                        response,
                        "summary",
                        "",
                    )

            requested_parts = "\n".join(
                f"{part.part_name_snapshot} (Qty: {part.quantity})"
                for part in request.request_parts
            )

            status_value = (
                request.status.value
                if hasattr(request.status, "value")
                else request.status
            )

            brand_model = " / ".join(
                str(value)
                for value in (
                    request.device_brand,
                    request.device_model,
                )
                if value
            )

            data.append([
                make_cell(request.id),
                make_cell(request.created_at),
                make_cell(request.device_type),
                make_cell(brand_model),
                make_cell(
                    f"{customer.first_name} {customer.last_name}"
                    if customer else ""
                ),
                make_cell(
                    f"{technician.first_name} {technician.last_name}"
                    if technician else ""
                ),
                make_cell(fault_descriptions),
                make_cell(status_value),
                make_cell(diagnosis_summary),
                make_cell(requested_parts),
            ])

        column_widths = [
            15 * mm,
            24 * mm,
            20 * mm,
            26 * mm,
            25 * mm,
            25 * mm,
            42 * mm,
            22 * mm,
            48 * mm,
            32 * mm,
        ]

        table = Table(
            data,
            colWidths=column_widths,
            repeatRows=1,
            hAlign="LEFT",
        )

        table.setStyle(TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#1F4E78"),
            ),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.4,
                colors.HexColor("#CCCCCC"),
            ),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [
                    colors.white,
                    colors.HexColor("#F2F6FA"),
                ],
            ),
        ]))

        story.append(table)
        document.build(story)

        return output.getvalue()
