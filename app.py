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
    page_title="SND Interior & Designs | Luxury Home Interiors Bangalore",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- DLIFE Inspired Luxury CSS & Animations ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #F8FAFC;
        color: #0F172A;
    }

    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(12px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* Top Utility Bar */
    .top-nav {
        background-color: #0F172A;
        color: #94A3B8;
        padding: 8px 24px;
        font-size: 0.8rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #D97706;
    }

    /* Luxury Header Banner */
    .dlife-hero {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.92) 0%, rgba(15, 23, 42, 0.85) 100%), 
                    url('https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        border-radius: 18px;
        padding: 3.5rem 2.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 20px 35px -10px rgba(15, 23, 42, 0.5);
        margin-bottom: 2rem;
        animation: fadeIn 0.8s ease-out;
    }

    .hero-badge {
        background: linear-gradient(90deg, #D97706 0%, #F59E0B 100%);
        color: #FFFFFF;
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 1rem;
    }

    .dlife-hero h1 {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        color: #FFFFFF;
        margin-bottom: 0.5rem;
    }

    .dlife-hero p {
        font-size: 1.1rem;
        color: #CBD5E1;
        max-width: 750px;
        margin: 0 auto;
    }

    /* Horizontal Sliding Gallery Container */
    .slider-container {
        display: flex;
        gap: 18px;
        overflow-x: auto;
        padding: 10px 5px 25px 5px;
        scroll-snap-type: x mandatory;
        -webkit-overflow-scrolling: touch;
    }

    .slider-container::-webkit-scrollbar {
        height: 8px;
    }

    .slider-container::-webkit-scrollbar-track {
        background: #E2E8F0;
        border-radius: 10px;
    }

    .slider-container::-webkit-scrollbar-thumb {
        background: #D97706;
        border-radius: 10px;
    }

    /* Portfolio Cards inside Slider */
    .portfolio-card {
        flex: 0 0 320px;
        scroll-snap-align: start;
        background: #FFFFFF;
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 20px rgba(0,0,0,0.04);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .portfolio-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 30px rgba(217, 119, 6, 0.15);
        border-color: #F59E0B;
    }

    .portfolio-img {
        width: 100%;
        height: 210px;
        object-fit: cover;
    }

    .portfolio-body {
        padding: 1.25rem;
    }

    .portfolio-tag {
        color: #D97706;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    .portfolio-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0F172A;
        margin: 4px 0 8px 0;
    }

    .portfolio-desc {
        font-size: 0.85rem;
        color: #64748B;
        line-height: 1.4;
    }

    /* Glass Card Layout */
    .glass-card {
        background: #FFFFFF;
        border-radius: 18px;
        border: 1px solid #E2E8F0;
        padding: 2.2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        margin-top: 1rem;
        animation: fadeIn 0.6s ease-out;
    }

    .result-card {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border: 1px solid #FCD34D;
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1rem;
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

def fetch_all_logs():
    if not supabase: return []
    response = supabase.table("estimation_logs").select("*").order("created_at", desc=True).execute()
    return response.data

def generate_estimation_pdf_bytes(owner, address, est_date, target_total):
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
        
        # Header text block featuring email
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


# --- Top Utility Header ---
st.markdown("""
<div class="top-nav">
    <div>📍 <b>BANGALORE SHOWROOMS:</b> Sahakarnagar | HSR Layout | Whitefield | Yelahanka</div>
    <div>📞 <b>CLIENT SUPPORT:</b> +91 98765 43210 &nbsp;|&nbsp; ✉️ contact@sndinteriors.com</div>
</div>
""", unsafe_allow_html=True)

# --- Hero Section (DLIFE Style) ---
st.markdown("""
<div class="dlife-hero">
    <div class="hero-badge">✨ BANGALORE'S PREMIUM HOME INTERIOR BRAND</div>
    <h1>Customized Home Interiors & Modern Living</h1>
    <p>100% Customized Modular Kitchens, Sliding Wardrobes, Premium Lighting & Contemporary Living Spaces for Apartments and Villas in Bengaluru.</p>
</div>
""", unsafe_allow_html=True)


# --- SECTION 1: SLIDING PHOTO SHOWCASE ---
st.markdown("### 🎨 Design Portfolio Showcase")
st.caption("👈 Swipe / Scroll horizontally to explore our signature modern designs for Bengaluru homes 👉")

st.markdown("""
<div class="slider-container">
    <div class="portfolio-card">
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=800&q=80" alt="Modern Kitchen">
        <div class="portfolio-body">
            <div class="portfolio-tag">MODERN KITCHEN</div>
            <div class="portfolio-title">Acrylic Island Kitchen</div>
            <div class="portfolio-desc">German hinges, tandem drawers, quartz countertop & integrated profile LEDs.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=800&q=80" alt="Sliding Wardrobes">
        <div class="portfolio-body">
            <div class="portfolio-tag">SLIDING STORAGE</div>
            <div class="portfolio-title">Lacquered Glass Wardrobe</div>
            <div class="portfolio-desc">Floor-to-ceiling soft-close sliding doors with sensor-activated interior strip lights.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80" alt="Tiles & Flooring">
        <div class="portfolio-body">
            <div class="portfolio-tag">TILES & FLOORING</div>
            <div class="portfolio-title">Italian Marble Finish Tiles</div>
            <div class="portfolio-desc">Large format vitrified tiles with seamless grout lines and anti-skid bathroom finishes.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80" alt="Luxury Bathrooms">
        <div class="portfolio-body">
            <div class="portfolio-tag">BATHROOM VANITY</div>
            <div class="portfolio-title">Contemporary En-Suite</div>
            <div class="portfolio-desc">Floating vanity units, rainfall shower enclosures, and backlit LED vanity mirrors.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=800&q=80" alt="Lights & Ceilings">
        <div class="portfolio-body">
            <div class="portfolio-tag">LIGHTS & CEILINGS</div>
            <div class="portfolio-title">Ambient False Ceilings</div>
            <div class="portfolio-desc">Gypsum drop ceilings, warm cove illumination, magnetic track lights & chandeliers.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=800&q=80" alt="Balcony & Outdoors">
        <div class="portfolio-body">
            <div class="portfolio-tag">BALCONY RETREAT</div>
            <div class="portfolio-title">Aesthetic Garden Balcony</div>
            <div class="portfolio-desc">WPC teak deck flooring, vertical green walls, weatherproof ambient sconce lights.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- SECTION 2: INTERACTIVE PORTAL TABS ---
tab1, tab2 = st.tabs(["⚡ Instant Project Estimator", "🔍 Client Portal & Cloud Lookup"])

# --- TAB 1: ESTIMATION GENERATOR ---
with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📋 Generate Official Design Estimate")
    st.caption("Select your target project budget to auto-calculate itemised interior scope, generate a QR-coded PDF, and save to cloud.")

    with st.form("estimation_form", clear_on_submit=False):
        col_a, col_b = st.columns(2)
        with col_a:
            owner_input = st.text_input("👤 Client / Property Owner Name:", value="KUSHAL ANAND & HKS")
            date_input = st.text_input("📅 Date of Issue:", value=datetime.now().strftime("%d-%m-%Y"))
        
        with col_b:
            amount_input = st.number_input("💰 Target Estimated Budget (Rs.):", min_value=50000, max_value=10000000, value=1499000, step=25000)
            
        address_input = st.text_area("📍 Site Address / Apartment Details:", value="BIRLA TRIMAYA PHASE 4 FLAT-1205, T-6, F-12, DEVANAHALLI CHIKKAJALA, BENGALURU")

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("⚡ Compute Estimation & Sync to Cloud", type="primary", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        with st.spinner('Calculating modular quantities & building QR-verified document...'):
            try:
                pdf_bytes, filename, generated_ref, final_total = generate_estimation_pdf_bytes(
                    owner_input, address_input, date_input, float(amount_input)
                )
                
                if supabase:
                    cloud_url = upload_to_cloud(generated_ref, pdf_bytes, filename, owner_input, date_input, final_total)
                    st.balloons()
                    st.success(f"🎉 **Estimation Generated & Synced to Cloud!** (Ref No: `{generated_ref}`)")
                else:
                    st.success(f"✅ **Estimation Generated Locally!** (Ref No: `{generated_ref}`)")

                st.download_button(
                    label="📄 Download Official PDF Estimation",
                    data=pdf_bytes,
                    file_name=filename,
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- TAB 2: CLOUD LOOKUP ---
with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🔍 Retrieve Existing Estimation")
    st.caption("Enter your Reference Number (`REF NO`) to download original estimation PDFs directly from cloud storage anytime.")

    search_ref = st.text_input("Enter Reference Number (REF NO):", placeholder="e.g. 152329072026")
    
    if search_ref:
        if supabase:
            with st.spinner('Fetching document from cloud archive...'):
                record, pdf_data = fetch_estimation_by_ref(search_ref)
                
                if record:
                    st.markdown(f"""
                    <div class="result-card">
                        <h4 style="color:#B45309; margin:0;">🎯 Estimation Located!</h4>
                        <p style="margin-top:8px; color:#1F2937;">
                            <b>REF NO:</b> {record['ref_no']}<br>
                            <b>Customer Name:</b> {record['customer_name']}<br>
                            <b>Date:</b> {record['est_date']}<br>
                            <b>Total Amount:</b> ₹ {record['amount']:,.2f}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    if pdf_data:
                        st.download_button(
                            label=f"📥 Download PDF Document ({record['ref_no']})",
                            data=pdf_data,
                            file_name=f"Estimation_{record['ref_no']}_{record['customer_name']}.pdf",
                            mime="application/pdf",
                            type="primary",
                            use_container_width=True
                        )
                    elif record.get('pdf_url'):
                        st.markdown(f"[🔗 Direct Download Link]({record['pdf_url']})")
                else:
                    st.error(f"❌ No record found in cloud storage matching REF NO: `{search_ref.strip()}`")
        else:
            st.error("Supabase cloud storage connection is missing.")

    st.markdown("---")
    st.subheader("📋 Cloud Estimation History")
    if supabase:
        all_logs = fetch_all_logs()
        if all_logs:
            st.dataframe(all_logs, use_container_width=True)
        else:
            st.caption("No historical estimations found in database.")
    st.markdown('</div>', unsafe_allow_html=True)
