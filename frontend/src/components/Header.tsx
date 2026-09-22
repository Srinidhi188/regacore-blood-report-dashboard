import React from 'react';
import { Activity, Upload, Sparkles, ShieldAlert } from 'lucide-react';

interface HeaderProps {
  onUploadClick: () => void;
  onLoadSamplesClick: () => void;
  isLoading: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  onUploadClick,
  onLoadSamplesClick,
  isLoading,
}) => {
  return (
    <header className="sticky top-0 z-30 bg-white/90 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        {/* Brand & Title */}
        <div className="flex items-center space-x-3.5">
          <div className="w-10 h-10 rounded-xl bg-teal-600 text-white flex items-center justify-center shadow-sm shadow-teal-700/20">
            <Activity className="w-6 h-6 stroke-[2.2]" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-bold uppercase tracking-wider text-teal-700 bg-teal-50 px-2 py-0.5 rounded border border-teal-200/60">
                Regacore
              </span>
              <span className="text-xs text-slate-400 font-medium">Health Analytics MVP</span>
            </div>
            <h1 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
              Blood Report Dashboard
            </h1>
            <p className="text-xs sm:text-sm text-slate-500">
              Upload your blood reports to track biomarker changes over time.
            </p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center flex-wrap gap-2.5">
          <button
            type="button"
            onClick={onLoadSamplesClick}
            disabled={isLoading}
            className="inline-flex items-center space-x-1.5 px-3.5 py-2 text-xs sm:text-sm font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 active:bg-slate-300 rounded-lg transition-colors disabled:opacity-50 cursor-pointer"
            title="Load the 3 built-in sample reports to test historical tracking instantly"
          >
            <Sparkles className="w-4 h-4 text-teal-600" />
            <span>Load Demo Reports</span>
          </button>

          <button
            type="button"
            onClick={onUploadClick}
            disabled={isLoading}
            className="inline-flex items-center space-x-1.5 px-4 py-2 text-xs sm:text-sm font-semibold text-white bg-teal-600 hover:bg-teal-700 active:bg-teal-800 rounded-lg shadow-sm transition-all disabled:opacity-50 cursor-pointer"
          >
            <Upload className="w-4 h-4" />
            <span>Upload Reports</span>
          </button>
        </div>
      </div>

      {/* Subtle Safety Strip */}
      <div className="bg-amber-50/70 border-t border-b border-amber-200/50 px-4 py-1 text-center">
        <p className="text-[11px] sm:text-xs text-amber-800 font-medium flex items-center justify-center space-x-1.5">
          <ShieldAlert className="w-3.5 h-3.5 text-amber-600 inline shrink-0" />
          <span>Notice: This dashboard is for organizing and visualizing laboratory report data. It is not medical advice.</span>
        </p>
      </div>
    </header>
  );
};
