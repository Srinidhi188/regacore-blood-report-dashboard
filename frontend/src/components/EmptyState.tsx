import React from 'react';
import { FileUp, Sparkles, Activity, ShieldCheck } from 'lucide-react';

interface EmptyStateProps {
  onUploadClick: () => void;
  onLoadSamplesClick: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  onUploadClick,
  onLoadSamplesClick,
}) => {
  return (
    <div className="bg-white rounded-3xl border border-slate-200/80 p-8 sm:p-14 text-center max-w-2xl mx-auto shadow-xs">
      <div className="w-16 h-16 rounded-3xl bg-teal-50 text-teal-600 border border-teal-100/80 flex items-center justify-center mx-auto mb-5">
        <Activity className="w-8 h-8 stroke-[2]" />
      </div>

      <h3 className="text-xl sm:text-2xl font-bold text-slate-900">
        No blood reports analyzed yet
      </h3>

      <p className="text-sm text-slate-500 mt-2 max-w-md mx-auto">
        Upload one or more PDF blood reports to extract biomarkers, match historical records, and view interactive longitudinal trend charts.
      </p>

      {/* Feature highlights */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 my-8 text-left text-xs text-slate-600">
        <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/60">
          <p className="font-semibold text-slate-800">Automatic Extraction</p>
          <p className="text-slate-500 mt-1">Parses biomarker names, numeric values, units & ranges.</p>
        </div>
        <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/60">
          <p className="font-semibold text-slate-800">Biomarker Normalization</p>
          <p className="text-slate-500 mt-1">Confidently maps aliases (e.g. Hb → Hemoglobin).</p>
        </div>
        <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/60">
          <p className="font-semibold text-slate-800">Time-Series Trends</p>
          <p className="text-slate-500 mt-1">Tracks and plots changes across multiple lab dates.</p>
        </div>
      </div>

      {/* Action CTA buttons */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
        <button
          type="button"
          onClick={onUploadClick}
          className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-6 py-3 rounded-xl font-semibold text-white bg-teal-600 hover:bg-teal-700 active:bg-teal-800 shadow-sm transition-all cursor-pointer text-sm"
        >
          <FileUp className="w-4 h-4" />
          <span>Upload Reports</span>
        </button>

        <button
          type="button"
          onClick={onLoadSamplesClick}
          className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-6 py-3 rounded-xl font-semibold text-teal-800 bg-teal-50 hover:bg-teal-100 active:bg-teal-200 border border-teal-200 transition-colors cursor-pointer text-sm"
        >
          <Sparkles className="w-4 h-4 text-teal-600" />
          <span>Load 3 Demo Reports</span>
        </button>
      </div>

      <div className="mt-8 pt-6 border-t border-slate-100 flex items-center justify-center space-x-2 text-xs text-slate-400">
        <ShieldCheck className="w-4 h-4 text-slate-400" />
        <span>Privacy first: Files are processed securely in memory for report synthesis.</span>
      </div>
    </div>
  );
};
