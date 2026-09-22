import { useState, useCallback } from 'react';
import { 
  SelectedFileItem, 
  AnalyzeResponse, 
  Report, 
  StepIndicatorItem, 
  ProcessingStepKey 
} from '../types';
import { analyzeReportsApi, fetchSampleDataApi, fetchSampleFileAsRealFile } from '../services/api';

const INITIAL_STEPS: StepIndicatorItem[] = [
  { key: 'uploading', label: 'Uploading reports', status: 'upcoming' },
  { key: 'extracting', label: 'Extracting text and tables', status: 'upcoming' },
  { key: 'detecting', label: 'Detecting and normalizing biomarkers', status: 'upcoming' },
  { key: 'organizing', label: 'Organizing historical timeline', status: 'upcoming' },
  { key: 'generating', label: 'Generating dashboard & charts', status: 'upcoming' },
];

export function useReportAnalysis() {
  const [files, setFiles] = useState<SelectedFileItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [analysisData, setAnalysisData] = useState<AnalyzeResponse | null>(null);
  const [selectedBiomarkerKey, setSelectedBiomarkerKey] = useState<string>('hemoglobin');
  const [selectedReportModal, setSelectedReportModal] = useState<Report | null>(null);
  const [steps, setSteps] = useState<StepIndicatorItem[]>(INITIAL_STEPS);
  const [progressPercent, setProgressPercent] = useState<number>(0);

  const addFiles = useCallback((newFiles: File[]) => {
    setErrorMessage(null);
    setFiles((prev) => {
      const existingNames = new Set(prev.map((f) => f.name));
      const added: SelectedFileItem[] = newFiles
        .filter((f) => !existingNames.has(f.name))
        .map((f) => ({
          id: `file_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`,
          file: f,
          name: f.name,
          size: f.size,
          status: 'pending',
        }));
      return [...prev, ...added];
    });
  }, []);

  const removeFile = useCallback((fileId: string) => {
    setFiles((prev) => prev.filter((f) => f.id !== fileId));
  }, []);

  const clearFiles = useCallback(() => {
    setFiles([]);
    setErrorMessage(null);
  }, []);

  // Simulates multi-step indicator progression smoothly
  const runProgressSimulation = async () => {
    const keys: ProcessingStepKey[] = ['uploading', 'extracting', 'detecting', 'organizing', 'generating'];
    
    for (let i = 0; i < keys.length; i++) {
      const currentKey = keys[i];
      setSteps((prev) =>
        prev.map((s) => {
          if (s.key === currentKey) return { ...s, status: 'current' };
          if (keys.indexOf(s.key) < i) return { ...s, status: 'completed' };
          return { ...s, status: 'upcoming' };
        })
      );
      setProgressPercent(Math.round(((i + 1) / keys.length) * 85));
      await new Promise((r) => setTimeout(r, 220));
    }
  };

  const runAnalysis = useCallback(async () => {
    if (files.length === 0) {
      setErrorMessage('Please select at least one PDF blood report file.');
      return;
    }

    setIsLoading(true);
    setErrorMessage(null);
    setProgressPercent(10);
    setSteps(INITIAL_STEPS);

    try {
      // Mark files as uploading
      setFiles((prev) => prev.map((f) => ({ ...f, status: 'uploading' })));

      // Trigger progress animation concurrently with upload
      const progressPromise = runProgressSimulation();
      const rawFiles = files.map((f) => f.file);
      const apiPromise = analyzeReportsApi(rawFiles);

      const [, response] = await Promise.all([progressPromise, apiPromise]);

      setProgressPercent(100);
      setSteps((prev) => prev.map((s) => ({ ...s, status: 'completed' })));
      
      // Mark files as completed
      setFiles((prev) => prev.map((f) => ({ ...f, status: 'completed' })));

      setAnalysisData(response);

      // Auto-select first available biomarker or hemoglobin if present
      const keys = Object.keys(response.historicalTrends);
      if (keys.includes('hemoglobin')) {
        setSelectedBiomarkerKey('hemoglobin');
      } else if (keys.length > 0) {
        setSelectedBiomarkerKey(keys[0]);
      }
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to analyze reports. Please check your files.');
      setFiles((prev) => prev.map((f) => ({ ...f, status: 'error' })));
    } finally {
      setIsLoading(false);
    }
  }, [files]);

  const loadSampleData = useCallback(async () => {
    setIsLoading(true);
    setErrorMessage(null);
    setProgressPercent(10);
    setSteps(INITIAL_STEPS);

    try {
      // Download the 3 real sample PDF files as File objects
      const sampleNames = ['sample-report-1.pdf', 'sample-report-2.pdf', 'sample-report-3.pdf'];
      const realFiles = await Promise.all(
        sampleNames.map((name) => fetchSampleFileAsRealFile(name))
      );

      setFiles(
        realFiles.map((f, idx) => ({
          id: `demo-${idx + 1}`,
          file: f,
          name: f.name,
          size: f.size,
          status: 'uploading' as const
        }))
      );

      const progressPromise = runProgressSimulation();
      const apiPromise = analyzeReportsApi(realFiles);

      const [, response] = await Promise.all([progressPromise, apiPromise]);

      setProgressPercent(100);
      setSteps((prev) => prev.map((s) => ({ ...s, status: 'completed' })));
      setFiles((prev) => prev.map((f) => ({ ...f, status: 'completed' as const })));

      setAnalysisData(response);

      const keys = Object.keys(response.historicalTrends);
      if (keys.includes('hemoglobin')) {
        setSelectedBiomarkerKey('hemoglobin');
      } else if (keys.length > 0) {
        setSelectedBiomarkerKey(keys[0]);
      }
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to load sample demonstration reports.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    files,
    isLoading,
    errorMessage,
    analysisData,
    selectedBiomarkerKey,
    selectedReportModal,
    steps,
    progressPercent,
    addFiles,
    removeFile,
    clearFiles,
    runAnalysis,
    loadSampleData,
    setSelectedBiomarkerKey,
    setSelectedReportModal,
  };
}
