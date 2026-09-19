const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

type ApiError = {
  detail?: string
}

async function request<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  })

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`

    try {
      const error = (await response.json()) as ApiError

      if (error.detail) {
        message = error.detail
      }
    } catch {
      // Keep the default message when the response is not JSON.
    }

    throw new Error(message)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return (await response.json()) as T
}

function authHeaders(token: string): HeadersInit {
  return {
    Authorization: `Bearer ${token}`,
  }
}

export type RegisterRequest = {
  email: string
  password: string
  full_name: string
}

export type LoginRequest = {
  email: string
  password: string
}

export type User = {
  id: string
  email: string
  full_name: string
  is_active: boolean
}

export type TokenResponse = {
  access_token: string
  token_type: string
}

export type StudyPlan = {
  id: string
  user_id: string
  title: string
  subject: string
  goal: string
  start_date: string
  end_date: string
  daily_hours: number
  status: string
  created_at: string
  updated_at: string
}

export type StudyTask = {
  id: string
  study_plan_id: string
  title: string
  description: string | null
  scheduled_date: string
  estimated_minutes: number
  status: string
  created_at: string
  updated_at: string
}

export type StudyPlanGenerationRequest = {
  subject: string
  goal: string
  available_hours_per_day: number
  start_date: string
  end_date: string
}

export type GeneratedTask = {
  title: string
  description: string | null
  scheduled_date: string
  estimated_minutes: number
}

export type StudyPlanGenerationResponse = {
  title: string
  subject: string
  goal: string
  start_date: string
  end_date: string
  daily_hours: number
  tasks: GeneratedTask[]
}

export const api = {
  register: (data: RegisterRequest) =>
    request<User>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  login: (data: LoginRequest) =>
    request<TokenResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  me: (token: string) =>
    request<User>('/auth/me', {
      headers: authHeaders(token),
    }),

  listStudyPlans: (token: string) =>
    request<StudyPlan[]>('/study-plans', {
      headers: authHeaders(token),
    }),

  getStudyPlan: (token: string, studyPlanId: string) =>
    request<StudyPlan>(`/study-plans/${studyPlanId}`, {
      headers: authHeaders(token),
    }),

  listStudyTasks: (token: string, studyPlanId: string) =>
    request<StudyTask[]>(`/study-plans/${studyPlanId}/tasks`, {
      headers: authHeaders(token),
    }),

  generateStudyPlan: (
    token: string,
    data: StudyPlanGenerationRequest,
  ) =>
    request<StudyPlanGenerationResponse>('/study-plans/generate', {
      method: 'POST',
      headers: authHeaders(token),
      body: JSON.stringify(data),
    }),

  updateStudyTask: (
    token: string,
    studyPlanId: string,
    taskId: string,
    data: {
      title?: string
      description?: string | null
      scheduled_date?: string
      estimated_minutes?: number
      status?: string
    },
  ) =>
    request<StudyTask>(
      `/study-plans/${studyPlanId}/tasks/${taskId}`,
      {
        method: 'PUT',
        headers: authHeaders(token),
        body: JSON.stringify(data),
      },
    ),

  deleteStudyPlan: (token: string, studyPlanId: string) =>
    request<void>(`/study-plans/${studyPlanId}`, {
      method: 'DELETE',
      headers: authHeaders(token),
    }),
}