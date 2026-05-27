import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../context/useAuth'
import LoadingSpinner from '../components/LoadingSpinner'

export default function ProtectedRoute({ requiredRole }) {
  const { isAuthenticated, isLoading, user } = useAuth()

  if (isLoading) {
    return <LoadingSpinner message="Checking your session..." />
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (requiredRole && user?.role !== requiredRole) {
    return <Navigate to="/dashboard" replace />
  }

  return <Outlet />
}
