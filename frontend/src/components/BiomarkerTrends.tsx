import React from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ReferenceLine
} from 'recharts';
import { BiomarkerHistory } from '../types';
import { formatDate } from '../utils/formatters';
import { LineChart as ChartIcon, Calendar, Info } from 'lucide-react';

interface BiomarkerTrendsProps {
  trends: Record<string, BiomarkerHistory>;
  selectedBiomarkerKey: string;
  onSelectBiomarker: (key: string) => void;
}

export const BiomarkerTrends: React.FC<BiomarkerTrendsProps> = ({
  trends,
  selectedBiomarkerKey,
  onSelectBiomarker,
}) => {
  const trendKeys = Object.keys(trends);
  const activeTrend = trends[selectedBiomarkerKey] || trends[trendKeys[0]];

  if (!activeTrend) return null;

  // Format data for Recharts
  const chartData = activeTrend.points.map((pt) => ({
    date: pt.reportDate,
    formattedDate: formatDate(pt.reportDate),
    value: pt.value,
    unit: pt.unit || activeTrend.unit,
    fileName: pt.fileName,
    referenceRange: pt.referenceRange || activeTrend.referenceRange,
  }));

  // Identify common quick-preset biomarkers dynamically
  const quickKeys = trendKeys.filter((k) =>
    ['hemoglobin', 'fasting_glucose', 'total_cholesterol', 'vitamin_d', 'creatinine', 'wbc'].includes(k)
  );

  // Determine Y-domain with padding
  const values = chartData.map((d) => d.value);
  const minVal = Math.min(...values);
  const maxVal = Math.max(...values);
  const yPadding = (maxVal - minVal) * 0.2 || minVal * 0.1 || 2;
  const yDomainMin = Math.max(0, Math.floor(minVal - yPadding));
  const yDomainMax = Math.ceil(maxVal + yPadding);

  return (
    <div id="trends-section" className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8">
      {/* Section Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 pb-6 border-b border-slate-100">
        <div>
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center">
              <ChartIcon className="w-4 h-4" />
            </div>
            <h2 className="text-lg sm:text-xl font-bold text-slate-900">
              Biomarker Trends
            </h2>
          </div>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Interactive longitudinal timeline tracking biomarker measurements across reports.
          </p>
        </div>

        {/* Dropdown Selector */}
        <div className="flex flex-col sm:flex-row sm:items-center gap-3">
          <label htmlFor="biomarker-select" className="text-xs font-semibold uppercase tracking-wider text-slate-500 shrink-0">
            Select Biomarker:
          </label>
          <select
            id="biomarker-select"
            value={activeTrend.normalizedName}
            onChange={(e) => onSelectBiomarker(e.target.value)}
            className="bg-slate-50 border border-slate-300 text-slate-800 text-sm font-semibold rounded-xl focus:ring-teal-500 focus:border-teal-500 block w-full sm:w-64 p-2.5 cursor-pointer"
          >
            {trendKeys.map((key) => (
              <option key={key} value={key}>
                {trends[key].displayName} ({trends[key].points.length} {trends[key].points.length === 1 ? 'pt' : 'pts'})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Quick Select Buttons */}
      {quickKeys.length > 0 && (
        <div className="flex items-center flex-wrap gap-2 pt-4">
          <span className="text-xs text-slate-400 font-medium mr-1">Quick Select:</span>
          {quickKeys.map((k) => (
            <button
              key={k}
              type="button"
              onClick={() => onSelectBiomarker(k)}
              className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors cursor-pointer ${
                k === activeTrend.normalizedName
                  ? 'bg-teal-600 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {trends[k].displayName}
            </button>
          ))}
        </div>
      )}

      {/* Active Biomarker Header Info */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6 p-4 rounded-xl bg-slate-50/70 border border-slate-200/70">
        <div>
          <span className="text-[11px] font-semibold text-slate-400 uppercase">Active Biomarker</span>
          <p className="text-sm sm:text-base font-bold text-slate-800 truncate">
            {activeTrend.displayName}
          </p>
        </div>
        <div>
          <span className="text-[11px] font-semibold text-slate-400 uppercase">Latest Measurement</span>
          <p className="text-sm sm:text-base font-bold text-teal-700">
            {activeTrend.latestValue} {activeTrend.unit || ''}
          </p>
        </div>
        <div>
          <span className="text-[11px] font-semibold text-slate-400 uppercase">Reference Range</span>
          <p className="text-sm sm:text-base font-medium text-slate-700">
            {activeTrend.referenceRange || 'Not available'}
          </p>
        </div>
        <div>
          <span className="text-[11px] font-semibold text-slate-400 uppercase">Data Points</span>
          <p className="text-sm sm:text-base font-bold text-slate-800">
            {activeTrend.points.length} {activeTrend.points.length === 1 ? 'Report' : 'Reports'}
          </p>
        </div>
      </div>

      {/* Chart Canvas */}
      <div className="mt-6 w-full h-80 sm:h-96">
        {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={chartData}
              margin={{ top: 20, right: 30, left: 10, bottom: 10 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
              <XAxis
                dataKey="formattedDate"
                stroke="#64748b"
                tick={{ fontSize: 12 }}
                tickLine={false}
                dy={8}
              />
              <YAxis
                stroke="#64748b"
                domain={[yDomainMin, yDomainMax]}
                tick={{ fontSize: 12 }}
                tickLine={false}
                dx={-4}
                unit={` ${activeTrend.unit || ''}`}
              />
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="bg-slate-900 text-white rounded-xl shadow-xl p-3.5 border border-slate-800 text-xs space-y-1 min-w-44">
                        <div className="flex items-center space-x-1.5 text-slate-400 pb-1 border-b border-slate-800">
                          <Calendar className="w-3.5 h-3.5" />
                          <span>{data.formattedDate} ({data.date})</span>
                        </div>
                        <p className="text-sm font-bold text-teal-400 pt-0.5">
                          {activeTrend.displayName}: {data.value} {data.unit}
                        </p>
                        <p className="text-slate-300">
                          Ref: {data.referenceRange || 'Not available'}
                        </p>
                        <p className="text-[11px] text-slate-400 truncate">
                          File: {data.fileName}
                        </p>
                      </div>
                    );
                  }
                  return null;
                }}
              />

              {/* Optional Reference Range Bounds */}
              {activeTrend.refLow !== null && activeTrend.refLow !== undefined && (
                <ReferenceLine
                  y={activeTrend.refLow}
                  stroke="#10b981"
                  strokeDasharray="4 4"
                  label={{
                    value: `Lower Ref (${activeTrend.refLow})`,
                    position: 'insideBottomRight',
                    fill: '#10b981',
                    fontSize: 10
                  }}
                />
              )}
              {activeTrend.refHigh !== null && activeTrend.refHigh !== undefined && (
                <ReferenceLine
                  y={activeTrend.refHigh}
                  stroke="#f59e0b"
                  strokeDasharray="4 4"
                  label={{
                    value: `Upper Ref (${activeTrend.refHigh})`,
                    position: 'insideTopRight',
                    fill: '#f59e0b',
                    fontSize: 10
                  }}
                />
              )}

              <Line
                type="monotone"
                dataKey="value"
                stroke="#0d9488"
                strokeWidth={3}
                dot={{ r: 5, fill: '#0d9488', strokeWidth: 2, stroke: '#ffffff' }}
                activeDot={{ r: 8, fill: '#0f766e', strokeWidth: 3, stroke: '#ffffff' }}
                animationDuration={600}
              />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div className="h-full flex items-center justify-center text-slate-400 text-sm">
            No data points available for this biomarker.
          </div>
        )}
      </div>

      {chartData.length === 1 && (
        <div className="mt-4 p-3 rounded-xl bg-slate-50 border border-slate-200 text-slate-600 text-xs flex items-center space-x-2">
          <Info className="w-4 h-4 text-slate-500 shrink-0" />
          <span>
            This biomarker currently has 1 report observation. Upload additional reports across different dates to connect and visualize its trajectory line.
          </span>
        </div>
      )}
    </div>
  );
};
