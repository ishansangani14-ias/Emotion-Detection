import { useState, useEffect } from 'react';
import { getHistory } from '../services/api';

const History = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    emotion: '',
    mode: ''
  });

  const EMOJI_MAP = {
    happy: '😊',
    sad: '😢',
    angry: '😠',
    surprise: '😲',
    fear: '😨',
    neutral: '😐',
    disgust: '🤢'
  };

  useEffect(() => {
    loadHistory();
  }, [filters]);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const data = await getHistory(filters);
      setHistory(data);
    } catch (error) {
      console.error('Error loading history:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-text-primary">Detection History</h1>
        <button
          onClick={loadHistory}
          className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors"
        >
          🔄 Refresh
        </button>
      </div>

      {/* Filters */}
      <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
        <h2 className="text-lg font-semibold text-text-primary mb-4">Filters</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-text-secondary text-sm mb-2">Emotion</label>
            <select
              value={filters.emotion}
              onChange={(e) => setFilters({ ...filters, emotion: e.target.value })}
              className="w-full p-2 bg-bg-tertiary text-text-primary rounded-lg border border-border-primary focus:border-primary focus:outline-none"
            >
              <option value="">All Emotions</option>
              <option value="happy">Happy</option>
              <option value="sad">Sad</option>
              <option value="angry">Angry</option>
              <option value="surprise">Surprise</option>
              <option value="fear">Fear</option>
              <option value="neutral">Neutral</option>
              <option value="disgust">Disgust</option>
            </select>
          </div>

          <div>
            <label className="block text-text-secondary text-sm mb-2">Mode</label>
            <select
              value={filters.mode}
              onChange={(e) => setFilters({ ...filters, mode: e.target.value })}
              className="w-full p-2 bg-bg-tertiary text-text-primary rounded-lg border border-border-primary focus:border-primary focus:outline-none"
            >
              <option value="">All Modes</option>
              <option value="face">Face Only</option>
              <option value="text">Text Only</option>
              <option value="multimodal">Multimodal</option>
            </select>
          </div>

          <div className="flex items-end">
            <button
              onClick={() => setFilters({ emotion: '', mode: '' })}
              className="w-full p-2 bg-bg-tertiary text-text-secondary rounded-lg hover:bg-border-primary transition-colors"
            >
              Clear Filters
            </button>
          </div>
        </div>
      </div>

      {/* History Table */}
      <div className="bg-bg-secondary rounded-lg border border-border-primary overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-text-tertiary">
            <div className="text-4xl mb-4">⏳</div>
            <p>Loading history...</p>
          </div>
        ) : history.length === 0 ? (
          <div className="p-12 text-center text-text-tertiary">
            <div className="text-6xl mb-4">📜</div>
            <p className="text-xl">No detections found</p>
            <p className="text-sm mt-2">Start detecting emotions to see history here</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-bg-tertiary">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-text-tertiary uppercase">Date</th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-text-tertiary uppercase">Emotion</th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-text-tertiary uppercase">Confidence</th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-text-tertiary uppercase">Mode</th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-text-tertiary uppercase">Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-primary">
                {history.map((item, idx) => (
                  <tr key={idx} className="hover:bg-bg-tertiary transition-colors">
                    <td className="px-6 py-4 text-sm text-text-secondary">
                      {formatDate(item.timestamp)}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl">{EMOJI_MAP[item.emotion]}</span>
                        <span className="text-text-primary capitalize font-semibold">
                          {item.emotion}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-2">
                        <div className="w-24 bg-bg-tertiary rounded-full h-2">
                          <div
                            className="bg-primary h-full rounded-full"
                            style={{ width: `${item.confidence * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-text-primary text-sm font-semibold">
                          {(item.confidence * 100).toFixed(1)}%
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        item.mode === 'face' ? 'bg-primary/20 text-primary' :
                        item.mode === 'text' ? 'bg-info/20 text-info' :
                        'bg-success/20 text-success'
                      }`}>
                        {item.mode}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-text-secondary">
                      {item.mode === 'multimodal' && (
                        <div className="text-xs">
                          <div>Face: {item.face_emotion} ({(item.face_confidence * 100).toFixed(0)}%)</div>
                          <div>Text: {item.text_emotion} ({(item.text_confidence * 100).toFixed(0)}%)</div>
                        </div>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Stats */}
      {history.length > 0 && (
        <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
          <h2 className="text-lg font-semibold text-text-primary mb-4">Summary</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">{history.length}</div>
              <div className="text-sm text-text-tertiary">Total Detections</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-info">
                {history.filter(h => h.mode === 'face').length}
              </div>
              <div className="text-sm text-text-tertiary">Face Only</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-success">
                {history.filter(h => h.mode === 'text').length}
              </div>
              <div className="text-sm text-text-tertiary">Text Only</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-warning">
                {history.filter(h => h.mode === 'multimodal').length}
              </div>
              <div className="text-sm text-text-tertiary">Multimodal</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default History;
