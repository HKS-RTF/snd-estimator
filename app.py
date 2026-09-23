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
    page_title="SND Interior & Designs | Building Floor Plans & Civil Works Dashboard",
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


def generate_estimation_pdf_bytes(customer_name, address, est_date, target_total, builtin_area, selected_floors, include_header=True):
    # Master list of exactly 35 Civil & Building Floor Plan particulars
    CIVIL_PARTICULARS_MASTER = [
        ("Site clearing, excavation, and earthwork in foundation", "CU. M", 0.025),
        ("PCC bed (1:4:8) for foundation footings and base", "SQ. FT", 0.025),
        ("Reinforced cement concrete (RCC 1:1.5:3) for footings", "CU. M", 0.040),
        ("RCC columns, pedestals, and vertical ties casting", "CU. M", 0.045),
        ("RCC plinth beams and damp proof course (DPC)", "R. FT", 0.030),
        ("Granite/Stone masonry work for foundation basement", "CU. M", 0.035),
        ("Backfilling with approved soil and compaction", "CU. M", 0.020),
        ("Anti-termite soil treatment pre-construction stage", "SQ. FT", 0.015),
        ("RCC columns above plinth up to roof level", "CU. M", 0.045),
        ("RCC beam and lintel casting across all bays", "CU. M", 0.040),
        ("RCC slab casting (1st Roof Slab & Shuttering)", "SQ. FT", 0.050),
        ("RCC staircase construction with landing steps", "SQ. FT", 0.025),
        ("External wall masonry with solid concrete blocks", "SQ. FT", 0.045),
        ("Internal partition walls with solid blocks/bricks", "SQ. FT", 0.035),
        ("Internal wall plastering (single coat smooth finish)", "SQ. FT", 0.030),
        ("External wall plastering (weatherproof double coat)", "SQ. FT", 0.035),
        ("Ceiling plastering and architectural finishes", "SQ. FT", 0.025),
        ("Underground sump tank construction (RCC watertight)", "LITERS", 0.030),
        ("Overhead water tank erection (Sintex/RCC structure)", "LITERS", 0.020),
        ("Main entrance teak wood door frame and shutter", "UNIT", 0.025),
        ("Internal flush doors with laminate and hardware", "UNIT", 0.030),
        ("UPVC/Aluminium glazed windows with mosquito mesh", "SQ. FT", 0.030),
        ("Vrified tile flooring and skirting installation", "SQ. FT", 0.040),
        ("Bathroom ceramic wall tiling up to 7ft height", "SQ. FT", 0.030),
        ("Anti-skid floor tiles for bathrooms and balconies", "SQ. FT", 0.025),
        ("Granite slab for kitchen counter top and dado", "R. FT", 0.025),
        ("Sanitary fixtures (EWC, wash basins, diverters)", "SETS", 0.030),
        ("CP fittings, shower arms, and sink faucets", "SETS", 0.025),
        ("Electrical conduit pipe laying (walls and ceiling)", "POINT", 0.025),
        ("Wiring, DB box, MCBs, and switches installation", "POINT", 0.035),
        ("Plumbing supply and drainage PVC pipe networks", "JOB", 0.030),
        ("Internal wall putty (2 coats) and primer application", "SQ. FT", 0.030),
        ("Internal painting with premium emulsion paint", "SQ. FT", 0.025),
        ("External weather shield painting and texture finish", "SQ. FT", 0.030),
        ("Compound wall construction and MS safety gate", "R. FT", 0.030)
    ]

    # Subtotal targeting from user budget
    subtotal_target = target_total / 1.18
    
    # Weight distribution across 35 items
    raw_weights = [item[2] * random.uniform(0.9, 1.1) for item in CIVIL_PARTICULARS_MASTER]
    total_w = sum(raw_weights)
    norm_weights = [w / total_w for w in raw_weights]
    
    item_amounts = [round(subtotal_target * w) for w in norm_weights]
    item_amounts[-1] += round(subtotal_target) - sum(item_amounts)

    processed_items = []
    floor_multiplier = max(1, len(selected_floors))
    
    for idx, (desc, unit_type, _) in enumerate(CIVIL_PARTICULARS_MASTER):
        total_amt = item_amounts[idx]
        if unit_type in ["SQ. FT", "R. FT"]:
            qty = round(builtin_area * random.uniform(0.15, 0.35) * floor_multiplier)
            qty = max(1, qty)
        elif unit_type in ["CU. M"]:
            qty = round(builtin_area * 0.08 * floor_multiplier, 1)
            qty = max(0.5, qty)
        elif unit_type in ["UNIT", "SETS", "POINT"]:
            qty = round(random.uniform(4, 16) * floor_multiplier)
            qty = max(1, qty)
        else:
            qty = floor_multiplier
            
        rate = round(total_amt / qty, 2) if qty > 0 else total_amt
        processed_items.append((desc, unit_type, qty, rate, total_amt))

    actual_subtotal = sum(item[4] for item in processed_items)
    actual_gst = round(actual_subtotal * 0.18)
    final_total = actual_subtotal + actual_gst

    now = datetime.now()
    ref_no = now.strftime("%H%M%d%m%Y")
    clean_customer_name = customer_name.replace(' ', '_').replace('&', 'AND')
    filename = f"BuildingEstimation_{ref_no}_{clean_customer_name}{'_NoHeader' if not include_header else ''}.pdf"

    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=25, leftMargin=25, topMargin=15, bottomMargin=15)
    styles = getSampleStyleSheet()

    RED_COLOR, BLUE_COLOR, LIGHT_PINK, BORDER_BLUE = colors.HexColor("#DC2626"), colors.HexColor("#1E40AF"), colors.HexColor("#EC4899"), colors.HexColor("#2563EB")

    title_style = ParagraphStyle("Title", parent=styles["Heading1"], alignment=1, fontSize=26, leading=30, fontName="Helvetica-Bold", textColor=RED_COLOR)
    sub_style = ParagraphStyle("Sub", parent=styles["Normal"], alignment=1, fontSize=8.5, leading=11, fontName="Helvetica-Bold", textColor=BLUE_COLOR)
    contact_style = ParagraphStyle("Contact", parent=styles["Normal"], alignment=1, fontSize=8, leading=10, fontName="Helvetica-Bold", textColor=BLUE_COLOR)
    gstin_style = ParagraphStyle("GSTIN", parent=styles["Normal"], alignment=1, fontSize=8.5, leading=11, fontName="Helvetica-Bold", textColor=LIGHT_PINK)
    ref_left_style = ParagraphStyle("RefLeft", parent=styles["Normal"], alignment=0, fontSize=9.5, leading=12, fontName="Helvetica")
    ref_right_style = ParagraphStyle("RefRight", parent=styles["Normal"], alignment=2, fontSize=9.5, leading=12, fontName="Helvetica")
    box_hdr_style = ParagraphStyle("BoxHdr", parent=styles["Normal"], alignment=1, fontSize=12, leading=14, fontName="Helvetica-Bold", textColor=colors.black)
    box_detail_style = ParagraphStyle("BoxDetail", parent=styles["Normal"], alignment=1, fontSize=11, leading=13.5, fontName="Helvetica-Bold", textColor=colors.black)
    
    cell_style = ParagraphStyle("Cell", parent=styles["Normal"], alignment=0, fontSize=8.5, leading=11, fontName="Helvetica", textColor=colors.black)
    cell_center = ParagraphStyle("CellC", parent=styles["Normal"], alignment=1, fontSize=8.5, leading=11, fontName="Helvetica", textColor=colors.black)
    cell_right = ParagraphStyle("CellR", parent=styles["Normal"], alignment=2, fontSize=8.5, leading=11, fontName="Helvetica", textColor=colors.black)
    
    hdr_style = ParagraphStyle("Hdr", parent=styles["Normal"], alignment=1, fontSize=9, leading=11, fontName="Helvetica-Bold", textColor=colors.black)
    total_style = ParagraphStyle("Tot", parent=styles["Normal"], alignment=2, fontSize=10, leading=12, fontName="Helvetica-Bold", textColor=colors.black)
    total_val_style = ParagraphStyle("TotV", parent=styles["Normal"], alignment=2, fontSize=10, leading=12, fontName="Helvetica-Bold", textColor=colors.black)
    words_style = ParagraphStyle("Words", parent=styles["Normal"], alignment=1, fontSize=10, leading=13, fontName="Helvetica-Bold", textColor=colors.black)
    terms_hdr = ParagraphStyle("TermH", parent=styles["Normal"], alignment=1, fontSize=9, leading=11, fontName="Helvetica-Bold", textColor=colors.black)
    terms_pt = ParagraphStyle("TermP", parent=styles["Normal"], alignment=0, fontSize=7.5, leading=9.5, fontName="Helvetica-Bold", textColor=colors.black)

    elements = []

    def create_header_with_qr():
        qr_data = f"CUSTOMER: {customer_name.upper()}\nAREA: {builtin_area} SQFT\nFLOORS: {', '.join(selected_floors)}\nREF: {ref_no}\nTOTAL: Rs. {final_total:,}"
        qr = QrCodeWidget(qr_data)
        qr_bounds = qr.getBounds()
        w, h = qr_bounds[2] - qr_bounds[0], qr_bounds[3] - qr_bounds[1]
        d = Drawing(55, 55, transform=[55.0/w, 0, 0, 55.0/h, 0, 0])
        d.add(qr)
        
        if include_header:
            header_text_flowables = [
                Paragraph("SND INTERIOR & DESIGNS", title_style), Spacer(1, 2),
                Paragraph("BUILDING FLOOR PLANS, CIVIL WORKS, STRUCTURAL & TURNKEY CONSTRUCTION", sub_style),
                Paragraph("#15, E BLOCK, SAHAKAR NAGAR, BANGALORE-560092", sub_style),
                Paragraph("EMAIL: contact@sndinteriors.com", contact_style),
                Paragraph("GSTIN: 29ABCDE1234F1Z5", gstin_style),
            ]
        else:
            header_text_flowables = [Spacer(1, 10), Spacer(1, 10), Spacer(1, 10), Spacer(1, 10), Spacer(1, 10)]
            
        header_table = Table([["", header_text_flowables, d]], colWidths=[55, 435, 55])
        header_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0)]))
        return [header_table, Spacer(1, 3)]

    # We will slice our 35 items across 4 pages cleanly: e.g. 9 items on page 1, 9 items on page 2, 9 items on page 3, 8 items on page 4
    page_splits = [
        (0, 9),   # Page 1
        (9, 18),  # Page 2
        (18, 27), # Page 3
        (27, 35)  # Page 4
    ]

    for page_idx, (start_i, end_i) in enumerate(page_splits):
        if page_idx > 0:
            elements.append(PageBreak())
            
        elements.extend(create_header_with_qr())
        elements.append(Table([[Paragraph(f"REF NO:- {ref_no}", ref_left_style), Paragraph(f"DATE: {est_date}", ref_right_style)]], colWidths=[272, 273]))
        elements.append(Spacer(1, 3))

        if page_idx == 0:
            address_parts = [p.strip() for p in address.split(',')]
            mid_idx = len(address_parts) // 2
            addr_line_1 = ", ".join(address_parts[:mid_idx]) if mid_idx > 0 else address
            addr_line_2 = ", ".join(address_parts[mid_idx:]) if mid_idx > 0 else ""

            floors_str = ", ".join(selected_floors)
            box_content = [
                [Paragraph("CIVIL CONSTRUCTION & BUILDING FLOOR PLANS ESTIMATION", box_hdr_style)],
                [Paragraph(f"BUILT-UP AREA: {builtin_area} SQ. FT. | FLOORS: {floors_str.upper()}", box_hdr_style)],
                [Paragraph(addr_line_1.upper(), box_detail_style)]
            ]
            if addr_line_2: 
                box_content.append([Paragraph(addr_line_2.upper(), box_detail_style)])
            box_content.append([Paragraph(f"OWNER: - {customer_name.upper()}", box_detail_style)])

            project_box = Table(box_content, colWidths=[545])
            project_box.setStyle(TableStyle([
                ('BOX', (0,0), (-1,-1), 1.5, BORDER_BLUE), 
                ('ROUNDEDCORNERS', [6, 6, 6, 6]), 
                ('TOPPADDING', (0,0), (-1,-1), 3), 
                ('BOTTOMPADDING', (0,0), (-1,-1), 3)
            ]))
            elements.append(project_box)
            elements.append(Spacer(1, 4))

        table_data = [[
            Paragraph("SL.NO", hdr_style), 
            Paragraph("Particulars / Description", hdr_style), 
            Paragraph("Unit", hdr_style), 
            Paragraph("Rate (₹)", hdr_style), 
            Paragraph("Qty", hdr_style), 
            Paragraph("Total Amount (₹)", hdr_style)
        ]]

        for idx in range(start_i, end_i):
            desc, unit, qty, rate, amt = processed_items[idx]
            table_data.append([
                Paragraph(f"{idx+1}.", cell_center),
                Paragraph(desc, cell_style),
                Paragraph(unit, cell_center),
                Paragraph(f"{rate:,.2f}", cell_right),
                Paragraph(str(qty), cell_center),
                Paragraph(f"{amt:,.2f}", cell_right)
            ])

        # If it's the last page, append GST and Total rows inside the table
        if page_idx == len(page_splits) - 1:
            table_data.append([
                "", Paragraph("Subtotal", total_style), "", "", "", Paragraph(f"{actual_subtotal:,.2f}", total_val_style)
            ])
            table_data.append([
                "", Paragraph("GST 18%", total_style), "", "", "", Paragraph(f"{actual_gst:,.2f}", total_val_style)
            ])
            table_data.append([
                "", Paragraph("TOTAL PAYABLE", total_style), "", "", "", Paragraph(f"{final_total:,.2f}", total_val_style)
            ])

        # Column Widths total 545
        t_page = Table(table_data, colWidths=[35, 245, 55, 75, 45, 90])
        t_page.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0"))
        ]))
        elements.append(t_page)

        # On the final page, add amount in words and Terms & Conditions
        if page_idx == len(page_splits) - 1:
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(num_to_words_indian_clean(final_total), words_style))
            elements.append(Spacer(1, 4))
            elements.append(Paragraph("TERMS AND CONDITIONS:", terms_hdr))
            elements.append(Spacer(1, 2))

            terms_points = [
                "1. This Is A Detailed Civil & Building Estimate Based On Selected Built-Up Area & Floors.",
                "2. Payment Schedule: 20% Advance, 25% Plinth Completion, 25% Roof Slab, 20% Masonry/Finishing, 10% Handover.",
                "3. Validity: This Estimation Is Valid For 45 Days From The Date Of Issue.",
                "4. Scope Of Work: Any Structural Modification or Extra Civil Works Will Be Billed Separately.",
                "5. Materials: Cement, Steel, Bricks, and Aggregate will conform to IS Standard Specifications.",
                "6. Timeline: Estimated Project Completion is governed by the total floors and site readiness."
            ]
            for point in terms_points:
                elements.append(Paragraph(point, terms_pt))
                elements.append(Spacer(1, 1))

    doc.build(elements)
    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()

    return pdf_bytes, filename, ref_no, final_total


# --- AUTHENTIC MODAL POPUP DIALOG FOR ESTIMATION ---
@st.dialog("⚡ BUILDING FLOOR PLANS & CIVIL WORKS ESTIMATOR", width="large")
def show_quotation_dialog():
    st.markdown("""
    <div class="commercial-auth-banner">
        <div style="font-size:2.2rem;">🔐</div>
        <div>
            <div style="color:#818CF8; font-weight:700; font-size:0.85rem; letter-spacing:1px;">SECURE SSL GATEWAY • 4-PAGE CIVIL ESTIMATION</div>
            <div style="color:#FFFFFF; font-size:0.8rem;">Generate comprehensive 35-particular civil estimates with floor selection and built-up area calculations.</div>
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
        st.subheader("🏠 Property & Floor Plan Configuration")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            customer_name = st.text_input("Customer Full Name *", value="", placeholder="Customer name")
            date_input = st.text_input("Quotation Date", value=datetime.now().strftime("%d-%m-%Y"))
        with col_c2:
            builtin_area = st.number_input("Total Built-up Area (SQ. FT) *", min_value=500.0, max_value=25000.0, value=2400.0, step=100.0)

        st.markdown("<b>Select Building Floors (Multi-select enabled):</b>", unsafe_allow_html=True)
        col_f1, col_f2, col_f3, col_f4, col_f5, col_f6 = st.columns(6)
        with col_f1: f_ground = st.checkbox("Ground Floor", value=True)
        with col_f2: f_first = st.checkbox("1st Floor", value=True)
        with col_f3: f_second = st.checkbox("2nd Floor", value=False)
        with col_f4: f_third = st.checkbox("3rd Floor", value=False)
        with col_f5: f_fourth = st.checkbox("4th Floor", value=False)
        with col_f6: f_fifth = st.checkbox("5th Floor", value=False)

        selected_floors = []
        if f_ground: selected_floors.append("Ground Floor")
        if f_first: selected_floors.append("1st Floor")
        if f_second: selected_floors.append("2nd Floor")
        if f_third: selected_floors.append("3rd Floor")
        if f_fourth: selected_floors.append("4th Floor")
        if f_fifth: selected_floors.append("5th Floor")

        address_input = st.text_area(
            "Site / Construction Address *", 
            value="",
            placeholder="Enter complete site address"
        )

        st.markdown("---")
        st.subheader("💰 ESTIMATED BUDGET")
        
        amount_input = st.number_input(
            "✏️ Enter Total Estimated Budget (INR ₹):",
            min_value=200000.0,
            max_value=50000000.0,
            value=3500000.0,
            step=50000.0,
            format="%.2f"
        )

        subtotal_est = round(amount_input / 1.18)
        gst_est = amount_input - subtotal_est
        st.info(f"📊 **Base Estimate:** ₹ {subtotal_est:,.2f} | **GST (18%):** ₹ {gst_est:,.2f} | **Total Payable:** ₹ {amount_input:,.2f}")

        submitted = st.form_submit_button("⚡ GENERATE 4-PAGE CIVIL ESTIMATE", type="primary", use_container_width=True)

    if submitted:
        if not user_name.strip() or not user_mobile.strip() or not user_email.strip() or not customer_name.strip() or not address_input.strip():
            st.warning("⚠️ Please fill in all required fields before generating the quotation.")
            return
        if not selected_floors:
            st.warning("⚠️ Please select at least one building floor.")
            return

        with st.spinner('Generating 4-page detailed PDF and syncing with cloud storage...'):
            try:
                pdf_bytes_std, filename_std, generated_ref, final_total = generate_estimation_pdf_bytes(
                    customer_name, address_input, date_input, float(amount_input), builtin_area, selected_floors, include_header=True
                )
                pdf_bytes_no_hdr, filename_no_hdr, _, _ = generate_estimation_pdf_bytes(
                    customer_name, address_input, date_input, float(amount_input), builtin_area, selected_floors, include_header=False
                )
                
                if supabase:
                    upload_to_cloud(
                        generated_ref, pdf_bytes_std, pdf_bytes_no_hdr, 
                        filename_std, filename_no_hdr, user_name, user_mobile, user_email, 
                        customer_name, date_input, final_total
                    )
                
                st.balloons()
                st.success("🎉 **Civil Estimation Generated & Synced Successfully!**")
                
                st.markdown(f"""
                <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid #F59E0B; padding: 20px; border-radius: 14px; margin: 15px 0;">
                    <h3 style="color: #F59E0B; margin-top: 0;">REF NO: {generated_ref}</h3>
                    <p style="font-size: 1.05rem; color: #F8FAFC; line-height: 1.6;">
                        <b>Your 4-page civil estimate has been successfully created. You will receive it via email or WhatsApp shortly.</b>
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
        <div><span class="live-dot"></span>LIVE CIVIL WORKS HUB: BENGALURU (SAHAKARNAGAR | HSR | WHITEFIELD)</div>
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
            <span class="gradient-text-gold">✦ BUILDING FLOOR PLANS & CIVIL WORKS </span>
        </div>
        <h1 class="hero-title-3d" style="font-size: 3rem;">SND INTERIOR & DESIGNS</h1>
        <p style="color: #CBD5E1; font-size: 1.1rem; line-height: 1.7; margin-bottom: 2rem;">
            Turnkey structural engineering, floor plan design, multi-floor extensions, and precise civil estimation for residential and commercial developments across Bengaluru.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_hero2:
    st.markdown("""
    <div class="slider-box" id="interiorCarousel">
        <div class="carousel-slide active">
            <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1000&q=80" alt="Civil Structure">
            <div class="carousel-caption">01 - Structural Foundation & RCC Framework</div>
        </div>
        <div class="carousel-slide">
            <img src="https://images.unsplash.com/photo-1541888946425-d0fbb18fcd07?auto=format&fit=crop&w=1000&q=80" alt="Building Construction">
            <div class="carousel-caption">02 - Multi-Floor Building Construction Site</div>
        </div>
        <div class="carousel-slide">
            <img src="https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1000&q=80" alt="Floor Plans">
            <div class="carousel-caption">03 - Architectural Floor Plan Blueprints</div>
        </div>
        <div class="carousel-slide">
            <img src="https://images.unsplash.com/photo-1590381105924-c72589b9ef3f?auto=format&fit=crop&w=1000&q=80" alt="Brick Masonry">
            <div class="carousel-caption">04 - Solid Block Masonry & Wall Construction</div>
        </div>
        <div class="carousel-slide">
            <img src="https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1000&q=80" alt="Slab Casting">
            <div class="carousel-caption">05 - RCC Roof Slab Shuttering & Casting</div>
        </div>
        <div class="carousel-slide">
            <img src="https://images.unsplash.com/photo-1581094288338-2314dddb7ece?auto=format&fit=crop&w=1000&q=80" alt="Civil Engineering">
            <div class="carousel-caption">06 - Engineering Site Supervision & Inspection</div>
        </div>
        <div class="carousel-slide">
            <img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1000&q=80" alt="Plastering Work">
            <div class="carousel-caption">07 - Internal & External Wall Plastering</div>
        </div>
        <div class="carousel-slide">
            <img src="https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1000&q=80" alt="Heavy Machinery">
            <div class="carousel-caption">08 - Earthwork Excavation & Foundation Base</div>
        </div>
        <div class="carousel-slide">
            <img src="https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=1000&q=80" alt="Structural Steel">
            <div class="carousel-caption">09 - TMT Steel Reinforcement Bending & Binding</div>
        </div>
        <div class="carousel-slide">
            <img src="https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=1000&q=80" alt="Completed Exterior">
            <div class="carousel-caption">10 - Completed Turnkey Building Elevation</div>
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
st.markdown("### 🏛️ Portfolio Master Collection (10 Fixed Showcase Galleries)")
st.markdown("<p style='color:#94A3B8; font-size:0.95rem; margin-bottom:1rem;'>Explore our permanent civil engineering and architectural planning catalog.</p>", unsafe_allow_html=True)

st.markdown("""
<div class="static-gallery-grid">
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80" alt="Foundation">
        <div class="static-gallery-label">01. Foundation RCC</div>
    </div>
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1541888946425-d0fbb18fcd07?auto=format&fit=crop&w=600&q=80" alt="Construction Site">
        <div class="static-gallery-label">02. Site Progress</div>
    </div>
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=600&q=80" alt="Floor Blueprints">
        <div class="static-gallery-label">03. Floor Plans</div>
    </div>
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1590381105924-c72589b9ef3f?auto=format&fit=crop&w=600&q=80" alt="Brick Masonry">
        <div class="static-gallery-label">04. Block Masonry</div>
    </div>
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=600&q=80" alt="Roof Slab">
        <div class="static-gallery-label">05. Roof Slab Casting</div>
    </div>
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1581094288338-2314dddb7ece?auto=format&fit=crop&w=600&q=80" alt="Engineering">
        <div class="static-gallery-label">06. Supervision</div>
    </div>
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=600&q=80" alt="Plastering">
        <div class="static-gallery-label">07. Wall Plastering</div>
    </div>
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=600&q=80" alt="Excavation">
        <div class="static-gallery-label">08. Earth Excavation</div>
    </div>
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=600&q=80" alt="Steel Reinforcement">
        <div class="static-gallery-label">09. Steel Bending</div>
    </div>
    <div class="static-gallery-item">
        <img src="https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=600&q=80" alt="Turnkey Elevation">
        <div class="static-gallery-label">10. Completed Elevation</div>
    </div>
</div>
""", unsafe_allow_html=True)


# --- FULL-SIZE VERTICAL SCROLLING SHOWCASE (10 FULL SIZE IMAGES) ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📸 10 Full-Size Vertical Civil Architectural Showcase")
st.markdown("<p style='color:#94A3B8; font-size:0.95rem; margin-bottom:1.5rem;'>Scroll down through our high-definition structural and civil project features.</p>", unsafe_allow_html=True)

st.markdown("""
<div class="vertical-gallery-container">
    <!-- 01 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1600&q=80" alt="Structural Foundation">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Civil Feature • 01</span>
            <div class="vertical-card-title">Robust RCC Footings & Foundation Framework</div>
            <div class="vertical-card-desc">Deep pile and isolated footing foundation designed to withstand maximum seismic load with high-grade Fe550 TMT steel.</div>
        </div>
    </div>
    <!-- 02 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1541888946425-d0fbb18fcd07?auto=format&fit=crop&w=1600&q=80" alt="Multi-Floor Construction">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Civil Feature • 02</span>
            <div class="vertical-card-title">Multi-Floor Residential Construction Execution</div>
            <div class="vertical-card-desc">Simultaneous ground and multi-story structural casting with automated batching plant concrete and rigorous quality audits.</div>
        </div>
    </div>
    <!-- 03 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1600&q=80" alt="Floor Plans">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Civil Feature • 03</span>
            <div class="vertical-card-title">Precision Architectural Floor Planning & CAD</div>
            <div class="vertical-card-desc">Vastu-compliant spatial layouts, structural load calculations, and municipal approval blueprinting for multi-floor expansions.</div>
        </div>
    </div>
    <!-- 04 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1590381105924-c72589b9ef3f?auto=format&fit=crop&w=1600&q=80" alt="Block Masonry">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Civil Feature • 04</span>
            <div class="vertical-card-title">Precision Solid Concrete Block Masonry</div>
            <div class="vertical-card-desc">High-density thermal insulating concrete blocks laid with plumb-line alignment for superior acoustic and thermal control.</div>
        </div>
    </div>
    <!-- 05 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1600&q=80" alt="Roof Slab">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Civil Feature • 05</span>
            <div class="vertical-card-title">Monolithic RCC Roof Slab Shuttering & Casting</div>
            <div class="vertical-card-desc">Pumped concrete slab casting with integral waterproofing compounds and systematic curing protocols.</div>
        </div>
    </div>
    <!-- 06 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1581094288338-2314dddb7ece?auto=format&fit=crop&w=1600&q=80" alt="Engineering Supervision">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Civil Feature • 06</span>
            <div class="vertical-card-title">On-Site Structural Engineering & Quality Control</div>
            <div class="vertical-card-desc">Regular cube testing, slump cone verification, and laser-level alignment inspections by certified civil engineers.</div>
        </div>
    </div>
    <!-- 07 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1600&q=80" alt="Plastering">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Civil Feature • 07</span>
            <div class="vertical-card-title">Smooth Interior & Weatherproof Exterior Plastering</div>
            <div class="vertical-card-desc">Machine-finished cement mortar rendering ensuring flat, crack-free surfaces ready for putty and prime coats.</div>
        </div>
    </div>
    <!-- 08 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1600&q=80" alt="Excavation">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Civil Feature • 08</span>
            <div class="vertical-card-title">Site Earthwork Excavation & Basement Prep</div>
            <div class="vertical-card-desc">Heavy excavator deployment for grading, trenching, soil stabilization, and anti-termite chemical barrier injection.</div>
        </div>
    </div>
    <!-- 09 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=1600&q=80" alt="Steel Bending">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Civil Feature • 09</span>
            <div class="vertical-card-title">TMT Steel Reinforcement Bending & Fabrication</div>
            <div class="vertical-card-desc">Computerized bar bending schedules and precise lap-length bindings for columns, beams, and sheer walls.</div>
        </div>
    </div>
    <!-- 10 -->
    <div class="vertical-gallery-card">
        <img src="https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=1600&q=80" alt="Turnkey Elevation">
        <div class="vertical-card-overlay">
            <span class="vertical-card-badge">Civil Feature • 10</span>
            <div class="vertical-card-title">Completed Turnkey Building Elevation & Handover</div>
            <div class="vertical-card-desc">Full architectural completion with exterior texture paint, compound wall, gates, and utility connections.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# --- Commercial Metrics Grid ---
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.markdown("""
    <div class="stat-box-commercial">
        <div style="font-size: 1.8rem; font-weight: 800;" class="gradient-text-gold">35+</div>
        <div style="font-size: 0.8rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; margin-top: 5px;">Civil Particulars</div>
    </div>
    """, unsafe_allow_html=True)
with col_m2:
    st.markdown("""
    <div class="stat-box-commercial">
        <div style="font-size: 1.8rem; font-weight: 800;" class="gradient-text-cyan">UP TO 5</div>
        <div style="font-size: 0.8rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; margin-top: 5px;">Floor Extensions</div>
    </div>
    """, unsafe_allow_html=True)
with col_m3:
    st.markdown("""
    <div class="stat-box-commercial">
        <div style="font-size: 1.8rem; font-weight: 800;" class="gradient-text-gold">4 PAGES</div>
        <div style="font-size: 0.8rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; margin-top: 5px;">Detailed Report</div>
    </div>
    """, unsafe_allow_html=True)
with col_m4:
    st.markdown("""
    <div class="stat-box-commercial">
        <div style="font-size: 1.8rem; font-weight: 800;" class="gradient-text-cyan">100%</div>
        <div style="font-size: 0.8rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; margin-top: 5px;">ISO Standards</div>
    </div>
    """, unsafe_allow_html=True)


# --- INTERACTIVE 3D ANIMATED / GIF VISUALIZER ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🌀 Interactive Content")
st.markdown("<p style='color:#94A3B8; font-size:0.95rem; margin-bottom:1.5rem;'>Select a civil construction phase to inspect spatial engineering and structural specifications.</p>", unsafe_allow_html=True)

selected_room = st.radio(
    "Select Simulation Zone:",
    ["🏗️ Foundation & RCC Framework", "📐 Floor Planning & Blueprints", "🧱 Block Masonry & Walls", "🏠 Multi-Floor Extension", "🔨 Finishing & Plastering"],
    horizontal=True,
    label_visibility="collapsed"
)

if "Foundation" in selected_room:
    st.markdown("""
    <div class="dashboard-card-3d" style="display:flex; gap:35px; align-items:center;">
        <div style="flex:1;">
            <div style="font-family:'Space Grotesk', sans-serif; font-weight:800; font-size:0.8rem; letter-spacing:2px; color:#F59E0B; text-transform:uppercase;">CIVIL MODULE 01</div>
            <h2 style="font-family:'Outfit', sans-serif; font-size:2.2rem; font-weight:800; color:#FFF; margin:10px 0 15px 0;">Foundation & RCC Framework</h2>
            <p style="color:#CBD5E1; line-height:1.7; margin-bottom:1.5rem;">
                Heavy-duty excavation, anti-termite treatment, PCC base, and high-strength RCC column footings engineered for multi-story vertical weight distribution.
            </p>
            <div style="display:flex; gap:15px; color:#38BDF8; font-weight:700; font-size:0.9rem;">
                <div>⚡ Fe550 TMT Steel</div>
                <div>⚡ M25 Concrete Mix</div>
                <div>⚡ Anti-Termite</div>
            </div>
        </div>
        <div style="flex:1;">
            <div class="visualizer-frame-3d">
                <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1000&q=80" alt="Foundation">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
elif "Planning" in selected_room:
    st.markdown("""
    <div class="dashboard-card-3d" style="display:flex; gap:35px; align-items:center;">
        <div style="flex:1;">
            <div style="font-family:'Space Grotesk', sans-serif; font-weight:800; font-size:0.8rem; letter-spacing:2px; color:#F59E0B; text-transform:uppercase;">CIVIL MODULE 02</div>
            <h2 style="font-family:'Outfit', sans-serif; font-size:2.2rem; font-weight:800; color:#FFF; margin:10px 0 15px 0;">Floor Planning & Blueprints</h2>
            <p style="color:#CBD5E1; line-height:1.7; margin-bottom:1.5rem;">
                Comprehensive architectural drafting incorporating Vastu Shastra guidelines, optimal cross-ventilation, structural load calculations, and municipal approval compliance.
            </p>
            <div style="display:flex; gap:15px; color:#38BDF8; font-weight:700; font-size:0.9rem;">
                <div>⚡ Vastu Compliant</div>
                <div>⚡ CAD Blueprints</div>
                <div>⚡ Municipal Approval</div>
            </div>
        </div>
        <div style="flex:1;">
            <div class="visualizer-frame-3d">
                <img src="https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1000&q=80" alt="Planning">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
elif "Masonry" in selected_room:
    st.markdown("""
    <div class="dashboard-card-3d" style="display:flex; gap:35px; align-items:center;">
        <div style="flex:1;">
            <div style="font-family:'Space Grotesk', sans-serif; font-weight:800; font-size:0.8rem; letter-spacing:2px; color:#F59E0B; text-transform:uppercase;">CIVIL MODULE 03</div>
            <h2 style="font-family:'Outfit', sans-serif; font-size:2.2rem; font-weight:800; color:#FFF; margin:10px 0 15px 0;">Block Masonry & Wall Construction</h2>
            <p style="color:#CBD5E1; line-height:1.7; margin-bottom:1.5rem;">
                Precision solid concrete block laying for external and internal partitions with accurate vertical plumb alignment and lintel band reinforcements.
            </p>
            <div style="display:flex; gap:15px; color:#38BDF8; font-weight:700; font-size:0.9rem;">
                <div>⚡ Solid Blocks</div>
                <div>⚡ Plumb Alignment</div>
                <div>⚡ Lintel Bands</div>
            </div>
        </div>
        <div style="flex:1;">
            <div class="visualizer-frame-3d">
                <img src="https://images.unsplash.com/photo-1590381105924-c72589b9ef3f?auto=format&fit=crop&w=1000&q=80" alt="Masonry">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
elif "Extension" in selected_room:
    st.markdown("""
    <div class="dashboard-card-3d" style="display:flex; gap:35px; align-items:center;">
        <div style="flex:1;">
            <div style="font-family:'Space Grotesk', sans-serif; font-weight:800; font-size:0.8rem; letter-spacing:2px; color:#F59E0B; text-transform:uppercase;">CIVIL MODULE 04</div>
            <h2 style="font-family:'Outfit', sans-serif; font-size:2.2rem; font-weight:800; color:#FFF; margin:10px 0 15px 0;">Multi-Floor Extension (Up to 5 Floors)</h2>
            <p style="color:#CBD5E1; line-height:1.7; margin-bottom:1.5rem;">
                Seamless vertical extension engineering enabling structural stability from Ground up to 5 floors with integrated staircase and plumbing risers.
            </p>
            <div style="display:flex; gap:15px; color:#38BDF8; font-weight:700; font-size:0.9rem;">
                <div>⚡ Up to 5 Floors</div>
                <div>⚡ Staircase Cores</div>
                <div>⚡ Vertical Risers</div>
            </div>
        </div>
        <div style="flex:1;">
            <div class="visualizer-frame-3d">
                <img src="https://images.unsplash.com/photo-1541888946425-d0fbb18fcd07?auto=format&fit=crop&w=1000&q=80" alt="Extension">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="dashboard-card-3d" style="display:flex; gap:35px; align-items:center;">
        <div style="flex:1;">
            <div style="font-family:'Space Grotesk', sans-serif; font-weight:800; font-size:0.8rem; letter-spacing:2px; color:#F59E0B; text-transform:uppercase;">CIVIL MODULE 05</div>
            <h2 style="font-family:'Outfit', sans-serif; font-size:2.2rem; font-weight:800; color:#FFF; margin:10px 0 15px 0;">Finishing & Wall Plastering</h2>
            <p style="color:#CBD5E1; line-height:1.7; margin-bottom:1.5rem;">
                Double-coat external weatherproof plastering, smooth internal putty rendering, waterproofing for wet areas, and premium priming.
            </p>
            <div style="display:flex; gap:15px; color:#38BDF8; font-weight:700; font-size:0.9rem;">
                <div>⚡ Waterproofing</div>
                <div>⚡ Smooth Putty</div>
                <div>⚡ Weatherproof</div>
            </div>
        </div>
        <div style="flex:1;">
            <div class="visualizer-frame-3d">
                <img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1000&q=80" alt="Finishing">
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
