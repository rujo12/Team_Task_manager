import axios from 'axios'
import {
  clearTokens,
  getAccessToken,
  getRefreshToken,
  setTokens,
} from '../utils/storage'

function normalizeBaseUrl(url) {
  const cleanUrl = (url || '').trim().replace(/\/+$/, '')
  if (!cleanUrl) {
    return 'http://127.0.0.1:8000'
  }
  // Endpoints already include /api/*, so strip a trailing /api if provided.
  return cleanUrl.replace(/\/api$/i, '')
}

const baseURL = normalizeBaseUrl(import.meta.env.VITE_API_BASE_URL)

const publicClient = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
})

const privateClient = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
})

let isRefreshing = false
let pendingRequests = []

function resolvePendingRequests(newToken) {
  pendingRequests.forEach((callback) => callback(newToken))
  pendingRequests = []
}

privateClient.interceptors.request.use((config) => {
  const token = getAccessToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

privateClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    const status = error?.response?.status

    if (status !== 401 || originalRequest?._retry) {
      return Promise.reject(error)
    }

    const refresh = getRefreshToken()
    if (!refresh) {
      clearTokens()
      return Promise.reject(error)
    }

    originalRequest._retry = true

    if (isRefreshing) {
      return new Promise((resolve) => {
        pendingRequests.push((token) => {
          originalRequest.headers.Authorization = `Bearer ${token}`
          resolve(privateClient(originalRequest))
        })
      })
    }

    isRefreshing = true
    try {
      const refreshResponse = await publicClient.post('/api/auth/refresh/', {
        refresh,
      })
      const refreshedAccess =
        refreshResponse.data?.access || refreshResponse.data?.data?.access
      const refreshedRefresh =
        refreshResponse.data?.refresh || refreshResponse.data?.data?.refresh

      if (!refreshedAccess) {
        throw new Error('Unable to refresh token.')
      }

      setTokens({ access: refreshedAccess, refresh: refreshedRefresh || refresh })
      resolvePendingRequests(refreshedAccess)
      originalRequest.headers.Authorization = `Bearer ${refreshedAccess}`
      return privateClient(originalRequest)
    } catch (refreshError) {
      clearTokens()
      pendingRequests = []
      return Promise.reject(refreshError)
    } finally {
      isRefreshing = false
    }
  },
)

export { publicClient, privateClient }
