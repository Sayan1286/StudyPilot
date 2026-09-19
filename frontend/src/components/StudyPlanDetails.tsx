import { useEffect, useState } from 'react'

import { api } from '../lib/api'
import type { StudyPlan, StudyTask } from '../lib/api'
import './StudyPlanDetails.css'

type StudyPlanDetailsProps = {
  token: string
  studyPlanId: string
  onBack: () => void
}

function formatDate(dateString: string) {
  return new Intl.DateTimeFormat('en', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  }).format(new Date(`${dateString}T00:00:00`))
}

function StudyPlanDetails({
  token,
  studyPlanId,
  onBack,
}: StudyPlanDetailsProps) {
  const [studyPlan, setStudyPlan] = useState<StudyPlan | null>(null)
  const [studyTasks, setStudyTasks] = useState<StudyTask[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [updatingTaskId, setUpdatingTaskId] = useState<string | null>(null)

  useEffect(() => {
    let active = true

    async function loadPlan() {
      try {
        const [plan, tasks] = await Promise.all([
          api.getStudyPlan(token, studyPlanId),
          api.listStudyTasks(token, studyPlanId),
        ])

        if (!active) {
          return
        }

        setStudyPlan(plan)
        setStudyTasks(tasks)
        setError('')
      } catch (requestError) {
        if (active) {
          setError(
            requestError instanceof Error
              ? requestError.message
              : 'Could not load the study plan.',
          )
        }
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    void loadPlan()

    return () => {
      active = false
    }
  }, [studyPlanId, token])

  async function handleToggleTask(task: StudyTask) {
    const nextStatus = task.status === 'completed' ? 'pending' : 'completed'

    setUpdatingTaskId(task.id)
    setError('')

    try {
      const updatedTask = await api.updateStudyTask(
        token,
        studyPlanId,
        task.id,
        {
          status: nextStatus,
        },
      )

      setStudyTasks((currentTasks) =>
        currentTasks.map((currentTask) =>
          currentTask.id === updatedTask.id
            ? updatedTask
            : currentTask,
        ),
      )
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : 'Could not update the task.',
      )
    } finally {
      setUpdatingTaskId(null)
    }
  }

  if (loading) {
    return (
      <main className="plan-details-shell">
        <div className="plan-details-state">
          <p>Loading study plan...</p>
        </div>
      </main>
    )
  }

  if (error && !studyPlan) {
    return (
      <main className="plan-details-shell">
        <button
          type="button"
          className="plan-back-button"
          onClick={onBack}
        >
          ← Back to dashboard
        </button>

        <div className="plan-details-state plan-details-error">
          <p>{error}</p>
        </div>
      </main>
    )
  }

  if (!studyPlan) {
    return null
  }

  const completedTasks = studyTasks.filter(
    (task) => task.status === 'completed',
  ).length

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
          <span className="eyebrow">Study plan</span>

          <h1>{studyPlan.title}</h1>

          <p className="plan-details-subject">
            {studyPlan.subject}
          </p>

          <p className="plan-details-goal">{studyPlan.goal}</p>
        </div>

        <div className="plan-summary">
          <div>
            <span>Daily study</span>
            <strong>{studyPlan.daily_hours} hrs</strong>
          </div>

          <div>
            <span>Start</span>
            <strong>{formatDate(studyPlan.start_date)}</strong>
          </div>

          <div>
            <span>End</span>
            <strong>{formatDate(studyPlan.end_date)}</strong>
          </div>

          <div>
            <span>Progress</span>
            <strong>
              {completedTasks}/{studyTasks.length}
            </strong>
          </div>
        </div>
      </section>

      {error && (
        <div className="task-update-error">
          {error}
        </div>
      )}

      <section className="tasks-section">
        <div className="tasks-heading">
          <div>
            <span className="eyebrow">Daily schedule</span>
            <h2>Your Tasks</h2>
          </div>

          <span className="task-count">
            {completedTasks}/{studyTasks.length} completed
          </span>
        </div>

        {studyTasks.length === 0 ? (
          <div className="plan-details-state">
            <p>No tasks have been added to this plan yet.</p>
          </div>
        ) : (
          <div className="tasks-list">
            {studyTasks.map((task, index) => {
              const isCompleted = task.status === 'completed'
              const isUpdating = updatingTaskId === task.id

              return (
                <article
                  key={task.id}
                  className={`task-card ${
                    isCompleted ? 'task-card-completed' : ''
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
                          isCompleted
                            ? 'task-status-completed'
                            : ''
                        }`}
                      >
                        {task.status}
                      </span>
                    </div>

                    <h3>{task.title}</h3>

                    {task.description && <p>{task.description}</p>}

                    <span className="task-duration">
                      {task.estimated_minutes} minutes
                    </span>

                    <button
                      type="button"
                      className={
                        isCompleted
                          ? 'task-toggle-button task-toggle-button-completed'
                          : 'task-toggle-button'
                      }
                      disabled={isUpdating}
                      onClick={() => handleToggleTask(task)}
                    >
                      {isUpdating
                        ? 'Updating...'
                        : isCompleted
                          ? '↶ Reopen task'
                          : '✓ Mark complete'}
                    </button>
                  </div>
                </article>
              )
            })}
          </div>
        )}
      </section>
    </main>
  )
}

export default StudyPlanDetails