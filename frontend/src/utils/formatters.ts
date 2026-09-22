export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
}

export function formatDate(dateString: string | null | undefined, style: 'short' | 'long' = 'short'): string {
  if (!dateString) return 'Not Specified';
  
  // Try ISO parse
  try {
    const parts = dateString.split('-');
    if (parts.length === 3) {
      const year = parseInt(parts[0], 10);
      const month = parseInt(parts[1], 10) - 1;
      const day = parseInt(parts[2], 10);
      const d = new Date(year, month, day);
      if (!isNaN(d.getTime())) {
        if (style === 'long') {
          return d.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
        }
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
      }
    }
    const d = new Date(dateString);
    if (!isNaN(d.getTime())) {
      if (style === 'long') {
        return d.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
      }
      return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    }
  } catch {
    // fallback
  }

  return dateString;
}

export function formatDelta(change: number | null | undefined): { text: string; isPositive: boolean; isNegative: boolean; isZero: boolean } {
  if (change === null || change === undefined) {
    return { text: '—', isPositive: false, isNegative: false, isZero: true };
  }
  if (change > 0) {
    return { text: `+${change.toFixed(change % 1 === 0 ? 0 : 2)}`, isPositive: true, isNegative: false, isZero: false };
  }
  if (change < 0) {
    return { text: `${change.toFixed(change % 1 === 0 ? 0 : 2)}`, isPositive: false, isNegative: true, isZero: false };
  }
  return { text: '0.0', isPositive: false, isNegative: false, isZero: true };
}

export function getStatusBadgeInfo(status: string = 'unspecified') {
  switch (status.toLowerCase()) {
    case 'normal':
      return {
        label: 'In Range',
        bgClass: 'bg-emerald-50 text-emerald-700 border-emerald-200',
        dotClass: 'bg-emerald-500'
      };
    case 'high':
      return {
        label: 'Elevated',
        bgClass: 'bg-amber-50 text-amber-700 border-amber-200',
        dotClass: 'bg-amber-500'
      };
    case 'low':
      return {
        label: 'Low',
        bgClass: 'bg-blue-50 text-blue-700 border-blue-200',
        dotClass: 'bg-blue-500'
      };
    default:
      return {
        label: 'Recorded',
        bgClass: 'bg-slate-50 text-slate-600 border-slate-200',
        dotClass: 'bg-slate-400'
      };
  }
}
