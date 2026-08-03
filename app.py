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

# --- Enhanced High-End UI/UX & Graphics Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background: radial-gradient(circle at 50% 0%, #111827 0%, #070A12 70%);
        color: #F8FAFC;
    }

    /* Top Premium Glass Utility Nav */
    .top-nav {
        background: linear-gradient(90deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%);
        backdrop-filter: blur(12px);
        color: #CBD5E1;
        padding: 14px 32px;
        font-size: 0.85rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #D97706;
        box-shadow: 0 8px 32px rgba(0,0,0,0.7);
        border-radius: 0 0 20px 20px;
        margin-bottom: 2.5rem;
    }

    /* Hero Section Banner Art */
    .hero-banner-art {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%),
                    url('https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=2000&q=80');
        background-blend-mode: overlay;
        background-size: cover;
        background-position: center;
        border-radius: 32px;
        padding: 4rem 3rem;
        border: 1px solid rgba(217, 119, 6, 0.3);
        box-shadow: 0 25px 60px rgba(0,0,0,0.8), inset 0 1px 0 rgba(255,255,255,0.2);
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
    }

    .hero-banner-art::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(217,119,6,0.1) 0%, transparent 60%);
        pointer-events: none;
    }

    /* 3D Glassmorphism Cards with Glowing Depth */
    .glass-card-3d {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.9) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 28px;
        padding: 2.5rem;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        margin-bottom: 2rem;
    }

    .glass-card-3d:hover {
        transform: translateY(-8px) scale(1.01);
        border-color: #D97706;
        box-shadow: 0 35px 70px rgba(217, 119, 6, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.35);
    }

    /* Metric & Statistic Cards */
    .metric-card-3d {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.8));
        border: 1px solid rgba(217, 119, 6, 0.25);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        transition: transform 0.3s ease;
    }

    .metric-card-3d:hover {
        transform: translateY(-5px);
        border-color: #F59E0B;
    }

    /* Primary Gold Action Button Overrides */
    .stButton > button {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: #070A12;
        font-weight: 800;
        border-radius: 16px;
        padding: 0.85rem 2rem;
        border: none;
        box-shadow: 0 10px 25px rgba(217, 119, 6, 0.4);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #FBBF24 0%, #D97706 100%);
        box-shadow: 0 15px 35px rgba(217, 119, 6, 0.6);
        transform: translateY(-2px);
    }

    /* Authentic Security Header inside Form */
    .auth-banner {
        background: linear-gradient(135deg, #1E1B4B 0%, #0F172A 100%);
        border: 1px solid #6366F1;
        border-radius: 20px;
        padding: 1.5rem;
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 12px 30px rgba(99, 102, 241, 0.25);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# --- Initialize Session State for Login ---
if "is_admin_logged_in" not in st.session_state:
    st.session_state.is_admin_logged_in = False


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

def upload_to_cloud(ref_no, pdf_bytes_standard, pdf_bytes_no_header, filename_std, filename_no_hdr, user_name, user_mobile, user_email, customer_name, est_date, final_total):
    if not supabase: return None, None
    
    path_std = f"pdf_estimations/{filename_std}"
    supabase.storage.from_("estimations").upload(
        path=path_std,
        file=pdf_bytes_standard,
        file_options={"content-type": "application/pdf", "upsert": "true"}
    )
    url_std = supabase.storage.from_("estimations").get_public_url(path_std)

    path_no_hdr = f"pdf_estimations/{filename_no_hdr}"
    supabase.storage.from_("estimations").upload(
        path=path_no_hdr,
        file=pdf_bytes_no_header,
        file_options={"content-type": "application/pdf", "upsert": "true"}
    )
    url_no_hdr = supabase.storage.from_("estimations").get_public_url(path_no_hdr)

    data = {
        "ref_no": str(ref_no),
        "user_name": str(user_name.upper()),
        "user_mobile": str(user_mobile),
        "user_email": str(user_email),
        "customer_name": str(customer_name.upper()),
        "est_date": str(est_date),
        "amount": float(final_total),
        "pdf_url": url_std,
        "pdf_url_no_header": url_no_hdr
    }
    
    try:
        supabase.table("estimation_logs").upsert(data).execute()
    except Exception:
        fallback_data = {
            "ref_no": str(ref_no),
            "customer_name": str(customer_name.upper()),
            "est_date": str(est_date),
            "amount": float(final_total),
            "pdf_url": f"{url_std} || NO_HEADER::{url_no_hdr}"
        }
        supabase.table("estimation_logs").upsert(fallback_data).execute()

    return url_std, url_no_hdr


def generate_estimation_pdf_bytes(customer_name, address, est_date, target_total, include_header=True):
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
    clean_customer_name = customer_name.replace(' ', '_').replace('&', 'AND')
    filename = f"Estimation_{ref_no}_{clean_customer_name}{'_NoHeader' if not include_header else ''}.pdf"

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
        qr_data = f"CUSTOMER NAME: {customer_name.upper()}\nADDRESS: {address.upper()}\nREF NO: {ref_no}\nDATE: {est_date}\nESTIMATION AMOUNT: Rs. {final_total:,}\nEMAIL: contact@sndinteriors.com"
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
                Spacer(1, 10), Spacer(1, 10), Spacer(1, 10), Spacer(1, 10), Spacer(1, 10)
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
    box_content.append([Paragraph(f"OWNER: - {customer_name.upper()}", box_detail_style)])

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


# --- AUTHENTIC MODAL POPUP DIALOG WITH BLANK FIELDS ---
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
        st.subheader("👤 User / Submitter Details")
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            user_name = st.text_input("User / Agent Name *", value="", placeholder="Enter your name")
            user_mobile = st.text_input("User Mobile Number *", value="", placeholder="Enter mobile number")
        with col_u2:
            user_email = st.text_input("User Email ID *", value="", placeholder="Enter email address")

        st.markdown("---")
        st.subheader("🏠 Customer & Property Details (Printed on Quotation)")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            customer_name = st.text_input("Customer Full Name *", value="", placeholder="Enter customer name")
            date_input = st.text_input("Quotation Date", value=datetime.now().strftime("%d-%m-%Y"))
        with col_c2:
            pass 

        address_input = st.text_area(
            "Customer Property / Site Address in Bengaluru *", 
            value="",
            placeholder="Enter complete site or flat address in Bengaluru"
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

        submitted = st.form_submit_button("⚡ GENERATE PDF", type="primary", use_container_width=True)

    if submitted:
        if not user_name.strip() or not user_mobile.strip() or not user_email.strip() or not customer_name.strip() or not address_input.strip():
            st.warning("⚠️ Please fill in all required fields before generating the quotation.")
            return

        with st.spinner('Generating PDF copies and syncing securely with cloud storage...'):
            try:
                pdf_bytes_std, filename_std, generated_ref, final_total = generate_estimation_pdf_bytes(
                    customer_name, address_input, date_input, float(amount_input), include_header=True
                )
                pdf_bytes_no_hdr, filename_no_hdr, _, _ = generate_estimation_pdf_bytes(
                    customer_name, address_input, date_input, float(amount_input), include_header=False
                )
                
                if supabase:
                    upload_to_cloud(
                        generated_ref, pdf_bytes_std, pdf_bytes_no_hdr, 
                        filename_std, filename_no_hdr, user_name, user_mobile, user_email, 
                        customer_name, date_input, final_total
                    )
                
                st.balloons()
                st.success("🎉 **Quotation Generated Successfully!**")
                
                st.markdown(f"""
                <div style="background: rgba(217, 119, 6, 0.15); border: 1px solid #D97706; padding: 20px; border-radius: 14px; margin: 15px 0;">
                    <h3 style="color: #F59E0B; margin-top: 0;">REF NO: {generated_ref}</h3>
                    <p style="font-size: 1.05rem; color: #F8FAFC; line-height: 1.6;">
                        <b>Your request has been accepted. Please wait some time; you will receive it via mail or WhatsApp.</b>
                    </p>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")


# --- TOP NAVIGATION BAR ---
st.markdown("""
<div class="top-nav">
    <div>📍 <b>BANGALORE EXPERIENCE CENTERS:</b> Sahakarnagar | HSR Layout | Whitefield | Yelahanka</div>
    <div>📞 <b>VIP CLIENT DESK:</b> +91 98765 43210 &nbsp;|&nbsp; ✉️ contact@sndinteriors.com</div>
</div>
""", unsafe_allow_html=True)


# --- HIGH-END UI/UX HERO BANNER ART ---
st.markdown("""
<div class="hero-banner-art">
    <div style="max-width: 700px;">
        <div style="color: #F59E0B; font-weight: 800; font-size: 0.85rem; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 10px;">👑 BENGALURU'S PREMIER 3D INTERIOR STUDIO</div>
        <h1 style="font-family: 'Cinzel', serif; font-size: 3rem; font-weight: 900; color: #FFFFFF; line-height: 1.1; margin-bottom: 20px;">SND INTERIOR & DESIGNS</h1>
        <p style="color: #CBD5E1; font-size: 1.1rem; line-height: 1.6; margin-bottom: 30px;">
            Immersive 3D Photorealistic Visualizations, 100% Factory-Finished Modular Kitchens, Designer Wardrobes, and Turnkey Luxury Home Interiors.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)


# --- Trust Stats Metrics Grid in 3D Glass Cards ---
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
with col_stat1:
    st.markdown("""
    <div class="metric-card-3d">
        <div style="font-size: 1.8rem; font-weight: 800; color: #F59E0B; margin-bottom: 5px;">500+</div>
        <div style="font-size: 0.85rem; color: #94A3B8; font-weight: 600; text-transform: uppercase;">Luxury Homes Completed</div>
    </div>
    """, unsafe_allow_html=True)
with col_stat2:
    st.markdown("""
    <div class="metric-card-3d">
        <div style="font-size: 1.8rem; font-weight: 800; color: #F59E0B; margin-bottom: 5px;">10 YRS</div>
        <div style="font-size: 0.85rem; color: #94A3B8; font-weight: 600; text-transform: uppercase;">Material Warranty</div>
    </div>
    """, unsafe_allow_html=True)
with col_stat3:
    st.markdown("""
    <div class="metric-card-3d">
        <div style="font-size: 1.8rem; font-weight: 800; color: #F59E0B; margin-bottom: 5px;">45 DAYS</div>
        <div style="font-size: 0.85rem; color: #94A3B8; font-weight: 600; text-transform: uppercase;">Guaranteed Delivery</div>
    </div>
    """, unsafe_allow_html=True)
with col_stat4:
    st.markdown("""
    <div class="metric-card-3d">
        <div style="font-size: 1.8rem; font-weight: 800; color: #F59E0B; margin-bottom: 5px;">100%</div>
        <div style="font-size: 0.85rem; color: #94A3B8; font-weight: 600; text-transform: uppercase;">Transparent Pricing</div>
    </div>
    """, unsafe_allow_html=True)


# --- ADMIN LOGIN & RECENT HISTORY / LOOKUP SECTION ---
st.markdown("---")
st.markdown("### 🔐 Admin Portal: Recent History & Cloud Lookup")

if not st.session_state.is_admin_logged_in:
    with st.form("admin_login_form"):
        st.markdown("<p style='color:#94A3B8;'>Please enter administrator credentials to access client history and lookup tools.</p>", unsafe_allow_html=True)
        login_user = st.text_input("Username", value="")
        login_pass = st.text_input("Password", type="password", value="")
        login_submit = st.form_submit_button("🔑 Login to Admin Dashboard", type="primary")

    if login_submit:
        if login_user == "HARI1109" and login_pass == "73384@Hks":
            st.session_state.is_admin_logged_in = True
            st.success("🎉 Login successful! Unlocking dashboard...")
            st.rerun()
        else:
            st.error("❌ Invalid Username or Password. Please try again.")
else:
    st.success("🔓 Authenticated as Admin (HARI1109)")
    if st.button("🔒 Logout"):
        st.session_state.is_admin_logged_in = False
        st.rerun()

    st.markdown("---")
    tab_history, tab_lookup = st.tabs(["📊 Recent Quotation History", "🔍 Cloud Document Lookup"])

    with tab_history:
        st.markdown("#### 📋 Recent Quotation Records")
        if not supabase:
            st.warning("⚠️ Supabase client is not configured.")
        else:
            try:
                res = supabase.table("estimation_logs").select("*").order("est_date", desc=True).limit(20).execute()
                data = res.data
                if data:
                    st.dataframe(data, use_container_width=True)
                else:
                    st.info("No records found in database.")
            except Exception as e:
                st.error(f"Error fetching history: {e}")

    with tab_lookup:
        st.markdown("#### 🔎 Search Specific Quotation Record")
        search_ref = st.text_input("Enter Reference Number:", placeholder="e.g. 104502082026")
        if st.button("Search Cloud Record", type="primary"):
            if not supabase:
                st.warning("⚠️ Supabase client is not configured.")
            else:
                try:
                    response = supabase.table("estimation_logs").select("*").eq("ref_no", search_ref.strip()).execute()
                    records = response.data
                    if records:
                        rec = records[0]
                        st.success(f"✅ **Record Found!** Customer: **{rec.get('customer_name')}** | User: {rec.get('user_name', 'N/A')} | Date: {rec.get('est_date')} | Amount: ₹ {rec.get('amount'):,.2f}")
                        
                        url_std = rec.get('pdf_url')
                        url_no_hdr = rec.get('pdf_url_no_header')
                        if url_std and "|| NO_HEADER::" in url_std:
                            parts = url_std.split("|| NO_HEADER::")
                            url_std = parts[0]
                            url_no_hdr = parts[1] if len(parts) > 1 else None

                        sc1, sc2 = st.columns(2)
                        with sc1:
                            if url_std: st.markdown(f"[📥 Download Standard Copy (Cloud)]({url_std})")
                        with sc2:
                            if url_no_hdr: st.markdown(f"[📥 Download No-Header Copy (Cloud)]({url_no_hdr})")
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
    if st.button("🚀 GENERATE QUOTATION", type="primary", use_container_width=True):
        show_quotation_dialog()
