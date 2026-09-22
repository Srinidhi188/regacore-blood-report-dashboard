import React, { useState, useMemo } from 'react';
import { 
  Search, 
  TrendingUp, 
  TrendingDown, 
  Minus, 
  ArrowUpDown,
  Table as TableIcon
} from 'lucide-react';
import { BiomarkerTableRow } from '../types';
import { formatDate, formatDelta, getStatusBadgeInfo } from '../utils/formatters';

interface BiomarkerTableProps {
  rows: BiomarkerTableRow[];
  onSelectBiomarker: (key: string) => void;
  selectedKey: string;
}

export const BiomarkerTable: React.FC<BiomarkerTableProps> = ({
  rows,
  onSelectBiomarker,
  selectedKey,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('ALL');
  const [sortField, setSortField] = useState<'name' | 'value' | 'change'>('name');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  // Distinct categories
  const categories = useMemo(() => {
    const set = new Set(rows.map((r) => r.category).filter(Boolean));
    return ['ALL', ...Array.from(set)];
  }, [rows]);

  // Filtered & sorted rows
  const filteredRows = useMemo(() => {
    return rows
      .filter((row) => {
        const matchesSearch =
          row.displayName.toLowerCase().includes(searchTerm.toLowerCase()) ||
          row.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
          (row.unit && row.unit.toLowerCase().includes(searchTerm.toLowerCase()));
        const matchesCategory =
          categoryFilter === 'ALL' || row.category === categoryFilter;
        return matchesSearch && matchesCategory;
      })
      .sort((a, b) => {
        let valA: any = a.displayName;
        let valB: any = b.displayName;

        if (sortField === 'value') {
          valA = a.latestValue ?? -999999;
          valB = b.latestValue ?? -999999;
        } else if (sortField === 'change') {
          valA = a.change ?? -999999;
          valB = b.change ?? -999999;
        }

        if (valA < valB) return sortOrder === 'asc' ? -1 : 1;
        if (valA > valB) return sortOrder === 'asc' ? 1 : -1;
        return 0;
      });
  }, [rows, searchTerm, categoryFilter, sortField, sortOrder]);

  const toggleSort = (field: 'name' | 'value' | 'change') => {
    if (sortField === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortOrder('asc');
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
      {/* Table Controls Header */}
      <div className="p-6 border-b border-slate-100 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center">
              <TableIcon className="w-4 h-4" />
            </div>
            <h2 className="text-lg sm:text-xl font-bold text-slate-900">
              Detailed Biomarker Comparison
            </h2>
          </div>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Complete inventory of extracted biomarkers with latest findings and report-to-report deltas.
          </p>
        </div>

        {/* Search & Category Filter */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search biomarkers..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 text-xs sm:text-sm rounded-xl focus:ring-teal-500 focus:border-teal-500 w-full sm:w-56"
            />
          </div>

          <div className="relative">
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="py-2 pl-3 pr-8 bg-slate-50 border border-slate-200 text-xs sm:text-sm rounded-xl focus:ring-teal-500 focus:border-teal-500 font-medium text-slate-700 w-full cursor-pointer"
            >
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat === 'ALL' ? 'All Panels' : cat}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Desktop / Tablet Table View */}
      <div className="hidden md:block overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50/80 border-b border-slate-200 text-[11px] font-bold uppercase tracking-wider text-slate-500">
              <th 
                className="py-3.5 px-6 cursor-pointer hover:text-slate-800 transition-colors"
                onClick={() => toggleSort('name')}
              >
                <div className="flex items-center space-x-1">
                  <span>Biomarker</span>
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th 
                className="py-3.5 px-6 cursor-pointer hover:text-slate-800 transition-colors"
                onClick={() => toggleSort('value')}
              >
                <div className="flex items-center space-x-1">
                  <span>Latest Value</span>
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th className="py-3.5 px-4">Unit</th>
              <th className="py-3.5 px-6">Reference Range</th>
              <th className="py-3.5 px-6">Report Date</th>
              <th className="py-3.5 px-6">Previous Value</th>
              <th 
                className="py-3.5 px-6 cursor-pointer hover:text-slate-800 transition-colors"
                onClick={() => toggleSort('change')}
              >
                <div className="flex items-center space-x-1">
                  <span>Change</span>
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-sm">
            {filteredRows.length > 0 ? (
              filteredRows.map((row) => {
                const delta = formatDelta(row.change);
                const isSelected = row.key === selectedKey;
                const statusBadge = getStatusBadgeInfo(row.status);

                return (
                  <tr
                    key={row.key}
                    onClick={() => onSelectBiomarker(row.key)}
                    className={`cursor-pointer transition-colors ${
                      isSelected
                        ? 'bg-teal-50/60 font-medium'
                        : 'hover:bg-slate-50/80'
                    }`}
                  >
                    <td className="py-3.5 px-6">
                      <div>
                        <span className="font-semibold text-slate-900 block">
                          {row.displayName}
                        </span>
                        <span className="text-[11px] text-slate-400 font-normal">
                          {row.category}
                        </span>
                      </div>
                    </td>

                    <td className="py-3.5 px-6">
                      <div className="flex items-center space-x-2">
                        <span className="font-bold text-slate-900 text-base">
                          {row.latestValue !== null ? row.latestValue : '—'}
                        </span>
                        {row.status !== 'unspecified' && (
                          <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${statusBadge.bgClass}`}>
                            {statusBadge.label}
                          </span>
                        )}
                      </div>
                    </td>

                    <td className="py-3.5 px-4 text-slate-600 font-medium">
                      {row.unit || '—'}
                    </td>

                    <td className="py-3.5 px-6 text-slate-600">
                      {row.referenceRange ? row.referenceRange : <span className="text-slate-400">Not available</span>}
                    </td>

                    <td className="py-3.5 px-6 text-slate-600">
                      {formatDate(row.latestReportDate)}
                    </td>

                    <td className="py-3.5 px-6 text-slate-600 font-medium">
                      {row.previousValue !== null ? `${row.previousValue}` : <span className="text-slate-400">—</span>}
                    </td>

                    <td className="py-3.5 px-6">
                      <div className="flex items-center space-x-1.5 font-semibold text-slate-800">
                        {delta.isPositive && <TrendingUp className="w-4 h-4 text-slate-700" />}
                        {delta.isNegative && <TrendingDown className="w-4 h-4 text-slate-700" />}
                        {delta.isZero && row.change !== null && <Minus className="w-4 h-4 text-slate-400" />}
                        <span>{delta.text}</span>
                      </div>
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan={7} className="py-8 text-center text-slate-400 text-sm">
                  No biomarkers match your current search query.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Mobile Responsive Cards Transformation */}
      <div className="block md:hidden divide-y divide-slate-100 p-4 space-y-4">
        {filteredRows.length > 0 ? (
          filteredRows.map((row) => {
            const delta = formatDelta(row.change);
            const isSelected = row.key === selectedKey;
            const statusBadge = getStatusBadgeInfo(row.status);

            return (
              <div
                key={row.key}
                onClick={() => onSelectBiomarker(row.key)}
                className={`p-4 rounded-xl border transition-all cursor-pointer ${
                  isSelected
                    ? 'border-teal-500 bg-teal-50/40 ring-1 ring-teal-500'
                    : 'border-slate-200 bg-white'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <span className="text-[10px] uppercase font-bold text-slate-400">
                      {row.category}
                    </span>
                    <h4 className="text-base font-bold text-slate-900">
                      {row.displayName}
                    </h4>
                  </div>
                  {row.status !== 'unspecified' && (
                    <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${statusBadge.bgClass}`}>
                      {statusBadge.label}
                    </span>
                  )}
                </div>

                <div className="grid grid-cols-2 gap-3 mt-3 text-xs">
                  <div>
                    <span className="text-slate-400 block text-[11px]">Latest Value</span>
                    <span className="text-base font-bold text-slate-900">
                      {row.latestValue !== null ? row.latestValue : '—'} {row.unit || ''}
                    </span>
                  </div>

                  <div>
                    <span className="text-slate-400 block text-[11px]">Change from previous</span>
                    <span className="text-sm font-semibold text-slate-800">
                      {delta.text} {row.unit || ''}
                    </span>
                  </div>

                  <div>
                    <span className="text-slate-400 block text-[11px]">Reference Interval</span>
                    <span className="text-slate-700 font-medium">
                      {row.referenceRange || 'Not available'}
                    </span>
                  </div>

                  <div>
                    <span className="text-slate-400 block text-[11px]">Report Date</span>
                    <span className="text-slate-700 font-medium">
                      {formatDate(row.latestReportDate)}
                    </span>
                  </div>
                </div>
              </div>
            );
          })
        ) : (
          <p className="text-center py-6 text-slate-400 text-xs">
            No biomarkers match your search.
          </p>
        )}
      </div>
    </div>
  );
};
