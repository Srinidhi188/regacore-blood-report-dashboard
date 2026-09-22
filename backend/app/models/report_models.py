from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class Biomarker(BaseModel):
    name: str = Field(..., description="Original raw biomarker name from PDF")
    normalizedName: str = Field(..., description="Standardized normalized key for matching")
    displayName: str = Field(..., description="Clean, human-friendly display name")
    value: Optional[float] = Field(None, description="Numeric biomarker measurement")
    unit: Optional[str] = Field(None, description="Measurement unit (e.g. g/dL, mg/dL)")
    referenceRange: Optional[str] = Field(None, description="Reference range interval string")
    category: Optional[str] = Field("General", description="Health panel category")
    status: Optional[str] = Field("unspecified", description="Range status: normal, low, high, unspecified")
    refLow: Optional[float] = Field(None, description="Lower bound of reference range if parsed")
    refHigh: Optional[float] = Field(None, description="Upper bound of reference range if parsed")

class Report(BaseModel):
    id: str = Field(..., description="Unique ID for this report instance")
    fileName: str = Field(..., description="Uploaded PDF file name")
    reportDate: Optional[str] = Field(None, description="Extracted report date in YYYY-MM-DD format")
    biomarkers: List[Biomarker] = Field(default_factory=list, description="Extracted biomarkers")
    rawTextSample: Optional[str] = Field(None, description="Sample of extracted raw text for audit")
    warnings: List[str] = Field(default_factory=list, description="Non-fatal warnings (e.g. date ambiguity)")

class HistoricalPoint(BaseModel):
    reportId: str
    reportDate: str
    fileName: str
    value: float
    unit: Optional[str] = None
    referenceRange: Optional[str] = None

class BiomarkerHistory(BaseModel):
    normalizedName: str
    displayName: str
    category: str
    unit: Optional[str] = None
    referenceRange: Optional[str] = None
    latestValue: Optional[float] = None
    latestDate: Optional[str] = None
    previousValue: Optional[float] = None
    change: Optional[float] = None
    changePercent: Optional[float] = None
    points: List[HistoricalPoint] = Field(default_factory=list)
    refLow: Optional[float] = None
    refHigh: Optional[float] = None

class BiomarkerTableRow(BaseModel):
    key: str
    displayName: str
    category: str
    latestValue: Optional[float] = None
    unit: Optional[str] = None
    referenceRange: Optional[str] = None
    latestReportDate: Optional[str] = None
    previousValue: Optional[float] = None
    change: Optional[float] = None
    status: str = "unspecified"
    pointsCount: int = 0

class DashboardSummary(BaseModel):
    totalReports: int
    uniqueBiomarkers: int
    latestReportDate: Optional[str] = None
    earliestReportDate: Optional[str] = None
    dateRangeText: Optional[str] = None

class AnalyzeResponse(BaseModel):
    reports: List[Report]
    summary: DashboardSummary
    historicalTrends: Dict[str, BiomarkerHistory]
    biomarkersTable: List[BiomarkerTableRow]
    warnings: List[str] = Field(default_factory=list)
