import React, { useRef, useState } from 'react';
import { 
  UploadCloud, 
  FileText, 
  X, 
  CheckCircle2, 
  AlertCircle, 
  ArrowRight,
  Sparkles,
  FileCheck
} from 'lucide-react';
import { SelectedFileItem } from '../types';
import { formatFileSize } from '../utils/formatters';

interface FileUploadProps {
  files: SelectedFileItem[];
  onFilesSelected: (newFiles: File[]) => void;
  onRemoveFile: (fileId: string) => void;
  onClearFiles: () => void;
  onAnalyze: () => void;
  onLoadSamples: () => void;
  isLoading: boolean;
  errorMessage?: string | null;
}

export const FileUpload: React.FC<FileUploadProps> = ({
  files,
  onFilesSelected,
  onRemoveFile,
  onClearFiles,
  onAnalyze,
  onLoadSamples,
  isLoading,
  errorMessage,
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(true);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFiles = Array.from(e.dataTransfer.files).filter(
        (f) => f.type === 'application/pdf' || f.name.toLowerCase().endsWith('.pdf')
      );
      if (droppedFiles.length > 0) {
        onFilesSelected(droppedFiles);
      }
    }
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const selected = Array.from(e.target.files).filter(
        (f) => f.type === 'application/pdf' || f.name.toLowerCase().endsWith('.pdf')
      );
      if (selected.length > 0) {
        onFilesSelected(selected);
      }
      e.target.value = ''; // reset so same file can be re-selected if removed
    }
  };

  return (
    <div id="upload-section" className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8">
      {/* Section Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-6">
        <div>
          <h2 className="text-lg sm:text-xl font-bold text-slate-900">
            Upload Blood Reports
          </h2>
          <p className="text-xs sm:text-sm text-slate-500">
            Upload single or multiple PDF laboratory reports to extract and compare biomarkers.
          </p>
        </div>
        <button
          type="button"
          onClick={onLoadSamples}
          disabled={isLoading}
          className="self-start sm:self-auto inline-flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold text-teal-700 bg-teal-50 hover:bg-teal-100 active:bg-teal-200 border border-teal-200 rounded-lg transition-colors cursor-pointer"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>Quick Load 3 Sample Reports</span>
        </button>
      </div>

      {/* Drag & Drop Zone */}
      <div
        onDragEnter={handleDragEnter}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !isLoading && fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-xl p-8 sm:p-10 text-center transition-all cursor-pointer ${
          isDragOver
            ? 'border-teal-500 bg-teal-50/60 scale-[1.005]'
            : 'border-slate-300 hover:border-teal-400 bg-slate-50/50 hover:bg-slate-50'
        } ${isLoading ? 'opacity-50 pointer-events-none' : ''}`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          multiple
          onChange={handleFileInputChange}
          className="hidden"
          disabled={isLoading}
        />

        <div className="flex flex-col items-center">
          <div className="w-14 h-14 rounded-2xl bg-teal-50 text-teal-600 border border-teal-100 flex items-center justify-center mb-4">
            <UploadCloud className="w-7 h-7 stroke-[2]" />
          </div>
          <p className="text-base font-semibold text-slate-800 mb-1">
            Drag and drop PDF files here, or browse from your device
          </p>
          <p className="text-xs sm:text-sm text-slate-500 mb-3">
            Upload multiple reports across different dates for automatic timeline tracking.
          </p>
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-600 border border-slate-200">
            PDF files only (Digital reports supported)
          </span>
        </div>
      </div>

      {/* Error Message Banner */}
      {errorMessage && (
        <div className="mt-4 p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm flex items-start space-x-3">
          <AlertCircle className="w-5 h-5 text-rose-500 shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="font-semibold">Analysis Notice</p>
            <p className="text-xs sm:text-sm mt-0.5 text-rose-700">{errorMessage}</p>
          </div>
        </div>
      )}

      {/* Selected Files List */}
      {files.length > 0 && (
        <div className="mt-6">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-xs sm:text-sm font-semibold uppercase tracking-wider text-slate-500">
              Selected Files ({files.length})
            </h3>
            <button
              type="button"
              onClick={onClearFiles}
              disabled={isLoading}
              className="text-xs text-slate-500 hover:text-slate-800 font-medium cursor-pointer"
            >
              Clear all
            </button>
          </div>

          <div className="space-y-2.5 max-h-60 overflow-y-auto pr-1">
            {files.map((item) => (
              <div
                key={item.id}
                className="flex items-center justify-between p-3.5 rounded-xl border border-slate-200 bg-white hover:bg-slate-50/80 transition-colors"
              >
                <div className="flex items-center space-x-3 min-w-0">
                  <div className="w-8 h-8 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center shrink-0">
                    <FileText className="w-4 h-4" />
                  </div>
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-slate-800 truncate" title={item.name}>
                      {item.name}
                    </p>
                    <p className="text-xs text-slate-400">
                      {formatFileSize(item.size)}
                    </p>
                  </div>
                </div>

                <div className="flex items-center space-x-2 shrink-0 ml-4">
                  {item.status === 'completed' && (
                    <span className="inline-flex items-center text-xs text-emerald-600 font-medium bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                      <CheckCircle2 className="w-3.5 h-3.5 mr-1 text-emerald-500" />
                      Extracted
                    </span>
                  )}
                  {item.status === 'pending' && (
                    <span className="inline-flex items-center text-xs text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
                      <FileCheck className="w-3.5 h-3.5 mr-1 text-slate-400" />
                      Ready
                    </span>
                  )}
                  {item.status === 'error' && (
                    <span className="inline-flex items-center text-xs text-rose-600 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                      Error
                    </span>
                  )}

                  <button
                    type="button"
                    onClick={() => onRemoveFile(item.id)}
                    disabled={isLoading}
                    className="p-1 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors cursor-pointer"
                    title="Remove file"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Action Trigger Button */}
          <div className="mt-6 flex flex-col sm:flex-row items-center justify-between gap-3 pt-4 border-t border-slate-100">
            <p className="text-xs text-slate-500 text-center sm:text-left">
              Click analyze to run PDF extraction, normalization, and timeline synthesis.
            </p>
            <button
              type="button"
              onClick={onAnalyze}
              disabled={isLoading || files.length === 0}
              className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-6 py-2.5 rounded-xl font-semibold text-white bg-teal-600 hover:bg-teal-700 active:bg-teal-800 shadow-md shadow-teal-700/10 transition-all disabled:opacity-50 cursor-pointer text-sm"
            >
              <span>Analyze Reports</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
