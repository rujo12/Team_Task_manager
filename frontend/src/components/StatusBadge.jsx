const STATUS_CLASSES = {
  TODO: 'bg-slate-100 text-slate-700',
  IN_PROGRESS: 'bg-amber-100 text-amber-700',
  COMPLETED: 'bg-emerald-100 text-emerald-700',
}

export default function StatusBadge({ status }) {
  return (
    <span
      className={`inline-flex rounded-full px-2.5 py-1 text-xs font-medium ${
        STATUS_CLASSES[status] || 'bg-slate-100 text-slate-700'
      }`}
    >
      {status?.replace('_', ' ')}
    </span>
  )
}
