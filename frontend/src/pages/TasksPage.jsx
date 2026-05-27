import { useEffect, useState } from 'react'
import { getProjects } from '../api/projectApi'
import { createTask, getTasks, updateTaskStatus } from '../api/taskApi'
import AlertMessage from '../components/AlertMessage'
import LoadingSpinner from '../components/LoadingSpinner'
import PageHeader from '../components/PageHeader'
import StatusBadge from '../components/StatusBadge'
import { useAuth } from '../context/useAuth'
import { extractApiData, extractApiMessage } from '../utils/apiHelpers'

const statusOptions = ['TODO', 'IN_PROGRESS', 'COMPLETED']
const priorityOptions = ['low', 'medium', 'high']

const initialTaskForm = {
  project: '',
  title: '',
  description: '',
  assigned_to: '',
  status: 'TODO',
  priority: 'medium',
  due_date: '',
}

export default function TasksPage() {
  const { user } = useAuth()
  const isAdmin = user?.role === 'ADMIN'

  const [tasks, setTasks] = useState([])
  const [projects, setProjects] = useState([])
  const [taskForm, setTaskForm] = useState(initialTaskForm)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    let isMounted = true

    const loadData = async () => {
      setIsLoading(true)
      setError('')
      try {
        const tasksResponse = await getTasks()
        if (isMounted) {
          setTasks(extractApiData(tasksResponse) || [])
        }

        if (isAdmin) {
          const projectsResponse = await getProjects()
          if (isMounted) {
            setProjects(extractApiData(projectsResponse) || [])
          }
        }
      } catch (err) {
        if (isMounted) {
          setError(extractApiMessage(err, 'Failed to load tasks.'))
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    loadData()

    return () => {
      isMounted = false
    }
  }, [isAdmin])

  const reloadTasks = async () => {
    const response = await getTasks()
    setTasks(extractApiData(response) || [])
  }

  const handleCreateTask = async (event) => {
    event.preventDefault()
    setError('')
    setSuccess('')
    try {
      const payload = {
        ...taskForm,
        assigned_to: taskForm.assigned_to ? Number(taskForm.assigned_to) : null,
      }
      await createTask(payload)
      setSuccess('Task created successfully.')
      setTaskForm(initialTaskForm)
      await reloadTasks()
    } catch (err) {
      setError(extractApiMessage(err, 'Failed to create task.'))
    }
  }

  const handleUpdateStatus = async (taskId, status) => {
    setError('')
    setSuccess('')
    try {
      await updateTaskStatus(taskId, { status })
      setSuccess('Task status updated successfully.')
      await reloadTasks()
    } catch (err) {
      setError(extractApiMessage(err, 'Failed to update task status.'))
    }
  }

  return (
    <div className="space-y-6">
      <PageHeader title="Tasks" subtitle="Manage, assign, and track task progress." />

      <AlertMessage message={error} />
      <AlertMessage type="success" message={success} />

      {isAdmin ? (
        <form
          onSubmit={handleCreateTask}
          className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm"
        >
          <h2 className="mb-3 text-lg font-semibold text-slate-900">Create Task</h2>
          <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
            <select
              required
              value={taskForm.project}
              onChange={(event) =>
                setTaskForm((prev) => ({ ...prev, project: event.target.value }))
              }
              className="rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-500"
            >
              <option value="">Select project</option>
              {projects.map((project) => (
                <option key={project.id} value={project.id}>
                  {project.name}
                </option>
              ))}
            </select>
            <input
              required
              placeholder="Task title"
              value={taskForm.title}
              onChange={(event) =>
                setTaskForm((prev) => ({ ...prev, title: event.target.value }))
              }
              className="rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-500"
            />
            <input
              type="number"
              placeholder="Assign to user ID"
              value={taskForm.assigned_to}
              onChange={(event) =>
                setTaskForm((prev) => ({
                  ...prev,
                  assigned_to: event.target.value,
                }))
              }
              className="rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-500"
            />
            <input
              type="date"
              value={taskForm.due_date}
              onChange={(event) =>
                setTaskForm((prev) => ({ ...prev, due_date: event.target.value }))
              }
              className="rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-500"
            />
            <select
              value={taskForm.priority}
              onChange={(event) =>
                setTaskForm((prev) => ({ ...prev, priority: event.target.value }))
              }
              className="rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-500"
            >
              {priorityOptions.map((priority) => (
                <option key={priority} value={priority}>
                  {priority}
                </option>
              ))}
            </select>
            <select
              value={taskForm.status}
              onChange={(event) =>
                setTaskForm((prev) => ({ ...prev, status: event.target.value }))
              }
              className="rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-500"
            >
              {statusOptions.map((status) => (
                <option key={status} value={status}>
                  {status}
                </option>
              ))}
            </select>
          </div>
          <textarea
            placeholder="Task description"
            value={taskForm.description}
            onChange={(event) =>
              setTaskForm((prev) => ({ ...prev, description: event.target.value }))
            }
            className="mt-3 h-24 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-500"
          />
          <button
            type="submit"
            className="mt-3 rounded-md bg-slate-800 px-3 py-2 text-sm text-white hover:bg-slate-900"
          >
            Create Task
          </button>
        </form>
      ) : null}

      <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="mb-3 text-lg font-semibold text-slate-900">Task List</h2>
        {isLoading ? (
          <LoadingSpinner message="Loading tasks..." />
        ) : tasks.length === 0 ? (
          <p className="text-sm text-slate-500">No tasks available.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-slate-500">
                  <th className="py-2">Title</th>
                  <th className="py-2">Project</th>
                  <th className="py-2">Assigned To</th>
                  <th className="py-2">Status</th>
                  <th className="py-2">Due Date</th>
                  <th className="py-2">Action</th>
                </tr>
              </thead>
              <tbody>
                {tasks.map((task) => {
                  const canUpdate =
                    isAdmin || task.assigned_to === user?.id || task.assigned_to === user?.user_id
                  return (
                    <tr key={task.id} className="border-b border-slate-100">
                      <td className="py-2 font-medium text-slate-800">{task.title}</td>
                      <td className="py-2 text-slate-600">{task.project_name}</td>
                      <td className="py-2 text-slate-600">
                        {task.assigned_to_username || '-'}
                      </td>
                      <td className="py-2">
                        <StatusBadge status={task.status} />
                      </td>
                      <td className="py-2 text-slate-600">{task.due_date || '-'}</td>
                      <td className="py-2">
                        {canUpdate ? (
                          <select
                            value={task.status}
                            onChange={(event) =>
                              handleUpdateStatus(task.id, event.target.value)
                            }
                            className="rounded-md border border-slate-300 px-2 py-1 text-xs outline-none focus:border-slate-500"
                          >
                            {statusOptions.map((status) => (
                              <option key={status} value={status}>
                                {status}
                              </option>
                            ))}
                          </select>
                        ) : (
                          <span className="text-xs text-slate-400">No access</span>
                        )}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
