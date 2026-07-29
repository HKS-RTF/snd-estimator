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
        gap: 22px;
        overflow-x: auto;
        padding: 15px 5px 30px 5px;
        scroll-snap-type: x mandatory;
    }

    .slider-container::-webkit-scrollbar {
        height: 8px;
    }
    .slider-container::-webkit-scrollbar-thumb {
        background: linear-gradient(90deg, #D97706, #F59E0B);
        border-radius: 10px;
    }

    .portfolio-card {
        flex: 0 0 320px;
        scroll-snap-align: start;
        background: linear-gradient(145deg, #0F172A 0%, #1E293B 100%);
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid rgba(217, 119, 6, 0.2);
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }

    .portfolio-card:hover {
        transform: translateY(-8px);
        border-color: #F59E0B;
        box-shadow: 0 20px 35px rgba(217, 119, 6, 0.3);
    }

    .portfolio-img {
        width: 100%;
        height: 220px;
        object-fit: cover;
    }

    .portfolio-body {
        padding: 1.25rem;
    }

    .portfolio-tag {
        color: #F59E0B;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
    }

    .portfolio-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 6px 0 6px 0;
    }

    .portfolio-desc {
        font-size: 0.84rem;
        color: #94A3B8;
        line-height: 1.4;
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
        margin-top: 3rem;
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
        st.subheader("💰 Scope & Manual Budget Entry")
        
        amount_input = st.number_input(
            "✏️ Enter Total Estimated Budget (INR ₹):",
            min_value=50000.0,
            max_value=10000000.0,
            value=1499000.0,
            step=25000.0,
            format="%.2f"
        )

        # Live breakdown preview
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


# --- SLIDING PORTFOLIO SHOWCASE (EXPANDED TO 8 LUXURY SPACES) ---
st.markdown("### 🎨 Explore Signature Design Portfolio")
st.caption("👈 Swipe / Scroll horizontally to preview our recent grand interior executions across Bengaluru homes 👉")

st.markdown("""
<div class="slider-container">
    <div class="portfolio-card">
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=800&q=80" alt="Modern Kitchen">
        <div class="portfolio-body">
            <div class="portfolio-tag">MODERN KITCHEN</div>
            <div class="portfolio-title">Acrylic Island Kitchen</div>
            <div class="portfolio-desc">German soft-close hinges, quartz countertop & integrated LED profiles.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=800&q=80" alt="Living Room">
        <div class="portfolio-body">
            <div class="portfolio-tag">LIVING ROOM</div>
            <div class="portfolio-title">Contemporary TV Unit & Sofa</div>
            <div class="portfolio-desc">Fluted wooden paneling, italian marble media wall & ambient cove lighting.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=800&q=80" alt="Sliding Wardrobes">
        <div class="portfolio-body">
            <div class="portfolio-tag">BEDROOM STORAGE</div>
            <div class="portfolio-title">Lacquered Glass Wardrobe</div>
            <div class="portfolio-desc">Floor-to-ceiling sliding mechanisms with automated internal sensor lights.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1616594039964-ae9021a400a0?auto=format&fit=crop&w=800&q=80" alt="Master Bedroom">
        <div class="portfolio-body">
            <div class="portfolio-tag">MASTER SUITE</div>
            <div class="portfolio-title">Upholstered Bed & Headboard</div>
            <div class="portfolio-desc">Custom velvet headboard with side pendant lights and floating side tables.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80" alt="Luxury Bathroom">
        <div class="portfolio-body">
            <div class="portfolio-tag">BATHROOM & VANITY</div>
            <div class="portfolio-title">Backlit Mirror Vanity Unit</div>
            <div class="portfolio-desc">Anti-fog smart LED mirror, wall-hung wash basin & matte black Kohler fittings.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80" alt="Tiles & Flooring">
        <div class="portfolio-body">
            <div class="portfolio-tag">MARBLE & FLOORING</div>
            <div class="portfolio-title">Italian Marble Slab Flooring</div>
            <div class="portfolio-desc">Large-format vitrified polished slabs with precision seamless epoxy grouting.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=800&q=80" alt="Lights & Ceilings">
        <div class="portfolio-body">
            <div class="portfolio-tag">LIGHTING & CEILINGS</div>
            <div class="portfolio-title">Ambient Drop False Ceilings</div>
            <div class="portfolio-desc">Gypsum layered ceilings, warm cove lights, magnetic track spotlights.</div>
        </div>
    </div>
    <div class="portfolio-card">
        <img class="portfolio-img" src="https://images.unsplash.com/photo-1507089947368-19c1da9775ae?auto=format&fit=crop&w=800&q=80" alt="Dining Room">
        <div class="portfolio-body">
            <div class="portfolio-tag">DINING AREA</div>
            <div class="portfolio-title">Marble Top Dining & Crockery</div>
            <div class="portfolio-desc">Custom glass-door crockery unit with warm interior display lighting.</div>
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
