import { Activity, ShieldAlert } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-slate-200 mt-16 py-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
        {/* Medical Safety Card */}
        <div className="p-4 rounded-2xl bg-amber-50/70 border border-amber-200/70 text-amber-900 text-xs sm:text-sm flex items-start space-x-3.5">
          <ShieldAlert className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <p className="font-bold text-amber-950">Medical & Diagnostic Disclaimer</p>
            <p className="text-amber-800 leading-relaxed text-xs">
              This dashboard is for organizing and visualizing laboratory report data. It is not medical advice.
              Do not use these charts or metrics to diagnose medical conditions, evaluate treatments, or alter medical regimens without consulting a qualified healthcare professional.
            </p>
          </div>
        </div>

        {/* Brand & Attribution */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-100 text-xs text-slate-500">
          <div className="flex items-center space-x-2">
            <div className="w-6 h-6 rounded-lg bg-teal-600 text-white flex items-center justify-center">
              <Activity className="w-3.5 h-3.5" />
            </div>
            <span className="font-bold text-slate-800">REGACORE</span>
            <span>— AI-Powered Blood Report Dashboard</span>
          </div>

          <p className="text-slate-400 text-center sm:text-right">
            Data visualization only — not medical advice. Built for Regacore Technical Assignment.
          </p>
        </div>
      </div>
    </footer>
  );
};
