import { useEffect, useState } from 'react'

import GenerateStudyPlanModal from './GenerateStudyPlanModal'
import { api } from '../lib/api'
import type {
  StudyPlan,
  StudyPlanGenerationResponse,
  User,
} from '../lib/api'
import './Dashboard.css'

type DashboardProps = {
  user: User
  token: string
  onLogout: () => void
}

function formatDate(dateString: string) {
  return new Intl.DateTimeFormat('en', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  }).format(new Date(`${dateString}T00:00:00`))
}

function Dashboard({ user, token, onLogout }: DashboardProps) {
  const [studyPlans, setStudyPlans] = useState<StudyPlan[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showGenerationModal, setShowGenerationModal] = useState(false)
  const [generatedMessage, setGeneratedMessage] = useState('')

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

  function handleGenerated(generatedPlan: StudyPlanGenerationResponse) {
    setGeneratedMessage(
      `Created "${generatedPlan.title}" with ${generatedPlan.tasks.length} daily tasks.`,
    )

    api
      .listStudyPlans(token)
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

                  <button
                    type="button"
                    className="plan-view-button"
                  >
                    View plan
                  </button>
                </article>
              ))}
            </div>
          )}
        </section>
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