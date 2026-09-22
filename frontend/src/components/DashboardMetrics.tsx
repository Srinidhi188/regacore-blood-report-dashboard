import React from 'react';
import { FileStack, Dna, CalendarCheck, TrendingUp } from 'lucide-react';
import { DashboardSummary } from '../types';
import { formatDate } from '../utils/formatters';

interface DashboardMetricsProps {
  summary: DashboardSummary;
  trackedCount: number;
}

export const DashboardMetrics: React.FC<DashboardMetricsProps> = ({ summary, trackedCount }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* Metric 1: Reports Analyzed */}
      <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs hover:border-slate-300 transition-colors">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
              Reports Analyzed
            </p>
            <p className="text-2xl sm:text-3xl font-bold text-slate-900 mt-1">
              {summary.totalReports}
            </p>
          </div>
          <div className="w-11 h-11 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center">
            <FileStack className="w-5 h-5 stroke-[2]" />
          </div>
        </div>
        <p className="text-xs text-slate-400 mt-2">
          {summary.totalReports > 1 ? 'Multiple reports compared' : 'Single report analyzed'}
        </p>
      </div>

      {/* Metric 2: Unique Biomarkers */}
      <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs hover:border-slate-300 transition-colors">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
              Unique Biomarkers
            </p>
            <p className="text-2xl sm:text-3xl font-bold text-slate-900 mt-1">
              {summary.uniqueBiomarkers}
            </p>
          </div>
          <div className="w-11 h-11 rounded-xl bg-sky-50 text-sky-600 flex items-center justify-center">
            <Dna className="w-5 h-5 stroke-[2]" />
          </div>
        </div>
        <p className="text-xs text-slate-400 mt-2">
          Standardized & mapped from PDF text
        </p>
      </div>

      {/* Metric 3: Latest Report Date */}
      <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs hover:border-slate-300 transition-colors">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
              Latest Report Date
            </p>
            <p className="text-xl sm:text-2xl font-bold text-slate-900 mt-1 truncate">
              {formatDate(summary.latestReportDate, 'long')}
            </p>
          </div>
          <div className="w-11 h-11 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center">
            <CalendarCheck className="w-5 h-5 stroke-[2]" />
          </div>
        </div>
        <p className="text-xs text-slate-400 mt-2 truncate">
          {summary.dateRangeText ? `Range: ${summary.dateRangeText}` : 'Most recent lab assessment'}
        </p>
      </div>

      {/* Metric 4: Historical Series Active */}
      <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs hover:border-slate-300 transition-colors">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
              Historical Tracking
            </p>
            <p className="text-2xl sm:text-3xl font-bold text-slate-900 mt-1">
              {trackedCount}
            </p>
          </div>
          <div className="w-11 h-11 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <TrendingUp className="w-5 h-5 stroke-[2]" />
          </div>
        </div>
        <p className="text-xs text-slate-400 mt-2">
          Biomarkers with multiple timeline points
        </p>
      </div>
    </div>
  );
};
