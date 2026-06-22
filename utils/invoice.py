from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from num2words import num2words
from textwrap import wrap

from database import supabase
import os

downloads = os.path.join(os.path.expanduser("~"), "Downloads")

def generate_invoice(
    user_id,    
    bill_no,
    customer_name,
    customer_address,
    mobile_no,
    invoice_date,
    invoice_rows,
    subtotal,
    cgst,
    cgst_rate,
    sgst,
    sgst_rate,
    grand_total
):


    filename = os.path.join(downloads, f"{bill_no}.pdf")

    pdf = canvas.Canvas(
        filename,
        pagesize=A4
    )

    response = (
        supabase
        .table("userss")
        .select("*")
        .eq("shop_id", user_id)
        .execute()
    )

    width, height = A4

    # Background Template
    pdf.drawImage(
        "image.png",
        0,
        0,
        width=width,
        height=height
    )
    
    # ==========================
    # SHOP DETAILS
    # ==========================
           
    pdf.setFont("Helvetica-Bold", 42)

    pdf.drawCentredString(
        595 / 2,
        755,
        response.data[0]["shop_name"]
    )

    
    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawCentredString(
        595 / 2,
        730,
        response.data[0]["shop_des"]
    )
    
    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawCentredString(
        595 / 2,
        710,
        response.data[0]["shop_location"]
    )
    
    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawCentredString(
        595 / 2,
        690,
        f"GSTIN No.: {response.data[0]['gstin_no']}"
    )
            
    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        60,
        800,
        f"Mobile : {response.data[0]['mobile_no']}"
    )
        
    # ==========================
    # CUSTOMER DETAILS
    # ==========================
    pdf.drawString(
        421,
        648,
        str(bill_no)
    )

    pdf.drawString(
        391,
        634,
        invoice_date
    )

    pdf.drawString(
        86,
        653,
        customer_name
    )
    pdf.drawString(
        97,
        639,
        customer_address
    )

    pdf.drawString(
        96,
        624,
        mobile_no
    )

    # ==========================
    # PRODUCTS
    # ==========================
    y = 545

    for i, row in enumerate(invoice_rows, start=1):

        pdf.drawString(
            62,
            y,
            str(i)
        )

        lines = wrap(
            str(row["Product"]),
            width=30
        )

        # Product name
        for j, line in enumerate(lines):
            pdf.drawString(
                90,
                y - (j * 12),
                line
            )

        # Qty, Rate, Total
        pdf.drawString(
            377,
            y,
            str(row["Qty"])
        )

        pdf.drawString(
            412,
            y,
            str(row["Price"])
        )

        pdf.drawString(
            480,
            y,
            str(row["Total"])
        )

        # Move down according to number of lines used
        y -= max(20, len(lines) * 12)

    # ==========================
    # TOTALS
    # ==========================
    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    # Gross Amount
    pdf.drawString(
        480,
        290,
        str(subtotal)
    )

    # SGST
    pdf.drawString(
        480,
        245,
        str(sgst)
    )
    pdf.drawString(
        320,
        245,
        str(sgst_rate)
    )

    # CGST
    pdf.drawString(
        480,
        225,
        str(cgst)
    )
    pdf.drawString(
        320,
        225,
        str(cgst_rate)
    )
    
    # Net Amount
    pdf.drawString(
        480,
        160,
        str(grand_total)
    )
    
    words = num2words(
        grand_total,
        lang="en_IN"
    )

    words = words.title() + " Only"
    pdf.drawString(
        96,
        126,
        str(words)
    )

    # ==========================
    # SIGNATURE
    # ==========================

    # pdf.drawImage(
    #     "signature.png",
    #     464,
    #     57,
    #     width=80,
    #     height=30
    # )

    pdf.save()

    return filename

