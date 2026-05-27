import { useEffect, useState } from 'react'
import {
  addMemberToProject,
  createProject,
  getProjects,
} from '../api/projectApi'
import AlertMessage from '../components/AlertMessage'
import LoadingSpinner from '../components/LoadingSpinner'
import PageHeader from '../components/PageHeader'
import { useAuth } from '../context/useAuth'
import { extractApiData, extractApiMessage } from '../utils/apiHelpers'

const initialProjectForm = { name: '', description: '' }
const initialAddMemberForm = { project_id: '', user_id: '' }

export default function ProjectsPage() {
  const { user } = useAuth()
  const isAdmin = user?.role === 'ADMIN'
  const [projects, setProjects] = useState([])
  const [projectForm, setProjectForm] = useState(initialProjectForm)
  const [memberForm, setMemberForm] = useState(initialAddMemberForm)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    let isMounted = true

    const loadProjects = async () => {
      setIsLoading(true)
      setError('')
      try {
        const response = await getProjects()
        if (isMounted) {
          setProjects(extractApiData(response) || [])
        }
      } catch (err) {
        if (isMounted) {
          setError(extractApiMessage(err, 'Failed to load projects.'))
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    loadProjects()

    return () => {
      isMounted = false
    }
  }, [])

  const reloadProjects = async () => {
    const response = await getProjects()
    setProjects(extractApiData(response) || [])
  }

  const handleCreateProject = async (event) => {
    event.preventDefault()
    setError('')
    setSuccess('')
    try {
      await createProject(projectForm)
      setSuccess('Project created successfully.')
      setProjectForm(initialProjectForm)
      await reloadProjects()
    } catch (err) {
      setError(extractApiMessage(err, 'Failed to create project.'))
    }
  }

  const handleAddMember = async (event) => {
    event.preventDefault()
    setError('')
    setSuccess('')
    try {
      await addMemberToProject(memberForm.project_id, {
        user_id: Number(memberForm.user_id),
      })
      setSuccess('Member added to project successfully.')
      setMemberForm(initialAddMemberForm)
    } catch (err) {
      setError(extractApiMessage(err, 'Failed to add member to project.'))
    }
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Projects"
        subtitle="Create projects and manage team members."
      />

      <AlertMessage message={error} />
      <AlertMessage type="success" message={success} />

      {isAdmin ? (
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          <form
            onSubmit={handleCreateProject}
            className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm"
          >
            <h2 className="mb-3 text-lg font-semibold text-slate-900">
              Create Project
            </h2>
            <div className="space-y-3">
              <input
                required
                placeholder="Project name"
                value={projectForm.name}
                onChange={(event) =>
                  setProjectForm((prev) => ({ ...prev, name: event.target.value }))
                }
                className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-500"
              />
              <textarea
                placeholder="Description"
                value={projectForm.description}
                onChange={(event) =>
                  setProjectForm((prev) => ({
                    ...prev,
                    description: event.target.value,
                  }))
                }
                className="h-24 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-500"
              />
              <button
                type="submit"
                className="rounded-md bg-slate-800 px-3 py-2 text-sm text-white hover:bg-slate-900"
              >
                Create Project
              </button>
            </div>
          </form>

          <form
            onSubmit={handleAddMember}
            className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm"
          >
            <h2 className="mb-3 text-lg font-semibold text-slate-900">
              Add Member to Project
            </h2>
            <div className="space-y-3">
              <select
                required
                value={memberForm.project_id}
                onChange={(event) =>
                  setMemberForm((prev) => ({
                    ...prev,
                    project_id: event.target.value,
                  }))
                }
                className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-500"
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
                type="number"
                placeholder="User ID to add"
                value={memberForm.user_id}
                onChange={(event) =>
                  setMemberForm((prev) => ({ ...prev, user_id: event.target.value }))
                }
                className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-500"
              />
              <button
                type="submit"
                className="rounded-md bg-slate-800 px-3 py-2 text-sm text-white hover:bg-slate-900"
              >
                Add Member
              </button>
            </div>
          </form>
        </div>
      ) : null}

      <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="mb-3 text-lg font-semibold text-slate-900">Project List</h2>
        {isLoading ? (
          <LoadingSpinner message="Loading projects..." />
        ) : projects.length === 0 ? (
          <p className="text-sm text-slate-500">No projects found.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-slate-500">
                  <th className="py-2">Name</th>
                  <th className="py-2">Description</th>
                  <th className="py-2">Created By</th>
                  <th className="py-2">Members</th>
                </tr>
              </thead>
              <tbody>
                {projects.map((project) => (
                  <tr key={project.id} className="border-b border-slate-100">
                    <td className="py-2 font-medium text-slate-800">{project.name}</td>
                    <td className="py-2 text-slate-600">
                      {project.description || '-'}
                    </td>
                    <td className="py-2 text-slate-600">{project.created_by}</td>
                    <td className="py-2 text-slate-600">{project.members_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
