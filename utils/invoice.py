from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_invoice(
    bill_no,
    invoice_rows,
    grand_total
):

    filename = f"bills/{bill_no}.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Inventra",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            f"Bill No: {bill_no}",
            styles["Heading2"]
        )
    )

    elements.append(
        Spacer(1, 10)
    )

    for row in invoice_rows:

        elements.append(
            Paragraph(
                f"{row['Product']} × {row['Qty']} = Rs{row['Total']}",
                styles["Normal"]
            )
        )

    elements.append(
        Spacer(1, 10)
    )

    elements.append(
        Paragraph(
            f"Grand Total: Rs{grand_total}",
            styles["Heading1"]
        )
    )

    doc.build(elements)

    return filename