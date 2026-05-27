import { privateClient } from './client'

export function getTasks() {
  return privateClient.get('/api/tasks/')
}

export function createTask(payload) {
  return privateClient.post('/api/tasks/', payload)
}

export function updateTaskStatus(taskId, payload) {
  return privateClient.patch(`/api/tasks/${taskId}/status/`, payload)
}
