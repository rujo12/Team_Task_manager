import { privateClient } from './client'

export function getDashboardStats() {
  return privateClient.get('/api/dashboard/')
}
