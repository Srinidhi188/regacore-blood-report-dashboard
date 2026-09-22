from typing import List, Dict, Optional
from collections import defaultdict
from app.models.report_models import (
    Report,
    HistoricalPoint,
    BiomarkerHistory,
    BiomarkerTableRow,
    DashboardSummary,
    AnalyzeResponse
)
from app.utils.logger import get_logger

logger = get_logger(__name__)

def build_analysis_response(reports: List[Report], initial_warnings: Optional[List[str]] = None) -> AnalyzeResponse:
    """
    Consolidates parsed reports into a comprehensive analysis response:
    1. Sorts reports chronologically by report date (with fallback to uploaded order).
    2. Groups biomarkers across all reports by their normalized key.
    3. Generates date-wise historical tracking series for each biomarker.
    4. Calculates previous values, deltas (+/-), and status.
    5. Formulates summary metrics and detailed table rows.
    """
    warnings = list(initial_warnings) if initial_warnings else []

    # Sort reports chronologically: reports with dates first (ascending), followed by reports without dates
    sorted_reports = sorted(
        reports,
        key=lambda r: (0, r.reportDate) if r.reportDate else (1, r.id)
    )

    # Track all biomarker points per normalized key
    # key -> list of (report_date_or_seq, Biomarker, Report)
    biomarkers_by_key: Dict[str, List] = defaultdict(list)

    for report in sorted_reports:
        # Collect warnings from individual reports
        for w in report.warnings:
            if w not in warnings:
                warnings.append(f"{report.fileName}: {w}")

        for bm in report.biomarkers:
            biomarkers_by_key[bm.normalizedName].append({
                "report": report,
                "biomarker": bm
            })

    historical_trends: Dict[str, BiomarkerHistory] = {}
    table_rows: List[BiomarkerTableRow] = []

    for norm_key, records in biomarkers_by_key.items():
        # Representative sample for metadata
        first_bm = records[0]["biomarker"]
        last_record = records[-1]
        latest_bm = last_record["biomarker"]
        latest_report = last_record["report"]

        # Build chronological points list (filtering out null numeric values)
        points: List[HistoricalPoint] = []
        for rec in records:
            bm = rec["biomarker"]
            rep = rec["report"]
            if bm.value is not None:
                pt_date = rep.reportDate if rep.reportDate else f"Report ({rep.fileName})"
                points.append(
                    HistoricalPoint(
                        reportId=rep.id,
                        reportDate=pt_date,
                        fileName=rep.fileName,
                        value=bm.value,
                        unit=bm.unit or first_bm.unit,
                        referenceRange=bm.referenceRange or first_bm.referenceRange
                    )
                )

        # Compute delta from previous report
        latest_val = latest_bm.value
        prev_val: Optional[float] = None
        change: Optional[float] = None
        change_pct: Optional[float] = None

        if len(points) >= 2:
            prev_point = points[-2]
            prev_val = prev_point.value
            if latest_val is not None and prev_val is not None:
                change = round(latest_val - prev_val, 2)
                if prev_val != 0:
                    change_pct = round((change / prev_val) * 100, 1)

        history_item = BiomarkerHistory(
            normalizedName=norm_key,
            displayName=latest_bm.displayName or first_bm.displayName,
            category=latest_bm.category or first_bm.category or "General",
            unit=latest_bm.unit or first_bm.unit,
            referenceRange=latest_bm.referenceRange or first_bm.referenceRange,
            latestValue=latest_val,
            latestDate=latest_report.reportDate,
            previousValue=prev_val,
            change=change,
            changePercent=change_pct,
            points=points,
            refLow=latest_bm.refLow,
            refHigh=latest_bm.refHigh
        )
        historical_trends[norm_key] = history_item

        table_rows.append(
            BiomarkerTableRow(
                key=norm_key,
                displayName=history_item.displayName,
                category=history_item.category,
                latestValue=latest_val,
                unit=history_item.unit,
                referenceRange=history_item.referenceRange,
                latestReportDate=latest_report.reportDate,
                previousValue=prev_val,
                change=change,
                status=latest_bm.status or "unspecified",
                pointsCount=len(points)
            )
        )

    # Sort table rows alphabetically by display name or category
    table_rows.sort(key=lambda r: (r.category, r.displayName))

    # Calculate summary
    valid_dates = [r.reportDate for r in sorted_reports if r.reportDate]
    latest_date = valid_dates[-1] if valid_dates else None
    earliest_date = valid_dates[0] if valid_dates else None
    
    date_range_text = None
    if earliest_date and latest_date:
        if earliest_date == latest_date:
            date_range_text = earliest_date
        else:
            date_range_text = f"{earliest_date} to {latest_date}"

    summary = DashboardSummary(
        totalReports=len(sorted_reports),
        uniqueBiomarkers=len(biomarkers_by_key),
        latestReportDate=latest_date,
        earliestReportDate=earliest_date,
        dateRangeText=date_range_text
    )

    return AnalyzeResponse(
        reports=sorted_reports,
        summary=summary,
        historicalTrends=historical_trends,
        biomarkersTable=table_rows,
        warnings=warnings
    )
