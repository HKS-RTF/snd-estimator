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
    page_title="SND Interior & Designs | Commercial & Residential Interior Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Advanced Commercial 3D Glassmorphism & Gradient Dashboard Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;800;900&family=Space+Grotesk:wght@500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background: #030712;
        color: #F8FAFC;
    }

    /* Ambient Background Glow Orbs */
    .bg-glow-1 {
        position: fixed;
        top: -10%;
        left: -10%;
        width: 50vw;
        height: 50vw;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
        z-index: 0;
        pointer-events: none;
        animation: pulseGlow 8s ease-in-out infinite alternate;
    }

    .bg-glow-2 {
        position: fixed;
        bottom: -10%;
        right: -10%;
        width: 50vw;
        height: 50vw;
        background: radial-gradient(circle, rgba(245, 158, 11, 0.12) 0%, transparent 70%);
        z-index: 0;
        pointer-events: none;
        animation: pulseGlow 10s ease-in-out infinite alternate-reverse;
    }

    @keyframes pulseGlow {
        0% { transform: scale(1); opacity: 0.7; }
        100% { transform: scale(1.15); opacity: 1; }
    }

    /* Commercial Gradient Header Text with 3D Depth */
    .hero-title-3d {
        font-family: 'Outfit', sans-serif;
        font-weight: 900;
        font-size: 3.5rem;
        background: linear-gradient(135deg, #FFFFFF 20%, #94A3B8 50%, #F59E0B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 20px 40px rgba(0,0,0,0.8);
        letter-spacing: -1px;
        margin-bottom: 10px;
    }

    .gradient-text-gold {
        background: linear-gradient(135deg, #FDE047 0%, #F59E0B 50%, #D97706 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .gradient-text-cyan {
        background: linear-gradient(135deg, #67E8F9 0%, #38BDF8 50%, #6366F1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Top Commercial Ticker / Status Bar */
    .commercial-ticker {
        background: linear-gradient(90deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.95) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 12px 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 2rem;
        font-size: 0.85rem;
        font-weight: 600;
        color: #94A3B8;
    }

    .live-dot {
        height: 10px;
        width: 10px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 12px #10B981;
        animation: liveBlink 1.5s infinite;
        margin-right: 8px;
    }

    @keyframes liveBlink {
        0% { transform: scale(0.95); opacity: 0.8; box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); opacity: 1; box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); opacity: 0.8; box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Commercial Glass Dashboard Container */
    .dashboard-card-3d {
        background: linear-gradient(145deg, rgba(17, 24, 39, 0.85) 0%, rgba(3, 7, 18, 0.95) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 28px;
        padding: 2.5rem;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }

    .dashboard-card-3d:hover {
        transform: translateY(-6px);
        border-color: rgba(245, 158, 11, 0.4);
        box-shadow: 0 40px 80px rgba(245, 158, 11, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.25);
    }

    /* Interactive 3D Visualizer GIF Frame Container */
    .visualizer-frame-3d {
        border-radius: 20px;
        overflow: hidden;
        border: 2px solid rgba(245, 158, 11, 0.3);
        box-shadow: 0 20px 50px rgba(0,0,0,0.8), 0 0 30px rgba(245, 158, 11, 0.2);
        position: relative;
        background: #000;
    }

    .visualizer-frame-3d img {
        width: 100%;
        height: 380px;
        object-fit: cover;
        display: block;
        transition: transform 0.6s ease;
    }

    .visualizer-frame-3d:hover img {
        transform: scale(1.04);
    }

    /* Metric Stat Card */
    .stat-box-commercial {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.8));
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        transition: all 0.3s ease;
    }

    .stat-box-commercial:hover {
        border-color: #38BDF8;
        transform: translateY(-4px);
    }

    /* Primary Action Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: #030712;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        border-radius: 14px;
        padding: 0.85rem 2rem;
        border: none;
        box-shadow: 0 10px 30px rgba(217, 119, 6, 0.4);
        transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #FBBF24 0%, #D97706 100%);
        box-shadow: 0 15px 40px rgba(245, 158, 11, 0.6);
        transform: translateY(-3px);
    }

    /* Auth & Security Banner */
    .commercial-auth-banner {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(99, 102, 241, 0.4);
        border-radius: 20px;
        padding: 1.5rem;
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(99, 102, 241, 0.2);
    }

    /* Auto Sliding Interior Showcase Slideshow CSS */
    .slider-container {
        position: relative;
        width: 100%;
        height: 380px;
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 20px 50px rgba(0,0,0,0.8), 0 0 30px rgba(99, 102, 241, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .slide {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0;
        transition: opacity 1s ease-in-out;
        background-size: cover;
        background-position: center;
    }

    .slide.active {
        opacity: 1;
    }

    .slide-caption {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(to top, rgba(3, 7, 18, 0.9), transparent);
        padding: 25px 25px 20px 25px;
        color: #fff;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1.25rem;
        letter-spacing: 0.5px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>

<div class="bg-glow-1"></div>
<div class="bg-glow-2"></div>
""", unsafe_allow_html=True)


# --- Initialize Session State ---
if "is_admin_logged_in" not in st.session_state:
    st.session_state.is_admin_logged_in = False
if "show_admin_modal" not in st.session_state:
    st.session_state.show_admin_modal = False


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


# --- AUTHENTIC MODAL POPUP DIALOG FOR ESTIMATION ---
@st.dialog("⚡ COMMERCIAL 3D ESTIMATION GENERATOR", width="large")
def show_quotation_dialog():
    st.markdown("""
    <div class="commercial-auth-banner">
        <div style="font-size:2.2rem;">🔐</div>
        <div>
            <div style="color:#818CF8; font-weight:700; font-size:0.85rem; letter-spacing:1px;">SECURE SSL GATEWAY • COMMERCIAL GST INVOICING</div>
            <div style="color:#FFFFFF; font-size:0.8rem;">Generate encrypted PDF estimates with dynamic QR code authentication for Bengaluru projects.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("popup_estimation_form"):
        st.subheader("👤 Agent & Submitter Details")
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            user_name = st.text_input("Agent Name *", value="", placeholder="Enter name")
            user_mobile = st.text_input("Mobile Number *", value="", placeholder="Enter mobile")
        with col_u2:
            user_email = st.text_input("Email ID *", value="", placeholder="Enter email")

        st.markdown("---")
        st.subheader("🏠 Property Details")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            customer_name = st.text_input("Customer Full Name *", value="", placeholder="Customer name")
            date_input = st.text_input("Quotation Date", value=datetime.now().strftime("%d-%m-%Y"))
        with col_c2:
            pass

        address_input = st.text_area(
            "Site / Flat Address in Bengaluru *", 
            value="",
            placeholder="Enter complete address in Bengaluru"
        )

        st.markdown("---")
        st.subheader("💰 Financial Budget Calculation")
        
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

        submitted = st.form_submit_button("⚡ GENERATE ENCRYPTED PDF", type="primary", use_container_width=True)

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
                st.success("🎉 **Quotation Generated & Synced Successfully!**")
                
                st.markdown(f"""
                <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid #F59E0B; padding: 20px; border-radius: 14px; margin: 15px 0;">
                    <h3 style="color: #F59E0B; margin-top: 0;">REF NO: {generated_ref}</h3>
                    <p style="font-size: 1.05rem; color: #F8FAFC; line-height: 1.6;">
                        <b>Your request has been accepted. Please wait some time; you will receive it via mail or WhatsApp.</b>
                    </p>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")


# --- ADMIN MODAL POPUP DIALOG ---
@st.dialog("🔐 ENTERPRISE ADMIN PORTAL", width="large")
def show_admin_dialog():
    if not st.session_state.is_admin_logged_in:
        with st.form("admin_login_form"):
            st.markdown("<p style='color:#94A3B8;'>Authenticate with enterprise credentials to access live quotation databases and audit logs.</p>", unsafe_allow_html=True)
            login_user = st.text_input("Username", value="")
            login_pass = st.text_input("Password", type="password", value="")
            login_submit = st.form_submit_button("🔑 Authorize Access", type="primary")

        if login_submit:
            if login_user == "HARI1109" and login_pass == "73384@Hks":
                st.session_state.is_admin_logged_in = True
                st.success("🎉 Authorization successful!")
                st.rerun()
            else:
                st.error("❌ Invalid enterprise credentials.")
    else:
        st.success("🔓 Authenticated as Administrator (HARI1109)")
        if st.button("🔒 Terminate Session"):
            st.session_state.is_admin_logged_in = False
            st.rerun()

        st.markdown("---")
        tab_history, tab_lookup = st.tabs(["📊 Live Estimation Records", "🔍 Document Cloud Lookup"])

        with tab_history:
            st.markdown("#### 📋 Recent Quotations Ledger")
            if not supabase:
                st.warning("⚠️ Supabase connection inactive.")
            else:
                try:
                    res = supabase.table("estimation_logs").select("*").order("est_date", desc=True).limit(20).execute()
                    data = res.data
                    if data:
                        st.dataframe(data, use_container_width=True)
                    else:
                        st.info("No records found.")
                except Exception as e:
                    st.error(f"Database error: {e}")

        with tab_lookup:
            st.markdown("#### 🔎 Reference Code Cloud Search")
            search_ref = st.text_input("Enter Reference Number:", placeholder="e.g. 104502082026")
            if st.button("Query Cloud Database", type="primary"):
                if not supabase:
                    st.warning("⚠️ Supabase connection inactive.")
                else:
                    try:
                        response = supabase.table("estimation_logs").select("*").eq("ref_no", search_ref.strip()).execute()
                        records = response.data
                        if records:
                            rec = records[0]
                            st.success(f"✅ **Record Verified!** Customer: **{rec.get('customer_name')}** | Agent: {rec.get('user_name', 'N/A')} | Date: {rec.get('est_date')} | Total: ₹ {rec.get('amount'):,.2f}")
                            
                            url_std = rec.get('pdf_url')
                            url_no_hdr = rec.get('pdf_url_no_header')
                            if url_std and "|| NO_HEADER::" in url_std:
                                parts = url_std.split("|| NO_HEADER::")
                                url_std = parts[0]
                                url_no_hdr = parts[1] if len(parts) > 1 else None

                            sc1, sc2 = st.columns(2)
                            with sc1:
                                if url_std: st.markdown(f"[📥 Download Standard PDF (Cloud)]({url_std})")
                            with sc2:
                                if url_no_hdr: st.markdown(f"[📥 Download Clean PDF (Cloud)]({url_no_hdr})")
                        else:
                            st.error(f"❌ No records matched reference: `{search_ref}`")
                    except Exception as e:
                        st.error(f"Query execution failed: {e}")


# --- COMMERCIAL TICKER STATUS BAR WITH LOGIN ICON BUTTON ---
col_tick1, col_tick2 = st.columns([10, 1])
with col_tick1:
    st.markdown("""
    <div class="commercial-ticker" style="margin-bottom:0;">
        <div><span class="live-dot"></span>LIVE COMMERCIAL HUB: BENGALURU (SAHAKARNAGAR | HSR | WHITEFIELD)</div>
        <div>SUPPORT HOTLINE: +91 98765 43210 &nbsp;|&nbsp; SLA: 99.9% UPTIME</div>
    </div>
    """, unsafe_allow_html=True)
with col_tick2:
    if st.button("🔐", help="Enterprise Admin Portal Login"):
        show_admin_dialog()

st.markdown("<br>", unsafe_allow_html=True)


# --- 3D GRADIENT HERO SECTION WITH AUTO-SLIDING INTERIOR IMAGES ---
col_hero1, col_hero2 = st.columns([1.2, 1])

with col_hero1:
    st.markdown("""
    <div class="dashboard-card-3d" style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.85) 100%); padding: 3rem 2.5rem; height: 100%;">
        <div style="font-family:'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.85rem; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 12px;">
            <span class="gradient-text-gold">✦ ENTERPRISE EXTERIOR & INTERIOR </span>
        </div>
        <h1 class="hero-title-3d" style="font-size: 3rem;">SND INTERIOR & DESIGNS</h1>
        <p style="color: #CBD5E1; font-size: 1.1rem; line-height: 1.7; margin-bottom: 2rem;">
            Commercial-grade Materials and Raw Materials,  GST quotations, and turnkey interior manufacturing engineered for elite residential developments across Bengaluru.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_hero2:
    # Auto-sliding showcase slideshow using HTML/CSS + Javascript snippet injected into Streamlit
    st.markdown("""
    <div class="slider-container" id="interiorSlider">
        <div class="slide active" style="background-image: url('https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1000&q=80');">
            <div class="slide-caption">Luxury Living Room & Entertainment Lounge</div>
        </div>
        <div class="slide" style="background-image: url('https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=1000&q=80');">
            <div class="slide-caption">Modular German Acrylic Kitchen</div>
        </div>
        <div class="slide" style="background-image: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1000&q=80');">
            <div class="slide-caption">Acoustic Fluted Panel Wall Decor</div>
        </div>
        <div class="slide" style="background-image: url('https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=1000&q=80');">
            <div class="slide-caption">Floor-to-Ceiling Tinted Glass Wardrobes</div>
        </div>
        <div class="slide" style="background-image: url('https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1000&q=80');">
            <div class="slide-caption">Imported Italian Marble & Wood Paneling</div>
        </div>
    </div>

    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('#interiorSlider .slide');
        function nextSlide() {
            if(slides.length === 0) return;
            slides[currentSlide].classList.remove('active');
            currentSlide = (currentSlide + 1) % slides.length;
            slides[currentSlide].classList.add('active');
        }
        setInterval(nextSlide, 3500);
    </script>
    """, unsafe_allow_html=True)


# --- Commercial Metrics Grid ---
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.markdown("""
    <div class="stat-box-commercial">
        <div style="font-size: 1.8rem; font-weight: 800;" class="gradient-text-gold">500+</div>
        <div style="font-size: 0.8rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; margin-top: 5px;">Active Projects</div>
    </div>
    """, unsafe_allow_html=True)
with col_m2:
    st.markdown("""
    <div class="stat-box-commercial">
        <div style="font-size: 1.8rem; font-weight: 800;" class="gradient-text-cyan">10 YRS</div>
        <div style="font-size: 0.8rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; margin-top: 5px;">Structural Warranty</div>
    </div>
    """, unsafe_allow_html=True)
with col_m3:
    st.markdown("""
    <div class="stat-box-commercial">
        <div style="font-size: 1.8rem; font-weight: 800;" class="gradient-text-gold">45 DAYS</div>
        <div style="font-size: 0.8rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; margin-top: 5px;">Guaranteed Handover</div>
    </div>
    """, unsafe_allow_html=True)
with col_m4:
    st.markdown("""
    <div class="stat-box-commercial">
        <div style="font-size: 1.8rem; font-weight: 800;" class="gradient-text-cyan">100%</div>
        <div style="font-size: 0.8rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; margin-top: 5px;">Encrypted Sync</div>
    </div>
    """, unsafe_allow_html=True)


# --- INTERACTIVE 3D ANIMATED / GIF VISUALIZER ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🌀 Interactive Content")
st.markdown("<p style='color:#94A3B8; font-size:0.95rem; margin-bottom:1.5rem;'>Select a commercial zone to inspect real-time spatial physics, lighting loops, and modular material simulations.</p>", unsafe_allow_html=True)

selected_room = st.radio(
    "Select Simulation Zone:",
    ["🍳 Modular Kitchen (Island & U-Shape)", "🛋️ Luxury Living & Media Lounge", "🛏️ Designer Wardrobes & Bedroom", "💡 Architectural False Ceiling", "🪵 Italian Flooring & Paneling"],
    horizontal=True,
    label_visibility="collapsed"
)

if "Kitchen" in selected_room:
    st.markdown("""
    <div class="dashboard-card-3d" style="display:flex; gap:35px; align-items:center;">
        <div style="flex:1;">
            <div style="font-family:'Space Grotesk', sans-serif; font-weight:800; font-size:0.8rem; letter-spacing:2px; color:#F59E0B; text-transform:uppercase;">SIMULATION MODULE 01</div>
            <h2 style="font-family:'Outfit', sans-serif; font-size:2.2rem; font-weight:800; color:#FFF; margin:10px 0 15px 0;">German Soft-Close Acrylic Kitchen</h2>
            <p style="color:#CBD5E1; line-height:1.7; margin-bottom:1.5rem;">
                Engineered with Blum tandem box mechanisms, scratch-resistant quartz stone counters, integrated LED profile strip lighting, and water-resistant BWP marine-grade plywood cores.
            </p>
            <div style="display:flex; gap:15px; color:#38BDF8; font-weight:700; font-size:0.9rem;">
                <div>⚡ Blum Hardware</div>
                <div>⚡ Quartz Stone</div>
                <div>⚡ 10-Yr Warranty</div>
            </div>
        </div>
        <div style="flex:1;">
            <div class="visualizer-frame-3d">
                <img src="https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=1000&q=80" alt="Kitchen 3D GIF">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
elif "Living" in selected_room:
    st.markdown("""
    <div class="dashboard-card-3d" style="display:flex; gap:35px; align-items:center;">
        <div style="flex:1;">
            <div style="font-family:'Space Grotesk', sans-serif; font-weight:800; font-size:0.8rem; letter-spacing:2px; color:#F59E0B; text-transform:uppercase;">SIMULATION MODULE 02</div>
            <h2 style="font-family:'Outfit', sans-serif; font-size:2.2rem; font-weight:800; color:#FFF; margin:10px 0 15px 0;">Grand Living & Media Lounge</h2>
            <p style="color:#CBD5E1; line-height:1.7; margin-bottom:1.5rem;">
                Featuring custom acoustic fluted panels, sintered stone TV media backdrops, motorized smart curtains, and concealed wiring channels for high-end home theater setups.
            </p>
            <div style="display:flex; gap:15px; color:#38BDF8; font-weight:700; font-size:0.9rem;">
                <div>⚡ Fluted Panels</div>
                <div>⚡ Acoustic Wall</div>
                <div>⚡ Smart Motorized</div>
            </div>
        </div>
        <div style="flex:1;">
            <div class="visualizer-frame-3d">
                <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1000&q=80" alt="Living 3D GIF">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
elif "Wardrobes" in selected_room:
    st.markdown("""
    <div class="dashboard-card-3d" style="display:flex; gap:35px; align-items:center;">
        <div style="flex:1;">
            <div style="font-family:'Space Grotesk', sans-serif; font-weight:800; font-size:0.8rem; letter-spacing:2px; color:#F59E0B; text-transform:uppercase;">SIMULATION MODULE 03</div>
            <h2 style="font-family:'Outfit', sans-serif; font-size:2.2rem; font-weight:800; color:#FFF; margin:10px 0 15px 0;">Floor-to-Ceiling Glass Wardrobes</h2>
            <p style="color:#CBD5E1; line-height:1.7; margin-bottom:1.5rem;">
                Bronze tinted safety glass sliding doors equipped with motion-activated LED hanging rails, velvet-lined pull-out organizer trays, and soft-closing dampeners.
            </p>
            <div style="display:flex; gap:15px; color:#38BDF8; font-weight:700; font-size:0.9rem;">
                <div>⚡ Sensor Lighting</div>
                <div>⚡ Velvet Trays</div>
                <div>⚡ Tinted Glass</div>
            </div>
        </div>
        <div style="flex:1;">
            <div class="visualizer-frame-3d">
                <img src="https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=1000&q=80" alt="Wardrobes 3D GIF">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
elif "Ceiling" in selected_room:
    st.markdown("""
    <div class="dashboard-card-3d" style="display:flex; gap:35px; align-items:center;">
        <div style="flex:1;">
            <div style="font-family:'Space Grotesk', sans-serif; font-weight:800; font-size:0.8rem; letter-spacing:2px; color:#F59E0B; text-transform:uppercase;">SIMULATION MODULE 04</div>
            <h2 style="font-family:'Outfit', sans-serif; font-size:2.2rem; font-weight:800; color:#FFF; margin:10px 0 15px 0;">Architectural False Ceiling & Coves</h2>
            <p style="color:#CBD5E1; line-height:1.7; margin-bottom:1.5rem;">
                Multi-tier gypsum board architectural drops featuring warm concealed cove lighting lines, magnetic track spotlight fixtures, and statement crystal chandelier mounts.
            </p>
            <div style="display:flex; gap:15px; color:#38BDF8; font-weight:700; font-size:0.9rem;">
                <div>⚡ Magnetic Tracks</div>
                <div>⚡ Warm Cove LED</div>
                <div>⚡ Gypsum Finish</div>
            </div>
        </div>
        <div style="flex:1;">
            <div class="visualizer-frame-3d">
                <img src="https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1000&q=80" alt="Ceiling 3D GIF">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="dashboard-card-3d" style="display:flex; gap:35px; align-items:center;">
        <div style="flex:1;">
            <div style="font-family:'Space Grotesk', sans-serif; font-weight:800; font-size:0.8rem; letter-spacing:2px; color:#F59E0B; text-transform:uppercase;">SIMULATION MODULE 05</div>
            <h2 style="font-family:'Outfit', sans-serif; font-size:2.2rem; font-weight:800; color:#FFF; margin:10px 0 15px 0;">Imported Italian Marble & Wood Paneling</h2>
            <p style="color:#CBD5E1; line-height:1.7; margin-bottom:1.5rem;">
                Mirror-polished large-format Italian marble tiles paired with vertical natural wood veneer wall cladding and brushed brass inlay metal trims.
            </p>
            <div style="display:flex; gap:15px; color:#38BDF8; font-weight:700; font-size:0.9rem;">
                <div>⚡ Italian Marble</div>
                <div>⚡ Brass Inlays</div>
                <div>⚡ Veneer Finish</div>
            </div>
        </div>
        <div style="flex:1;">
            <div class="visualizer-frame-3d">
                <img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1000&q=80" alt="Flooring 3D GIF">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# --- MAIN ACTION BUTTON ---
st.markdown("<br>", unsafe_allow_html=True)
col_cta1, col_cta2, col_cta3 = st.columns([1, 2, 1])
with col_cta2:
    if st.button("⚡ GET YOUR QUOTATION NOW ", type="primary", use_container_width=True):
        show_quotation_dialog()
