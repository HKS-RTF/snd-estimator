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

# --- Grand Luxury CSS & Component Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #090D16;
        color: #F8FAFC;
    }

    /* Top Utility Navigation Bar */
    .top-nav {
        background: linear-gradient(90deg, #0F172A 0%, #1E293B 100%);
        color: #94A3B8;
        padding: 10px 28px;
        font-size: 0.82rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #D97706;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }

    /* Grand Hero Banner */
    .grand-hero {
        background: linear-gradient(180deg, rgba(9, 13, 22, 0.95) 0%, rgba(15, 23, 42, 0.88) 100%), 
                    url('https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1800&q=80');
        background-size: cover;
        background-position: center;
        border-radius: 24px;
        padding: 4.5rem 3rem;
        color: white;
        text-align: center;
        border: 1px solid rgba(217, 119, 6, 0.3);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
        margin-bottom: 2.5rem;
    }

    .brand-title {
        font-family: 'Cinzel', serif;
        font-size: 3.2rem;
        font-weight: 900;
        letter-spacing: 2px;
        background: linear-gradient(135deg, #FDE68A 0%, #D97706 50%, #B45309 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .hero-badge {
        background: rgba(217, 119, 6, 0.15);
        border: 1px solid #D97706;
        color: #FBBF24;
        padding: 6px 20px;
        border-radius: 50px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 1.2rem;
    }

    /* Trust Stats Grid */
    .trust-stats {
        display: flex;
        justify-content: center;
        gap: 35px;
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stat-item {
        text-align: center;
    }
    .stat-number {
        font-size: 1.6rem;
        font-weight: 800;
        color: #F59E0B;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Horizontal Sliding Gallery */
    .slider-container {
        display: flex;
        gap: 20px;
        overflow-x: auto;
        padding: 10px 5px 25px 5px;
        scroll-snap-type: x mandatory;
    }

    .slider-container::-webkit-scrollbar {
        height: 8px;
    }
    .slider-container::-webkit-scrollbar-track {
        background: #0F172A;
        border-radius: 10px;
    }
    .slider-container::-webkit-scrollbar-thumb {
        background: linear-gradient(90deg, #D97706, #F59E0B);
        border-radius: 10px;
    }

    .portfolio-card {
        flex: 0 0 320px;
        scroll-snap-align: start;
        background: #0F172A;
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.4s ease;
        position: relative;
    }

    .portfolio-card:hover {
        transform: translateY(-8px);
        border-color: #D97706;
        box-shadow: 0 15px 30px rgba(217, 119, 6, 0.25);
    }

    .portfolio-img {
        width: 100%;
        height: 220px;
        object-fit: cover;
    }

    .card-badge {
        position: absolute;
        top: 12px;
        right: 12px;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid #D97706;
        color: #FBBF24;
        font-size: 0.65rem;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 12px;
        backdrop-filter: blur(4px);
    }

    .portfolio-body {
        padding: 1.25rem;
    }

    .portfolio-tag {
        color: #F59E0B;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1px;
    }

    .portfolio-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 4px 0 6px 0;
    }

    .portfolio-desc {
        font-size: 0.85rem;
        color: #94A3B8;
    }

    /* Grid Layout for Specialty Showcase */
    .specialty-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin-top: 1.5rem;
    }

    /* Authentic Security Header inside Form */
    .auth-banner {
        background: linear-gradient(135deg, #1E1B4B 0%, #0F172A 100%);
        border: 1px solid #6366F1;
        border-radius: 14px;
        padding: 1rem 1.25rem;
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 1.5rem;
    }

    /* Grand Bottom Call-To-Action (CTA) Banner */
    .bottom-cta-container {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 2px solid #D97706;
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        margin-top: 3.5rem;
        margin-bottom: 2rem;
    }

    .bottom-cta-title {
        font-family: 'Cinzel', serif;
        font-size: 2.2rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 0.5rem;
    }

    .bottom-cta-subtitle {
        color: #CBD5E1;
        font-size: 1.05rem;
        max-width: 650px;
        margin: 0 auto 1.8rem auto;
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

def upload_to_cloud(ref_no, pdf_bytes, filename, owner, est_date, final_total):
    if not supabase: return None
    storage_path = f"pdf_estimations/{filename}"
    supabase.storage.from_("estimations").upload(
        path=storage_path,
        file=pdf_bytes,
        file_options={"content-type": "application/pdf", "upsert": "true"}
    )
    pdf_url = supabase.storage.from_("estimations").get_public_url(storage_path)
    data = {
        "ref_no": str(ref_no),
        "customer_name": str(owner.upper()),
        "est_date": str(est_date),
        "amount": float(final_total),
        "pdf_url": pdf_url
    }
    supabase.table("estimation_logs").upsert(data).execute()
    return pdf_url

def fetch_estimation_by_ref(ref_no):
    if not supabase: return None, None
    response = supabase.table("estimation_logs").select("*").eq("ref_no", str(ref_no).strip()).execute()
    if response.data:
        record = response.data[0]
        clean_name = record['customer_name'].replace(' ', '_').replace('&', 'AND')
        storage_path = f"pdf_estimations/Estimation_{record['ref_no']}_{clean_name}.pdf"
        try:
            pdf_data = supabase.storage.from_("estimations").download(storage_path)
            return record, pdf_data
        except Exception:
            return record, None
    return None, None


def generate_estimation_pdf_bytes(owner, address, est_date, target_total):
    # --- 50 MASTER PARTICULAR ITEMS (Description, Unit, Category, Weight, Tier) ---
    # Tier 1: Standard/Core (1-15) | Tier 2: Modern/Mid-Range (16-33) | Tier 3: Ultra Luxury/High-Tech (34-50)
    MASTER_ITEMS_50 = [
        # --- TIER 1: STANDARD / BUDGET ITEMS (15 Items) ---
        ("3 course of oil bond distemper (Inside repaint)", "SQ. FT", "SQFT", 0.05, 1),
        ("2 course of snow cem paint (Outside repaint)", "SQ. FT", "SQFT", 0.04, 1),
        ("Replacing sanitary fittings inside the toilets", "SETS", "SETS_UNITS", 0.06, 1),
        ("Replacing sanitary fittings inside the kitchen", "SET", "SETS_UNITS", 0.05, 1),
        ("Providing & casting bathroom glazed tiles fixing etc.", "SQ. FT", "SQFT", 0.05, 1),
        ("Wall plastering and surface levelling finishing", "SQ. FT", "SQFT", 0.06, 1),
        ("Demolition and debris clearance removal", "LOT", "JOB_LOT", 0.04, 1),
        ("Basic false ceiling work with gypsum board", "SQ. FT", "SQFT", 0.06, 1),
        ("Standard matte laminate modular wardrobe shutters", "SQ. FT", "SQFT", 0.08, 1),
        ("Basic electrical switchboards, wiring & point points", "JOB", "JOB_LOT", 0.06, 1),
        ("Standard ceramic floor tiling and grout filling", "SQ. FT", "SQFT", 0.07, 1),
        ("Polished granite counter slab fixing for kitchen", "SQ. FT", "SQFT", 0.06, 1),
        ("Commercial ply loft framing with shutter doors", "JOB", "JOB_LOT", 0.05, 1),
        ("Flush door polish and mortise lock replacement", "NOS", "SETS_UNITS", 0.04, 1),
        ("Aluminum powder-coated window frame grills & mesh", "SQ. FT", "SQFT", 0.05, 1),

        # --- TIER 2: MODERN & CREATIVE INTERIORS (18 Items) ---
        ("Asian Paints Royale Luxury Emulsion wall painting", "SQ. FT", "SQFT", 0.07, 2),
        ("Acrylic modular kitchen with Blum soft-close fittings", "JOB", "JOB_LOT", 0.12, 2),
        ("Sliding glass wardrobes with concealed sensor LED strips", "SQ. FT", "SQFT", 0.10, 2),
        ("Gypsum false ceiling with integrated magnetic track lights", "SQ. FT", "SQFT", 0.08, 2),
        ("Designer TV wall console unit with fluted charcoal panels", "JOB", "JOB_LOT", 0.08, 2),
        ("Vitrified large-format slab flooring (800x1600mm)", "SQ. FT", "SQFT", 0.08, 2),
        ("Grohe thermostatic rain showers & sanitary fixtures", "SETS", "SETS_UNITS", 0.07, 2),
        ("Teak veneer foyer shoe console with CNC brass inlay mesh", "UNIT", "SETS_UNITS", 0.06, 2),
        ("Floating bathroom vanity with backlit anti-fog mirror", "SETS", "SETS_UNITS", 0.06, 2),
        ("Balcony WPC wooden decking with vertical green wall", "SQ. FT", "SQFT", 0.06, 2),
        ("Architectural COB spotlights & magnetic profile lighting", "JOB", "JOB_LOT", 0.07, 2),
        ("Natural teak wood veneer paneling for bed back wall", "SQ. FT", "SQFT", 0.07, 2),
        ("Toughened glass shower cubicles with PVD black hardware", "SETS", "SETS_UNITS", 0.06, 2),
        ("Customized motorized window roller blinds with remote", "NOS", "SETS_UNITS", 0.05, 2),
        ("Quartz island breakfast counter with pendant hanging lights", "JOB", "JOB_LOT", 0.08, 2),
        ("PU lacquer finish kitchen overhead cabinets with bi-fold lift", "JOB", "JOB_LOT", 0.09, 2),
        ("Digital biometric smart door lock with RFID & app access", "UNIT", "SETS_UNITS", 0.04, 2),
        ("Acoustic fabric cushioned headboard wall panelling", "SQ. FT", "SQFT", 0.06, 2),

        # --- TIER 3: ULTRA LUXURY & HIGH-TECH MODERN (17 Items) ---
        ("Imported Italian Botticino marble flooring with epoxy polish", "SQ. FT", "SQFT", 0.14, 3),
        ("High-gloss lacquered glass sliding wardrobe (Hafele fittings)", "SQ. FT", "SQFT", 0.12, 3),
        ("Smart motorized IoT curtain tracks with home automation", "JOB", "JOB_LOT", 0.08, 3),
        ("Imported Calacatta quartz waterfall island with induction", "JOB", "JOB_LOT", 0.14, 3),
        ("CNC router-cut Corian mandir unit with gold leaf backlighting", "UNIT", "SETS_UNITS", 0.08, 3),
        ("Backlit translucent onyx stone illuminated bar counter", "JOB", "JOB_LOT", 0.10, 3),
        ("Italian stucco Venetian plaster decorative feature wall", "SQ. FT", "SQFT", 0.07, 3),
        ("Walk-in glass closet organizer system with island drawer console", "JOB", "JOB_LOT", 0.13, 3),
        ("Frameless panaromic sliding glass balcony enclosure systems", "SQ. FT", "SQFT", 0.09, 3),
        ("Flush hidden secret door integrated with wood panelled wall", "UNIT", "SETS_UNITS", 0.06, 3),
        ("Acoustic stretch ceiling with fiber optic starry night LEDs", "SQ. FT", "SQFT", 0.08, 3),
        ("Custom curved fluted wood architectural room divider partition", "SQ. FT", "SQFT", 0.07, 3),
        ("Built-in dual zone wine chiller & luxury coffee bar joinery", "JOB", "JOB_LOT", 0.09, 3),
        ("Solid Burma teak main door with custom CNC carving & brass handle", "UNIT", "SETS_UNITS", 0.08, 3),
        ("Smart vanity unit with touchscreen mirror, weather & Bluetooth", "SETS", "SETS_UNITS", 0.06, 3),
        ("Architectural metal acoustic louvers & exterior facade fins", "SQ. FT", "SQFT", 0.08, 3),
        ("Automated motorized pop-down projector ceiling nook setup", "JOB", "JOB_LOT", 0.07, 3)
    ]

    # --- DYNAMIC BUDGET & PAGE LOGIC ---
    if target_total < 1500000:
        is_single_page = True
        total_items_needed = 10
        # Lower budget: Focus on Tier 1 & Tier 2 items
        candidate_pool = [item for item in MASTER_ITEMS_50 if item[4] in (1, 2)]
        weights_pool = [0.7 if item[4] == 1 else 0.3 for item in candidate_pool]
    elif target_total < 3500000:
        is_single_page = False
        total_items_needed = 15
        # Mid budget: Balanced across Tier 1, Tier 2, and Tier 3
        candidate_pool = MASTER_ITEMS_50
        weights_pool = [0.2 if item[4] == 1 else (0.5 if item[4] == 2 else 0.3) for item in candidate_pool]
    else:
        is_single_page = False
        total_items_needed = 17
        # High budget: Focus heavily on Tier 2 & Tier 3 Luxury/Modern items
        candidate_pool = [item for item in MASTER_ITEMS_50 if item[4] in (2, 3)]
        weights_pool = [0.3 if item[4] == 2 else 0.7 for item in candidate_pool]

    # Weighted random sampling without replacement
    selected_items = []
    pool_copy = list(candidate_pool)
    weights_copy = list(weights_pool)

    for _ in range(total_items_needed):
        if not pool_copy: break
        chosen_idx = random.choices(range(len(pool_copy)), weights=weights_copy, k=1)[0]
        selected_items.append(pool_copy.pop(chosen_idx))
        weights_copy.pop(chosen_idx)

    # Randomize the item order completely for each generated estimation
    random.shuffle(selected_items)

    def calculate_quantity(unit_label, category, total_amount):
        min_budget, max_budget = 1000000.0, 5000000.0
        ratio = max(0.0, min(1.0, (total_amount - min_budget) / (max_budget - min_budget)))
        ratio = max(0.0, min(1.0, ratio + random.uniform(-0.05, 0.05)))
        
        if category == "SQFT":
            sqft = round(450 + ratio * (2800 - 450))
            return f"{sqft} {unit_label}"
        elif category == "SETS_UNITS":
            qty = round(1 + ratio * (6 - 1))
            return f"{qty} {unit_label}"
        elif category == "JOB_LOT":
            qty = round(1 + ratio * (2 - 1))
            return f"{qty} {unit_label}"
        return f"1 {unit_label}"

    processed_items = [
        (desc, calculate_quantity(unit_label, cat, target_total), weight) 
        for desc, unit_label, cat, weight, tier in selected_items
    ]

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
    filename = f"Estimation_{ref_no}_{clean_owner_name}.pdf"

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
        cell_12_bold_center = ParagraphStyle("Cell11BC", parent=styles["Normal"], alignment=1, fontSize=10.5, leading=13, fontName="Helvetica-Bold", textColor=colors.black)
        hdr_12_bold_center = ParagraphStyle("Hdr11BC", parent=styles["Normal"], alignment=1, fontSize=11, leading=13.5, fontName="Helvetica-Bold", textColor=colors.black)
        total_14_bold = ParagraphStyle("Total12B", parent=styles["Normal"], alignment=1, fontSize=11.5, leading=14, fontName="Helvetica-Bold", textColor=colors.black)
        words_13_bold_center = ParagraphStyle("Words11.5BC", parent=styles["Normal"], alignment=1, fontSize=11, leading=13.5, fontName="Helvetica-Bold", textColor=colors.black)
        terms_hdr_center = ParagraphStyle("TermsHdr9.5", parent=styles["Normal"], alignment=1, fontSize=9, leading=11.5, fontName="Helvetica-Bold", textColor=colors.black)
        terms_point_size_8 = ParagraphStyle("TermsPt8.5", parent=styles["Normal"], alignment=0, fontSize=8, leading=10, fontName="Helvetica-Bold", textColor=colors.black)
    else:
        cell_12_bold_center = ParagraphStyle("Cell12BC", parent=styles["Normal"], alignment=1, fontSize=11, leading=13.5, fontName="Helvetica-Bold", textColor=colors.black)
        hdr_12_bold_center = ParagraphStyle("Hdr12BC", parent=styles["Normal"], alignment=1, fontSize=11.5, leading=14, fontName="Helvetica-Bold", textColor=colors.black)
        total_14_bold = ParagraphStyle("Total14B", parent=styles["Normal"], alignment=1, fontSize=13, leading=15.5, fontName="Helvetica-Bold", textColor=colors.black)
        words_13_bold_center = ParagraphStyle("Words13BC", parent=styles["Normal"], alignment=1, fontSize=12, leading=15, fontName="Helvetica-Bold", textColor=colors.black)
        terms_hdr_center = ParagraphStyle("TermsHdr10", parent=styles["Normal"], alignment=1, fontSize=9.5, leading=13, fontName="Helvetica-Bold", textColor=colors.black)
        terms_point_size_8 = ParagraphStyle("TermsPt8", parent=styles["Normal"], alignment=0, fontSize=8, leading=10.5, fontName="Helvetica-Bold", textColor=colors.black)

    elements = []

    def create_header_with_qr():
        qr_data = f"CUSTOMER NAME: {owner.upper()}\nADDRESS: {address.upper()}\nREF NO: {ref_no}\nDATE: {est_date}\nESTIMATION AMOUNT: Rs. {final_total:,}\nEMAIL: contact@sndinteriors.com"
        qr = QrCodeWidget(qr_data)
        qr_bounds = qr.getBounds()
        w, h = qr_bounds[2] - qr_bounds[0], qr_bounds[3] - qr_bounds[1]
        d = Drawing(60, 60, transform=[60.0/w, 0, 0, 60.0/h, 0, 0])
        d.add(qr)
        
        header_text_flowables = [
            Paragraph("SND INTERIOR & DESIGNS", title_style), Spacer(1, 2),
            Paragraph("INTERIOR WORKS, DESIGN ESTIMATE, FLOOR VALUATIONS, BUILDING PLANS", sub_style),
            Paragraph("#15, E BLOCK, SAHAKHAR NAGAR, BANGALORE-560092", sub_style),
            Paragraph("EMAIL: contact@sndinteriors.com", contact_style),
            Paragraph("GSTIN: 29ABCDE1234F1Z5", gstin_style),
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

        t1 = Table(p_table_data, colWidths=[45, 285, 100, 120])
        t1.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.black), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 6.0), ('BOTTOMPADDING', (0,0), (-1,-1), 6.0)]))
        elements.append(t1)
    else:
        # Page 1 Table (Fixed 9 items)
        p1_table_data = [[Paragraph("SL.NO", hdr_12_bold_center), Paragraph("Description", hdr_12_bold_center), Paragraph("Qty", hdr_12_bold_center), Paragraph("Amount Rs.", hdr_12_bold_center)]]
        for idx in range(9):
            item = processed_items[idx]
            p1_table_data.append([Paragraph(f"{idx+1}.", cell_12_bold_center), Paragraph(item[0], cell_12_bold_center), Paragraph(item[1], cell_12_bold_center), Paragraph(f"{item_amounts[idx]:,}", cell_12_bold_center)])
        
        t1 = Table(p1_table_data, colWidths=[45, 285, 100, 120])
        t1.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.black), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 12.0), ('BOTTOMPADDING', (0,0), (-1,-1), 12.0)]))
        elements.append(t1)

        elements.append(PageBreak())
        elements.extend(create_header_with_qr())

        # Page 2 Table (Remaining items: index 9 to total_items_needed)
        p2_table_data = [[Paragraph("SL.NO", hdr_12_bold_center), Paragraph("Description", hdr_12_bold_center), Paragraph("Qty", hdr_12_bold_center), Paragraph("Amount Rs.", hdr_12_bold_center)]]
        for idx in range(9, len(processed_items)):
            item = processed_items[idx]
            p2_table_data.append([Paragraph(f"{idx+1}.", cell_12_bold_center), Paragraph(item[0], cell_12_bold_center), Paragraph(item[1], cell_12_bold_center), Paragraph(f"{item_amounts[idx]:,}", cell_12_bold_center)])

        p2_table_data.append(["", Paragraph("GST 18%", total_14_bold), "", Paragraph(f"{actual_gst:,}", total_14_bold)])
        p2_table_data.append(["", Paragraph("TOTAL", total_14_bold), "", Paragraph(f"{final_total:,}", total_14_bold)])

        t2 = Table(p2_table_data, colWidths=[45, 285, 100, 120])
        t2.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.black), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 10.0), ('BOTTOMPADDING', (0,0), (-1,-1), 10.0)]))
        elements.append(t2)

    elements.append(Spacer(1, 5))
    elements.append(Paragraph(num_to_words_indian_clean(final_total), words_13_bold_center))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("TERMS AND CONDITIONS:", terms_hdr_center))
    elements.append(Spacer(1, 2))

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
        elements.append(Spacer(1, 1.5))

    doc.build(elements)
    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()

    return pdf_bytes, filename, ref_no, final_total


# --- State Synchronization Callbacks for Dual Amount Selection ---
if "dialog_budget_val" not in st.session_state:
    st.session_state["dialog_budget_val"] = 1499000

def update_from_num():
    st.session_state["dialog_budget_val"] = st.session_state["dialog_num_key"]

def update_from_slider():
    st.session_state["dialog_budget_val"] = st.session_state["dialog_slider_key"]


# --- AUTHENTIC MODAL POPUP DIALOG ---
@st.dialog("✨ OFFICIAL INTERIOR DESIGN QUOTATION GENERATOR", width="large")
def show_quotation_dialog():
    st.markdown("""
    <div class="auth-banner">
        <div style="font-size:2rem;">🛡️</div>
        <div>
            <div style="color:#A5B4FC; font-weight:700; font-size:0.85rem; letter-spacing:1px;">VERIFIED PORTAL • GST REGISTERED FIRM</div>
            <div style="color:#FFFFFF; font-size:0.8rem;">Official Quotations for Home Interiors in Bengaluru. Document comes with encrypted QR verification.</div>
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
        st.subheader("💰 Budget & Cost Configuration")
        st.caption("You can type the exact amount manually OR adjust using the interactive slider below:")

        col_b1, col_b2 = st.columns([1, 1])
        with col_b1:
            st.number_input(
                "✏️ Manual Amount Entry (INR ₹):",
                min_value=50000,
                max_value=10000000,
                step=25000,
                key="dialog_num_key",
                value=st.session_state["dialog_budget_val"],
                on_change=update_from_num
            )

        with col_b2:
            slider_default = max(100000, min(5000000, st.session_state["dialog_budget_val"]))
            st.slider(
                "🎚️ Quick Budget Slider (INR ₹):",
                min_value=100000,
                max_value=5000000,
                step=25000,
                key="dialog_slider_key",
                value=slider_default,
                on_change=update_from_slider
            )

        amount_input = float(st.session_state["dialog_budget_val"])

        # Live calculation breakdown display
        subtotal_est = round(amount_input / 1.18)
        gst_est = amount_input - subtotal_est
        st.info(f"📊 **Base Estimate:** ₹ {subtotal_est:,.2f} | **GST (18%):** ₹ {gst_est:,.2f} | **Total Final Payable:** ₹ {amount_input:,.2f}")

        st.caption("🔒 All estimations are processed securely. Digital copies are archived automatically.")
        
        submitted = st.form_submit_button("⚡ GENERATE QR-VERIFIED OFFICIAL PDF", type="primary", use_container_width=True)

    if submitted:
        with st.spinner('Generating document & syncing with cloud...'):
            try:
                pdf_bytes, filename, generated_ref, final_total = generate_estimation_pdf_bytes(
                    owner_input, address_input, date_input, float(amount_input)
                )
                
                if supabase:
                    cloud_url = upload_to_cloud(generated_ref, pdf_bytes, filename, owner_input, date_input, final_total)
                    st.balloons()
                    st.success(f"🎉 **Estimation Logged to Cloud Storage!** Ref NO: `{generated_ref}`")
                else:
                    st.success(f"✅ **Estimation Generated Locally!** Ref NO: `{generated_ref}`")

                st.download_button(
                    label="📄 DOWNLOAD OFFICIAL PDF ESTIMATION",
                    data=pdf_bytes,
                    file_name=filename,
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")


# --- TOP NAVIGATION BAR ---
st.markdown("""
<div class="top-nav">
    <div>📍 <b>BANGALORE SHOWROOMS:</b> Sahakarnagar | HSR Layout | Whitefield | Yelahanka</div>
    <div>📞 <b>CLIENT SUPPORT:</b> +91 98765 43210 &nbsp;|&nbsp; ✉️ contact@sndinteriors.com</div>
</div>
""", unsafe_allow_html=True)


# --- GRAND HERO SECTION ---
st.markdown("""
<div class="grand-hero">
    <div class="hero-badge">👑 BENGALURU'S MOST TRUSTED LUXURY INTERIORS</div>
    <div class="brand-title">SND INTERIOR & DESIGNS</div>
    <p style="color:#CBD5E1; font-size:1.15rem; max-width:800px; margin:0 auto;">
        Crafting customized 100% factory-finished Modular Kitchens, Designer Wardrobes, False Ceilings, and Turnkey Home Interiors for Apartments and Villas.
    </p>
    <div class="trust-stats">
        <div class="stat-item">
            <div class="stat-number">500+</div>
            <div class="stat-label">Homes Completed</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">10 YEARS</div>
            <div class="stat-label">Material Warranty</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">45 DAYS</div>
            <div class="stat-label">Delivery Guarantee</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">100%</div>
            <div class="stat-label">Transparent Pricing</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# --- MAIN HORIZONTAL SLIDING PORTFOLIO ---
st.markdown("### 🎨 Signature Luxury Home Showcase")
st.caption("👈 Scroll horizontally to explore full apartment & villa interior execution concepts 👉")

st.markdown("""
<div class="slider-container">
    <div class="portfolio-card">
        <div class="card-badge">GERMAN FITTINGS</div>
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=800&q=80" alt="Modern Kitchen">
        <div class="portfolio-body">
            <div class="portfolio-tag">MODERN KITCHEN</div>
            <div class="portfolio-title">Acrylic Island Kitchen</div>
            <div class="portfolio-desc">Soft-close Blum hinges, quartz counter & concealed LED profiles.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <div class="card-badge">POPULAR</div>
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=800&q=80" alt="Luxury Living Room">
        <div class="portfolio-body">
            <div class="portfolio-tag">LIVING & LOUNGE</div>
            <div class="portfolio-title">Grand Marble Living Suite</div>
            <div class="portfolio-desc">Custom TV console, fluted panelling & warm cove ambient lighting.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <div class="card-badge">AUTO LIGHTING</div>
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=800&q=80" alt="Sliding Wardrobes">
        <div class="portfolio-body">
            <div class="portfolio-tag">SLIDING STORAGE</div>
            <div class="portfolio-title">Lacquered Glass Wardrobe</div>
            <div class="portfolio-desc">Floor-to-ceiling sliding panels with integrated wardrobe lighting.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <div class="card-badge">MASTER BEDROOM</div>
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1616594039964-ae9021a400a0?auto=format&fit=crop&w=800&q=80" alt="Master Suite">
        <div class="portfolio-body">
            <div class="portfolio-tag">BEDROOM SUITES</div>
            <div class="portfolio-title">Contemporary Master Suite</div>
            <div class="portfolio-desc">Upholstered headboard, veneer side tables & acoustic wall panels.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <div class="card-badge">ROYAL FINISH</div>
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1617806118233-18e1de247200?auto=format&fit=crop&w=800&q=80" alt="Dining Room">
        <div class="portfolio-body">
            <div class="portfolio-tag">DINING SPACES</div>
            <div class="portfolio-title">6-Seater Onyx Dining Area</div>
            <div class="portfolio-desc">Translucent stone table top with custom pendant accent lights.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <div class="card-badge">ITALIAN MARBLE</div>
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80" alt="Tiles & Flooring">
        <div class="portfolio-body">
            <div class="portfolio-tag">MARBLE & TILES</div>
            <div class="portfolio-title">Seamless Epoxy Flooring</div>
            <div class="portfolio-desc">Vitrified large-format slabs with mirror polish sealant finish.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <div class="card-badge">GYPSUM CEILING</div>
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=800&q=80" alt="Lights & Ceilings">
        <div class="portfolio-body">
            <div class="portfolio-tag">LIGHTING & CEILINGS</div>
            <div class="portfolio-title">Ambient Drop False Ceiling</div>
            <div class="portfolio-desc">Saint-Gobain plasterboard, magnetic track lights & spotlights.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <div class="card-badge">SPA EXPERIENCE</div>
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80" alt="Luxury Bathroom">
        <div class="portfolio-body">
            <div class="portfolio-tag">BATHROOM & VANITY</div>
            <div class="portfolio-title">Minimalist Resort Bathroom</div>
            <div class="portfolio-desc">Floating vanity, backlit anti-fog mirrors & thermostatic showers.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# --- SECONDARY SHOWCASE: SPECIALTY SPACES GRID ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🏆 Specialty Zones & Custom Joinery")
st.caption("Bespoke architectural concepts tailored specifically for high-end Bengaluru properties")

st.markdown("""
<div class="specialty-grid">
    <div class="portfolio-card" style="flex:auto;">
        <div class="card-badge">WORK FROM HOME</div>
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1524758631624-e2822e304c36?auto=format&fit=crop&w=800&q=80" alt="Home Office">
        <div class="portfolio-body">
            <div class="portfolio-tag">HOME OFFICE & STUDY</div>
            <div class="portfolio-title">Ergonomic Executive Desk</div>
            <div class="portfolio-desc">Cable management, floating bookshelf & built-in warm LED strips.</div>
        </div>
    </div>
    <div class="portfolio-card" style="flex:auto;">
        <div class="card-badge">OUTDOOR LIVING</div>
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80" alt="Balcony Garden">
        <div class="portfolio-body">
            <div class="portfolio-tag">BALCONY DECKING</div>
            <div class="portfolio-title">Zen Garden & Deck Nook</div>
            <div class="portfolio-desc">Weatherproof WPC flooring, vertical garden walls & ambient seating.</div>
        </div>
    </div>
    <div class="portfolio-card" style="flex:auto;">
        <div class="card-badge">ROYAL COLLECTION</div>
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1600565193348-f74bd3c7ccdf?auto=format&fit=crop&w=800&q=80" alt="Foyer Entryway">
        <div class="portfolio-body">
            <div class="portfolio-tag">FOYER & CONSOLE</div>
            <div class="portfolio-title">Grand Entry Foyer</div>
            <div class="portfolio-desc">Stone feature wall, CNC brass inlay partition & shoe storage console.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# --- PORTAL TABS & CLOUD SEARCH ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("### 🔍 Client Services & Cloud Search")

col_cloud1, col_cloud2 = st.columns([2, 1])

with col_cloud1:
    search_ref = st.text_input("Enter Reference Number (REF NO) to lookup archived estimation:", placeholder="e.g. 152329072026")
    if search_ref and supabase:
        with st.spinner('Fetching archived document...'):
            record, pdf_data = fetch_estimation_by_ref(search_ref)
            if record:
                st.success(f"🎯 Document Found for **{record['customer_name']}**! Amount: ₹ {record['amount']:,.2f}")
                if pdf_data:
                    st.download_button(
                        label=f"📥 Download PDF ({record['ref_no']})",
                        data=pdf_data,
                        file_name=f"Estimation_{record['ref_no']}_{record['customer_name']}.pdf",
                        mime="application/pdf",
                        type="primary"
                    )
            else:
                st.error("No record found matching this Reference Number.")

with col_cloud2:
    st.markdown("""
    <div style="background:#0F172A; border:1px solid rgba(255,255,255,0.1); border-radius:16px; padding:1.2rem;">
        <div style="font-weight:700; color:#F59E0B; margin-bottom:6px;">✉️ DIRECT EMAIL SUPPORT</div>
        <div style="color:#CBD5E1; font-size:0.85rem;">Have architectural drawings or custom floor plans? Mail us directly at:</div>
        <div style="font-weight:800; color:#FFFFFF; margin-top:8px;">contact@sndinteriors.com</div>
    </div>
    """, unsafe_allow_html=True)


# --- GRAND BOTTOM CALL-TO-ACTION (CTA) ---
st.markdown("""
<div class="bottom-cta-container">
    <div style="display:inline-block; background:rgba(217, 119, 6, 0.2); border:1px solid #D97706; padding:4px 16px; border-radius:50px; font-size:0.8rem; color:#FBBF24; font-weight:700; margin-bottom:1rem;">
        ✨ INSTANT DESIGN ESTIMATE
    </div>
    <div class="bottom-cta-title">LOOKING FOR QUOTATION FOR YOUR HOME?</div>
    <div class="bottom-cta-subtitle">
        Get an itemized, QR-verified PDF estimate tailored to your apartment or villa budget in under 30 seconds.
    </div>
</div>
""", unsafe_allow_html=True)

# Main Popup Trigger Button
cta_col1, cta_col2, cta_col3 = st.columns([1, 2, 1])
with cta_col2:
    if st.button("👉 CLICK HERE TO GENERATE QUOTATION 👈", type="primary", use_container_width=True):
        show_quotation_dialog()
