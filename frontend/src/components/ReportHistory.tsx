import React from 'react';
import { Calendar, FileText, CheckCircle2, ChevronRight, History } from 'lucide-react';
import { Report } from '../types';
import { formatDate } from '../utils/formatters';

interface ReportHistoryProps {
  reports: Report[];
  onSelectReport: (report: Report) => void;
}

export const ReportHistory: React.FC<ReportHistoryProps> = ({ reports, onSelectReport }) => {
  if (reports.length === 0) return null;

  // Chronological order: latest first
  const chronologicalReports = [...reports].sort((a, b) => {
    if (!a.reportDate) return 1;
    if (!b.reportDate) return -1;
    return b.reportDate.localeCompare(a.reportDate);
  });

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8">
      <div className="flex items-center space-x-2 mb-6">
        <div className="w-8 h-8 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center">
          <History className="w-4 h-4" />
        </div>
        <div>
          <h2 className="text-lg sm:text-xl font-bold text-slate-900">
            Report History
          </h2>
          <p className="text-xs sm:text-sm text-slate-500">
            Chronological log of analyzed PDF blood reports. Click any report to view all extracted measurements.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {chronologicalReports.map((report) => (
          <div
            key={report.id}
            onClick={() => onSelectReport(report)}
            className="p-5 rounded-2xl border border-slate-200 hover:border-teal-400 hover:shadow-sm bg-white hover:bg-slate-50/50 transition-all cursor-pointer flex flex-col justify-between group"
          >
            <div>
              <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
                <span className="inline-flex items-center space-x-1 font-semibold text-teal-700 bg-teal-50 px-2 py-0.5 rounded-full border border-teal-100">
                  <Calendar className="w-3 h-3" />
                  <span>{formatDate(report.reportDate, 'long')}</span>
                </span>
                <span className="text-[11px] text-slate-400">ID: {report.id}</span>
              </div>

              <div className="flex items-start space-x-3 mt-3">
                <div className="w-9 h-9 rounded-xl bg-slate-100 group-hover:bg-teal-50 text-slate-600 group-hover:text-teal-600 flex items-center justify-center shrink-0 transition-colors">
                  <FileText className="w-4 h-4" />
                </div>
                <div className="min-w-0 flex-1">
                  <h3 className="text-sm font-bold text-slate-800 truncate" title={report.fileName}>
                    {report.fileName}
                  </h3>
                  <p className="text-xs text-slate-500 mt-0.5 flex items-center space-x-1">
                    <CheckCircle2 className="w-3.5 h-3.5 text-teal-500 inline" />
                    <span>{report.biomarkers.length} biomarkers detected</span>
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-semibold text-teal-600 group-hover:text-teal-700">
              <span>View extracted values</span>
              <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
