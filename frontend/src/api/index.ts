import type { Candidate, Job, Interview, PaginatedResponse } from '@/types'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api/v1'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  })
  if (!res.ok) {
    throw new Error(`API Error: ${res.status} ${res.statusText}`)
  }
  if (res.status === 204) return undefined as T
  return res.json()
}

// ── Candidates ──
export const candidatesApi = {
  list: (params?: { skip?: number; limit?: number; status?: string; search?: string }) => {
    const qs = new URLSearchParams()
    if (params?.skip) qs.set('skip', String(params.skip))
    if (params?.limit) qs.set('limit', String(params.limit))
    if (params?.status) qs.set('status', params.status)
    if (params?.search) qs.set('search', params.search)
    return request<PaginatedResponse<Candidate>>(`/candidates?${qs}`)
  },
  get: (id: string) => request<Candidate>(`/candidates/${id}`),
  create: (data: Partial<Candidate>) =>
    request<Candidate>('/candidates', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: string, data: Partial<Candidate>) =>
    request<Candidate>(`/candidates/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  delete: (id: string) =>
    request<void>(`/candidates/${id}`, { method: 'DELETE' }),
}

// ── Jobs ──
export const jobsApi = {
  list: (params?: { skip?: number; limit?: number; status?: string; department?: string }) => {
    const qs = new URLSearchParams()
    if (params?.skip) qs.set('skip', String(params.skip))
    if (params?.limit) qs.set('limit', String(params.limit))
    if (params?.status) qs.set('status', params.status)
    if (params?.department) qs.set('department', params.department)
    return request<PaginatedResponse<Job>>(`/jobs?${qs}`)
  },
  get: (id: string) => request<Job>(`/jobs/${id}`),
  create: (data: Partial<Job>) =>
    request<Job>('/jobs', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: string, data: Partial<Job>) =>
    request<Job>(`/jobs/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  delete: (id: string) =>
    request<void>(`/jobs/${id}`, { method: 'DELETE' }),
}

// ── Interviews ──
export const interviewsApi = {
  list: (params?: { skip?: number; limit?: number; status?: string; candidate_id?: string }) => {
    const qs = new URLSearchParams()
    if (params?.skip) qs.set('skip', String(params.skip))
    if (params?.limit) qs.set('limit', String(params.limit))
    if (params?.status) qs.set('status', params.status)
    if (params?.candidate_id) qs.set('candidate_id', params.candidate_id)
    return request<PaginatedResponse<Interview>>(`/interviews?${qs}`)
  },
  get: (id: string) => request<Interview>(`/interviews/${id}`),
  create: (data: Partial<Interview>) =>
    request<Interview>('/interviews', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: string, data: Partial<Interview>) =>
    request<Interview>(`/interviews/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  delete: (id: string) =>
    request<void>(`/interviews/${id}`, { method: 'DELETE' }),
}
