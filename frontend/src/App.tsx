import { useEffect, useState } from 'react'
import type { SyntheticEvent } from 'react'

import Dashboard from './components/Dashboard'
import { api } from './lib/api'
import type { User } from './lib/api'
import './App.css'

type AuthMode = 'login' | 'register'

const TOKEN_KEY = 'studypilot_access_token'

function App() {
  const [user, setUser] = useState<User | null>(null)
  const [authFailed, setAuthFailed] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [mode, setMode] = useState<AuthMode>('login')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [fullName, setFullName] = useState('')

  const hasStoredToken = Boolean(localStorage.getItem(TOKEN_KEY))
  const loading = hasStoredToken && !user && !authFailed

  useEffect(() => {
    const token = localStorage.getItem(TOKEN_KEY)

    if (!token) {
      return
    }

    api.me(token)
      .then(setUser)
      .catch(() => {
        localStorage.removeItem(TOKEN_KEY)
        setAuthFailed(true)
      })
  }, [])

  async function handleSubmit(event: SyntheticEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setSubmitting(true)

    try {
      if (mode === 'register') {
        await api.register({
          email,
          password,
          full_name: fullName,
        })

        setMode('login')
        setPassword('')
        setFullName('')
        setShowPassword(false)
        setError('')
        return
      }

      const tokenResponse = await api.login({
        email,
        password,
      })

      localStorage.setItem(TOKEN_KEY, tokenResponse.access_token)

      const currentUser = await api.me(tokenResponse.access_token)

      setUser(currentUser)
      setPassword('')
      setShowPassword(false)
    } catch (submitError) {
      setError(
        submitError instanceof Error
          ? submitError.message
          : 'Something went wrong.',
      )
    } finally {
      setSubmitting(false)
    }
  }

  function handleLogout() {
    localStorage.removeItem(TOKEN_KEY)
    setUser(null)
    setAuthFailed(false)
    setEmail('')
    setPassword('')
    setFullName('')
    setShowPassword(false)
    setMode('login')
    setError('')
  }

  if (loading) {
    return (
      <main className="app-shell">
        <section className="auth-card">
          <p className="loading-text">Loading StudyPilot...</p>
        </section>
      </main>
    )
  }

  if (user) {
    const token = localStorage.getItem(TOKEN_KEY)

    if (!token) {
      return null
    }

    return (
      <Dashboard
        user={user}
        token={token}
        onLogout={handleLogout}
      />
    )
  }

  return (
    <main className="app-shell">
      <section className="auth-layout">
        <div className="hero-panel">
          <div className="brand">StudyPilot</div>

          <span className="eyebrow">AI-powered study planner</span>

          <h1>
            Plan smarter.
            <br />
            Study better.
          </h1>

          <p>
            Build focused study plans, organize daily tasks, and turn your
            learning goals into a clear path forward.
          </p>

          <div className="feature-list">
            <div>
              <span>01</span>
              <strong>Personal study plans</strong>
            </div>

            <div>
              <span>02</span>
              <strong>Daily task scheduling</strong>
            </div>

            <div>
              <span>03</span>
              <strong>AI-assisted planning</strong>
            </div>
          </div>
        </div>

        <section className="auth-card">
          <div className="auth-heading">
            <span className="eyebrow">
              {mode === 'login' ? 'Welcome back' : 'Get started'}
            </span>

            <h2>
              {mode === 'login' ? 'Sign in' : 'Create your account'}
            </h2>

            <p>
              {mode === 'login'
                ? 'Sign in to continue to your study workspace.'
                : 'Create your StudyPilot account to start planning.'}
            </p>
          </div>

          <div className="auth-switch">
            <button
              type="button"
              className={mode === 'login' ? 'active' : ''}
              onClick={() => {
                setMode('login')
                setError('')
              }}
            >
              Sign in
            </button>

            <button
              type="button"
              className={mode === 'register' ? 'active' : ''}
              onClick={() => {
                setMode('register')
                setError('')
              }}
            >
              Register
            </button>
          </div>

          <form onSubmit={handleSubmit} className="auth-form">
            {mode === 'register' && (
              <label>
                Full name

                <input
                  type="text"
                  value={fullName}
                  onChange={(event) => setFullName(event.target.value)}
                  placeholder="Your full name"
                  minLength={2}
                  maxLength={150}
                  required
                />
              </label>
            )}

            <label>
              Email

              <input
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="you@example.com"
                required
              />
            </label>

            <label>
              Password

              <div className="password-field">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  placeholder="Minimum 8 characters"
                  minLength={8}
                  maxLength={72}
                  required
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() =>
                    setShowPassword((visible) => !visible)
                  }
                  aria-label={
                    showPassword ? 'Hide password' : 'Show password'
                  }
                >
                  {showPassword ? 'Hide' : 'Show'}
                </button>
              </div>
            </label>

            {error && <div className="error-message">{error}</div>}

            <button
              type="submit"
              className="primary-button"
              disabled={submitting}
            >
              {submitting
                ? 'Please wait...'
                : mode === 'login'
                  ? 'Sign in'
                  : 'Create account'}
            </button>
          </form>
        </section>
      </section>
    </main>
  )
}

export default App