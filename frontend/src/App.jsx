import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/layout/Navbar'
import Dashboard from './pages/Dashboard'
import RealtimeDetection from './pages/RealtimeDetection'
import UploadAnalysis from './pages/UploadAnalysis'
import TextAnalysis from './pages/TextAnalysis'
import History from './pages/History'
import Analytics from './pages/Analytics'
import RLVisualization from './pages/RLVisualization'
import ModelInsights from './pages/ModelInsights'
import Theory from './pages/Theory'
import Settings from './pages/Settings'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-bg-primary">
        <Navbar />
        <main className="container mx-auto px-4 py-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/realtime" element={<RealtimeDetection />} />
            <Route path="/upload" element={<UploadAnalysis />} />
            <Route path="/text" element={<TextAnalysis />} />
            <Route path="/history" element={<History />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/rl-viz" element={<RLVisualization />} />
            <Route path="/insights" element={<ModelInsights />} />
            <Route path="/theory" element={<Theory />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
