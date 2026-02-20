import { useState, useEffect } from 'react';
import { LineChart, Line, PieChart, Pie, BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getAnalytics } from '../services/api';

const COLORS = ['#FF6B35', '#4ECDC4', '#FF3366', '#FFD93D', '#A78BFA', '#6B7280', '#10B981'];

const Analytics = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('7d');

  useEffect(() => {
    loadAnalytics();
  }, [timeRange]);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      const data = await getAnalytics(timeRange);
      setAnalytics(data);
    } catch (error) {
      console.error('Failed to load analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-text-secondary">Loading analytics...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-text-primary">Analytics Dashboard</h1>
        
        <div className="flex space-x-2">
          {['24h', '7d', '30d', 'all'].map(range => (
            <button
              key={range}
              onClick={() => setTimeRange(range)}
              className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
                timeRange === range
                  ? 'bg-primary text-white'
                  : 'bg-bg-secondary text-text-secondary hover:bg-bg-tertiary'
              }`}
            >
              {range === '24h' ? '24 Hours' : range === '7d' ? '7 Days' : range === '30d' ? '30 Days' : 'All Time'}
            </button>
          ))}
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
          <div className="text-text-tertiary text-sm mb-2">Total Detections</div>
          <div className="text-3xl font-bold text-primary">{analytics?.total_detections || 0}</div>
        </div>
        
        <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
          <div className="text-text-tertiary text-sm mb-2">Average Accuracy</div>
          <div className="text-3xl font-bold text-primary">
            {analytics?.avg_accuracy ? `${(analytics.avg_accuracy * 100).toFixed(1)}%` : 'N/A'}
          </div>
        </div>
        
        <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
          <div className="text-text-tertiary text-sm mb-2">Average Confidence</div>
          <div className="text-3xl font-bold text-primary">
            {analytics?.avg_confidence ? `${(analytics.avg_confidence * 100).toFixed(1)}%` : 'N/A'}
          </div>
        </div>
        
        <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
          <div className="text-text-tertiary text-sm mb-2">Most Common Emotion</div>
          <div className="text-2xl font-bold text-primary capitalize">
            {analytics?.most_common_emotion || 'N/A'}
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Emotion Distribution */}
        <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
          <h2 className="text-xl font-semibold text-text-primary mb-4">Emotion Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={analytics?.emotion_distribution || []}
                dataKey="count"
                nameKey="emotion"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={(entry) => entry.emotion}
              >
                {(analytics?.emotion_distribution || []).map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ backgroundColor: '#1A1A1A', border: '1px solid #3A3A3A' }} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Accuracy Trend */}
        <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
          <h2 className="text-xl font-semibold text-text-primary mb-4">Accuracy Trend</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={analytics?.accuracy_trend || []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="date" stroke="#9CA3AF" />
              <YAxis stroke="#9CA3AF" />
              <Tooltip contentStyle={{ backgroundColor: '#1A1A1A', border: '1px solid #3A3A3A' }} />
              <Legend />
              <Line type="monotone" dataKey="accuracy" stroke="#FF6B35" strokeWidth={2} dot={{ fill: '#FF6B35' }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Confidence Trend */}
        <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
          <h2 className="text-xl font-semibold text-text-primary mb-4">Confidence Trend</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={analytics?.confidence_trend || []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="date" stroke="#9CA3AF" />
              <YAxis stroke="#9CA3AF" />
              <Tooltip contentStyle={{ backgroundColor: '#1A1A1A', border: '1px solid #3A3A3A' }} />
              <Legend />
              <Line type="monotone" dataKey="avg_confidence" stroke="#4ECDC4" strokeWidth={2} dot={{ fill: '#4ECDC4' }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Detections Per Day */}
        <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
          <h2 className="text-xl font-semibold text-text-primary mb-4">Detections Per Day</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={analytics?.detections_per_day || []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="date" stroke="#9CA3AF" />
              <YAxis stroke="#9CA3AF" />
              <Tooltip contentStyle={{ backgroundColor: '#1A1A1A', border: '1px solid #3A3A3A' }} />
              <Legend />
              <Bar dataKey="count" fill="#FF6B35" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Mode Breakdown */}
      <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
        <h2 className="text-xl font-semibold text-text-primary mb-4">Detection Mode Breakdown</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {analytics?.mode_breakdown?.map(mode => (
            <div key={mode.mode} className="bg-bg-tertiary p-4 rounded-lg">
              <div className="text-text-tertiary text-sm mb-1 capitalize">{mode.mode}</div>
              <div className="text-2xl font-bold text-primary">{mode.count}</div>
              <div className="text-text-secondary text-sm">
                {((mode.count / analytics.total_detections) * 100).toFixed(1)}% of total
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Analytics;
