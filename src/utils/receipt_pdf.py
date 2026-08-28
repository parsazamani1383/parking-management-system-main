from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from src.utils.plate_converter import to_persian_plate
import arabic_reshaper
from bidi.algorithm import get_display

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
)
from reportlab.lib.units import mm
from reportlab.platypus import HRFlowable
from reportlab.lib.styles import ParagraphStyle

class ReceiptPDF:

    @staticmethod
    def create(
        receipt,
        vehicle,
        session,
        spot,
    ):
        output_dir = Path("receipts")

        output_dir.mkdir(
            exist_ok=True
        )

        pdf_file = output_dir / (
            f"receipt_{receipt.receipt_number}.pdf"
        )
        logo_path = Path(
            "src/ui/assets/logo1.png"
        )

        try:
            pdfmetrics.getFont("BNazanin")
        except:
            pdfmetrics.registerFont(
                TTFont(
                    "BNazanin",
                    "src/ui/assets/fonts/BNazanin.ttf",
                )
            )

        styles = getSampleStyleSheet()

        style = styles["Normal"]
        title_style = ParagraphStyle(
            "title",
            fontName="BNazanin",
            fontSize=22,
            leading=30,
            alignment=TA_CENTER,
        )
        style.fontName = "BNazanin"

        style.fontSize = 14

        style.leading = 28

        style.alignment = TA_CENTER

        RECEIPT_WIDTH = 80 * mm
        RECEIPT_HEIGHT = 220 * mm

        doc = SimpleDocTemplate(
            str(pdf_file),
            pagesize=(RECEIPT_WIDTH, RECEIPT_HEIGHT),
            leftMargin=8,
            rightMargin=8,
            topMargin=10,
            bottomMargin=10,
        )

        story = []

        if logo_path.exists():
            logo = Image(
                str(logo_path),
                width=170,
                height=55,
            )

            logo.hAlign = "CENTER"

            story.append(logo)

            story.append(
                Spacer(
                    1,
                    20,
                )
            )

        story.append(
            HRFlowable(
                width="100%",
                thickness=1,
                color="black",
            )
        )

        story.append(
            Spacer(1, 10)
        )

        story.append(
            Paragraph(
                ReceiptPDF.fa("رسید پارکینگ راپــا"),
                title_style,
            )
        )

        story.append(
            Spacer(
                1,
                20,
            )
        )

        story.append(
            Paragraph(
                ReceiptPDF.fa(f"شماره رسید: {receipt.receipt_number}"),
                style,
            )
        )

        story.append(
            Spacer(1, 15)
        )
        story.append(
            Paragraph(
                ReceiptPDF.fa(f"پلاک: {to_persian_plate(vehicle.plate_number)}"),
                style,
            )
        )

        story.append(
            Paragraph(
                ReceiptPDF.fa(f"جایگاه: {spot.spot_number}"),
                style,
            )
        )

        story.append(
            Paragraph(
                ReceiptPDF.fa("زمان ورود: "
                + session.entry_time.strftime(
                    "%Y/%m/%d  ساعت: %H:%M"
                )),
                style,
            )
        )

        story.append(
            Paragraph(
                ReceiptPDF.fa("زمان خروج: "
                + session.exit_time.strftime(
                    "%Y/%m/%d  ساعت: %H:%M"
                )),
                style,
            )
        )

        duration = (
            session.exit_time
            - session.entry_time
        )

        hours = duration.seconds // 3600

        minutes = (
            duration.seconds % 3600
        ) // 60

        story.append(
            Paragraph(
                ReceiptPDF.fa(f"مدت توقف: {hours} ساعت و {minutes} دقیقه"),
                style,
            )
        )

        story.append(
            Paragraph(
                ReceiptPDF.fa(f"مبلغ: {int(receipt.amount):,} تومان"),
                style,
            )
        )

        payment = (
            ReceiptPDF.fa("نقدی")
            if receipt.payment_method == "cash"
            else ReceiptPDF.fa("کارت")
        )

        story.append(
            Paragraph(
                ReceiptPDF.fa(f"روش پرداخت: {ReceiptPDF.fa(payment)}"),
                style,
            )
        )

        story.append(
            Paragraph(
                ReceiptPDF.fa("تاریخ صدور: "
                + receipt.issued_at.strftime(
                    "%Y/%m/%d  ساعت: %H:%M"
                )),
                style,
            )
        )

        story.append(
            Spacer(
                1,
                25,
            )
        )

        story.append(
            Paragraph(
                ReceiptPDF.fa("با تشکر"),
                style,
            )
        )
        story.append(
            Paragraph(
                ReceiptPDF.fa(" سیستم مدیریت پارکینگ راپــا"),
                style,
            )
        )

        doc.build(
            story
        )

        return str(
            pdf_file
        )

    @staticmethod
    def fa(text):
        reshaped = arabic_reshaper.reshape(str(text))
        return get_display(reshaped)