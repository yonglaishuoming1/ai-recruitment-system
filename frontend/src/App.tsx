import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { DashboardLayout } from './layouts/DashboardLayout'
import { DashboardPage } from './pages/DashboardPage'
import { CandidatesPage } from './pages/CandidatesPage'
import { JobsPage } from './pages/JobsPage'
import { InterviewsPage } from './pages/InterviewsPage'
import { Toaster } from './components/ui/toaster'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DashboardLayout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="candidates" element={<CandidatesPage />} />
          <Route path="jobs" element={<JobsPage />} />
          <Route path="interviews" element={<InterviewsPage />} />
        </Route>
      </Routes>
      <Toaster />
    </BrowserRouter>
  )
}

export default App
