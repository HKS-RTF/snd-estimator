import os
import random
import io
from datetime import datetime
import streamlit as st
from supabase import create_client, Client

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget

# --- Page Configuration ---
st.set_page_config(
    page_title="SND Interior & Designs | Grand Luxury Home Interiors Bengaluru",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Grand Luxury CSS & 3D Interactive Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #070A12;
        color: #F8FAFC;
    }

    /* Top Utility Navigation Bar */
    .top-nav {
        background: linear-gradient(90deg, #0F172A 0%, #1E293B 100%);
        color: #94A3B8;
        padding: 12px 32px;
        font-size: 0.82rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #D97706;
        box-shadow: 0 4px 20px rgba(0,0,0,0.6);
        border-radius: 0 0 16px 16px;
        margin-bottom: 2rem;
    }

    /* Grand 3D Hero Section */
    .grand-hero-3d {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(9, 13, 22, 0.98) 100%), 
                    url('https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=2000&q=80');
        background-size: cover;
        background-position: center;
        border-radius: 28px;
        padding: 5rem 3rem;
        color: white;
        text-align: center;
        border: 1px solid rgba(217, 119, 6, 0.4);
        box-shadow: 0 30px 60px -15px rgba(217, 119, 6, 0.2), inset 0 0 40px rgba(0,0,0,0.8);
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
    }

    .brand-title {
        font-family: 'Cinzel', serif;
        font-size: 3.6rem;
        font-weight: 900;
        letter-spacing: 3px;
        background: linear-gradient(135deg, #FDE68A 0%, #F59E0B 40%, #D97706 80%, #B45309 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.75rem;
        text-shadow: 0 10px 30px rgba(217, 119, 6, 0.3);
    }

    .hero-badge {
        background: rgba(217, 119, 6, 0.2);
        border: 1px solid #D97706;
        color: #FBBF24;
        padding: 8px 24px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(217, 119, 6, 0.3);
    }

    /* 3D Glassmorphism Cards & Containers */
    .glass-card-3d {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        margin-bottom: 1.5rem;
    }

    .glass-card-3d:hover {
        transform: translateY(-8px) scale(1.01);
        border-color: #D97706;
        box-shadow: 0 30px 60px rgba(217, 119, 6, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }

    /* Trust Stats 3D Grid */
    .trust-stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-top: 2.5rem;
    }

    .stat-box-3d {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(217, 119, 6, 0.3);
        border-radius: 18px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        transition: transform 0.3s ease;
    }

    .stat-box-3d:hover {
        transform: translateY(-5px);
        border-color: #F59E0B;
    }

    .stat-number {
        font-size: 2rem;
        font-weight: 900;
        color: #F59E0B;
        font-family: 'Cinzel', serif;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 4px;
    }

    /* Authentic Security Header inside Form */
    .auth-banner {
        background: linear-gradient(135deg, #1E1B4B 0%, #0F172A 100%);
        border: 1px solid #6366F1;
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.2);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# --- Initialize Supabase Client ---
@st.cache_resource
def init_supabase() -> Client:
    url, key = None, None
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except Exception:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
    if not url or not key:
        return None
    return create_client(url, key)

supabase = init_supabase()


# --- Helper Functions ---
def num_to_words_indian_clean(num):
    num = int(round(num))
    if num == 0: return "ZERO RUPEES ONLY"
    units = ["", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", 
             "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"]
    tens = ["", "", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"]
    
    def convert_below_thousand(n):
        res = ""
        if n >= 100:
            res += units[n // 100] + " HUNDRED "
            n %= 100
        if n >= 20:
            res += tens[n // 10] + " "
            n %= 10
        if n > 0:
            res += units[n] + " "
        return res.strip()

    result = ""
    crore = num // 10000000; num %= 10000000
    lakh = num // 100000; num %= 100000
    thousand = num // 1000; num %= 1000

    if crore > 0: result += convert_below_thousand(crore) + (" CRORES " if crore > 1 else " CRORE ")
    if lakh > 0: result += convert_below_thousand(lakh) + (" LAKHS " if lakh > 1 else " LAKH ")
    if thousand > 0: result += convert_below_thousand(thousand) + " THOUSAND "
    if num > 0: result += convert_below_thousand(num)
    return f"{result.strip()} RUPEES ONLY"

def upload_to_cloud(ref_no, pdf_bytes_standard, pdf_bytes_no_header, filename_std, filename_no_hdr, owner, est_date, final_total):
    if not supabase: return None, None
    
    # Upload Standard Version
    path_std = f"pdf_estimations/{filename_std}"
    supabase.storage.from_("estimations").upload(
        path=path_std,
        file=pdf_bytes_standard,
        file_options={"content-type": "application/pdf", "upsert": "true"}
    )
    url_std = supabase.storage.from_("estimations").get_public_url(path_std)

    # Upload No-Header Version
    path_no_hdr = f"pdf_estimations/{filename_no_hdr}"
    supabase.storage.from_("estimations").upload(
        path=path_no_hdr,
        file=pdf_bytes_no_header,
        file_options={"content-type": "application/pdf", "upsert": "true"}
    )
    url_no_hdr = supabase.storage.from_("estimations").get_public_url(path_no_hdr)

    # Log record using standard existing columns (storing both filenames/paths and URLs cleanly)
    data = {
        "ref_no": str(ref_no),
        "customer_name": str(owner.upper()),
        "est_date": str(est_date),
        "amount": float(final_total),
        "pdf_url": url_std,
        "pdf_url_no_header": url_no_hdr
    }
    
    try:
        supabase.table("estimation_logs").upsert(data).execute()
    except Exception:
        # Fallback if 'pdf_url_no_header' column has not been added to Supabase table yet
        fallback_data = {
            "ref_no": str(ref_no),
            "customer_name": str(owner.upper()),
            "est_date": str(est_date),
            "amount": float(final_total),
            "pdf_url": f"{url_std} || NO_HEADER::{url_no_hdr}"
        }
        supabase.table("estimation_logs").upsert(fallback_data).execute()

    return url_std, url_no_hdr


def generate_estimation_pdf_bytes(owner, address, est_date, target_total, include_header=True):
    is_single_page = target_total < 1500000
    FIXED_ITEMS_MASTER = [
        ("Replacing sanitary fittings inside the toilets", "SETS", "SETS_UNITS", 0.08),
        ("3 course of oil bond distemper (Inside repaint)", "SQ. FT", "SQFT", 0.07),
        ("Providing & casting bathroom glazed tiles fixing etc.", "SQ. FT", "SQFT", 0.05),
        ("Interior works (Wardrobes, Modular Kitchen)", "JOB", "JOB_LOT", 0.12),
        ("Electrical fittings, cables, switches etc.", "JOB", "JOB_LOT", 0.07),
        ("Painting (exterior walls)", "SQ. FT", "SQFT", 0.06),
        ("New plumbing lines and fixtures", "JOB", "JOB_LOT", 0.05),
        ("Landscaping/Balcony improvements", "JOB", "JOB_LOT", 0.06),
        ("False ceiling work", "SQ. FT", "SQFT", 0.07),
        ("Flooring (Tiles/Marble)", "SQ. FT", "SQFT", 0.07),
        ("Providing & fixing teak wood show case", "UNIT", "SETS_UNITS", 0.06),
        ("2 course of snow cem paint (Outside repaint)", "SQ. FT", "SQFT", 0.04),
        ("Replacing sanitary fittings inside the kitchen", "SET", "SETS_UNITS", 0.05),
        ("Demolition and debris removal", "LOT", "JOB_LOT", 0.06),
        ("Wall plastering and finishing", "SQ. FT", "SQFT", 0.09)
    ]

    def calculate_quantity(category, total_amount):
        min_budget, max_budget = 1500000.0, 4500000.0
        ratio = max(0.0, min(1.0, (total_amount - min_budget) / (max_budget - min_budget)))
        ratio = max(0.0, min(1.0, ratio + random.uniform(-0.05, 0.05)))
        if category == "SQFT": return f"{round(650 + ratio * (2500 - 650))} SQ. FT"
        elif category == "SETS_UNITS":
            qty = round(1 + ratio * (5 - 1))
            return f"{qty} SETS" if qty > 1 else "1 SET"
        elif category == "JOB_LOT":
            qty = round(1 + ratio * (2 - 1))
            return f"{qty} JOB" if qty > 1 else "1 JOB"
        return "1 JOB"

    total_items_needed = 10 if is_single_page else 15
    processed_items = [(desc, calculate_quantity(cat, target_total), w) for desc, _, cat, w in FIXED_ITEMS_MASTER]
    random.shuffle(processed_items)
    processed_items = processed_items[:total_items_needed]

    subtotal_target = target_total / 1.18
    weights = [item[2] * random.uniform(0.85, 1.15) for item in processed_items]
    total_weight = sum(weights)
    norm_weights = [w / total_weight for w in weights]
    item_amounts = [round(subtotal_target * w) for w in norm_weights]
    item_amounts[-1] += round(subtotal_target) - sum(item_amounts)

    actual_subtotal = sum(item_amounts)
    actual_gst = round(actual_subtotal * 0.18)
    final_total = actual_subtotal + actual_gst

    now = datetime.now()
    ref_no = now.strftime("%H%M%d%m%Y")
    clean_owner_name = owner.replace(' ', '_').replace('&', 'AND')
    filename = f"Estimation_{ref_no}_{clean_owner_name}{'_NoHeader' if not include_header else ''}.pdf"

    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=15, bottomMargin=15)
    styles = getSampleStyleSheet()

    RED_COLOR, BLUE_COLOR, LIGHT_PINK, BORDER_BLUE = colors.HexColor("#DC2626"), colors.HexColor("#1E40AF"), colors.HexColor("#EC4899"), colors.HexColor("#2563EB")

    title_style = ParagraphStyle("Title", parent=styles["Heading1"], alignment=1, fontSize=28, leading=32, fontName="Helvetica-Bold", textColor=RED_COLOR)
    sub_style = ParagraphStyle("Sub", parent=styles["Normal"], alignment=1, fontSize=9, leading=12, fontName="Helvetica-Bold", textColor=BLUE_COLOR)
    contact_style = ParagraphStyle("Contact", parent=styles["Normal"], alignment=1, fontSize=8.5, leading=11, fontName="Helvetica-Bold", textColor=BLUE_COLOR)
    gstin_style = ParagraphStyle("GSTIN", parent=styles["Normal"], alignment=1, fontSize=9, leading=12, fontName="Helvetica-Bold", textColor=LIGHT_PINK)
    ref_left_style = ParagraphStyle("RefLeft", parent=styles["Normal"], alignment=0, fontSize=10, leading=12, fontName="Helvetica")
    ref_right_style = ParagraphStyle("RefRight", parent=styles["Normal"], alignment=2, fontSize=10, leading=12, fontName="Helvetica")
    box_hdr_style = ParagraphStyle("BoxHdr", parent=styles["Normal"], alignment=1, fontSize=14, leading=16, fontName="Helvetica-Bold", textColor=colors.black)
    box_detail_style = ParagraphStyle("BoxDetail", parent=styles["Normal"], alignment=1, fontSize=12.5, leading=15, fontName="Helvetica-Bold", textColor=colors.black)
    
    if is_single_page:
        cell_12_bold_center = ParagraphStyle("Cell11BC", parent=styles["Normal"], alignment=1, fontSize=11, leading=13.5, fontName="Helvetica-Bold", textColor=colors.black)
        hdr_12_bold_center = ParagraphStyle("Hdr11BC", parent=styles["Normal"], alignment=1, fontSize=11, leading=13.5, fontName="Helvetica-Bold", textColor=colors.black)
        total_14_bold = ParagraphStyle("Total12B", parent=styles["Normal"], alignment=1, fontSize=12, leading=14.5, fontName="Helvetica-Bold", textColor=colors.black)
        words_13_bold_center = ParagraphStyle("Words11.5BC", parent=styles["Normal"], alignment=1, fontSize=11.5, leading=14, fontName="Helvetica-Bold", textColor=colors.black)
        terms_hdr_center = ParagraphStyle("TermsHdr9.5", parent=styles["Normal"], alignment=1, fontSize=9.5, leading=12, fontName="Helvetica-Bold", textColor=colors.black)
        terms_point_size_8 = ParagraphStyle("TermsPt8.5", parent=styles["Normal"], alignment=0, fontSize=8.5, leading=10.5, fontName="Helvetica-Bold", textColor=colors.black)
    else:
        cell_12_bold_center = ParagraphStyle("Cell12BC", parent=styles["Normal"], alignment=1, fontSize=12, leading=14, fontName="Helvetica-Bold", textColor=colors.black)
        hdr_12_bold_center = ParagraphStyle("Hdr12BC", parent=styles["Normal"], alignment=1, fontSize=12, leading=14, fontName="Helvetica-Bold", textColor=colors.black)
        total_14_bold = ParagraphStyle("Total14B", parent=styles["Normal"], alignment=1, fontSize=14, leading=16, fontName="Helvetica-Bold", textColor=colors.black)
        words_13_bold_center = ParagraphStyle("Words13BC", parent=styles["Normal"], alignment=1, fontSize=13, leading=16, fontName="Helvetica-Bold", textColor=colors.black)
        terms_hdr_center = ParagraphStyle("TermsHdr10", parent=styles["Normal"], alignment=1, fontSize=10, leading=14, fontName="Helvetica-Bold", textColor=colors.black)
        terms_point_size_8 = ParagraphStyle("TermsPt8", parent=styles["Normal"], alignment=0, fontSize=8, leading=11, fontName="Helvetica-Bold", textColor=colors.black)

    elements = []

    def create_header_with_qr():
        qr_data = f"CUSTOMER NAME: {owner.upper()}\nADDRESS: {address.upper()}\nREF NO: {ref_no}\nDATE: {est_date}\nESTIMATION AMOUNT: Rs. {final_total:,}\nEMAIL: contact@sndinteriors.com"
        qr = QrCodeWidget(qr_data)
        qr_bounds = qr.getBounds()
        w, h = qr_bounds[2] - qr_bounds[0], qr_bounds[3] - qr_bounds[1]
        d = Drawing(60, 60, transform=[60.0/w, 0, 0, 60.0/h, 0, 0])
        d.add(qr)
        
        if include_header:
            header_text_flowables = [
                Paragraph("SND INTERIOR & DESIGNS", title_style), Spacer(1, 2),
                Paragraph("INTERIOR WORKS, DESIGN ESTIMATE, FLOOR VALUATIONS, BUILDING PLANS", sub_style),
                Paragraph("#15, E BLOCK, SAHAKHAR NAGAR, BANGALORE-560092", sub_style),
                Paragraph("EMAIL: contact@sndinteriors.com", contact_style),
                Paragraph("GSTIN: 29ABCDE1234F1Z5", gstin_style),
            ]
        else:
            header_text_flowables = [
                Spacer(1, 10),
                Spacer(1, 10),
                Spacer(1, 10),
                Spacer(1, 10),
                Spacer(1, 10)
            ]
        header_table = Table([["", header_text_flowables, d]], colWidths=[75, 400, 75])
        header_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0)]))
        return [header_table, Spacer(1, 4)]

    elements.extend(create_header_with_qr())
    elements.append(Table([[Paragraph(f"REF NO:-{ref_no}", ref_left_style), Paragraph(f"DATE: {est_date}", ref_right_style)]], colWidths=[270, 280]))
    elements.append(Spacer(1, 4))

    address_parts = [p.strip() for p in address.split(',')]
    mid_idx = len(address_parts) // 2
    addr_line_1 = ", ".join(address_parts[:mid_idx]) if mid_idx > 0 else address
    addr_line_2 = ", ".join(address_parts[mid_idx:]) if mid_idx > 0 else ""

    box_content = [[Paragraph("ESTIMATION FOR RENOVATION & INTERIOR DESIGN WORK AT", box_hdr_style)], [Paragraph("RESIDENTIAL FLAT AT", box_hdr_style)], [Paragraph(addr_line_1.upper(), box_detail_style)]]
    if addr_line_2: box_content.append([Paragraph(addr_line_2.upper(), box_detail_style)])
    box_content.append([Paragraph(f"OWNER: - {owner.upper()}", box_detail_style)])

    project_box = Table(box_content, colWidths=[550])
    project_box.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 2, BORDER_BLUE), ('ROUNDEDCORNERS', [8, 8, 8, 8]), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    elements.append(project_box)
    elements.append(Spacer(1, 6))

    if is_single_page:
        p_table_data = [[Paragraph("SL.NO", hdr_12_bold_center), Paragraph("Description", hdr_12_bold_center), Paragraph("Qty", hdr_12_bold_center), Paragraph("Amount Rs.", hdr_12_bold_center)]]
        for idx in range(10):
            item = processed_items[idx]
            p_table_data.append([Paragraph(f"{idx+1}.", cell_12_bold_center), Paragraph(item[0], cell_12_bold_center), Paragraph(item[1], cell_12_bold_center), Paragraph(f"{item_amounts[idx]:,}", cell_12_bold_center)])
        p_table_data.append(["", Paragraph("GST 18%", total_14_bold), "", Paragraph(f"{actual_gst:,}", total_14_bold)])
        p_table_data.append(["", Paragraph("TOTAL", total_14_bold), "", Paragraph(f"{final_total:,}", total_14_bold)])

        t1 = Table(p_table_data, colWidths=[50, 280, 100, 120])
        t1.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.black), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 6.5), ('BOTTOMPADDING', (0,0), (-1,-1), 6.5)]))
        elements.append(t1)
    else:
        p1_table_data = [[Paragraph("SL.NO", hdr_12_bold_center), Paragraph("Description", hdr_12_bold_center), Paragraph("Qty", hdr_12_bold_center), Paragraph("Amount Rs.", hdr_12_bold_center)]]
        for idx in range(9):
            item = processed_items[idx]
            p1_table_data.append([Paragraph(f"{idx+1}.", cell_12_bold_center), Paragraph(item[0], cell_12_bold_center), Paragraph(item[1], cell_12_bold_center), Paragraph(f"{item_amounts[idx]:,}", cell_12_bold_center)])
        
        t1 = Table(p1_table_data, colWidths=[50, 280, 100, 120])
        t1.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.black), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 16), ('BOTTOMPADDING', (0,0), (-1,-1), 16)]))
        elements.append(t1)

        elements.append(PageBreak())
        elements.extend(create_header_with_qr())

        p2_table_data = [[Paragraph("SL.NO", hdr_12_bold_center), Paragraph("Description", hdr_12_bold_center), Paragraph("Qty", hdr_12_bold_center), Paragraph("Amount Rs.", hdr_12_bold_center)]]
        for idx in range(9, 15):
            item = processed_items[idx]
            p2_table_data.append([Paragraph(f"{idx+1}.", cell_12_bold_center), Paragraph(item[0], cell_12_bold_center), Paragraph(item[1], cell_12_bold_center), Paragraph(f"{item_amounts[idx]:,}", cell_12_bold_center)])

        p2_table_data.append(["", Paragraph("GST 18%", total_14_bold), "", Paragraph(f"{actual_gst:,}", total_14_bold)])
        p2_table_data.append(["", Paragraph("TOTAL", total_14_bold), "", Paragraph(f"{final_total:,}", total_14_bold)])

        t2 = Table(p2_table_data, colWidths=[50, 280, 100, 120])
        t2.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.black), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 16), ('BOTTOMPADDING', (0,0), (-1,-1), 16)]))
        elements.append(t2)

    elements.append(Spacer(1, 6))
    elements.append(Paragraph(num_to_words_indian_clean(final_total), words_13_bold_center))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph("TERMS AND CONDITIONS:", terms_hdr_center))
    elements.append(Spacer(1, 3))

    terms_points = [
        "1. This Is A Preliminary Estimate And Not A Final Invoice",
        "2. Payment: 50% Advance, 30% After Material Delivery, 20% Upon Completion.",
        "3. Validity: This Estimation Is Valid For 45 Days From The Date Of Issue.",
        "4. Scope Of Work: Any Work Not Explicitly Mentioned In This Estimate Will Be Charged Extra.",
        "5. Materials: All Materials Used Will Be Of Standard Quality Unless Specified Otherwise.",
        "6. Project Duration: Estimated Project Completion Time Is 90 Working Days From Advance."
    ]
    for point in terms_points:
        elements.append(Paragraph(point, terms_point_size_8))
        elements.append(Spacer(1, 2))

    doc.build(elements)
    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()

    return pdf_bytes, filename, ref_no, final_total


# --- AUTHENTIC MODAL POPUP DIALOG WITH MANUAL ENTRY ---
@st.dialog("✨ OFFICIAL 3D INTERIOR DESIGN QUOTATION GENERATOR", width="large")
def show_quotation_dialog():
    st.markdown("""
    <div class="auth-banner">
        <div style="font-size:2.2rem;">🛡️</div>
        <div>
            <div style="color:#A5B4FC; font-weight:700; font-size:0.85rem; letter-spacing:1px;">SECURE SSL PORTAL • GST REGISTERED FIRM</div>
            <div style="color:#FFFFFF; font-size:0.8rem;">Official Quotations for Luxury Home Interiors in Bengaluru with encrypted QR verification.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("popup_estimation_form"):
        st.subheader("👤 Client & Site Profile")
        col1, col2 = st.columns(2)
        with col1:
            owner_input = st.text_input("Full Name of Property Owner *", value="KUSHAL ANAND & HKS")
        with col2:
            date_input = st.text_input("Date of Issue", value=datetime.now().strftime("%d-%m-%Y"))

        address_input = st.text_area(
            "Property / Site Address in Bengaluru *", 
            value="BIRLA TRIMAYA PHASE 4 FLAT-1205, T-6, F-12, DEVANAHALLI CHIKKAJALA, BENGALURU"
        )

        st.markdown("---")
        st.subheader("💰 Manual Amount Entry (INR ₹)")
        
        amount_input = st.number_input(
            "✏️ Enter Total Estimated Budget (INR ₹):",
            min_value=50000.0,
            max_value=10000000.0,
            value=1499000.0,
            step=25000.0,
            format="%.2f"
        )

        subtotal_est = round(amount_input / 1.18)
        gst_est = amount_input - subtotal_est
        st.info(f"📊 **Base Estimate:** ₹ {subtotal_est:,.2f} | **GST (18%):** ₹ {gst_est:,.2f} | **Total Final Payable:** ₹ {amount_input:,.2f}")

        st.caption("🔒 Both Standard and No-Header copies are generated simultaneously and archived to cloud storage.")
        
        submitted = st.form_submit_button("⚡ GENERATE & SAVE BOTH PDF VERSIONS", type="primary", use_container_width=True)

    if submitted:
        with st.spinner('Generating both PDF copies & syncing securely with cloud storage...'):
            try:
                # Generate Standard Version
                pdf_bytes_std, filename_std, generated_ref, final_total = generate_estimation_pdf_bytes(
                    owner_input, address_input, date_input, float(amount_input), include_header=True
                )
                # Generate No-Header Version
                pdf_bytes_no_hdr, filename_no_hdr, _, _ = generate_estimation_pdf_bytes(
                    owner_input, address_input, date_input, float(amount_input), include_header=False
                )
                
                if supabase:
                    url_std, url_no_hdr = upload_to_cloud(
                        generated_ref, pdf_bytes_std, pdf_bytes_no_hdr, 
                        filename_std, filename_no_hdr, owner_input, date_input, final_total
                    )
                    st.balloons()
                    st.success(f"🎉 **Both Versions Logged to Cloud Storage!** Reference No: `{generated_ref}`")
                else:
                    st.success(f"✅ **Both Versions Generated Successfully Locally!** Reference No: `{generated_ref}`")

                st.markdown("### 📥 Instant Downloads")
                dl_col1, dl_col2 = st.columns(2)
                with dl_col1:
                    st.download_button(
                        label="📄 Download Standard PDF",
                        data=pdf_bytes_std,
                        file_name=filename_std,
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )
                with dl_col2:
                    st.download_button(
                        label="📄 Download No-Header PDF",
                        data=pdf_bytes_no_hdr,
                        file_name=filename_no_hdr,
                        mime="application/pdf",
                        type="secondary",
                        use_container_width=True
                    )

            except Exception as e:
                st.error(f"An error occurred: {e}")


# --- TOP NAVIGATION BAR ---
st.markdown("""
<div class="top-nav">
    <div>📍 <b>BANGALORE EXPERIENCE CENTERS:</b> Sahakarnagar | HSR Layout | Whitefield | Yelahanka</div>
    <div>📞 <b>VIP CLIENT DESK:</b> +91 98765 43210 &nbsp;|&nbsp; ✉️ contact@sndinteriors.com</div>
</div>
""", unsafe_allow_html=True)


# --- GRAND 3D HERO SECTION ---
st.markdown("""
<div class="grand-hero-3d">
    <div class="hero-badge">👑 BENGALURU'S PREMIER 3D INTERIOR STUDIO</div>
    <div class="brand-title">SND INTERIOR & DESIGNS</div>
    <p style="color:#CBD5E1; font-size:1.2rem; max-width:850px; margin:0 auto; line-height:1.6;">
        Immersive 3D Photorealistic Visualizations, 100% Factory-Finished Modular Kitchens, Designer Wardrobes, and Turnkey Luxury Home Interiors.
    </p>
    
    <div class="trust-stats-grid">
        <div class="stat-box-3d">
            <div class="stat-number">500+</div>
            <div class="stat-label">Luxury Homes Completed</div>
        </div>
        <div class="stat-box-3d">
            <div class="stat-number">10 YRS</div>
            <div class="stat-label">Material Warranty</div>
        </div>
        <div class="stat-box-3d">
            <div class="stat-number">45 DAYS</div>
            <div class="stat-label">Guaranteed Delivery</div>
        </div>
        <div class="stat-box-3d">
            <div class="stat-number">100%</div>
            <div class="stat-label">Transparent Pricing</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# --- CLOUD LOOKUP & REFERENCE SEARCH SECTION ---
st.markdown("---")
st.markdown("### 🔍 Cloud Document Lookup & Reference Search")
st.markdown("<p style='color:#94A3B8; font-size:0.95rem;'>Enter a Reference Number (e.g. `104502082026`) to retrieve and download both standard and no-header versions from the cloud database.</p>", unsafe_allow_html=True)

lookup_col1, lookup_col2 = st.columns([3, 1])
with lookup_col1:
    search_ref = st.text_input("Enter Reference Number:", placeholder="e.g. 104502082026", label_visibility="collapsed")
with lookup_col2:
    search_triggered = st.button("🔍 Search Record", type="primary", use_container_width=True)

if search_triggered and search_ref:
    if not supabase:
        st.warning("⚠️ Supabase client is not configured. Live cloud lookup is unavailable.")
    else:
        with st.spinner("Searching cloud records..."):
            try:
                response = supabase.table("estimation_logs").select("*").eq("ref_no", search_ref.strip()).execute()
                records = response.data
                
                if records:
                    rec = records[0]
                    st.success(f"✅ **Record Found!** Client: **{rec.get('customer_name')}** | Date: {rec.get('est_date')} | Amount: ₹ {rec.get('amount'):,.2f}")
                    
                    url_std = rec.get('pdf_url')
                    url_no_hdr = rec.get('pdf_url_no_header')
                    
                    # Handle fallback storage format if separate column isn't migrated yet
                    if url_std and "|| NO_HEADER::" in url_std:
                        parts = url_std.split("|| NO_HEADER::")
                        url_std = parts[0]
                        url_no_hdr = parts[1] if len(parts) > 1 else None

                    sc1, sc2 = st.columns(2)
                    with sc1:
                        if url_std:
                            st.markdown(f"[📥 Download Standard Copy (Cloud)]({url_std})")
                        else:
                            st.info("Standard copy URL not found in record.")
                    with sc2:
                        if url_no_hdr:
                            st.markdown(f"[📥 Download No-Header Copy (Cloud)]({url_no_hdr})")
                        else:
                            st.info("No-header copy URL not found in record.")
                else:
                    st.error(f"❌ No record found matching Reference Number: `{search_ref}`")
            except Exception as e:
                st.error(f"Error executing lookup: {e}")


# --- INTERACTIVE 3D ROOM VISUALIZER SELECTOR ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🥽 Explore Interactive 3D Room Visualizer Gallery")
st.markdown("<p style='color:#94A3B8; font-size:0.95rem; margin-bottom:1.5rem;'>Select a zone below to inspect 3D spatial layouts, lighting configurations, and premium material finishes.</p>", unsafe_allow_html=True)

selected_room = st.radio(
    "Select Zone to Visualize:",
    ["🍳 Modular Kitchen (Island & U-Shape)", "🛋️ Luxury Living & Entertainment", "🛏️ Designer Wardrobes & Bedroom", "💡 False Ceiling & Ambient Lighting", "🪵 Italian Flooring & Wall Paneling"],
    horizontal=True,
    label_visibility="collapsed"
)

if "Kitchen" in selected_room:
    st.markdown("""
    <div class="glass-card-3d" style="display:flex; gap:30px; align-items:center;">
        <div style="flex:1;">
            <div style="color:#F59E0B; font-weight:800; font-size:0.8rem; letter-spacing:2px; text-transform:uppercase;">3D SPATIAL ZONE 01</div>
            <h2 style="font-family:'Cinzel', serif; font-size:2rem; color:#FFF; margin:8px 0 12px 0;">German Soft-Close Acrylic Kitchen</h2>
            <p style="color:#CBD5E1; line-height:1.6; margin-bottom:1.5rem;">
                Featuring Blum tandem box systems, quartz stone countertops with anti-scratch coating, integrated profile LED under-cabinet illumination, and water-resistant boiling waterproof (BWP) ply cores.
            </p>
            <div style="display:flex; gap:15px; color:#FBBF24; font-size:0.9rem; font-weight:700;">
                <div>✔️ Handleless Profile</div>
                <div>✔️ Anti-Fingerprint Finish</div>
                <div>✔️ 10-Year Warranty</div>
            </div>
        </div>
        <div style="flex:1;">
            <img src="https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=1000&q=80" style="width:100%; height:320px; object-fit:cover; border-radius:18px; border:1px solid rgba(217,119,6,0.4);" alt="Kitchen 3D">
        </div>
    </div>
    """, unsafe_allow_html=True)
elif "Living" in selected_room:
    st.markdown("""
    <div class="glass-card-3d" style="display:flex; gap:30px; align-items:center;">
        <div style="flex:1;">
            <div style="color:#F59E0B; font-weight:800; font-size:0.8rem; letter-spacing:2px; text-transform:uppercase;">3D SPATIAL ZONE 02</div>
            <h2 style="font-family:'Cinzel', serif; font-size:2rem; color:#FFF; margin:8px 0 12px 0;">Grand Living & TV Media Lounge</h2>
            <p style="color:#CBD5E1; line-height:1.6; margin-bottom:1.5rem;">
                Custom fluted wall paneling, Italian marble media console backdrops, concealed wiring ducts, automated smart curtains, and acoustic wall insulation for high-fidelity home theater experiences.
            </p>
            <div style="display:flex; gap:15px; color:#FBBF24; font-size:0.9rem; font-weight:700;">
                <div>✔️ Fluted Wooden Panels</div>
                <div>✔️ Acoustic Insulation</div>
                <div>✔️ Smart Lighting Sync</div>
            </div>
        </div>
        <div style="flex:1;">
            <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1000&q=80" style="width:100%; height:320px; object-fit:cover; border-radius:18px; border:1px solid rgba(217,119,6,0.4);" alt="Living 3D">
        </div>
    </div>
    """, unsafe_allow_html=True)
elif "Wardrobes" in selected_room:
    st.markdown("""
    <div class="glass-card-3d" style="display:flex; gap:30px; align-items:center;">
        <div style="flex:1;">
            <div style="color:#F59E0B; font-weight:800; font-size:0.8rem; letter-spacing:2px; text-transform:uppercase;">3D SPATIAL ZONE 03</div>
            <h2 style="font-family:'Cinzel', serif; font-size:2rem; color:#FFF; margin:8px 0 12px 0;">Floor-to-Ceiling Glass Wardrobes</h2>
            <p style="color:#CBD5E1; line-height:1.6; margin-bottom:1.5rem;">
                Tinted bronze glass wardrobe shutters with integrated sensor-activated wardrobe lighting rails, velvet-lined pull-out jewelry drawers, and heavy-duty soft-close mechanisms.
            </p>
            <div style="display:flex; gap:15px; color:#FBBF24; font-size:0.9rem; font-weight:700;">
                <div>✔️ Sensor Lighting</div>
                <div>✔️ Velvet Pull-outs</div>
                <div>✔️ Bronze Tinted Glass</div>
            </div>
        </div>
        <div style="flex:1;">
            <img src="https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=1000&q=80" style="width:100%; height:320px; object-fit:cover; border-radius:18px; border:1px solid rgba(217,119,6,0.4);" alt="Wardrobes 3D">
        </div>
    </div>
    """, unsafe_allow_html=True)
elif "Ceiling" in selected_room:
    st.markdown("""
    <div class="glass-card-3d" style="display:flex; gap:30px; align-items:center;">
        <div style="flex:1;">
            <div style="color:#F59E0B; font-weight:800; font-size:0.8rem; letter-spacing:2px; text-transform:uppercase;">3D SPATIAL ZONE 04</div>
            <h2 style="font-family:'Cinzel', serif; font-size:2rem; color:#FFF; margin:8px 0 12px 0;">Architectural False Ceiling & Coves</h2>
            <p style="color:#CBD5E1; line-height:1.6; margin-bottom:1.5rem;">
                Multi-layered gypsum board ceilings with concealed warm LED cove lighting, architectural magnetic track spotlights, and elegant chandelier centerpieces engineered for luxury ambiance.
            </p>
            <div style="display:flex; gap:15px; color:#FBBF24; font-size:0.9rem; font-weight:700;">
                <div>✔️ Magnetic Track Lights</div>
                <div>✔️ Warm Cove LED</div>
                <div>✔️ Gypsum Precision</div>
            </div>
        </div>
        <div style="flex:1;">
            <img src="https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1000&q=80" style="width:100%; height:320px; object-fit:cover; border-radius:18px; border:1px solid rgba(217,119,6,0.4);" alt="Ceiling 3D">
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="glass-card-3d" style="display:flex; gap:30px; align-items:center;">
        <div style="flex:1;">
            <div style="color:#F59E0B; font-weight:800; font-size:0.8rem; letter-spacing:2px; text-transform:uppercase;">3D SPATIAL ZONE 05</div>
            <h2 style="font-family:'Cinzel', serif; font-size:2rem; color:#FFF; margin:8px 0 12px 0;">Italian Marble & Wood Paneling</h2>
            <p style="color:#CBD5E1; line-height:1.6; margin-bottom:1.5rem;">
                Imported large-format Italian marble flooring with mirror-finish diamond polishing, coupled with seamless veneer wall paneling and brass inlay accents.
            </p>
            <div style="display:flex; gap:15px; color:#FBBF24; font-size:0.9rem; font-weight:700;">
                <div>✔️ Imported Marble</div>
                <div>✔️ Brass Inlays</div>
                <div>✔️ Mirror Polish</div>
            </div>
        </div>
        <div style="flex:1;">
            <img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1000&q=80" style="width:100%; height:320px; object-fit:cover; border-radius:18px; border:1px solid rgba(217,119,6,0.4);" alt="Flooring 3D">
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- MAIN CALL TO ACTION ---
st.markdown("<br>", unsafe_allow_html=True)
col_cta1, col_cta2, col_cta3 = st.columns([1, 2, 1])
with col_cta2:
    if st.button("🚀 LAUNCH OFFICIAL QUOTATION & PDF GENERATOR", type="primary", use_container_width=True):
        show_quotation_dialog()
