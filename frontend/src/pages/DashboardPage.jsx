import { useEffect, useState } from 'react'
import { getDashboardStats } from '../api/dashboardApi'
import AlertMessage from '../components/AlertMessage'
import DashboardCard from '../components/DashboardCard'
import LoadingSpinner from '../components/LoadingSpinner'
import PageHeader from '../components/PageHeader'
import { extractApiData, extractApiMessage } from '../utils/apiHelpers'

export default function DashboardPage() {
  const [stats, setStats] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const loadStats = async () => {
      setIsLoading(true)
      setError('')
      try {
        const response = await getDashboardStats()
        setStats(extractApiData(response))
      } catch (err) {
        setError(extractApiMessage(err, 'Failed to load dashboard data.'))
      } finally {
        setIsLoading(false)
      }
    }
    loadStats()
  }, [])

  return (
    <div>
      <PageHeader
        title="Dashboard"
        subtitle="Track task progress and pending work at a glance."
      />
      <AlertMessage message={error} />
      {isLoading ? (
        <LoadingSpinner message="Loading dashboard..." />
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <DashboardCard title="Total Tasks" value={stats?.total_tasks ?? 0} />
          <DashboardCard
            title="Completed Tasks"
            value={stats?.completed_tasks ?? 0}
          />
          <DashboardCard title="Pending Tasks" value={stats?.pending_tasks ?? 0} />
          <DashboardCard title="Overdue Tasks" value={stats?.overdue_tasks ?? 0} />
        </div>
      )}
    </div>
  )
}
