import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

SAMPLE_DIR = os.path.dirname(os.path.abspath(__file__))

# Standardized 12 overlapping biomarkers matching user requirements
REPORT_1_BIOMARKERS = [
    ("Hemoglobin", "13.2", "g/dL", "12.0 - 16.0"),
    ("Fasting Blood Glucose", "96", "mg/dL", "70 - 99"),
    ("Total Cholesterol", "185", "mg/dL", "< 200"),
    ("HDL Cholesterol", "48", "mg/dL", "> 40"),
    ("LDL Cholesterol", "110", "mg/dL", "< 100"),
    ("Triglycerides", "135", "mg/dL", "< 150"),
    ("Vitamin D (25-OH)", "24", "ng/mL", "30 - 100"),
    ("Serum Creatinine", "0.95", "mg/dL", "0.70 - 1.30"),
    ("Blood Urea Nitrogen (BUN)", "14", "mg/dL", "7 - 20"),
    ("White Blood Cell Count (WBC)", "6.8", "10^3/µL", "4.5 - 11.0"),
    ("Red Blood Cell Count (RBC)", "4.75", "10^6/µL", "4.3 - 5.9"),
    ("Platelet Count", "240", "10^3/µL", "150 - 450")
]

REPORT_2_BIOMARKERS = [
    ("Hemoglobin", "13.5", "g/dL", "12.0 - 16.0"),
    ("Fasting Blood Glucose", "102", "mg/dL", "70 - 99"),
    ("Total Cholesterol", "178", "mg/dL", "< 200"),
    ("HDL Cholesterol", "51", "mg/dL", "> 40"),
    ("LDL Cholesterol", "104", "mg/dL", "< 100"),
    ("Triglycerides", "125", "mg/dL", "< 150"),
    ("Vitamin D (25-OH)", "28", "ng/mL", "30 - 100"),
    ("Serum Creatinine", "0.98", "mg/dL", "0.70 - 1.30"),
    ("Blood Urea Nitrogen (BUN)", "15", "mg/dL", "7 - 20"),
    ("White Blood Cell Count (WBC)", "7.2", "10^3/µL", "4.5 - 11.0"),
    ("Red Blood Cell Count (RBC)", "4.82", "10^6/µL", "4.3 - 5.9"),
    ("Platelet Count", "255", "10^3/µL", "150 - 450")
]

REPORT_3_BIOMARKERS = [
    ("Hemoglobin", "13.8", "g/dL", "12.0 - 16.0"),
    ("Fasting Blood Glucose", "94", "mg/dL", "70 - 99"),
    ("Total Cholesterol", "172", "mg/dL", "< 200"),
    ("HDL Cholesterol", "54", "mg/dL", "> 40"),
    ("LDL Cholesterol", "98", "mg/dL", "< 100"),
    ("Triglycerides", "118", "mg/dL", "< 150"),
    ("Vitamin D (25-OH)", "31", "ng/mL", "30 - 100"),
    ("Serum Creatinine", "0.92", "mg/dL", "0.70 - 1.30"),
    ("Blood Urea Nitrogen (BUN)", "13", "mg/dL", "7 - 20"),
    ("White Blood Cell Count (WBC)", "6.5", "10^3/µL", "4.5 - 11.0"),
    ("Red Blood Cell Count (RBC)", "4.90", "10^6/µL", "4.3 - 5.9"),
    ("Platelet Count", "248", "10^3/µL", "150 - 450")
]

REPORTS_DATA = [
    # sample-report files
    {
        "filename": "sample-report-1.pdf",
        "date_str": "January 15, 2026",
        "iso_date": "2026-01-15",
        "patient": "John Doe (Demo Patient)",
        "patient_id": "REG-8841",
        "age_gender": "42 Y / Male",
        "referred_by": "Dr. Sarah Jenkins, MD",
        "biomarkers": REPORT_1_BIOMARKERS
    },
    {
        "filename": "sample-report-2.pdf",
        "date_str": "March 20, 2026",
        "iso_date": "2026-03-20",
        "patient": "John Doe (Demo Patient)",
        "patient_id": "REG-8841",
        "age_gender": "42 Y / Male",
        "referred_by": "Dr. Sarah Jenkins, MD",
        "biomarkers": REPORT_2_BIOMARKERS
    },
    {
        "filename": "sample-report-3.pdf",
        "date_str": "June 10, 2026",
        "iso_date": "2026-06-10",
        "patient": "John Doe (Demo Patient)",
        "patient_id": "REG-8841",
        "age_gender": "42 Y / Male",
        "referred_by": "Dr. Sarah Jenkins, MD",
        "biomarkers": REPORT_3_BIOMARKERS
    },
    # Also keep report-1, report-2, report-3 for backwards compatibility
    {
        "filename": "report-1.pdf",
        "date_str": "January 15, 2026",
        "iso_date": "2026-01-15",
        "patient": "John Doe (Demo Patient)",
        "patient_id": "REG-8841",
        "age_gender": "42 Y / Male",
        "referred_by": "Dr. Sarah Jenkins, MD",
        "biomarkers": REPORT_1_BIOMARKERS
    },
    {
        "filename": "report-2.pdf",
        "date_str": "March 20, 2026",
        "iso_date": "2026-03-20",
        "patient": "John Doe (Demo Patient)",
        "patient_id": "REG-8841",
        "age_gender": "42 Y / Male",
        "referred_by": "Dr. Sarah Jenkins, MD",
        "biomarkers": REPORT_2_BIOMARKERS
    },
    {
        "filename": "report-3.pdf",
        "date_str": "June 10, 2026",
        "iso_date": "2026-06-10",
        "patient": "John Doe (Demo Patient)",
        "patient_id": "REG-8841",
        "age_gender": "42 Y / Male",
        "referred_by": "Dr. Sarah Jenkins, MD",
        "biomarkers": REPORT_3_BIOMARKERS
    }
]

def generate_pdf(rep: dict):
    out_path = os.path.join(SAMPLE_DIR, rep["filename"])
    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F766E'),
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#64748B')
    )

    disclaimer_style = ParagraphStyle(
        'DemoBanner',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#DC2626'),
        fontName='Helvetica-Bold',
        alignment=1
    )

    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1E293B')
    )

    cell_normal = ParagraphStyle(
        'CellNormal',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#334155')
    )

    elements = []

    # Demo Banner
    banner_data = [[
        Paragraph("<b>SAMPLE / DEMONSTRATION DATA — NOT A REAL MEDICAL REPORT</b>", disclaimer_style)
    ]]
    banner_table = Table(banner_data, colWidths=[540])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEE2E2')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#F87171')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(banner_table)
    elements.append(Spacer(1, 10))

    # Header
    header_data = [
        [
            Paragraph("<b>APEX DIAGNOSTIC LABORATORIES</b>", title_style),
            Paragraph(f"<b>Report Date:</b> {rep['date_str']}<br/><b>Collection Date:</b> {rep['date_str']}", cell_normal)
        ],
        [
            Paragraph("ISO 15189 Certified Clinical Diagnostics Facility | Ph: +1 (800) 555-APEX", subtitle_style),
            Paragraph("<b>Status:</b> Final Verified", cell_normal)
        ]
    ]
    header_table = Table(header_data, colWidths=[360, 180])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 8))

    # Patient info
    patient_data = [
        [
            Paragraph(f"<b>Patient Name:</b> {rep['patient']}", cell_normal),
            Paragraph(f"<b>Patient ID:</b> {rep['patient_id']}", cell_normal),
            Paragraph(f"<b>Age / Sex:</b> {rep['age_gender']}", cell_normal)
        ],
        [
            Paragraph(f"<b>Referred By:</b> {rep['referred_by']}", cell_normal),
            Paragraph("<b>Sample Type:</b> Whole Blood (EDTA/Serum)", cell_normal),
            Paragraph("<b>Barcode:</b> 998822104", cell_normal)
        ]
    ]
    patient_table = Table(patient_data, colWidths=[180, 180, 180])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(patient_table)
    elements.append(Spacer(1, 14))

    # Biomarkers Table
    panel_title = Paragraph("<b>COMPREHENSIVE METABOLIC & HEMATOLOGY PANEL</b>", cell_bold)
    elements.append(panel_title)
    elements.append(Spacer(1, 4))

    table_rows = [
        [
            Paragraph("<b>Biomarker</b>", cell_bold),
            Paragraph("<b>Value</b>", cell_bold),
            Paragraph("<b>Unit</b>", cell_bold),
            Paragraph("<b>Reference Range</b>", cell_bold)
        ]
    ]

    for name, val, unit, ref in rep["biomarkers"]:
        table_rows.append([
            Paragraph(name, cell_normal),
            Paragraph(f"<b>{val}</b>", cell_bold),
            Paragraph(unit, cell_normal),
            Paragraph(ref, cell_normal)
        ])

    results_table = Table(table_rows, colWidths=[200, 100, 100, 140])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E0F2FE')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0369A1')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    elements.append(results_table)
    elements.append(Spacer(1, 20))

    # Footer Signoff
    footer_data = [
        [
            Paragraph("<i>*** End of Report ***<br/>Organized and rendered for laboratory visualization demonstration.</i>", subtitle_style),
            Paragraph("<b>Dr. Robert Chen, MD, Pathologist</b><br/>Electronic Sign-off Verified", subtitle_style)
        ]
    ]
    footer_table = Table(footer_data, colWidths=[340, 200])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(footer_table)

    doc.build(elements)
    print(f"Generated: {out_path}")

if __name__ == "__main__":
    for r in REPORTS_DATA:
        generate_pdf(r)
