export interface Biomarker {
  name: string;
  normalizedName: string;
  displayName: string;
  value: number | null;
  unit: string | null;
  referenceRange: string | null;
  category?: string;
  status?: 'normal' | 'low' | 'high' | 'unspecified';
  refLow?: number | null;
  refHigh?: number | null;
}

export interface Report {
  id: string;
  fileName: string;
  reportDate: string | null;
  biomarkers: Biomarker[];
  rawTextSample?: string | null;
  warnings?: string[];
}

export interface HistoricalPoint {
  reportId: string;
  reportDate: string;
  fileName: string;
  value: number;
  unit?: string | null;
  referenceRange?: string | null;
}

export interface BiomarkerHistory {
  normalizedName: string;
  displayName: string;
  category: string;
  unit?: string | null;
  referenceRange?: string | null;
  latestValue?: number | null;
  latestDate?: string | null;
  previousValue?: number | null;
  change?: number | null;
  changePercent?: number | null;
  points: HistoricalPoint[];
  refLow?: number | null;
  refHigh?: number | null;
}

export interface BiomarkerTableRow {
  key: string;
  displayName: string;
  category: string;
  latestValue: number | null;
  unit: string | null;
  referenceRange: string | null;
  latestReportDate: string | null;
  previousValue: number | null;
  change: number | null;
  status: 'normal' | 'low' | 'high' | 'unspecified';
  pointsCount: number;
}

export interface DashboardSummary {
  totalReports: number;
  uniqueBiomarkers: number;
  latestReportDate: string | null;
  earliestReportDate: string | null;
  dateRangeText: string | null;
}

export interface AnalyzeResponse {
  reports: Report[];
  summary: DashboardSummary;
  historicalTrends: Record<string, BiomarkerHistory>;
  biomarkersTable: BiomarkerTableRow[];
  warnings: string[];
}

export interface SelectedFileItem {
  id: string;
  file: File;
  name: string;
  size: number;
  status: 'pending' | 'uploading' | 'completed' | 'error';
  errorMessage?: string;
}

export type ProcessingStepKey = 
  | 'uploading'
  | 'extracting'
  | 'detecting'
  | 'organizing'
  | 'generating';

export interface StepIndicatorItem {
  key: ProcessingStepKey;
  label: string;
  status: 'upcoming' | 'current' | 'completed';
}
