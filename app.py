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

    .dashboard-card-3d {
        background: linear-gradient(145deg, rgba(17, 24, 39, 0.85) 0%, rgba(3, 7, 18, 0.95) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 28px;
        padding: 2.5rem;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        margin-bottom: 2rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: #030712;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        border-radius: 14px;
        padding: 0.85rem 2rem;
        border: none;
        box-shadow: 0 10px 30px rgba(217, 119, 6, 0.4);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #FBBF24 0%, #D97706 100%);
        box-shadow: 0 15px 40px rgba(245, 158, 11, 0.6);
        transform: translateY(-3px);
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
        path=path_std, file=pdf_bytes_standard, file_options={"content-type": "application/pdf", "upsert": "true"}
    )
    url_std = supabase.storage.from_("estimations").get_public_url(path_std)

    path_no_hdr = f"pdf_estimations/{filename_no_hdr}"
    supabase.storage.from_("estimations").upload(
        path=path_no_hdr, file=pdf_bytes_no_header, file_options={"content-type": "application/pdf", "upsert": "true"}
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


# --- FULLY EXPANDED 35 MASTER ITEMS FOR CIVIL WORKS ---
CIVIL_ITEMS_MASTER_35 = [
    ("Site clearance, leveling, debris removal & temporary storage shed setup", "JOB", 1, 0.015),
    ("Setting out, centerline marking & architectural layout transfer", "SQ. FT", 1, 0.015),
    ("Chipping existing roof slab/plinth for structural rebar bonding", "SQ. FT", 1, 0.020),
    ("Drilling and chemical anchoring of Fe550 dowel bars into columns", "Pcs", 40, 0.025),
    ("RCC Column starter casting & pedestal strengthening (M25 Grade)", "CU. FT", 120, 0.030),
    ("Column reinforcement fabrication with high-tensile Fe550 steel", "Kg", 850, 0.035),
    ("Column formwork shuttering, alignment and dismantling", "SQ. FT", 300, 0.025),
    ("M25 Grade concrete pouring and mechanical vibration for columns", "CU. FT", 150, 0.030),
    ("Roof beam bottom & side shuttering staging with heavy props", "SQ. FT", 450, 0.030),
    ("Beam reinforcement steel assembly & stirrup binding", "Kg", 1100, 0.040),
    ("RCC Floor slab shuttering plywood & timber span setup", "SQ. FT", 1, 0.045),
    ("Slab main and distribution steel grid reinforcement laying", "Kg", 1400, 0.050),
    ("Concealed electrical conduit and junction box placement in slab", "Points", 35, 0.025),
    ("Plumbing drainage pipe sleeves and core-cutting through slab", "Spots", 12, 0.020),
    ("Ready-mix / site-mixed M25 concrete pumping & slab casting", "CU. FT", 350, 0.060),
    ("Slab concrete curing with water ponding and Hessian cloth", "Days", 14, 0.015),
    ("External wall masonry with solid concrete blocks / AAC blocks", "SQ. FT", 1, 0.040),
    ("Internal partition walls with standard cement solid blocks", "SQ. FT", 1, 0.035),
    ("Door and window concrete lintel casting & sunshades", "RFT", 120, 0.030),
    ("Door frame (Sal wood/Granite) and window frame installation", "Units", 10, 0.025),
    ("Internal wall rough plastering (Cement mortar 1:5)", "SQ. FT", 1, 0.035),
    ("Ceiling smooth plastering with anti-crack mesh at joints", "SQ. FT", 1, 0.030),
    ("External wall weather-proof double-coat plastering", "SQ. FT", 1, 0.035),
    ("Parapet wall construction around terrace boundary (3 feet height)", "RFT", 110, 0.025),
    ("Staircase waist slab, riser & tread concrete casting", "Steps", 22, 0.035),
    ("Staircase stainless steel / MS railing fabrication & fixing", "RFT", 40, 0.030),
    ("Terrace waterproofing base screed and slope gradient leveling", "SQ. FT", 1, 0.025),
    ("Polymer chemical membrane waterproofing application on terrace", "SQ. FT", 1, 0.030),
    ("Underground & overhead water supply pipe network (CPVC)", "RFT", 180, 0.025),
    ("Drainage waste pipe network layout and PVC chambers", "RFT", 150, 0.025),
    ("Electrical main DB box installation, MCB & RCCB wiring", "Set", 1, 0.025),
    ("Floor tile bedding screed preparation (Cement mortar)", "SQ. FT", 1, 0.030),
    ("Bathroom dado wall tiling and anti-skid floor tiling", "SQ. FT", 250, 0.035),
    ("Balcony and utility area vitrified/ceramic tile paving", "SQ. FT", 180, 0.025),
    ("Final site clean-up, debris haulage & handover preparation", "JOB", 1, 0.015)
];


def generate_estimation_pdf_bytes(customer_name, address, est_date, target_total, floors_option, buildup_sqft, include_header=True):
    subtotal_target = target_total / 1.18
    
    item_rows = []
    raw_amounts = []
    for desc, unit_type, base_qty_multiplier, weight_factor in CIVIL_ITEMS_MASTER_35:
        if unit_type == "SQ. FT":
            qty = round(buildup_sqft)
        elif unit_type in ["Kg", "CU. FT", "RFT"]:
            qty = round(buildup_sqft * base_qty_multiplier) if base_qty_multiplier > 1 else round(buildup_sqft)
        else:
            qty = base_qty_multiplier
            
        amt = round(subtotal_target * weight_factor * random.uniform(0.9, 1.1))
        raw_amounts.append((desc, unit_type, qty, amt))

    current_sum = sum([x[3] for x in raw_amounts])
    factor = subtotal_target / current_sum if current_sum > 0 else 1.0
    
    adjusted_items = []
    running_sum = 0
    for idx, (desc, unit_type, qty, amt) in enumerate(raw_amounts):
        if idx == len(raw_amounts) - 1:
            final_amt = round(subtotal_target - running_sum)
        else:
            final_amt = round(amt * factor)
            running_sum += final_amt
            
        rate = round(final_amt / qty, 2) if qty > 0 else final_amt
        adjusted_items.append((desc, unit_type, qty, rate, final_amt))

    actual_subtotal = sum([x[4] for x in adjusted_items])
    actual_gst = round(actual_subtotal * 0.18)
    final_total = actual_subtotal + actual_gst

    now = datetime.now()
    ref_no = now.strftime("%H%M%d%m%Y")
    clean_customer_name = customer_name.replace(' ', '_').replace('&', 'AND')
    filename = f"Civil_Extension_4P_{ref_no}_{clean_customer_name}{'_NoHeader' if not include_header else ''}.pdf"

    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=25, leftMargin=25, topMargin=15, bottomMargin=15)
    styles = getSampleStyleSheet()

    RED_COLOR, BLUE_COLOR, LIGHT_PINK, BORDER_BLUE = colors.HexColor("#DC2626"), colors.HexColor("#1E40AF"), colors.HexColor("#EC4899"), colors.HexColor("#2563EB")

    title_style = ParagraphStyle("Title", parent=styles["Heading1"], alignment=1, fontSize=24, leading=28, fontName="Helvetica-Bold", textColor=RED_COLOR)
    sub_style = ParagraphStyle("Sub", parent=styles["Normal"], alignment=1, fontSize=8.5, leading=11, fontName="Helvetica-Bold", textColor=BLUE_COLOR)
    gstin_style = ParagraphStyle("GSTIN", parent=styles["Normal"], alignment=1, fontSize=8.5, leading=11, fontName="Helvetica-Bold", textColor=LIGHT_PINK)
    ref_left_style = ParagraphStyle("RefLeft", parent=styles["Normal"], alignment=0, fontSize=9.5, leading=11, fontName="Helvetica")
    ref_right_style = ParagraphStyle("RefRight", parent=styles["Normal"], alignment=2, fontSize=9.5, leading=11, fontName="Helvetica")
    box_hdr_style = ParagraphStyle("BoxHdr", parent=styles["Normal"], alignment=1, fontSize=11, leading=13, fontName="Helvetica-Bold", textColor=colors.black)
    box_detail_style = ParagraphStyle("BoxDetail", parent=styles["Normal"], alignment=1, fontSize=10, leading=12, fontName="Helvetica-Bold", textColor=colors.black)
    
    cell_style = ParagraphStyle("Cell", parent=styles["Normal"], alignment=0, fontSize=8, leading=10, fontName="Helvetica", textColor=colors.black)
    cell_center = ParagraphStyle("CellC", parent=styles["Normal"], alignment=1, fontSize=8, leading=10, fontName="Helvetica", textColor=colors.black)
    cell_right = ParagraphStyle("CellR", parent=styles["Normal"], alignment=2, fontSize=8, leading=10, fontName="Helvetica", textColor=colors.black)
    
    hdr_style = ParagraphStyle("Hdr", parent=styles["Normal"], alignment=1, fontSize=8.5, leading=11, fontName="Helvetica-Bold", textColor=colors.black)
    total_style = ParagraphStyle("Tot", parent=styles["Normal"], alignment=2, fontSize=10, leading=12, fontName="Helvetica-Bold", textColor=colors.black)
    total_val_style = ParagraphStyle("TotVal", parent=styles["Normal"], alignment=2, fontSize=10, leading=12, fontName="Helvetica-Bold", textColor=colors.black)
    words_style = ParagraphStyle("Words", parent=styles["Normal"], alignment=1, fontSize=9.5, leading=12, fontName="Helvetica-Bold", textColor=colors.black)
    terms_hdr = ParagraphStyle("TermH", parent=styles["Normal"], alignment=1, fontSize=9, leading=11, fontName="Helvetica-Bold", textColor=colors.black)
    terms_pt = ParagraphStyle("TermP", parent=styles["Normal"], alignment=0, fontSize=7.5, leading=9.5, fontName="Helvetica-Bold", textColor=colors.black)

    elements = []

    def create_header_with_qr():
        qr_data = f"CUSTOMER: {customer_name.upper()}\nEXTENSION: {floors_option} ({buildup_sqft} SQFT)\nREF: {ref_no}\nTOTAL: Rs. {final_total:,}"
        qr = QrCodeWidget(qr_data)
        qr_bounds = qr.getBounds()
        w, h = qr_bounds[2] - qr_bounds[0], qr_bounds[3] - qr_bounds[1]
        d = Drawing(55, 55, transform=[55.0/w, 0, 0, 55.0/h, 0, 0])
        d.add(qr)
        
        if include_header:
            header_text_flowables = [
                Paragraph("SND INTERIOR & DESIGNS", title_style), Spacer(1, 1),
                Paragraph("STRUCTURAL CIVIL WORKS, FLOOR EXTENSIONS & BUILDING ESTIMATES", sub_style),
                Paragraph("#15, E BLOCK, SAHAKHAR NAGAR, BANGALORE-560092", sub_style),
                Paragraph("EMAIL: contact@sndinteriors.com | GSTIN: 29ABCDE1234F1Z5", gstin_style),
            ]
        else:
            header_text_flowables = [Spacer(1, 10), Spacer(1, 10), Spacer(1, 10), Spacer(1, 10)]
            
        header_table = Table([["", header_text_flowables, d]], colWidths=[45, 450, 55])
        header_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0)]))
        return [header_table, Spacer(1, 3)]

    # --- PAGE 1: Header, Project Info, Items 1 to 9 ---
    elements.extend(create_header_with_qr())
    elements.append(Table([[Paragraph(f"REF NO:-{ref_no}", ref_left_style), Paragraph(f"DATE: {est_date}", ref_right_style)]], colWidths=[275, 275]))
    elements.append(Spacer(1, 3))

    project_box = Table([
        [Paragraph(f"CIVIL CONSTRUCTION & STRUCTURAL EXTENSION ESTIMATE FOR ADDITION OF {floors_option.upper()} ({buildup_sqft} SQ. FT)", box_hdr_style)],
        [Paragraph(f"SITE ADDRESS: {address.upper()}", box_detail_style)],
        [Paragraph(f"PROPERTY OWNER: {customer_name.upper()}", box_detail_style)]
    ], colWidths=[550])
    project_box.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 1.5, BORDER_BLUE), ('ROUNDEDCORNERS', [6,6,6,6]), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    elements.append(project_box)
    elements.append(Spacer(1, 4))

    col_w = [28, 202, 45, 45, 75, 75, 80]

    def build_table_chunk(start_idx, end_idx, include_totals=False, is_last_page=False):
        t_data = [[
            Paragraph("SL", hdr_style), 
            Paragraph("Particulars / Civil Description", hdr_style), 
            Paragraph("Unit", hdr_style), 
            Paragraph("Qty", hdr_style), 
            Paragraph("Rate (₹)", hdr_style), 
            Paragraph("Amount (₹)", hdr_style)
        ]]
        for idx in range(start_idx, end_idx):
            desc, unit_type, qty, rate, amt = adjusted_items[idx]
            t_data.append([
                Paragraph(str(idx+1), cell_center),
                Paragraph(desc, cell_style),
                Paragraph(unit_type, cell_center),
                Paragraph(str(qty), cell_center),
                Paragraph(f"{rate:,.2f}", cell_right),
                Paragraph(f"{amt:,.2f}", cell_right)
            ])
            
        if include_totals:
            t_data.append(["", Paragraph("SUBTOTAL", total_style), "", "", "", Paragraph(f"{actual_subtotal:,.2f}", total_val_style)])
            t_data.append(["", Paragraph("GST 18%", total_style), "", "", "", Paragraph(f"{actual_gst:,.2f}", total_val_style)])
            t_data.append(["", Paragraph("TOTAL ESTIMATE", total_style), "", "", "", Paragraph(f"{final_total:,.2f}", total_val_style)])

        t = Table(t_data, colWidths=col_w)
        t.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0"))
        ]))
        return t

    # Page 1 items (0 to 9 -> 10 items)
    elements.append(build_table_chunk(0, 10))
    elements.append(PageBreak())

    # --- PAGE 2: Items 10 to 18 (9 items) ---
    elements.extend(create_header_with_qr())
    elements.append(Table([[Paragraph(f"REF NO:-{ref_no} (Page 2/4)", ref_left_style), Paragraph(f"DATE: {est_date}", ref_right_style)]], colWidths=[275, 275]))
    elements.append(Spacer(1, 4))
    elements.append(build_table_chunk(10, 19))
    elements.append(PageBreak())

    # --- PAGE 3: Items 19 to 27 (9 items) ---
    elements.extend(create_header_with_qr())
    elements.append(Table([[Paragraph(f"REF NO:-{ref_no} (Page 3/4)", ref_left_style), Paragraph(f"DATE: {est_date}", ref_right_style)]], colWidths=[275, 275]))
    elements.append(Spacer(1, 4))
    elements.append(build_table_chunk(19, 28))
    elements.append(PageBreak())

    # --- PAGE 4: Items 28 to 35 (7 items) + Totals + Terms ---
    elements.extend(create_header_with_qr())
    elements.append(Table([[Paragraph(f"REF NO:-{ref_no} (Page 4/4)", ref_left_style), Paragraph(f"DATE: {est_date}", ref_right_style)]], colWidths=[275, 275]))
    elements.append(Spacer(1, 4))
    elements.append(build_table_chunk(28, 35, include_totals=True, is_last_page=True))
    
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(num_to_words_indian_clean(final_total), words_style))
    elements.append(Spacer(1, 3))
    elements.append(Paragraph("TERMS AND CONDITIONS FOR CIVIL & STRUCTURAL WORKS:", terms_hdr))
    elements.append(Spacer(1, 2))

    terms_points = [
        "1. Preliminary civil estimate based on buildup area, structural load requirements & technical site evaluation.",
        "2. Payment Schedule: 30% Advance, 30% Upon Slab Casting, 30% Masonry & Plastering, 10% Handover.",
        "3. Validity: Estimate valid for 30 days due to market fluctuations in steel (Fe550) and cement pricing.",
        "4. Structural Responsibility: Existing foundation and column load capacity must be verified prior to casting.",
        "5. Material Standards: Fe550 Grade TMT Steel, OPC/PPC Cement & approved masonry blocks will be utilized.",
        "6. Project Duration: Estimated structural completion time is 120 working days from advance receipt."
    ]
    for pt in terms_points:
        elements.append(Paragraph(pt, terms_pt))
        elements.append(Spacer(1, 1))

    doc.build(elements)
    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()

    return pdf_bytes, filename, ref_no, final_total


# --- AUTHENTIC MODAL POPUP DIALOG FOR CIVIL ESTIMATION ---
@st.dialog("🏗️ 4-PAGE DETAILED CIVIL CONSTRUCTION ESTIMATOR", width="large")
def show_quotation_dialog():
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%); border: 1px solid rgba(99, 102, 241, 0.4); border-radius: 20px; padding: 1.5rem; display: flex; align-items: center; gap: 20px; margin-bottom: 2rem;">
        <div style="font-size:2.2rem;">🔐</div>
        <div>
            <div style="color:#818CF8; font-weight:700; font-size:0.85rem; letter-spacing:1px;">SECURE SSL GATEWAY • 35-PARTICULAR TECHNICAL INVOICING</div>
            <div style="color:#FFFFFF; font-size:0.8rem;">Generates a comprehensive 4-page PDF with separate Rate, Quantity, and Amount columns.</div>
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
                "📐 Buildup Area (SQ. FT) *", min_value=100.0, max_value=10000.0, value=1500.0, step=50.0, format="%.2f"
            )

        address_input = st.text_area("Site / Building Address *", value="", placeholder="Enter complete site address")

        st.markdown("---")
        st.subheader("💰 CIVIL WORKS BUDGET")
        amount_input = st.number_input(
            "✏️ Enter Total Estimated Civil Budget (INR ₹):", min_value=100000.0, max_value=20000000.0, value=3000000.0, step=50000.0, format="%.2f"
        )

        subtotal_est = round(amount_input / 1.18)
        gst_est = amount_input - subtotal_est
        st.info(f"📊 **Base Civil Estimate:** ₹ {subtotal_est:,.2f} | **GST (18%):** ₹ {gst_est:,.2f} | **Total Final Payable:** ₹ {amount_input:,.2f}")

        submitted = st.form_submit_button("⚡ GENERATE 4-PAGE DETAILED ESTIMATE", type="primary", use_container_width=True)

    if submitted:
        if not user_name.strip() or not user_mobile.strip() or not user_email.strip() or not customer_name.strip() or not address_input.strip():
            st.warning("⚠️ Please fill in all required fields before generating the quotation.")
            return

        with st.spinner('Generating 4-page detailed PDF with 35 particulars and syncing with cloud storage...'):
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
                st.success("🎉 **4-Page Detailed Civil Quotation Generated Successfully!**")
                
                st.markdown(f"""
                <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid #F59E0B; padding: 20px; border-radius: 14px; margin: 15px 0;">
                    <h3 style="color: #F59E0B; margin-top: 0;">REF NO: {generated_ref}</h3>
                    <p style="font-size: 1.05rem; color: #F8FAFC; line-height: 1.6;">
                        <b>Your 4-page technical breakdown has been successfully created. The PDF includes all 35 particulars with separate Rate, Qty, and Amount columns for your technical team.</b>
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
            st.markdown("<p style='color:#94A3B8;'>Authenticate with enterprise credentials to access live quotation databases.</p>", unsafe_allow_html=True)
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
        if not supabase:
            st.warning("⚠️ Supabase connection inactive.")
        else:
            try:
                res = supabase.table("estimation_logs").select("*").order("est_date", desc=True).limit(20).execute()
                if res.data:
                    st.dataframe(res.data, use_container_width=True)
                else:
                    st.info("No records found.")
            except Exception as e:
                st.error(f"Database error: {e}")


# --- DASHBOARD LAYOUT ---
col_tick1, col_tick2 = st.columns([10, 1])
with col_tick1:
    st.markdown("""
    <div class="commercial-ticker" style="margin-bottom:0;">
        <div><span class="live-dot"></span>LIVE CIVIL HUB: BENGALURU (SAHAKARNAGAR | HSR | WHITEFIELD)</div>
        <div>SUPPORT HOTLINE: +91 98765 43210 &nbsp;|&nbsp; 35-ITEM TECHNICAL SPECIFICATION ACTIVE</div>
    </div>
    """, unsafe_allow_html=True)
with col_tick2:
    if st.button("🔐", help="Enterprise Admin Portal Login"):
        show_admin_dialog()

st.markdown("<br>", unsafe_allow_html=True)

col_top_btn1, col_top_btn2, col_top_btn3 = st.columns([2, 2, 2])
with col_top_btn2:
    if st.button("⚡ GENERATE 4-PAGE DETAILED ESTIMATE", type="primary", use_container_width=True):
        show_quotation_dialog()

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="dashboard-card-3d" style="text-align: center; padding: 3rem;">
    <div style="font-family:'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.85rem; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 12px;">
        <span class="gradient-text-gold">✦ COMPREHENSIVE TECHNICAL CIVIL SPECIFICATION ✦</span>
    </div>
    <h1 class="hero-title-3d" style="font-size: 2.8rem;">35-Particular 4-Page Engineering Estimator</h1>
    <p style="color: #CBD5E1; font-size: 1.1rem; line-height: 1.7; max-width: 800px; margin: 0 auto 2rem auto;">
        Our upgraded estimation engine splits every structural phase into explicit line items across 4 detailed pages. Every row features distinct <b>Rate per Unit</b>, <b>Quantity</b>, and <b>Total Amount</b> columns so your technician team has absolute clarity with zero queries.
    </p>
</div>
""", unsafe_allow_html=True)
