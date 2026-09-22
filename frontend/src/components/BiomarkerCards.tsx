import React from 'react';
import { TrendingUp, TrendingDown, Minus, ArrowUpRight } from 'lucide-react';
import { BiomarkerHistory } from '../types';
import { formatDelta } from '../utils/formatters';

interface BiomarkerCardsProps {
  trends: Record<string, BiomarkerHistory>;
  selectedBiomarkerKey: string;
  onSelectBiomarker: (key: string) => void;
}

export const BiomarkerCards: React.FC<BiomarkerCardsProps> = ({
  trends,
  selectedBiomarkerKey,
  onSelectBiomarker,
}) => {
  const trendList = Object.values(trends);

  if (trendList.length === 0) return null;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg sm:text-xl font-bold text-slate-900">
            Biomarker Highlights
          </h2>
          <p className="text-xs sm:text-sm text-slate-500">
            Overview of detected biomarkers, latest values, reference intervals, and change from previous report.
          </p>
        </div>
        <span className="text-xs font-medium text-slate-400">
          Showing {trendList.length} items
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {trendList.map((item) => {
          const isSelected = item.normalizedName === selectedBiomarkerKey;
          const delta = formatDelta(item.change);
          const hasMultiplePoints = item.points.length > 1;

          return (
            <div
              key={item.normalizedName}
              onClick={() => onSelectBiomarker(item.normalizedName)}
              className={`bg-white rounded-2xl border p-5 transition-all duration-200 cursor-pointer flex flex-col justify-between ${
                isSelected
                  ? 'border-teal-500 shadow-md ring-2 ring-teal-500/15'
                  : 'border-slate-200 hover:border-slate-300 hover:shadow-xs'
              }`}
            >
              <div>
                {/* Card Header: Category & Name */}
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <span className="text-[10px] font-semibold tracking-wider uppercase text-slate-400">
                      {item.category}
                    </span>
                    <h3 className="text-base font-bold text-slate-900 mt-0.5 line-clamp-1" title={item.displayName}>
                      {item.displayName}
                    </h3>
                  </div>
                  <button
                    type="button"
                    className={`p-1 rounded-lg transition-colors shrink-0 ${
                      isSelected
                        ? 'text-teal-600 bg-teal-50'
                        : 'text-slate-400 hover:text-slate-700'
                    }`}
                    title="View timeline chart"
                  >
                    <ArrowUpRight className="w-4 h-4" />
                  </button>
                </div>

                {/* Latest Value Display */}
                <div className="mt-3.5 flex items-baseline space-x-1.5">
                  <span className="text-2xl sm:text-3xl font-extrabold text-slate-900">
                    {item.latestValue !== null && item.latestValue !== undefined ? item.latestValue : '—'}
                  </span>
                  <span className="text-xs sm:text-sm font-semibold text-slate-500">
                    {item.unit || ''}
                  </span>
                </div>

                {/* Reference Range */}
                <div className="mt-2.5 text-xs text-slate-500">
                  <span className="text-slate-400">Reference: </span>
                  <span className="font-medium text-slate-700">
                    {item.referenceRange ? `${item.referenceRange} ${item.unit || ''}` : 'Not available'}
                  </span>
                </div>
              </div>

              {/* Bottom Section: Previous Value & Neutral Change */}
              <div className="mt-4 pt-3.5 border-t border-slate-100 flex items-center justify-between text-xs">
                <div>
                  <span className="text-slate-400 block text-[11px]">Previous</span>
                  <span className="font-semibold text-slate-700">
                    {item.previousValue !== null && item.previousValue !== undefined 
                      ? `${item.previousValue} ${item.unit || ''}` 
                      : 'None'}
                  </span>
                </div>

                <div className="text-right">
                  <span className="text-slate-400 block text-[11px]">Change from previous</span>
                  <div className="flex items-center justify-end space-x-1 font-semibold">
                    {hasMultiplePoints ? (
                      <>
                        {delta.isPositive && <TrendingUp className="w-3.5 h-3.5 text-slate-700" />}
                        {delta.isNegative && <TrendingDown className="w-3.5 h-3.5 text-slate-700" />}
                        {delta.isZero && <Minus className="w-3.5 h-3.5 text-slate-400" />}
                        <span className="text-slate-800">
                          {delta.text} {item.unit || ''}
                        </span>
                      </>
                    ) : (
                      <span className="text-slate-400 font-normal">First record</span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
