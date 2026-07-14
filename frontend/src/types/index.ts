export interface Candidate {
  id: string
  name: string
  email: string
  phone?: string
  position: string
  status: 'new' | 'screening' | 'interviewing' | 'offered' | 'hired' | 'rejected'
  resume_url?: string
  ai_score?: number
  notes?: string
  created_at: string
  updated_at: string
}

export interface Job {
  id: string
  title: string
  department: string
  location?: string
  description?: string
  requirements?: string
  salary_range?: string
  headcount: number
  status: 'draft' | 'published' | 'closed'
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Interview {
  id: string
  candidate_id: string
  job_id?: string
  interview_type: 'phone' | 'video' | 'onsite' | 'technical'
  status: 'scheduled' | 'completed' | 'cancelled' | 'no_show'
  scheduled_at: string
  duration_minutes: number
  interviewer?: string
  location?: string
  notes?: string
  feedback?: string
  rating?: number
  created_at: string
  updated_at: string
}

export interface PaginatedResponse<T> {
  total: number
  items: T[]
}
