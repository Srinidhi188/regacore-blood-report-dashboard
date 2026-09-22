# Regacore Blood Report Dashboard

An AI-powered, full-stack laboratory report analysis and visualization system. This application allows users to upload digital PDF blood test reports, extracts text and tabular biomarker measurements, normalizes names across multiple reporting standards, tracks longitudinal changes date-wise, and renders interactive time-series visualizations.

> **Medical Disclaimer:** This dashboard is strictly designed for organizing and visualizing laboratory report data. It does not provide medical advice, diagnosis, treatment recommendations, or risk evaluations.

---

## Overview

Clinical laboratory blood reports frequently originate from different facilities with varying terminology, formatting conventions, and reference intervals (e.g. `Hb` vs `Hemoglobin`, `FBS` vs `Fasting Blood Glucose`).

**Regacore Blood Report Dashboard** bridges this gap:
1. **Multi-Report Upload**: Drag and drop single or multiple lab reports simultaneously.
2. **Intelligent Text & Table Extraction**: Uses PyMuPDF (`pymupdf`) to parse tabular results and unstructured text.
3. **Biomarker Normalization**: Standardizes aliases into canonical medical representations with fallback preservation of unknown tests.
4. **Automated Date Extraction**: Identifies collection and report dates in ISO (`YYYY-MM-DD`), European (`DD/MM/YYYY`), and written formats.
5. **Historical Timeline Tracking**: Matches identical biomarkers across chronological dates, computing relative deltas.
6. **Dynamic Visualization**: Renders interactive time-series charts with reference intervals and custom tooltips via Recharts.

---

## Architecture

```
regacore-blood-dashboard/
├── frontend/                     # React + Vite + TypeScript Single Page App
│   ├── src/
│   │   ├── components/           # Modular UI components (Header, Upload, Trends, Cards, Table, History)
│   │   ├── hooks/                # useReportAnalysis state orchestration
│   │   ├── services/             # API client with VITE_API_BASE_URL
│   │   ├── types/                # Strongly typed shared models
│   │   ├── utils/                # Date, delta, and status formatters
│   │   ├── App.tsx               # Primary dashboard layout
│   │   └── main.tsx              # Entrypoint
│   ├── package.json
│   ├── vite.config.ts            # Vite 8 + Tailwind CSS v4 setup
│   └── vercel.json               # Vercel SPA routing configuration
│
├── backend/                      # FastAPI Python Application
│   ├── app/
│   │   ├── main.py               # FastAPI entry, CORS middleware, health check
│   │   ├── routes/               # API route definitions (/api/reports)
│   │   ├── models/               # Pydantic schemas (Report, Biomarker, AnalyzeResponse)
│   │   ├── parsers/              # PyMuPDF parser, date extractor, regex & anchor tables
│   │   ├── services/             # Canonical normalization registry & history alignment
│   │   └── utils/                # Logging utilities
│   ├── tests/                    # Automated test suites (test_extraction.py, test_api.py)
│   ├── requirements.txt          # Python dependencies
│   └── Dockerfile                # Container definition
│
├── sample-reports/               # Realistic demonstration PDFs with overlapping dates
│   ├── generate_sample_reports.py# ReportLab generator for test datasets
│   ├── report-1.pdf              # Report Date: January 15, 2026
│   ├── report-2.pdf              # Report Date: March 20, 2026
│   └── report-3.pdf              # Report Date: June 10, 2026
│
├── render.yaml                   # Cloud deployment blueprint
├── README.md                     # Documentation
└── .gitignore
```

---

## Tech Stack

### Frontend
- **Framework**: React 19 + TypeScript
- **Tooling**: Vite
- **Styling**: Tailwind CSS v4 (Modern healthcare design, accessible contrast)
- **Charts**: Recharts (ResponsiveContainer, LineChart, ReferenceLine)
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI (Python 3.12)
- **PDF Engine**: PyMuPDF (`pymupdf`)
- **Data Validation**: Pydantic v2
- **PDF Generator**: ReportLab (for realistic sample generation)
- **Server**: Uvicorn

---

## Features

- **Drag-and-Drop Upload**: Multi-file drop zone accepting PDF blood reports with file removal and real-time status badges.
- **1-Click Demo Mode**: Immediate "Load Demo Reports" button allowing evaluators to test all features in one click without manually picking files.
- **Live Multi-Step Loader**: Visual progress indicators tracking *Uploading -> Extracting Text -> Detecting Biomarkers -> Organizing History -> Generating Dashboard*.
- **Summary Metrics**: High-level counts of total reports analyzed, unique biomarkers, date range, and historical trends.
- **Biomarker Highlights Cards**: Displays latest value, units, reference range, previous measurement, and neutral change (`+0.3 g/dL`).
- **Interactive Biomarker Trends**:
  - Dropdown selector for any detected biomarker.
  - Interactive line chart with hover tooltips displaying date, value, unit, and source filename.
  - Dashed reference interval lines (Lower and Upper reference limits).
  - Quick-preset selectors for common panels (Hemoglobin, Glucose, Cholesterol, Vitamin D).
- **Responsive Comparison Table**:
  - Columns: Biomarker, Latest Value, Unit, Reference Range, Report Date, Previous Value, Change.
  - Search filter and category panel filtering.
  - Mobile card transformation for viewports down to 390px.
- **Chronological Report History**:
  - Interactive timeline of all processed reports.
  - Detailed modal inspection showing all raw extracted parameters and extraction notices per report.

---

## Local Setup

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Clone & Enter Project
```bash
git clone <repository-url>
cd RegacoreAssignment
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS / Linux:
source venv/bin/activate

pip install -r requirements.txt

# Start backend server on http://localhost:8000
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup
In a new terminal window:
```bash
cd frontend
npm install

# Start Vite dev server on http://localhost:5173
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## Environment Variables

### Frontend (`frontend/.env`)
```ini
VITE_API_BASE_URL=http://localhost:8000
```
*Note: In production (e.g. Vercel), set this to your deployed backend URL on Render.*

### Backend (`backend/.env`)
```ini
PORT=8000
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,https://<your-frontend>.vercel.app
```

---

## API Endpoints

### `POST /api/reports/analyze`
Accepts `multipart/form-data` with one or multiple PDF files (`files`).
Returns structured JSON:
```json
{
  "reports": [
    {
      "id": "rep_2cd3306b",
      "fileName": "report-1.pdf",
      "reportDate": "2026-01-15",
      "biomarkers": [
        {
          "name": "Hemoglobin (Hb)",
          "normalizedName": "hemoglobin",
          "displayName": "Hemoglobin",
          "value": 13.2,
          "unit": "g/dL",
          "referenceRange": "12.0 - 16.0",
          "category": "Complete Blood Count",
          "status": "normal"
        }
      ]
    }
  ],
  "summary": {
    "totalReports": 3,
    "uniqueBiomarkers": 12,
    "latestReportDate": "2026-06-10",
    "earliestReportDate": "2026-01-15",
    "dateRangeText": "2026-01-15 to 2026-06-10"
  },
  "historicalTrends": {
    "hemoglobin": {
      "displayName": "Hemoglobin",
      "latestValue": 13.8,
      "previousValue": 13.5,
      "change": 0.3,
      "points": [
        { "reportDate": "2026-01-15", "value": 13.2 },
        { "reportDate": "2026-03-20", "value": 13.5 },
        { "reportDate": "2026-06-10", "value": 13.8 }
      ]
    }
  }
}
```

### `GET /api/reports/sample-data`
Returns pre-processed historical analysis of the 3 built-in sample reports for 1-click exploration.

### `GET /api/reports/download-sample/{filename}`
Streams the sample PDF report (`report-1.pdf`, `report-2.pdf`, `report-3.pdf`) for manual upload testing.

### `GET /api/health`
Returns health status (`{"status": "healthy"}`).

---

## Sample Reports Demonstration

Three realistic sample PDF reports are pre-generated in `sample-reports/`:
- **`report-1.pdf`** — January 15, 2026
- **`report-2.pdf`** — March 20, 2026
- **`report-3.pdf`** — June 10, 2026

To regenerate them at any time:
```bash
python sample-reports/generate_sample_reports.py
```

These sample reports test overlapping biomarkers across time:
- **Hemoglobin**: `13.2` → `13.5` → `13.8` g/dL
- **Fasting Glucose**: `96` → `102` → `94` mg/dL
- **Total Cholesterol**: `185` → `178` → `172` mg/dL
- **Vitamin D**: `24` → `28` → `31` ng/mL
- **Creatinine**: `0.95` → `0.98` → `0.92` mg/dL

---

## Automated Tests

Run backend extraction and API test suites:
```bash
# Test extraction & history normalization
python backend/tests/test_extraction.py

# Test FastAPI endpoints & error handlers
python backend/tests/test_api.py

# Test frontend production build
cd frontend && npm run build
```

---

## Deployment

### Frontend (Vercel)
1. Push this repository to GitHub.
2. Import project into Vercel and select root directory `frontend`.
3. Set environment variable:
   `VITE_API_BASE_URL=https://<your-render-backend-url>`
4. Deploy. `vercel.json` ensures SPA client-side routes resolve properly.

### Backend (Render)
1. In Render, select **New Web Service** pointing to your repository.
2. Root Directory: `backend`
3. Environment: `Python`
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add Environment Variable: `CORS_ORIGINS=*` (or your Vercel URL).

Alternatively, deploy using the included `render.yaml` blueprint or Dockerfile.

---

## Limitations

- **Scanned Images / Handwritten Notes**: The core engine expects digital PDF files containing text and vector tables. Extremely low-resolution scanned documents without optical text streams require additional OCR pre-processing.
- **Reference Range Formatting**: Unconventional or multi-paragraph reference intervals are preserved as strings, while numeric intervals (e.g. `12.0 - 16.0`) are automatically parsed into lower and upper bounds.

---

## Future Improvements

- User accounts and encrypted cloud report storage (HIPAA/GDPR compliant).
- Export dashboard analysis as a consolidated PDF summary report.
- Multi-language laboratory report support.
- Configurable unit converter (e.g. converting `mmol/L` to `mg/dL`).

---

## Screenshots

*(Placeholders for application walkthrough screenshots)*

| Drag & Drop Upload | Interactive Trends Chart |
|---|---|
| *Multi-report upload with file statuses* | *Longitudinal time-series with reference lines* |

| Detailed Comparison Table | Report History Modal |
|---|---|
| *Search, sorting & category filters* | *Per-report raw extraction inspection* |
