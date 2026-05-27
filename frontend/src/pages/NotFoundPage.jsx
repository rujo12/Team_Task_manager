import { Link } from 'react-router-dom'

export default function NotFoundPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-100 px-4">
      <div className="text-center">
        <h1 className="text-3xl font-semibold text-slate-900">404</h1>
        <p className="mt-2 text-slate-600">The page you are looking for does not exist.</p>
        <Link
          to="/dashboard"
          className="mt-4 inline-block rounded-md bg-slate-800 px-4 py-2 text-sm text-white hover:bg-slate-900"
        >
          Go to Dashboard
        </Link>
      </div>
    </div>
  )
}
