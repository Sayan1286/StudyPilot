import { useEffect, useState } from 'react'

import GenerateStudyPlanModal from './GenerateStudyPlanModal'
import StudyPlanDetails from './StudyPlanDetails'
import { api } from '../lib/api'
import type {
  StudyPlan,
  StudyPlanGenerationResponse,
  StudyTask,
  User,
} from '../lib/api'
import './Dashboard.css'

type DashboardProps = {
  user: User
  token: string
  onLogout: () => void
}

type DemoPlanData = {
  plan: StudyPlan
  tasks: StudyTask[]
}

const demoPlans: DemoPlanData[] = [
  {
    plan: {
      id: 'demo-python',
      user_id: 'demo',
      title: 'Python Fundamentals',
      subject: 'Python',
      goal: 'Build a strong Python foundation',
      start_date: '2026-09-20',
      end_date: '2026-09-26',
      daily_hours: 2,
      status: 'demo',
      created_at: '',
      updated_at: '',
    },
    tasks: [
      {
        id: 'demo-python-1',
        study_plan_id: 'demo-python',
        title: 'Python syntax and variables',
        description:
          'Learn variables, data types, operators, and basic input/output.',
        scheduled_date: '2026-09-20',
        estimated_minutes: 120,
        status: 'pending',
        created_at: '',
        updated_at: '',
      },
      {
        id: 'demo-python-2',
        study_plan_id: 'demo-python',
        title: 'Conditions and loops',
        description:
          'Practice if statements, for loops, while loops, and ranges.',
        scheduled_date: '2026-09-21',
        estimated_minutes: 120,
        status: 'pending',
        created_at: '',
        updated_at: '',
      },
      {
        id: 'demo-python-3',
        study_plan_id: 'demo-python',
        title: 'Functions',
        description:
          'Study parameters, return values, scope, and reusable functions.',
        scheduled_date: '2026-09-22',
        estimated_minutes: 120,
        status: 'pending',
        created_at: '',
        updated_at: '',
      },
    ],
  },
  {
    plan: {
      id: 'demo-backend',
      user_id: 'demo',
      title: 'Backend Development',
      subject: 'FastAPI',
      goal: 'Learn REST APIs and backend architecture',
      start_date: '2026-09-20',
      end_date: '2026-09-27',
      daily_hours: 2.5,
      status: 'demo',
      created_at: '',
      updated_at: '',
    },
    tasks: [
      {
        id: 'demo-backend-1',
        study_plan_id: 'demo-backend',
        title: 'HTTP and REST fundamentals',
        description:
          'Understand requests, responses, methods, headers, and status codes.',
        scheduled_date: '2026-09-20',
        estimated_minutes: 150,
        status: 'pending',
        created_at: '',
        updated_at: '',
      },
      {
        id: 'demo-backend-2',
        study_plan_id: 'demo-backend',
        title: 'FastAPI routes',
        description: 'Build GET and POST endpoints with FastAPI.',
        scheduled_date: '2026-09-21',
        estimated_minutes: 150,
        status: 'pending',
        created_at: '',
        updated_at: '',
      },
      {
        id: 'demo-backend-3',
        study_plan_id: 'demo-backend',
        title: 'Pydantic schemas',
        description:
          'Validate request and response data with Pydantic.',
        scheduled_date: '2026-09-22',
        estimated_minutes: 150,
        status: 'pending',
        created_at: '',
        updated_at: '',
      },
    ],
  },
  {
    plan: {
      id: 'demo-database',
      user_id: 'demo',
      title: 'Database Fundamentals',
      subject: 'PostgreSQL',
      goal: 'Learn SQL, relationships, indexes, and migrations',
      start_date: '2026-09-22',
      end_date: '2026-09-28',
      daily_hours: 1.5,
      status: 'demo',
      created_at: '',
      updated_at: '',
    },
    tasks: [
      {
        id: 'demo-db-1',
        study_plan_id: 'demo-database',
        title: 'SQL basics',
        description:
          'Learn SELECT, INSERT, UPDATE, DELETE, and filtering.',
        scheduled_date: '2026-09-22',
        estimated_minutes: 90,
        status: 'pending',
        created_at: '',
        updated_at: '',
      },
      {
        id: 'demo-db-2',
        study_plan_id: 'demo-database',
        title: 'Relationships and joins',
        description:
          'Practice primary keys, foreign keys, and SQL joins.',
        scheduled_date: '2026-09-23',
        estimated_minutes: 90,
        status: 'pending',
        created_at: '',
        updated_at: '',
      },
      {
        id: 'demo-db-3',
        study_plan_id: 'demo-database',
        title: 'Indexes and migrations',
        description:
          'Understand indexes and how Alembic migrations work.',
        scheduled_date: '2026-09-24',
        estimated_minutes: 90,
        status: 'pending',
        created_at: '',
        updated_at: '',
      },
    ],
  },
  {
    plan: {
      id: 'demo-javascript',
      user_id: 'demo',
      title: 'JavaScript Essentials',
      subject: 'JavaScript',
      goal: 'Master modern JavaScript for frontend development',
      start_date: '2026-09-20',
      end_date: '2026-09-26',
      daily_hours: 2,
      status: 'demo',
      created_at: '',
      updated_at: '',
    },
    tasks: [
      {
        id: 'demo-js-1',
        study_plan_id: 'demo-javascript',
        title: 'JavaScript fundamentals',
        description:
          'Learn variables, functions, arrays, objects, and operators.',
        scheduled_date: '2026-09-20',
        estimated_minutes: 120,
        status: 'pending',
        created_at: '',
        updated_at: '',
      },
      {
        id: 'demo-js-2',
        study_plan_id: 'demo-javascript',
        title: 'Modern JavaScript',
        description:
          'Practice destructuring, spread syntax, modules, and async code.',
        scheduled_date: '2026-09-21',
        estimated_minutes: 120,
        status: 'pending',
        created_at: '',
        updated_at: '',
      },
      {
        id: 'demo-js-3',
        study_plan_id: 'demo-javascript',
        title: 'Promises and async/await',
        description:
          'Build asynchronous workflows with fetch and async/await.',
        scheduled_date: '2026-09-22',
        estimated_minutes: 120,
        status: 'pending',
        created_at: '',
        updated_at: '',
      },
    ],
  },
  {
    plan: {
      id: 'demo-react',
      user_id: 'demo',
      title: 'React Development',
      subject: 'React',
      goal: 'Build reusable React components and modern interfaces',
      start_date: '2026-09-21',
      end_date: '2026-09-28',
      daily_hours: 2,
      status: 'demo',
      created_at: '',
      updated_at: '',
    },
    tasks: [
      {
        id: 'demo-react-1',
        study_plan_id: 'demo-react',
        title: 'React components',
        description:
          'Learn JSX, components, props, and component composition.',
        scheduled_date: '2026-09-21',
        estimated_minutes: 120,
        status: 'pending',
        created_at: '',
        updated_at: '',
      },
      {
        id: 'demo-react-2',
        study_plan_id: 'demo-react',
        title: 'State and events',
        description:
          'Practice useState, event handlers, and controlled forms.',
        scheduled_date: '2026-09-22',
        estimated_minutes: 120,
        status: 'pending',
        created_at: '',
        updated_at: '',
      },
      {
        id: 'demo-react-3',
        study_plan_id: 'demo-react',
        title: 'Effects and API calls',
        description:
          'Use useEffect and fetch data from an API.',
        scheduled_date: '2026-09-23',
        estimated_minutes: 120,
        status: 'pending',
        created_at: '',
        updated_at: '',
      },
    ],
  },
  {
    plan: {
      id: 'demo-git',
      user_id: 'demo',
      title: 'Git & GitHub Workflow',
      subject: 'Git',
      goal: 'Learn branches, commits, pull requests, and collaboration',
      start_date: '2026-09-23',
      end_date: '2026-09-27',
      daily_hours: 1.5,
      status: 'demo',
      created_at: '',
      updated_at: '',
    },
    tasks: [
      {
        id: 'demo-git-1',
        study_plan_id: 'demo-git',
        title: 'Git basics',
        description:
          'Practice status, add, commit, log, and restore.',
        scheduled_date: '2026-09-23',
        estimated_minutes: 90,
        status: 'pending',
        created_at: '',
        updated_at: '',
      },
      {
        id: 'demo-git-2',
        study_plan_id: 'demo-git',
        title: 'Branches and rebasing',
        description:
          'Learn branches, merge, rebase, and conflict resolution.',
        scheduled_date: '2026-09-24',
        estimated_minutes: 90,
        status: 'pending',
        created_at: '',
        updated_at: '',
      },
      {
        id: 'demo-git-3',
        study_plan_id: 'demo-git',
        title: 'GitHub pull requests',
        description:
          'Practice pushing branches and creating pull requests.',
        scheduled_date: '2026-09-25',
        estimated_minutes: 90,
        status: 'pending',
        created_at: '',
        updated_at: '',
      },
    ],
  },
]

function formatDate(dateString: string) {
  return new Intl.DateTimeFormat('en', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  }).format(new Date(`${dateString}T00:00:00`))
}

function DemoPlanDetails({
  data,
  onBack,
}: {
  data: DemoPlanData
  onBack: () => void
}) {
  const [tasks, setTasks] = useState(data.tasks)

  const completedTasks = tasks.filter(
    (task) => task.status === 'completed',
  ).length

  function toggleTask(taskId: string) {
    setTasks((currentTasks) =>
      currentTasks.map((task) =>
        task.id === taskId
          ? {
              ...task,
              status:
                task.status === 'completed'
                  ? 'pending'
                  : 'completed',
            }
          : task,
      ),
    )
  }

  return (
    <main className="plan-details-shell">
      <button
        type="button"
        className="plan-back-button"
        onClick={onBack}
      >
        ← Back to dashboard
      </button>

      <section className="plan-hero">
        <div>
          <span className="eyebrow">Demo study plan</span>

          <h1>{data.plan.title}</h1>

          <p className="plan-details-subject">
            {data.plan.subject}
          </p>

          <p className="plan-details-goal">
            {data.plan.goal}
          </p>
        </div>

        <div className="plan-summary">
          <div>
            <span>Daily study</span>
            <strong>{data.plan.daily_hours} hrs</strong>
          </div>

          <div>
            <span>Start</span>
            <strong>{formatDate(data.plan.start_date)}</strong>
          </div>

          <div>
            <span>End</span>
            <strong>{formatDate(data.plan.end_date)}</strong>
          </div>

          <div>
            <span>Progress</span>
            <strong>
              {completedTasks}/{tasks.length}
            </strong>
          </div>
        </div>
      </section>

      <section className="tasks-section">
        <div className="tasks-heading">
          <div>
            <span className="eyebrow">Demo schedule</span>
            <h2>Your Tasks</h2>
          </div>

          <span className="task-count">
            {completedTasks}/{tasks.length} completed
          </span>
        </div>

        <div className="tasks-list">
          {tasks.map((task, index) => {
            const completed = task.status === 'completed'

            return (
              <article
                key={task.id}
                className={`task-card ${
                  completed ? 'task-card-completed' : ''
                }`}
              >
                <div className="task-number">
                  {String(index + 1).padStart(2, '0')}
                </div>

                <div className="task-content">
                  <div className="task-topline">
                    <span className="task-date">
                      {formatDate(task.scheduled_date)}
                    </span>

                    <span
                      className={`task-status ${
                        completed ? 'task-status-completed' : ''
                      }`}
                    >
                      {task.status}
                    </span>
                  </div>

                  <h3>{task.title}</h3>

                  <p>{task.description}</p>

                  <span className="task-duration">
                    {task.estimated_minutes} minutes
                  </span>

                  <button
                    type="button"
                    className={
                      completed
                        ? 'task-toggle-button task-toggle-button-completed'
                        : 'task-toggle-button'
                    }
                    onClick={() => toggleTask(task.id)}
                  >
                    {completed
                      ? '↶ Reopen task'
                      : '✓ Mark complete'}
                  </button>
                </div>
              </article>
            )
          })}
        </div>
      </section>
    </main>
  )
}

function Dashboard({ user, token, onLogout }: DashboardProps) {
  const [studyPlans, setStudyPlans] = useState<StudyPlan[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showGenerationModal, setShowGenerationModal] = useState(false)
  const [generatedMessage, setGeneratedMessage] = useState('')
  const [selectedPlanId, setSelectedPlanId] = useState<string | null>(null)
  const [deletingPlanId, setDeletingPlanId] = useState<string | null>(null)

  useEffect(() => {
    let active = true

    api.listStudyPlans(token)
      .then((plans) => {
        if (active) {
          setStudyPlans(plans)
          setError('')
        }
      })
      .catch((requestError) => {
        if (active) {
          setError(
            requestError instanceof Error
              ? requestError.message
              : 'Could not load your study plans.',
          )
        }
      })
      .finally(() => {
        if (active) {
          setLoading(false)
        }
      })

    return () => {
      active = false
    }
  }, [token])

  function openGenerationModal() {
    setGeneratedMessage('')
    setError('')
    setShowGenerationModal(true)
  }

  function handleGenerated(
    generatedPlan: StudyPlanGenerationResponse,
  ) {
    setGeneratedMessage(
      `Created "${generatedPlan.title}" with ${generatedPlan.tasks.length} daily tasks.`,
    )

    api.listStudyPlans(token)
      .then((plans) => {
        setStudyPlans(plans)
        setError('')
      })
      .catch((requestError) => {
        setError(
          requestError instanceof Error
            ? requestError.message
            : 'The plan was created, but the dashboard could not refresh.',
        )
      })
  }

  async function handleDeletePlan(planId: string) {
    const plan = studyPlans.find((item) => item.id === planId)

    if (!plan) {
      return
    }

    const confirmed = window.confirm(
      `Delete "${plan.title}"? This will also delete its study tasks.`,
    )

    if (!confirmed) {
      return
    }

    setDeletingPlanId(planId)
    setError('')

    try {
      await api.deleteStudyPlan(token, planId)

      setStudyPlans((currentPlans) =>
        currentPlans.filter((item) => item.id !== planId),
      )

      setGeneratedMessage(`Deleted "${plan.title}".`)
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : 'Could not delete the study plan.',
      )
    } finally {
      setDeletingPlanId(null)
    }
  }

  const selectedDemo = selectedPlanId
    ? demoPlans.find((item) => item.plan.id === selectedPlanId)
    : null

  if (selectedDemo) {
    return (
      <DemoPlanDetails
        data={selectedDemo}
        onBack={() => setSelectedPlanId(null)}
      />
    )
  }

  if (selectedPlanId) {
    return (
      <StudyPlanDetails
        token={token}
        studyPlanId={selectedPlanId}
        onBack={() => setSelectedPlanId(null)}
      />
    )
  }

  return (
    <main className="dashboard-shell">
      <header className="dashboard-header">
        <div>
          <div className="dashboard-brand">StudyPilot</div>

          <p className="dashboard-subtitle">
            Your personal study workspace
          </p>
        </div>

        <div className="dashboard-user">
          <div className="dashboard-user-info">
            <strong>{user.full_name}</strong>
            <span>{user.email}</span>
          </div>

          <button
            type="button"
            className="dashboard-logout"
            onClick={onLogout}
          >
            Log out
          </button>
        </div>
      </header>

      <section className="dashboard-content">
        <div className="dashboard-welcome">
          <div>
            <span className="eyebrow">Your workspace</span>

            <h1>Welcome back, {user.full_name}</h1>

            <p>
              Keep your goals organized and turn them into daily progress.
            </p>
          </div>

          <button
            type="button"
            className="dashboard-primary-button"
            onClick={openGenerationModal}
          >
            + Generate Study Plan
          </button>
        </div>

        {generatedMessage && (
          <div className="generation-success">
            {generatedMessage}
          </div>
        )}

        <section className="plans-section">
          <div className="section-heading">
            <div>
              <span className="eyebrow">Planning</span>
              <h2>Your Study Plans</h2>
            </div>

            <span className="plan-count">
              {studyPlans.length}{' '}
              {studyPlans.length === 1 ? 'plan' : 'plans'}
            </span>
          </div>

          {loading && (
            <div className="dashboard-state">
              <p>Loading your study plans...</p>
            </div>
          )}

          {!loading && error && (
            <div className="dashboard-state dashboard-error">
              <p>{error}</p>
            </div>
          )}

          {!loading && !error && studyPlans.length === 0 && (
            <div className="empty-plans">
              <div className="empty-icon">＋</div>

              <h3>No study plans yet</h3>

              <p>
                Create your first plan and start turning your learning
                goal into daily tasks.
              </p>

              <button
                type="button"
                className="dashboard-primary-button"
                onClick={openGenerationModal}
              >
                Generate your first plan
              </button>
            </div>
          )}

          {!loading && !error && studyPlans.length > 0 && (
            <div className="plans-grid">
              {studyPlans.map((plan) => (
                <article key={plan.id} className="plan-card">
                  <div className="plan-card-top">
                    <span className="plan-status">
                      {plan.status}
                    </span>

                    <span className="plan-hours">
                      {plan.daily_hours} hrs/day
                    </span>
                  </div>

                  <h3>{plan.title}</h3>

                  <p className="plan-subject">{plan.subject}</p>

                  <p className="plan-goal">{plan.goal}</p>

                  <div className="plan-meta">
                    <span>{formatDate(plan.start_date)}</span>
                    <span>→</span>
                    <span>{formatDate(plan.end_date)}</span>
                  </div>

                  <div className="plan-actions">
                    <button
                      type="button"
                      className="plan-view-button"
                      onClick={() => setSelectedPlanId(plan.id)}
                    >
                      View plan
                    </button>

                    <button
                      type="button"
                      className="plan-delete-button"
                      disabled={deletingPlanId === plan.id}
                      onClick={() => handleDeletePlan(plan.id)}
                    >
                      {deletingPlanId === plan.id
                        ? 'Deleting...'
                        : 'Delete'}
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        {!loading && !error && (
          <section className="demo-plans-section">
            <div className="section-heading">
              <div>
                <span className="eyebrow">Examples</span>
                <h2>Demo Study Plans</h2>
              </div>

              <span className="plan-count">
                {demoPlans.length} demos
              </span>
            </div>

            <div className="plans-grid">
              {demoPlans.map(({ plan }) => (
                <article
                  key={plan.id}
                  className="plan-card demo-plan-card"
                >
                  <div className="plan-card-top">
                    <span className="plan-status plan-status-demo">
                      Demo
                    </span>

                    <span className="plan-hours">
                      {plan.daily_hours} hrs/day
                    </span>
                  </div>

                  <h3>{plan.title}</h3>

                  <p className="plan-subject">{plan.subject}</p>

                  <p className="plan-goal">{plan.goal}</p>

                  <div className="plan-meta">
                    <span>{formatDate(plan.start_date)}</span>
                    <span>→</span>
                    <span>{formatDate(plan.end_date)}</span>
                  </div>

                  <button
                    type="button"
                    className="plan-view-button"
                    onClick={() => setSelectedPlanId(plan.id)}
                  >
                    View demo
                  </button>
                </article>
              ))}
            </div>
          </section>
        )}
      </section>

      {showGenerationModal && (
        <GenerateStudyPlanModal
          token={token}
          onClose={() => setShowGenerationModal(false)}
          onGenerated={(generatedPlan) => {
            handleGenerated(generatedPlan)
            setShowGenerationModal(false)
          }}
        />
      )}
    </main>
  )
}

export default Dashboard