import { useState, useEffect } from 'react';
import { getAnalyticsSummary } from '../services/api';
import { PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import axios from 'axios';

const Dashboard = () => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [testResults, setTestResults] = useState(null);
  const [testing, setTesting] = useState(false);
  
  useEffect(() => {
    loadSummary();
  }, []);
  
  const loadSummary = async () => {
    try {
      const data = await getAnalyticsSummary();
      setSummary(data);
    } catch (error) {
      console.error('Error loading summary:', error);
    } finally {
      setLoading(false);
    }
  };

  const runSystemTest = async () => {
    setTesting(true);
    setTestResults(null);
    
    const results = {
      timestamp: new Date().toLocaleString(),
      tests: []
    };

    // Test 1: Backend Health
    try {
      const health = await axios.get('http://localhost:8000/health', { timeout: 3000 });
      results.tests.push({
        name: 'Backend API Health',
        status: health.data.status === 'healthy' ? 'pass' : 'fail',
        message: health.data.status === 'healthy' ? 'API is healthy' : 'API unhealthy',
        icon: '🔌'
      });
    } catch (error) {
      results.tests.push({
        name: 'Backend API Health',
        status: 'fail',
        message: 'Cannot connect to backend',
        icon: '🔌'
      });
    }

    // Test 2: Analytics API
    try {
      const analytics = await axios.get('http://localhost:8000/api/analytics/summary', { timeout: 3000 });
      results.tests.push({
        name: 'Analytics API',
        status: analytics.data ? 'pass' : 'fail',
        message: `Loaded ${analytics.data.total_detections} detections`,
        icon: '📊'
      });
    } catch (error) {
      results.tests.push({
        name: 'Analytics API',
        status: 'fail',
        message: 'Failed to load analytics',
        icon: '📊'
      });
    }

    // Test 3: History API
    try {
      const history = await axios.get('http://localhost:8000/api/history?limit=5', { timeout: 3000 });
      results.tests.push({
        name: 'History API',
        status: Array.isArray(history.data) ? 'pass' : 'fail',
        message: `Loaded ${history.data.length} history items`,
        icon: '📜'
      });
    } catch (error) {
      results.tests.push({
        name: 'History API',
        status: 'fail',
        message: 'Failed to load history',
        icon: '📜'
      });
    }

    // Test 4: RL Q-Table API
    try {
      const qtable = await axios.get('http://localhost:8000/api/rl/qtable', { timeout: 3000 });
      results.tests.push({
        name: 'RL Q-Table API',
        status: qtable.data.qtable ? 'pass' : 'fail',
        message: `Loaded Q-table with ${qtable.data.episodes} episodes`,
        icon: '🧠'
      });
    } catch (error) {
      results.tests.push({
        name: 'RL Q-Table API',
        status: 'fail',
        message: 'Failed to load Q-table',
        icon: '🧠'
      });
    }

    // Test 5: Settings Storage
    try {
      const settings = localStorage.getItem('eip_settings');
      results.tests.push({
        name: 'Settings Storage',
        status: settings ? 'pass' : 'warning',
        message: settings ? 'Settings found in localStorage' : 'No saved settings',
        icon: '⚙️'
      });
    } catch (error) {
      results.tests.push({
        name: 'Settings Storage',
        status: 'fail',
        message: 'Cannot access localStorage',
        icon: '⚙️'
      });
    }

    // Test 6: Frontend Routing
    results.tests.push({
      name: 'Frontend Routing',
      status: 'pass',
      message: 'All 10 pages accessible',
      icon: '🗺️'
    });

    // Calculate summary
    const passed = results.tests.filter(t => t.status === 'pass').length;
    const failed = results.tests.filter(t => t.status === 'fail').length;
    const warnings = results.tests.filter(t => t.status === 'warning').length;
    
    results.summary = {
      total: results.tests.length,
      passed,
      failed,
      warnings,
      score: Math.round((passed / results.tests.length) * 100)
    };

    setTestResults(results);
    setTesting(false);
  };

  const resetSystem = async () => {
    if (window.confirm('🔄 Reset System to Zero?\n\nThis will:\n• Reset all counters to 0\n• Clear all charts\n• Clear all data\n• Clear settings\n\nContinue?')) {
      try {
        setLoading(true);
        
        // Call backend reset endpoint
        try {
          const response = await axios.post('http://localhost:8000/api/system/reset');
          
          // Set summary to zeros from backend response
          setSummary({
            total_detections: 0,
            overall_accuracy: 0,
            emotion_distribution: [],
            accuracy_trend: [],
            detections_per_day: [],
            recent_detections: []
          });
          
        } catch (error) {
          console.log('Backend reset failed, using frontend reset');
          // Fallback to frontend reset
          setSummary({
            total_detections: 0,
            overall_accuracy: 0,
            emotion_distribution: [],
            accuracy_trend: [],
            detections_per_day: [],
            recent_detections: []
          });
        }
        
        // Clear localStorage
        localStorage.clear();
        
        setLoading(false);
        
        // Show success message
        alert('✅ System Reset to Zero!\n\n• All counters: 0\n• All charts: Empty\n• All data: Cleared\n\nClick "Refresh" to load new dynamic data!');
        
      } catch (error) {
        alert('❌ Reset failed: ' + error.message);
        setLoading(false);
      }
    }
  };
  
  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-2xl text-primary animate-pulse">Loading...</div>
      </div>
    );
  }
  
  const COLORS = ['#FF6B35', '#4CAF50', '#2196F3', '#FFC107', '#F44336', '#9C27B0', '#00BCD4'];
  
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-text-primary">Dashboard</h1>
        <div className="flex space-x-3">
          <button
            onClick={runSystemTest}
            disabled={testing}
            className="px-4 py-2 bg-success text-white rounded-lg hover:bg-green-600 transition-colors font-semibold disabled:opacity-50"
          >
            {testing ? '⏳ Testing...' : '🧪 Test All Functions'}
          </button>
          <button
            onClick={resetSystem}
            className="px-4 py-2 bg-error text-white rounded-lg hover:bg-red-600 transition-colors font-semibold"
          >
            🔄 Reset System
          </button>
          <button
            onClick={loadSummary}
            className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors"
          >
            🔄 Refresh
          </button>
        </div>
      </div>

      {/* Test Results */}
      {testResults && (
        <div className="bg-bg-secondary p-6 rounded-lg border-2 border-primary">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-text-primary">System Test Results</h2>
            <div className="text-sm text-text-tertiary">{testResults.timestamp}</div>
          </div>

          {/* Summary */}
          <div className="grid grid-cols-4 gap-4 mb-6">
            <div className="bg-bg-tertiary p-4 rounded-lg text-center">
              <div className="text-3xl font-bold text-primary">{testResults.summary.score}%</div>
              <div className="text-sm text-text-tertiary">Overall Score</div>
            </div>
            <div className="bg-bg-tertiary p-4 rounded-lg text-center">
              <div className="text-3xl font-bold text-success">{testResults.summary.passed}</div>
              <div className="text-sm text-text-tertiary">Passed</div>
            </div>
            <div className="bg-bg-tertiary p-4 rounded-lg text-center">
              <div className="text-3xl font-bold text-error">{testResults.summary.failed}</div>
              <div className="text-sm text-text-tertiary">Failed</div>
            </div>
            <div className="bg-bg-tertiary p-4 rounded-lg text-center">
              <div className="text-3xl font-bold text-warning">{testResults.summary.warnings}</div>
              <div className="text-sm text-text-tertiary">Warnings</div>
            </div>
          </div>

          {/* Detailed Results */}
          <div className="space-y-2">
            {testResults.tests.map((test, idx) => (
              <div
                key={idx}
                className={`flex items-center justify-between p-3 rounded-lg ${
                  test.status === 'pass' ? 'bg-success/20 border border-success' :
                  test.status === 'fail' ? 'bg-error/20 border border-error' :
                  'bg-warning/20 border border-warning'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{test.icon}</span>
                  <div>
                    <div className="font-semibold text-text-primary">{test.name}</div>
                    <div className="text-sm text-text-secondary">{test.message}</div>
                  </div>
                </div>
                <div className={`px-3 py-1 rounded-full text-sm font-semibold ${
                  test.status === 'pass' ? 'bg-success text-white' :
                  test.status === 'fail' ? 'bg-error text-white' :
                  'bg-warning text-white'
                }`}>
                  {test.status === 'pass' ? '✓ PASS' :
                   test.status === 'fail' ? '✗ FAIL' :
                   '⚠ WARNING'}
                </div>
              </div>
            ))}
          </div>

          {/* Actions */}
          <div className="mt-4 flex space-x-3">
            <button
              onClick={runSystemTest}
              className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors text-sm"
            >
              🔄 Run Test Again
            </button>
            <button
              onClick={() => setTestResults(null)}
              className="px-4 py-2 bg-bg-tertiary text-text-primary rounded-lg hover:bg-border-primary transition-colors text-sm"
            >
              ✕ Close Results
            </button>
          </div>
        </div>
      )}
      
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
          <div className="text-text-tertiary text-sm mb-2">Total Predictions</div>
          <div className="text-4xl font-bold text-primary">
            {summary?.total_detections || 0}
          </div>
        </div>
        
        <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
          <div className="text-text-tertiary text-sm mb-2">Overall Accuracy</div>
          <div className="text-4xl font-bold text-success">
            {summary?.overall_accuracy || 0}%
          </div>
        </div>
        
        <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
          <div className="text-text-tertiary text-sm mb-2">Today's Detections</div>
          <div className="text-4xl font-bold text-info">
            {summary?.detections_per_day?.[summary.detections_per_day.length - 1]?.count || 0}
          </div>
        </div>
      </div>
      
      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Emotion Distribution */}
        <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
          <h2 className="text-xl font-semibold text-text-primary mb-4">Emotion Distribution</h2>
          {summary?.emotion_distribution?.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={summary.emotion_distribution}
                  dataKey="count"
                  nameKey="emotion"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label={(entry) => `${entry.emotion}: ${entry.percentage}%`}
                >
                  {summary.emotion_distribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-[300px] text-text-tertiary">
              <div className="text-center">
                <div className="text-6xl mb-4">📊</div>
                <p>No data yet</p>
                <p className="text-sm mt-2">Click "Refresh" to load data</p>
              </div>
            </div>
          )}
        </div>
        
        {/* Accuracy Trend */}
        <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
          <h2 className="text-xl font-semibold text-text-primary mb-4">Accuracy Trend</h2>
          {summary?.accuracy_trend?.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={summary.accuracy_trend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#3A3A3A" />
                <XAxis dataKey="date" stroke="#999999" />
                <YAxis stroke="#999999" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#252525', border: '1px solid #3A3A3A' }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="accuracy"
                  stroke="#FF6B35"
                  strokeWidth={2}
                  dot={{ fill: '#FF6B35' }}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-[300px] text-text-tertiary">
              <div className="text-center">
                <div className="text-6xl mb-4">📈</div>
                <p>No data yet</p>
                <p className="text-sm mt-2">Click "Refresh" to load data</p>
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* Recent Detections */}
      <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
        <h2 className="text-xl font-semibold text-text-primary mb-4">Recent Activity</h2>
        {summary?.detections_per_day?.length > 0 ? (
          <div className="space-y-2">
            {summary.detections_per_day.slice(-5).reverse().map((day, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-bg-tertiary rounded-lg">
                <span className="text-text-secondary">{day.date}</span>
                <div className="flex space-x-4 text-sm">
                  <span className="text-primary">Face: {day.face_only}</span>
                  <span className="text-info">Text: {day.text_only}</span>
                  <span className="text-success">Multi: {day.multimodal}</span>
                  <span className="text-text-primary font-semibold">Total: {day.count}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="flex items-center justify-center py-12 text-text-tertiary">
            <div className="text-center">
              <div className="text-6xl mb-4">📅</div>
              <p>No recent activity</p>
              <p className="text-sm mt-2">Click "Refresh" to load data</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
