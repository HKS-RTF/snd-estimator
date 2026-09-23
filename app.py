import os
import random
import io
from datetime import datetime
import streamlit as st
from supabase import create_client, Client

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget

# --- Page Configuration ---
st.set_page_config(
    page_title="SND Interior & Designs | Civil Construction & Floor Extension Dashboard",
    page_icon="🏗️",
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

    /* Interactive 3D Visualizer Frame Container */
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

    /* Robust Direct IMG Carousel Styles */
    .slider-box {
        position: relative;
        width: 100%;
        height: 380px;
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 20px 50px rgba(0,0,0,0.8), 0 0 30px rgba(99, 102, 241, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: #0b0f19;
    }

    .carousel-slide {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0;
        transition: opacity 1s ease-in-out;
    }

    .carousel-slide.active {
        opacity: 1;
    }

    .carousel-slide img {
        width: 100%;
        height: 380px;
        object-fit: cover;
        display: block;
    }

    .carousel-caption {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(to top, rgba(3, 7, 18, 0.95), transparent);
        padding: 30px 25px 20px 25px;
        color: #fff;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1.25rem;
        letter-spacing: 0.5px;
    }

    /* Static Grid Gallery Styles */
    .static-gallery-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 16px;
        margin-top: 1.5rem;
        margin-bottom: 2rem;
    }

    .static-gallery-item {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        transition: all 0.3s ease;
    }

    .static-gallery-item:hover {
        transform: translateY(-5px);
        border-color: rgba(245, 158, 11, 0.5);
        box-shadow: 0 15px 35px rgba(245, 158, 11, 0.2);
    }

    .static-gallery-item img {
        width: 100%;
        height: 160px;
        object-fit: cover;
        display: block;
    }

    .static-gallery-label {
        padding: 10px 12px;
        font-size: 0.8rem;
        font-weight: 700;
        color: #F8FAFC;
        text-align: center;
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(to bottom, rgba(15, 23, 42, 0.9), rgba(3, 7, 18, 0.95));
    }

    /* Full-Size Vertical Scrolling Gallery Section */
    .vertical-gallery-container {
        display: flex;
        flex-direction: column;
        gap: 2rem;
        margin-top: 1.5rem;
        margin-bottom: 2.5rem;
    }

    .vertical-gallery-card {
        position: relative;
        width: 100%;
        height: 520px;
        border-radius: 24px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.7);
        transition: transform 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease;
        background: #0b0f19;
    }

    .vertical-gallery-card:hover {
        transform: translateY(-6px);
        border-color: rgba(245, 158, 11, 0.5);
        box-shadow: 0 35px 70px rgba(245, 158, 11, 0.25);
    }

    .vertical-gallery-card img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
        transition: transform 0.6s ease;
    }

    .vertical-gallery-card:hover img {
        transform: scale(1.03);
    }

    .vertical-card-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(to top, rgba(3, 7, 18, 0.95) 0%, rgba(3, 7, 18, 0.6) 60%, transparent 100%);
        padding: 40px 35px 30px 35px;
        color: #FFFFFF;
        font-family: 'Outfit', sans-serif;
    }

    .vertical-card-badge {
        display: inline-block;
        padding: 6px 14px;
        background: rgba(245, 158, 11, 0.2);
        border: 1px solid rgba(245, 158, 11, 0.5);
        color: #FBBF24;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        border-radius: 20px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .vertical-card-title {
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 8px;
        color: #FFFFFF;
    }

    .vertical-card-desc {
        color: #94A3B8;
        font-size: 0.95rem;
        font-weight: 500;
        max-width: 800px;
        line-height: 1.5;
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


def generate_estimation_pdf_bytes(customer_name, address, est_date, target_total, floors_option, buildup_sqft, include_header=True):
    is_single_page = target_total < 2000000
    
    # CIVIL WORKS MASTER ITEMS FOR FLOOR EXTENSIONS
    CIVIL_ITEMS_MASTER = [
        ("Foundation & Column starter extension breaking/reinforcement", "JOB", "JOB_LOT", 0.07),
        ("RCC Column casting & structural steel framework (Fe550)", "CU. FT", "SQFT", 0.10),
        ("RCC Beam & Slab casting for floor extension (M25 Grade)", "SQ. FT", "SQFT", 0.12),
        ("External & Internal Brick masonry / AAC block work", "SQ. FT", "SQFT", 0.09),
        ("Structural plastering (Internal walls & ceiling)", "SQ. FT", "SQFT", 0.08),
        ("External wall plastering & weatherproof textured finish", "SQ. FT", "SQFT", 0.07),
        ("Structural staircase extension & concrete steps casting", "UNIT", "SETS_UNITS", 0.06),
        ("Terrace waterproofing and chemical damp-proofing", "SQ. FT", "SQFT", 0.06),
        ("Underground/Overhead plumbing lines & drainage rough-in", "JOB", "JOB_LOT", 0.07),
        ("Electrical conduit piping, concealed wiring & DB box setup", "JOB", "JOB_LOT", 0.07),
        ("Parapet wall construction around terrace boundary", "RUN. FT", "SQFT", 0.05),
        ("Scaffolding erection, safety netting & debris removal", "LOT", "JOB_LOT", 0.05),
        ("Door and window concrete lintel casting & framing", "JOB", "JOB_LOT", 0.05),
        ("Flooring screed and tile bedding preparation", "SQ. FT", "SQFT", 0.06),
        ("Site clearing, architectural layout & centering work", "JOB", "JOB_LOT", 0.04)
    ]

    def calculate_civil_quantity(category, total_sqft):
        if category == "SQFT": 
            return f"{round(buildup_sqft)} SQ. FT"
        elif category == "SETS_UNITS":
            qty = round(buildup_sqft / 400) if buildup_sqft > 0 else 1
            return f"{max(1, qty)} SETS"
        elif category == "JOB_LOT":
            return "1 JOB"
        return f"{round(buildup_sqft)} SQ. FT"

    total_items_needed = 10 if is_single_page else 15
    processed_items = [(desc, calculate_civil_quantity(cat, buildup_sqft), w) for desc, _, cat, w in CIVIL_ITEMS_MASTER]
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
    filename = f"Civil_Extension_{ref_no}_{clean_customer_name}{'_NoHeader' if not include_header else ''}.pdf"

    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=15, bottomMargin=15)
    styles = getSampleStyleSheet()

    RED_COLOR, BLUE_COLOR, LIGHT_PINK, BORDER_BLUE = colors.HexColor("#DC2626"), colors.HexColor("#1E40AF"), colors.HexColor("#EC4899"), colors.HexColor("#2563EB")

    title_style = ParagraphStyle("Title", parent=styles["Heading1"], alignment=1, fontSize=28, leading=32, fontName="Helvetica-Bold", textColor=RED_COLOR)
    sub_style = ParagraphStyle("Sub", parent=styles["Normal"], alignment=1, fontSize=9, leading=12, fontName="Helvetica-Bold", textColor=BLUE_COLOR)
    contact_style = ParagraphStyle("Contact", parent=styles["Normal"], alignment=1, fontSize=8.5, leading=11, fontName="Helvetica-Bold", textColor=BLUE_COLOR)
    gstin_style = ParagraphStyle("GSTIN", parent=styles["Normal"], alignment=1, fontSize=9, leading=12, fontName="Helvetica-Bold", textColor=LIGHT_PINK)
    ref_left_style = ParagraphStyle("RefLeft", parent=styles["Normal"], alignment=0, fontSize=10, leading=12, fontName="Helvetica")
    ref_right_style = ParagraphStyle("RefRight", parent=styles["Normal"], alignment=2, fontSize=10, leading=12, fontName="Helvetica")
    box_hdr_style = ParagraphStyle("BoxHdr", parent=styles["Normal"], alignment=1, fontSize=13, leading=15, fontName="Helvetica-Bold", textColor=colors.black)
    box_detail_style = ParagraphStyle("BoxDetail", parent=styles["Normal"], alignment=1, fontSize=11.5, leading=14, fontName="Helvetica-Bold", textColor=colors.black)
    
    if is_single_page:
        cell_12_bold_center = ParagraphStyle("Cell11BC", parent=styles["Normal"], alignment=1, fontSize=10.5, leading=13, fontName="Helvetica-Bold", textColor=colors.black)
        hdr_12_bold_center = ParagraphStyle("Hdr11BC", parent=styles["Normal"], alignment=1, fontSize=10.5, leading=13, fontName="Helvetica-Bold", textColor=colors.black)
        total_14_bold = ParagraphStyle("Total12B", parent=styles["Normal"], alignment=1, fontSize=12, leading=14.5, fontName="Helvetica-Bold", textColor=colors.black)
        words_13_bold_center = ParagraphStyle("Words11.5BC", parent=styles["Normal"], alignment=1, fontSize=11, leading=13.5, fontName="Helvetica-Bold", textColor=colors.black)
        terms_hdr_center = ParagraphStyle("TermsHdr9.5", parent=styles["Normal"], alignment=1, fontSize=9.5, leading=12, fontName="Helvetica-Bold", textColor=colors.black)
        terms_point_size_8 = ParagraphStyle("TermsPt8.5", parent=styles["Normal"], alignment=0, fontSize=8, leading=10, fontName="Helvetica-Bold", textColor=colors.black)
    else:
        cell_12_bold_center = ParagraphStyle("Cell12BC", parent=styles["Normal"], alignment=1, fontSize=11, leading=13.5, fontName="Helvetica-Bold", textColor=colors.black)
        hdr_12_bold_center = ParagraphStyle("Hdr12BC", parent=styles["Normal"], alignment=1, fontSize=11, leading=13.5, fontName="Helvetica-Bold", textColor=colors.black)
        total_14_bold = ParagraphStyle("Total14B", parent=styles["Normal"], alignment=1, fontSize=14, leading=16, fontName="Helvetica-Bold", textColor=colors.black)
        words_13_bold_center = ParagraphStyle("Words13BC", parent=styles["Normal"], alignment=1, fontSize=12, leading=15, fontName="Helvetica-Bold", textColor=colors.black)
        terms_hdr_center = ParagraphStyle("TermsHdr10", parent=styles["Normal"], alignment=1, fontSize=10, leading=14, fontName="Helvetica-Bold", textColor=colors.black)
        terms_point_size_8 = ParagraphStyle("TermsPt8", parent=styles["Normal"], alignment=0, fontSize=8, leading=11, fontName="Helvetica-Bold", textColor=colors.black)

    elements = []

    def create_header_with_qr():
        qr_data = f"CUSTOMER NAME: {customer_name.upper()}\nEXTENSION: {floors_option} ({buildup_sqft} SQFT)\nREF NO: {ref_no}\nDATE: {est_date}\nTOTAL ESTIMATE: Rs. {final_total:,}\nEMAIL: contact@sndinteriors.com"
        qr = QrCodeWidget(qr_data)
        qr_bounds = qr.getBounds()
        w, h = qr_bounds[2] - qr_bounds[0], qr_bounds[3] - qr_bounds[1]
        d = Drawing(60, 60, transform=[60.0/w, 0, 0, 60.0/h, 0, 0])
        d.add(qr)
        
        if include_header:
            header_text_flowables = [
                Paragraph("SND INTERIOR & DESIGNS", title_style), Spacer(1, 2),
                Paragraph("STRUCTURAL CIVIL WORKS, FLOOR EXTENSIONS & BUILDING ESTIMATES", sub_style),
                Paragraph("#15, E BLOCK, SAHAKHAR NAGAR, BANGALORE-560092", sub_style),
                Paragraph("EMAIL: contact@sndinteriors.com", contact_style),
                Paragraph("GSTIN: 29ABCDE1234F1Z5", gstin_style),
            ]
        else:
            header_text_flowables = [
                Spacer(1, 10), Spacer(1, 10), Spacer(1, 10), Spacer(1, 10), Spacer(1, 10)
            ]
        header_table = Table([["", header_text_flowables, d]], colWidths=[65, 405, 65])
        header_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0)]))
        return [header_table, Spacer(1, 4)]

    elements.extend(create_header_with_qr())
    elements.append(Table([[Paragraph(f"REF NO:-{ref_no}", ref_left_style), Paragraph(f"DATE: {est_date}", ref_right_style)]], colWidths=[265, 270]))
    elements.append(Spacer(1, 4))

    address_parts = [p.strip() for p in address.split(',')]
    mid_idx = len(address_parts) // 2
    addr_line_1 = ", ".join(address_parts[:mid_idx]) if mid_idx > 0 else address
    addr_line_2 = ", ".join(address_parts[mid_idx:]) if mid_idx > 0 else ""

    box_content = [
        [Paragraph(f"CIVIL CONSTRUCTION & STRUCTURAL EXTENSION ESTIMATE FOR", box_hdr_style)], 
        [Paragraph(f"ADDITION OF {floors_option.upper()} ({buildup_sqft} SQ. FT) AT", box_hdr_style)], 
        [Paragraph(addr_line_1.upper(), box_detail_style)]
    ]
    if addr_line_2: box_content.append([Paragraph(addr_line_2.upper(), box_detail_style)])
    box_content.append([Paragraph(f"PROPERTY OWNER: - {customer_name.upper()}", box_detail_style)])

    project_box = Table(box_content, colWidths=[535])
    project_box.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 2, BORDER_BLUE), ('ROUNDEDCORNERS', [8, 8, 8, 8]), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    elements.append(project_box)
    elements.append(Spacer(1, 6))

    if is_single_page:
        p_table_data = [[Paragraph("SL.NO", hdr_12_bold_center), Paragraph("Civil Work Description", hdr_12_bold_center), Paragraph("Qty / Area", hdr_12_bold_center), Paragraph("Amount Rs.", hdr_12_bold_center)]]
        for idx in range(10):
            item = processed_items[idx]
            p_table_data.append([Paragraph(f"{idx+1}.", cell_12_bold_center), Paragraph(item[0], cell_12_bold_center), Paragraph(item[1], cell_12_bold_center), Paragraph(f"{item_amounts[idx]:,}", cell_12_bold_center)])
        p_table_data.append(["", Paragraph("GST 18%", total_14_bold), "", Paragraph(f"{actual_gst:,}", total_14_bold)])
        p_table_data.append(["", Paragraph("TOTAL", total_14_bold), "", Paragraph(f"{final_total:,}", total_14_bold)])

        t1 = Table(p_table_data, colWidths=[45, 270, 100, 120])
        t1.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.black), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6)]))
        elements.append(t1)
    else:
        p1_table_data = [[Paragraph("SL.NO", hdr_12_bold_center), Paragraph("Civil Work Description", hdr_12_bold_center), Paragraph("Qty / Area", hdr_12_bold_center), Paragraph("Amount Rs.", hdr_12_bold_center)]]
        for idx in range(9):
            item = processed_items[idx]
            p1_table_data.append([Paragraph(f"{idx+1}.", cell_12_bold_center), Paragraph(item[0], cell_12_bold_center), Paragraph(item[1], cell_12_bold_center), Paragraph(f"{item_amounts[idx]:,}", cell_12_bold_center)])
        
        t1 = Table(p1_table_data, colWidths=[45, 270, 100, 120])
        t1.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.black), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 14), ('BOTTOMPADDING', (0,0), (-1,-1), 14)]))
        elements.append(t1)

        elements.append(PageBreak())
        elements.extend(create_header_with_qr())
        elements.append(Table([[Paragraph(f"REF NO:-{ref_no}", ref_left_style), Paragraph(f"DATE: {est_date}", ref_right_style)]], colWidths=[265, 270]))
        elements.append(Spacer(1, 4))

        p2_table_data = [[Paragraph("SL.NO", hdr_12_bold_center), Paragraph("Civil Work Description", hdr_12_bold_center), Paragraph("Qty / Area", hdr_12_bold_center), Paragraph("Amount Rs.", hdr_12_bold_center)]]
        for idx in range(9, 15):
            item = processed_items[idx]
            p2_table_data.append([Paragraph(f"{idx+1}.", cell_12_bold_center), Paragraph(item[0], cell_12_bold_center), Paragraph(item[1], cell_12_bold_center), Paragraph(f"{item_amounts[idx]:,}", cell_12_bold_center)])

        p2_table_data.append(["", Paragraph("GST 18%", total_14_bold), "", Paragraph(f"{actual_gst:,}", total_14_bold)])
        p2_table_data.append(["", Paragraph("TOTAL", total_14_bold), "", Paragraph(f"{final_total:,}", total_14_bold)])

        t2 = Table(p2_table_data, colWidths=[45, 270, 100, 120])
        t2.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.black), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 14), ('BOTTOMPADDING', (0,0), (-1,-1), 14)]))
        elements.append(t2)

    elements.append(Spacer(1, 6))
    elements.append(Paragraph(num_to_words_indian_clean(final_total), words_13_bold_center))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph("TERMS AND CONDITIONS FOR CIVIL & STRUCTURAL WORKS:", terms_hdr_center))
    elements.append(Spacer(1, 3))

    terms_points = [
        "1. This Is A Preliminary Civil Estimate Based On Buildup Area And Structural Requirements.",
        "2. Payment Schedule: 30% Advance, 30% Upon Slab Casting, 30% Masonry & Plastering, 10% Handover.",
        "3. Validity: This Estimate Is Valid For 30 Days From The Date Of Issue Due To Steel/Cement Price Fluctuations.",
        "4. Structural Responsibility: Existing Foundation Load-Bearing Capacity Must Be Verified Prior to Work.",
        "5. Material Standards: Fe550 Grade TMT Steel and OPC/PPC Cement will be utilized as per specifications.",
        "6. Project Duration: Estimated Structural Completion Time Is 120 Working Days From Advance Receipt."
    ]
    for point in terms_points:
        elements.append(Paragraph(point, terms_point_size_8))
        elements.append(Spacer(1, 2))

    doc.build(elements)
    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()

    return pdf_bytes, filename, ref_no, final_total


# --- AUTHENTIC MODAL POPUP DIALOG FOR CIVIL ESTIMATION ---
@st.dialog("🏗️ CIVIL CONSTRUCTION & FLOOR EXTENSION ESTIMATOR", width="large")
def show_quotation_dialog():
    st.markdown("""
    <div class="commercial-auth-banner">
        <div style="font-size:2.2rem;">🔐</div>
        <div>
            <div style="color:#818CF8; font-weight:700; font-size:0.85rem; letter-spacing:1px;">SECURE SSL GATEWAY • CIVIL STRUCTURAL INVOICING</div>
            <div style="color:#FFFFFF; font-size:0.8rem;">Generate encrypted civil estimation PDFs for building upper floor extensions in Bengaluru.</div>
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
        st.subheader("🏠 Property & Extension Floor Options")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            customer_name = st.text_input("Customer Full Name *", value="", placeholder="Customer name")
            floors_option = st.selectbox(
                "Select Floors to Add *",
                ["2nd Floor Only", "2nd & 3rd Floors", "3rd Floor Only", "1st, 2nd & 3rd Floors", "Custom Multi-Floor Extension"]
            )
        with col_c2:
            date_input = st.text_input("Quotation Date", value=datetime.now().strftime("%d-%m-%Y"))
            buildup_sqft = st.number_input(
                "📐 Buildup Area (SQ. FT) *",
                min_value=100.0,
                max_value=10000.0,
                value=1200.0,
                step=50.0,
                format="%.2f"
            )

        address_input = st.text_area(
            "Site / Building Address *", 
            value="",
            placeholder="Enter complete site address"
        )

        st.markdown("---")
        st.subheader("💰 CIVIL WORKS BUDGET")
        
        amount_input = st.number_input(
            "✏️ Enter Total Estimated Civil Budget (INR ₹):",
            min_value=100000.0,
            max_value=20000000.0,
            value=2500000.0,
            step=50000.0,
            format="%.2f"
        )

        subtotal_est = round(amount_input / 1.18)
        gst_est = amount_input - subtotal_est
        st.info(f"📊 **Base Civil Estimate:** ₹ {subtotal_est:,.2f} | **GST (18%):** ₹ {gst_est:,.2f} | **Total Final Payable:** ₹ {amount_input:,.2f}")

        submitted = st.form_submit_button("⚡ GENERATE CIVIL ESTIMATE", type="primary", use_container_width=True)

    if submitted:
        if not user_name.strip() or not user_mobile.strip() or not user_email.strip() or not customer_name.strip() or not address_input.strip():
            st.warning("⚠️ Please fill in all required fields before generating the quotation.")
            return

        with st.spinner('Generating PDF copies and syncing securely with cloud storage...'):
            try:
                pdf_bytes_std, filename_std, generated_ref, final_total = generate_estimation_pdf_bytes(
                    customer_name, address_input, date_input, float(amount_input), floors_option, float(buildup_sqft), include_header=True
                )
                pdf_bytes_no_hdr, filename_no_hdr, _, _ = generate_estimation_pdf_bytes(
                    customer_name, address_input, date_input, float(amount_input), floors_option, float(buildup_sqft), include_header=False
                )
                
                if supabase:
                    upload_to_cloud(
                        generated_ref, pdf_bytes_std, pdf_bytes_no_hdr, 
                        filename_std, filename_no_hdr, user_name, user_mobile, user_email, 
                        customer_name, date_input, final_total
                    )
                
                st.balloons()
                st.success("🎉 **Civil Quotation Generated & Synced Successfully!**")
                
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
        <div><span class="live-dot"></span>LIVE CIVIL HUB: BENGALURU (SAHAKARNAGAR | HSR | WHITEFIELD)</div>
        <div>SUPPORT HOTLINE: +91 98765 43210 &nbsp;|&nbsp; SLA: 99.9% UPTIME</div>
    </div>
    """, unsafe_allow_html=True)
with col_tick2:
    if st.button("🔐", help="Enterprise Admin Portal Login"):
        show_admin_dialog()

# --- TOP GET YOUR QUOTATION NOW BUTTON ---
col_top_btn1, col_top_btn2, col_top_btn3 = st.columns([2, 2, 2])
with col_top_btn2:
    if st.button("⚡ GET YOUR QUOTATION NOW ", type="primary", use_container_width=True):
        show_quotation_dialog()

st.markdown("<br>", unsafe_allow_html=True)


# --- 3D GRADIENT HERO SECTION WITH CAROUSEL ---
col_hero1, col_hero2 = st.columns([1.2, 1])

with col_hero1:
    st.markdown("""
    <div class="dashboard-card-3d" style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.85) 100%); padding: 3rem 2.5rem; height: 100%;">
        <div style="font-family:'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.85rem; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 12px;">
            <span class="gradient-text-gold">✦ STRUCTURAL CIVIL & FLOOR EXTENSION </span>
        </div>
        <h1 class="hero-title-3d" style="font-size: 3rem;">SND INTERIOR & DESIGNS</h1>
        <p style="color: #CBD5E1; font-size: 1.1rem; line-height: 1.7; margin-bottom: 2rem;">
            Professional civil construction, floor additions (2nd and 3rd floors), structural framework engineering, GST quotations, and turnkey building execution across Bengaluru.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_hero2:
    st.markdown("""
    <div class="slider-box" id="interiorCarousel">
        <div class="carousel-slide active">
            <img src="https://images.unsplash.com/photo-1541888946425-d0fbb18f7292?auto=format&fit=crop&w=1000&q=80" alt="Civil Construction">
            <div class="carousel-caption">01 - Structural Floor Extension & Column Casting</div>
        </div>
        <div class="carousel-slide">
            <img src="https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1000&q=80" alt="Building Blueprint">
            <div class="carousel-caption">02 - Architectural Planning & Structural Design</div>
        </div>
        <div class="carousel-slide">
            <img src="https://images.unsplash.com/photo-1590381105924-c72589b9ef3f?auto=format&fit=crop&w=1000&q=80" alt="RCC Slab">
            <div class="carousel-caption">03 - RCC Roof Slab Casting & Reinforcement</div>
        </div>
        <div class="carousel-slide">
            <img src="https://images.unsplash.com/photo-1581094288338-2314dddb7ece?auto=format&fit=crop&w=1000&q=80" alt="Brick Masonry">
            <div class="carousel-caption">04 - External & Internal Brick Masonry Walls</div>
        </div>
        <div class="carousel-slide">
            <img src="https://images.unsplash.com/photo-1517581177682-a085bb7ffb15?auto=format&fit=crop&w=1000&q=80" alt="Scaffolding">
            <div class="carousel-caption">05 - Multi-Floor Scaffolding & Safety Works</div>
        </div>
        <div class="carousel-slide">
            <img src="https://images.unsplash.com/photo-1541971875076-8f970d573be6?auto=format&fit=crop&w=1000&q=80" alt="Concrete Plastering">
            <div class="carousel-caption">06 - Structural Plastering & Wall Finishing</div>
        </div>
        <div class="carousel-slide">
            <img src="https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=1000&q=80" alt="Electrical Plumbing">
            <div class="carousel-caption">07 - Concealed Conduit & Plumbing Rough-in</div>
        </div>
        <div class="carousel-slide">
            <img src="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1000&q=80" alt="Finished Exterior">
            <div class="carousel-caption">08 - Multi-Storey Building Elevation Handover</div>
        </div>
        <div class="carousel-slide">
            <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1000&q=80" alt="Terrace Waterproofing">
            <div class="carousel-caption">09 - Terrace Waterproofing & Parapet Walls</div>
        </div>
        <div class="carousel-slide">
            <img src="https://images.unsplash.com/photo-1590069261209-f8e9b8642343?auto=format&fit=crop&w=1000&q=80" alt="Foundation Works">
            <div class="carousel-caption">10 - Foundation & Column Starter Reinforcement</div>
        </div>
    </div>

    <script>
        let slideIndex = 0;
        const allSlides = document.querySelectorAll('#interiorCarousel .carousel-slide');
        function cycleSlides() {
            if(allSlides.length === 0) return;
            allSlides[slideIndex].classList.remove('active');
            slideIndex = (slideIndex + 1) % allSlides.length;
            allSlides[slideIndex].classList.add('active');
        }
        setInterval(cycleSlides, 3500);
    </script>
    """, unsafe_allow_html=True)


# --- STATIC & FIXED 10 IMAGES GALLERY SHOWCASE ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🏛️ Civil Construction Master Collection (10 Fixed Showcase Galleries)")
st.markdown("<p style='color:#94A3B8; font-size:0.95rem; margin-bottom:1rem;'>Explore our curated permanent catalog of structural frames, slab casting, and multi-floor building extensions.</p>", unsafe_allow_html=True)

st.markdown("""
<div class="static-gallery-grid">
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1541888946425-d0fbb18f7292?auto=format&fit=crop&w=600&q=80" alt="Extension">
        <div class="static-gallery-label">01. Floor Extension</div>
    </div>
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=600&q=80" alt="Blueprint">
        <div class="static-gallery-label">02. Structural Plan</div>
    </div>
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1590381105924-c72589b9ef3f?auto=format&fit=crop&w=600&q=80" alt="RCC Slab">
        <div class="static-gallery-label">03. RCC Slab Casting</div>
    </div>
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1581094288338-2314dddb7ece?auto=format&fit=crop&w=600&q=80" alt="Masonry">
        <div class="static-gallery-label">04. Brick Masonry</div>
    </div>
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1517581177682-a085bb7ffb15?auto=format&fit=crop&w=600&q=80" alt="Scaffolding">
        <div class="static-gallery-label">05. Safety Scaffolding</div>
    </div>
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1541971875076-8f970d573be6?auto=format&fit=crop&w=600&q=80" alt="Plastering">
        <div class="static-gallery-label">06. Wall Plastering</div>
    </div>
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=600&q=80" alt="Conduits">
        <div class="static-gallery-label">07. Electrical/Plumbing</div>
    </div>
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=600&q=80" alt="Elevation">
        <div class="static-gallery-label">08. Building Handover</div>
    </div>
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80" alt="Waterproofing">
        <div class="static-gallery-label">09. Waterproofing</div>
    </div>
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1590069261209-f8e9b8642343?auto=format&fit=crop&w=600&q=80" alt="Foundation">
        <div class="static-gallery-label">10. Column Starter</div>
    </div>
</div>
""", unsafe_allow_html=True)


# --- FULL-SIZE VERTICAL SCROLLING SHOWCASE (10 FULL SIZE IMAGES) ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📸 10 Full-Size Vertical Civil Construction Showcase")
st.markdown("<p style='color:#94A3B8; font-size:0.95rem; margin-bottom:1.5rem;'>Scroll down through our 10 full-width, high-definition structural and floor extension project features.</p>", unsafe_allow_html=True)

st.markdown("""
<div class="vertical-gallery-container">
    <!-- 01 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1541888946425-d0fbb18f7292?auto=format&fit=crop&w=1600&q=80" alt="Civil Construction">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Full Size Feature • 01</span>
            <div class="vertical-card-title">Structural Floor Extension & Column Starter Casting</div>
            <div class="vertical-card-desc">Strengthening existing footings, chemical anchoring of rebar, and precision column extensions for upper 2nd & 3rd floors.</div>
        </div>
    </div>
    <!-- 02 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1600&q=80" alt="Blueprint">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Full Size Feature • 02</span>
            <div class="vertical-card-title">Architectural Planning & Load Calculation</div>
            <div class="vertical-card-desc">Comprehensive structural stability analysis, BBMP compliance drafting, and exact material takeoff for vertical additions.</div>
        </div>
    </div>
    <!-- 03 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1590381105924-c72589b9ef3f?auto=format&fit=crop&w=1600&q=80" alt="RCC Slab">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Full Size Feature • 03</span>
            <div class="vertical-card-title">M25 Grade RCC Roof Slab Casting & Shuttering</div>
            <div class="vertical-card-desc">Heavy-duty centering, Fe550 grade steel grid reinforcement, and mechanized pump concrete pouring for superior slab strength.</div>
        </div>
    </div>
    <!-- 04 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1581094288338-2314dddb7ece?auto=format&fit=crop&w=1600&q=80" alt="Brickwork">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Full Size Feature • 04</span>
            <div class="vertical-card-title">AAC Block & Red Brick Masonry Partition Walls</div>
            <div class="vertical-card-desc">Precision wall alignment, damp-proof course integration, and sturdy lintel beam support over all door and window openings.</div>
        </div>
    </div>
    <!-- 05 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1517581177682-a085bb7ffb15?auto=format&fit=crop&w=1600&q=80" alt="Scaffolding">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Full Size Feature • 05</span>
            <div class="vertical-card-title">External Scaffolding & Multi-Storey Safety Systems</div>
            <div class="vertical-card-desc">Industrial steel scaffolding structures, safety debris netting, and harness compliance for secure upper-level execution.</div>
        </div>
    </div>
    <!-- 06 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1541971875076-8f970d573be6?auto=format&fit=crop&w=1600&q=80" alt="Plastering">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Full Size Feature • 06</span>
            <div class="vertical-card-title">Internal & External Structural Wall Plastering</div>
            <div class="vertical-card-desc">Double-coat cement mortar plastering with chicken mesh reinforcement at column junctions to prevent structural cracking.</div>
        </div>
    </div>
    <!-- 07 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=1600&q=80" alt="Conduits">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Full Size Feature • 07</span>
            <div class="vertical-card-title">Concealed Electrical Piping & Plumbing Rough-Ins</div>
            <div class="vertical-card-desc">Heavy-gauge FR PVC conduit laying in slabs/walls and CPVC/UPVC water supply line networking for bathrooms and kitchens.</div>
        </div>
    </div>
    <!-- 08 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1600&q=80" alt="Handover">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Full Size Feature • 08</span>
            <div class="vertical-card-title">Completed Multi-Storey Building Elevation Handover</div>
            <div class="vertical-card-desc">Fully cured structural extension ready for interior finishing, painting, flooring, and final client occupancy inspection.</div>
        </div>
    </div>
    <!-- 09 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1600&q=80" alt="Waterproofing">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Full Size Feature • 09</span>
            <div class="vertical-card-title">Terrace Waterproofing & Parapet Wall Construction</div>
            <div class="vertical-card-desc">Multi-layer polymer chemical waterproofing membrane for terrace slabs and solid brick parapet boundary walls.</div>
        </div>
    </div>
    <!-- 10 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1590069261209-f8e9b8642343?auto=format&fit=crop&w=1600&q=80" alt="Foundation">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Full Size Feature • 10</span>
            <div class="vertical-card-title">Foundation & Column Starter Reinforcement Checks</div>
            <div class="vertical-card-desc">Rigorous non-destructive testing (NDT) and rebar tensile verification before initiating upper floor load additions.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# --- Commercial Metrics Grid ---
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.markdown("""
    <div class="stat-box-commercial">
        <div style="font-size: 1.8rem; font-weight: 800;" class="gradient-text-gold">350+</div>
        <div style="font-size: 0.8rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; margin-top: 5px;">Floor Extensions</div>
    </div>
    """, unsafe_allow_html=True)
with col_m2:
    st.markdown("""
    <div class="stat-box-commercial">
        <div style="font-size: 1.8rem; font-weight: 800;" class="gradient-text-cyan">15 YRS</div>
        <div style="font-size: 0.8rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; margin-top: 5px;">Structural Guarantee</div>
    </div>
    """, unsafe_allow_html=True)
with col_m3:
    st.markdown("""
    <div class="stat-box-commercial">
        <div style="font-size: 1.8rem; font-weight: 800;" class="gradient-text-gold">120 DAYS</div>
        <div style="font-size: 0.8rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; margin-top: 5px;">Slab & Frame Handover</div>
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
st.markdown("### 🌀 Interactive Civil Simulation Modules")
st.markdown("<p style='color:#94A3B8; font-size:0.95rem; margin-bottom:1.5rem;'>Select a civil construction stage to inspect structural engineering specifications and load-bearing parameters.</p>", unsafe_allow_html=True)

selected_room = st.radio(
    "Select Simulation Zone:",
    ["🏗️ Column & Foundation Extension", "🧱 RCC Slab & Beam Casting", "🧱 Brick Masonry & AAC Blocks", "🌧️ Terrace Waterproofing", "🔌 Electrical & Plumbing Rough-In"],
    horizontal=True,
    label_visibility="collapsed"
)

if "Column" in selected_room:
    st.markdown("""
    <div class="dashboard-card-3d" style="display:flex; gap:35px; align-items:center;">
        <div style="flex:1;">
            <div style="font-family:'Space Grotesk', sans-serif; font-weight:800; font-size:0.8rem; letter-spacing:2px; color:#F59E0B; text-transform:uppercase;">CIVIL MODULE 01</div>
            <h2 style="font-family:'Outfit', sans-serif; font-size:2.2rem; font-weight:800; color:#FFF; margin:10px 0 15px 0;">Column & Foundation Extension</h2>
            <p style="color:#CBD5E1; line-height:1.7; margin-bottom:1.5rem;">
                Chemical anchoring of high-tensile rebar into existing foundation footings, chipping old column starters, and extending structural pillars to support upper 2nd and 3rd floors safely.
            </p>
            <div style="display:flex; gap:15px; color:#38BDF8; font-weight:700; font-size:0.9rem;">
                <div>⚡ Fe550 Steel Rebar</div>
                <div>⚡ Chemical Anchoring</div>
                <div>⚡ NDT Verified</div>
            </div>
        </div>
        <div style="flex:1;">
            <div class="visualizer-frame-3d">
                <img src="https://images.unsplash.com/photo-1541888946425-d0fbb18f7292?auto=format&fit=crop&w=1000&q=80" alt="Column Extension">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
elif "Slab" in selected_room:
    st.markdown("""
    <div class="dashboard-card-3d" style="display:flex; gap:35px; align-items:center;">
        <div style="flex:1;">
            <div style="font-family:'Space Grotesk', sans-serif; font-weight:800; font-size:0.8rem; letter-spacing:2px; color:#F59E0B; text-transform:uppercase;">CIVIL MODULE 02</div>
            <h2 style="font-family:'Outfit', sans-serif; font-size:2.2rem; font-weight:800; color:#FFF; margin:10px 0 15px 0;">RCC Roof Slab & Beam Casting</h2>
            <p style="color:#CBD5E1; line-height:1.7; margin-bottom:1.5rem;">
                Heavy-duty scaffolding centering, double-mesh steel reinforcement laying, and M25 grade mechanized pump concrete pouring to ensure robust roof slab integrity.
            </p>
            <div style="display:flex; gap:15px; color:#38BDF8; font-weight:700; font-size:0.9rem;">
                <div>⚡ M25 Grade Concrete</div>
                <div>⚡ Double-Mesh Grid</div>
                <div>⚡ Mechanized Pumping</div>
            </div>
        </div>
        <div style="flex:1;">
            <div class="visualizer-frame-3d">
                <img src="https://images.unsplash.com/photo-1590381105924-c72589b9ef3f?auto=format&fit=crop&w=1000&q=80" alt="Slab Casting">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
elif "Brick" in selected_room:
    st.markdown("""
    <div class="dashboard-card-3d" style="display:flex; gap:35px; align-items:center;">
        <div style="flex:1;">
            <div style="font-family:'Space Grotesk', sans-serif; font-weight:800; font-size:0.8rem; letter-spacing:2px; color:#F59E0B; text-transform:uppercase;">CIVIL MODULE 03</div>
            <h2 style="font-family:'Outfit', sans-serif; font-size:2.2rem; font-weight:800; color:#FFF; margin:10px 0 15px 0;">Brick Masonry & AAC Blocks</h2>
            <p style="color:#CBD5E1; line-height:1.7; margin-bottom:1.5rem;">
                Precision outer and inner wall construction using high-density AAC blocks or first-quality wire-cut red bricks with damp-proof course (DPC) layers.
            </p>
            <div style="display:flex; gap:15px; color:#38BDF8; font-weight:700; font-size:0.9rem;">
                <div>⚡ AAC / Red Bricks</div>
                <div>⚡ DPC Protected</div>
                <div>⚡ Plumb Alignment</div>
            </div>
        </div>
        <div style="flex:1;">
            <div class="visualizer-frame-3d">
                <img src="https://images.unsplash.com/photo-1581094288338-2314dddb7ece?auto=format&fit=crop&w=1000&q=80" alt="Masonry">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
elif "Waterproofing" in selected_room:
    st.markdown("""
    <div class="dashboard-card-3d" style="display:flex; gap:35px; align-items:center;">
        <div style="flex:1;">
            <div style="font-family:'Space Grotesk', sans-serif; font-weight:800; font-size:0.8rem; letter-spacing:2px; color:#F59E0B; text-transform:uppercase;">CIVIL MODULE 04</div>
            <h2 style="font-family:'Outfit', sans-serif; font-size:2.2rem; font-weight:800; color:#FFF; margin:10px 0 15px 0;">Terrace Waterproofing & Parapet</h2>
            <p style="color:#CBD5E1; line-height:1.7; margin-bottom:1.5rem;">
                Multi-layer polymer chemical waterproofing membrane applied on terrace roofs with brick-bat coba slope grading and solid parapet boundary walls.
            </p>
            <div style="display:flex; gap:15px; color:#38BDF8; font-weight:700; font-size:0.9rem;">
                <div>⚡ Polymer Membrane</div>
                <div>⚡ Brick-Bat Coba</div>
                <div>⚡ Leak-Proof Guarantee</div>
            </div>
        </div>
        <div style="flex:1;">
            <div class="visualizer-frame-3d">
                <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1000&q=80" alt="Waterproofing">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="dashboard-card-3d" style="display:flex; gap:35px; align-items:center;">
        <div style="flex:1;">
            <div style="font-family:'Space Grotesk', sans-serif; font-weight:800; font-size:0.8rem; letter-spacing:2px; color:#F59E0B; text-transform:uppercase;">CIVIL MODULE 05</div>
            <h2 style="font-family:'Outfit', sans-serif; font-size:2.2rem; font-weight:800; color:#FFF; margin:10px 0 15px 0;">Electrical & Plumbing Rough-In</h2>
            <p style="color:#CBD5E1; line-height:1.7; margin-bottom:1.5rem;">
                Concealed heavy-gauge FR PVC conduit pipe laying in columns/slabs and CPVC/UPVC water supply network installation prior to wall plastering.
            </p>
            <div style="display:flex; gap:15px; color:#38BDF8; font-weight:700; font-size:0.9rem;">
                <div>⚡ FR PVC Conduits</div>
                <div>⚡ CPVC Water Lines</div>
                <div>⚡ Pressure Tested</div>
            </div>
        </div>
        <div style="flex:1;">
            <div class="visualizer-frame-3d">
                <img src="https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=1000&q=80" alt="Conduits">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# --- MAIN ACTION BUTTON ---
st.markdown("<br>", unsafe_allow_html=True)
col_cta1, col_cta2, col_cta3 = st.columns([1, 2, 1])
with col_cta2:
    if st.button("⚡ GET YOUR QUOTATION ", type="primary", use_container_width=True):
        show_quotation_dialog()
