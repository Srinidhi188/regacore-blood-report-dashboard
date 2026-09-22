import { X, Calendar, FileText, AlertTriangle } from 'lucide-react';
import { Report } from '../types';
import { formatDate } from '../utils/formatters';

interface ReportDetailModalProps {
  report: Report | null;
  onClose: () => void;
}

export const ReportDetailModal: React.FC<ReportDetailModalProps> = ({ report, onClose }) => {
  if (!report) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/40 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl max-w-2xl w-full overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Modal Header */}
        <div className="p-5 sm:p-6 border-b border-slate-100 flex items-start justify-between bg-slate-50/70">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base sm:text-lg font-bold text-slate-900 line-clamp-1">
                {report.fileName}
              </h3>
              <div className="flex items-center space-x-2 text-xs text-slate-500 mt-0.5">
                <Calendar className="w-3.5 h-3.5 text-slate-400" />
                <span>Date: {formatDate(report.reportDate, 'long')}</span>
                <span>•</span>
                <span>{report.biomarkers.length} biomarkers detected</span>
              </div>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-200/60 rounded-xl transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Content */}
        <div className="p-5 sm:p-6 max-h-[70vh] overflow-y-auto space-y-4">
          {/* Warnings if any */}
          {report.warnings && report.warnings.length > 0 && (
            <div className="p-3.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-xs space-y-1">
              <div className="flex items-center space-x-1.5 font-semibold text-amber-800">
                <AlertTriangle className="w-4 h-4 text-amber-600" />
                <span>Extraction Notices</span>
              </div>
              <ul className="list-disc list-inside space-y-0.5 text-amber-700">
                {report.warnings.map((w, idx) => (
                  <li key={idx}>{w}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Biomarkers Table */}
          <div className="border border-slate-200 rounded-xl overflow-hidden">
            <div className="bg-slate-50 px-4 py-2.5 border-b border-slate-200 text-xs font-bold uppercase tracking-wider text-slate-500 flex justify-between">
              <span>Extracted Biomarker</span>
              <span>Observed Value</span>
            </div>
            <div className="divide-y divide-slate-100 max-h-80 overflow-y-auto">
              {report.biomarkers.map((bm, index) => (
                <div key={index} className="px-4 py-3 flex items-center justify-between text-xs sm:text-sm hover:bg-slate-50/60">
                  <div>
                    <span className="font-semibold text-slate-800 block">
                      {bm.displayName}
                    </span>
                    <span className="text-[11px] text-slate-400">
                      Original: "{bm.name}" {bm.referenceRange ? `• Ref: ${bm.referenceRange}` : ''}
                    </span>
                  </div>
                  <div className="text-right">
                    <span className="font-bold text-slate-900 text-sm">
                      {bm.value !== null ? bm.value : '—'}
                    </span>
                    <span className="text-xs text-slate-500 ml-1 font-medium">
                      {bm.unit || ''}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Modal Footer */}
        <div className="p-4 border-t border-slate-100 bg-slate-50/50 flex justify-end">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 text-xs sm:text-sm font-semibold text-slate-700 bg-white border border-slate-200 hover:bg-slate-50 rounded-xl transition-colors cursor-pointer"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
