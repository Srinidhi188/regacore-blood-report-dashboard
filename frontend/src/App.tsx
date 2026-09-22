import React, { useRef } from 'react';
import { Header } from './components/Header';
import { FileUpload } from './components/FileUpload';
import { ProcessingState } from './components/ProcessingState';
import { DashboardMetrics } from './components/DashboardMetrics';
import { BiomarkerCards } from './components/BiomarkerCards';
import { BiomarkerTrends } from './components/BiomarkerTrends';
import { BiomarkerTable } from './components/BiomarkerTable';
import { ReportHistory } from './components/ReportHistory';
import { ReportDetailModal } from './components/ReportDetailModal';
import { EmptyState } from './components/EmptyState';
import { Footer } from './components/Footer';
import { useReportAnalysis } from './hooks/useReportAnalysis';
import { AlertTriangle, ChevronUp, ChevronDown } from 'lucide-react';

export function App() {
  const {
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
  } = useReportAnalysis();

  const [showUploadDrawer, setShowUploadDrawer] = React.useState(true);
  const uploadSectionRef = useRef<HTMLDivElement>(null);

  const scrollToUpload = () => {
    setShowUploadDrawer(true);
    uploadSectionRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Count biomarkers with >1 historical points
  const multiPointCount = analysisData 
    ? Object.values(analysisData.historicalTrends).filter((t) => t.points.length > 1).length
    : 0;

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col selection:bg-teal-500 selection:text-white">
      {/* Global Header */}
      <Header
        onUploadClick={scrollToUpload}
        onLoadSamplesClick={loadSampleData}
        isLoading={isLoading}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Upload Section Wrapper */}
        <div ref={uploadSectionRef} className="space-y-4">
          {analysisData && (
            <div className="flex items-center justify-between bg-white px-5 py-3 rounded-2xl border border-slate-200 shadow-xs">
              <span className="text-xs sm:text-sm font-semibold text-slate-700">
                Upload New Blood Reports
              </span>
              <button
                type="button"
                onClick={() => setShowUploadDrawer(!showUploadDrawer)}
                className="text-xs font-semibold text-teal-600 hover:text-teal-700 inline-flex items-center space-x-1 cursor-pointer"
              >
                <span>{showUploadDrawer ? 'Hide Upload Area' : 'Upload Additional Reports'}</span>
                {showUploadDrawer ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
              </button>
            </div>
          )}

          {(!analysisData || showUploadDrawer) && (
            <FileUpload
              files={files}
              onFilesSelected={addFiles}
              onRemoveFile={removeFile}
              onClearFiles={clearFiles}
              onAnalyze={runAnalysis}
              onLoadSamples={loadSampleData}
              isLoading={isLoading}
              errorMessage={errorMessage}
            />
          )}
        </div>

        {/* Global Warnings Banner from Extraction */}
        {analysisData && analysisData.warnings && analysisData.warnings.length > 0 && (
          <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 text-amber-900 text-xs sm:text-sm flex items-start space-x-3">
            <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="font-bold text-amber-900">Extraction Observations</p>
              <ul className="list-disc list-inside mt-1 space-y-0.5 text-amber-800 text-xs">
                {analysisData.warnings.map((warn, i) => (
                  <li key={i}>{warn}</li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {/* Loading Progress State */}
        {isLoading && (
          <ProcessingState steps={steps} progressPercent={progressPercent} />
        )}

        {/* Empty State when no analysis performed yet */}
        {!analysisData && !isLoading && (
          <EmptyState
            onUploadClick={scrollToUpload}
            onLoadSamplesClick={loadSampleData}
          />
        )}

        {/* Dashboard Content */}
        {analysisData && !isLoading && (
          <div className="space-y-8 animate-in fade-in duration-300">
            {/* 1. High-level Summary Metrics */}
            <DashboardMetrics
              summary={analysisData.summary}
              trackedCount={multiPointCount}
            />

            {/* 2. Interactive Time-Series Charts */}
            <BiomarkerTrends
              trends={analysisData.historicalTrends}
              selectedBiomarkerKey={selectedBiomarkerKey}
              onSelectBiomarker={setSelectedBiomarkerKey}
            />

            {/* 3. Biomarker Highlight Cards */}
            <BiomarkerCards
              trends={analysisData.historicalTrends}
              selectedBiomarkerKey={selectedBiomarkerKey}
              onSelectBiomarker={(key) => {
                setSelectedBiomarkerKey(key);
                const elem = document.getElementById('trends-section');
                elem?.scrollIntoView({ behavior: 'smooth' });
              }}
            />

            {/* 4. Detailed Biomarker Table */}
            <BiomarkerTable
              rows={analysisData.biomarkersTable}
              selectedKey={selectedBiomarkerKey}
              onSelectBiomarker={(key) => {
                setSelectedBiomarkerKey(key);
                const elem = document.getElementById('trends-section');
                elem?.scrollIntoView({ behavior: 'smooth' });
              }}
            />

            {/* 5. Chronological Report History */}
            <ReportHistory
              reports={analysisData.reports}
              onSelectReport={setSelectedReportModal}
            />
          </div>
        )}
      </main>

      {/* Report Details Modal */}
      <ReportDetailModal
        report={selectedReportModal}
        onClose={() => setSelectedReportModal(null)}
      />

      {/* Global Footer */}
      <Footer />
    </div>
  );
}

export default App;
