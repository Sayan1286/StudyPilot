import { useState } from 'react'
import type { SyntheticEvent } from 'react'

import { api } from '../lib/api'
import type {
  StudyPlanGenerationRequest,
  StudyPlanGenerationResponse,
} from '../lib/api'
import './GenerateStudyPlanModal.css'

type GenerateStudyPlanModalProps = {
  token: string
  onClose: () => void
  onGenerated: (plan: StudyPlanGenerationResponse) => void
}

function getToday() {
  const today = new Date()

  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

function getDefaultEndDate() {
  const date = new Date()
  date.setDate(date.getDate() + 6)

  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

function GenerateStudyPlanModal({
  token,
  onClose,
  onGenerated,
}: GenerateStudyPlanModalProps) {
  const [subject, setSubject] = useState('')
  const [goal, setGoal] = useState('')
  const [hours, setHours] = useState('2')
  const [startDate, setStartDate] = useState(getToday())
  const [endDate, setEndDate] = useState(getDefaultEndDate())
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(
  event: SyntheticEvent<HTMLFormElement>,
) {
    event.preventDefault()
    setError('')
    setSubmitting(true)

    const request: StudyPlanGenerationRequest = {
      subject,
      goal,
      available_hours_per_day: Number(hours),
      start_date: startDate,
      end_date: endDate,
    }

    try {
      const generatedPlan = await api.generateStudyPlan(token, request)

      onGenerated(generatedPlan)
      onClose()
    } catch (submitError) {
      setError(
        submitError instanceof Error
          ? submitError.message
          : 'Could not generate the study plan.',
      )
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="modal-backdrop" onMouseDown={onClose}>
      <section
        className="generation-modal"
        onMouseDown={(event) => event.stopPropagation()}
      >
        <div className="generation-header">
          <div>
            <span className="eyebrow">AI planning</span>
            <h2>Generate Study Plan</h2>
            <p>
              Tell StudyPilot what you want to learn and we'll create a
              day-by-day plan.
            </p>
          </div>

          <button
            type="button"
            className="modal-close"
            onClick={onClose}
            aria-label="Close"
          >
            ×
          </button>
        </div>

        <form className="generation-form" onSubmit={handleSubmit}>
          <label>
            Subject
            <input
              type="text"
              value={subject}
              onChange={(event) => setSubject(event.target.value)}
              placeholder="e.g. Python"
              maxLength={150}
              required
            />
          </label>

          <label>
            Goal
            <textarea
              value={goal}
              onChange={(event) => setGoal(event.target.value)}
              placeholder="e.g. Build a strong Python foundation"
              maxLength={1000}
              rows={4}
              required
            />
          </label>

          <div className="generation-grid">
            <label>
              Hours per day
              <input
                type="number"
                value={hours}
                onChange={(event) => setHours(event.target.value)}
                min="0.25"
                max="24"
                step="0.25"
                required
              />
            </label>

            <label>
              Start date
              <input
                type="date"
                value={startDate}
                min={getToday()}
                onChange={(event) => setStartDate(event.target.value)}
                required
              />
            </label>

            <label>
              End date
              <input
                type="date"
                value={endDate}
                min={startDate}
                onChange={(event) => setEndDate(event.target.value)}
                required
              />
            </label>
          </div>

          {error && <div className="generation-error">{error}</div>}

          <div className="generation-actions">
            <button
              type="button"
              className="secondary-button"
              onClick={onClose}
              disabled={submitting}
            >
              Cancel
            </button>

            <button
              type="submit"
              className="dashboard-primary-button"
              disabled={submitting}
            >
              {submitting ? 'Generating...' : 'Generate Study Plan'}
            </button>
          </div>
        </form>
      </section>
    </div>
  )
}

export default GenerateStudyPlanModal