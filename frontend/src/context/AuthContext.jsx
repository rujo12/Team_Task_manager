import { createContext, useCallback, useEffect, useMemo, useState } from 'react'
import { getCurrentUser, login as loginApi, signup as signupApi } from '../api/authApi'
import { extractApiData, extractApiMessage } from '../utils/apiHelpers'
import {
  clearTokens,
  getAccessToken,
  getRefreshToken,
  setTokens,
} from '../utils/storage'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  const isAuthenticated = Boolean(user && getAccessToken())

  const loadCurrentUser = useCallback(async () => {
    try {
      const response = await getCurrentUser()
      const data = extractApiData(response)
      setUser(data)
      return data
    } catch (error) {
      clearTokens()
      setUser(null)
      throw error
    }
  }, [])

  const login = useCallback(async (credentials) => {
    const response = await loginApi(credentials)
    const responseData = response.data?.data ?? response.data
    const access = responseData?.access
    const refresh = responseData?.refresh

    if (!access || !refresh) {
      throw new Error('Authentication failed. Please try again.')
    }

    setTokens({ access, refresh })

    const loginUser = responseData?.user
    if (loginUser) {
      setUser(loginUser)
      return loginUser
    }
    return loadCurrentUser()
  }, [loadCurrentUser])

  const signup = useCallback(async (payload) => {
    const response = await signupApi(payload)
    return extractApiData(response)
  }, [])

  const logout = useCallback(() => {
    clearTokens()
    setUser(null)
  }, [])

  useEffect(() => {
    const bootstrapAuth = async () => {
      const hasTokens = Boolean(getAccessToken() && getRefreshToken())
      if (!hasTokens) {
        setIsLoading(false)
        return
      }

      try {
        await loadCurrentUser()
      } catch {
        // Handled in loadCurrentUser.
      } finally {
        setIsLoading(false)
      }
    }

    bootstrapAuth()
  }, [loadCurrentUser])

  const value = useMemo(
    () => ({
      user,
      isLoading,
      isAuthenticated,
      login,
      signup,
      logout,
      reloadUser: loadCurrentUser,
      getErrorMessage: extractApiMessage,
    }),
    [user, isLoading, isAuthenticated, login, signup, logout, loadCurrentUser],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export { AuthContext }
