import React from 'react';
import { CheckCircle2, Loader2, Circle } from 'lucide-react';
import { StepIndicatorItem } from '../types';

interface ProcessingStateProps {
  steps: StepIndicatorItem[];
  progressPercent: number;
}

export const ProcessingState: React.FC<ProcessingStateProps> = ({ steps, progressPercent }) => {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8 max-w-xl mx-auto my-8">
      <div className="text-center mb-6">
        <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-teal-50 text-teal-600 mb-3 animate-pulse">
          <Loader2 className="w-6 h-6 animate-spin text-teal-600" />
        </div>
        <h3 className="text-lg font-bold text-slate-900">
          Analyzing Reports...
        </h3>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Extracting text, recognizing biomarkers, and generating comparative timeline.
        </p>

        {/* Progress Bar */}
        <div className="w-full bg-slate-100 rounded-full h-2 mt-4 overflow-hidden">
          <div
            className="bg-teal-600 h-2 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      {/* Step Indicators */}
      <div className="space-y-3.5 border-t border-slate-100 pt-5">
        {steps.map((step) => {
          const isCompleted = step.status === 'completed';
          const isCurrent = step.status === 'current';

          return (
            <div
              key={step.key}
              className={`flex items-center space-x-3 px-3.5 py-2.5 rounded-xl transition-colors ${
                isCurrent
                  ? 'bg-teal-50/70 border border-teal-200/60'
                  : 'bg-transparent'
              }`}
            >
              <div className="shrink-0">
                {isCompleted ? (
                  <CheckCircle2 className="w-5 h-5 text-teal-600" />
                ) : isCurrent ? (
                  <Loader2 className="w-5 h-5 text-teal-600 animate-spin" />
                ) : (
                  <Circle className="w-5 h-5 text-slate-300" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p
                  className={`text-xs sm:text-sm font-medium ${
                    isCompleted
                      ? 'text-slate-800'
                      : isCurrent
                      ? 'text-teal-900 font-semibold'
                      : 'text-slate-400'
                  }`}
                >
                  {step.label}
                </p>
              </div>
              <div>
                {isCompleted && (
                  <span className="text-[11px] font-semibold text-teal-600 uppercase tracking-wider">
                    Done
                  </span>
                )}
                {isCurrent && (
                  <span className="text-[11px] font-semibold text-teal-700 animate-pulse uppercase tracking-wider">
                    Active
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
