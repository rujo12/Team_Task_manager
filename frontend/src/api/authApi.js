import { publicClient, privateClient } from './client'

export function signup(payload) {
  return publicClient.post('/api/auth/signup/', payload)
}

export function login(payload) {
  return publicClient.post('/api/auth/login/', payload)
}

export function getCurrentUser() {
  return privateClient.get('/api/auth/me/')
}
