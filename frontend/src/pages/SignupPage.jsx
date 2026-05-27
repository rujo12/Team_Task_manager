import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import AlertMessage from '../components/AlertMessage'
import AuthLayout from '../layouts/AuthLayout'
import { useAuth } from '../context/useAuth'

const initialState = {
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  password: '',
  password_confirm: '',
}

export default function SignupPage() {
  const { signup, getErrorMessage } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState(initialState)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleChange = (event) => {
    setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setSuccess('')
    setIsSubmitting(true)

    try {
      await signup(form)
      setSuccess('Signup successful. You can now login.')
      setForm(initialState)
      setTimeout(() => navigate('/login'), 900)
    } catch (err) {
      setError(getErrorMessage(err, 'Signup failed. Please try again.'))
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <AuthLayout title="Create account" subtitle="Start managing your team tasks">
      <form className="space-y-3" onSubmit={handleSubmit}>
        <AlertMessage message={error} />
        <AlertMessage type="success" message={success} />
        <input
          name="username"
          placeholder="Username"
          required
          value={form.username}
          onChange={handleChange}
          className="w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-slate-500"
        />
        <input
          name="email"
          type="email"
          placeholder="Email"
          required
          value={form.email}
          onChange={handleChange}
          className="w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-slate-500"
        />
        <div className="grid grid-cols-2 gap-2">
          <input
            name="first_name"
            placeholder="First name"
            value={form.first_name}
            onChange={handleChange}
            className="w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-slate-500"
          />
          <input
            name="last_name"
            placeholder="Last name"
            value={form.last_name}
            onChange={handleChange}
            className="w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-slate-500"
          />
        </div>
        <input
          name="password"
          type="password"
          placeholder="Password"
          required
          value={form.password}
          onChange={handleChange}
          className="w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-slate-500"
        />
        <input
          name="password_confirm"
          type="password"
          placeholder="Confirm password"
          required
          value={form.password_confirm}
          onChange={handleChange}
          className="w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-slate-500"
        />
        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full rounded-md bg-slate-800 px-3 py-2 text-sm font-medium text-white hover:bg-slate-900 disabled:opacity-60"
        >
          {isSubmitting ? 'Creating account...' : 'Signup'}
        </button>
      </form>
      <p className="mt-4 text-center text-sm text-slate-500">
        Already have an account?{' '}
        <Link to="/login" className="font-medium text-slate-700 hover:underline">
          Login
        </Link>
      </p>
    </AuthLayout>
  )
}
