import { privateClient } from './client'

export function getProjects() {
  return privateClient.get('/api/projects/')
}

export function createProject(payload) {
  return privateClient.post('/api/projects/', payload)
}

export function addMemberToProject(projectId, payload) {
  return privateClient.post(`/api/projects/${projectId}/add-member/`, payload)
}
