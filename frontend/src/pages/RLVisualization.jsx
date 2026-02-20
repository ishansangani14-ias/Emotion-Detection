import { useState, useEffect } from 'react';
import { getQTable } from '../services/api';

const RLVisualization = () => {
  const [qTable, setQTable] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadQTable();
  }, []);

  const loadQTable = async () => {
    setLoading(true);
    try {
      const data = await getQTable();
      setQTable(data);
    } catch (error) {
      console.error('Error loading Q-table:', error);
    } finally {
      setLoading(false);
    }
  };

  const getColorForValue = (value) => {
    const normalized = Math.max(0, Math.min(1, (value + 1) / 2));
    const r = Math.floor((1 - normalized) * 255);
    const g = Math.floor(normalized * 255);
    return `rgb(${r}, ${g}, 100)`;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-text-primary">Reinforcement Learning Visualization</h1>
        <button
          onClick={loadQTable}
          className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors"
        >
          🔄 Refresh
        </button>
      </div>

      {loading ? (
        <div className="bg-bg-secondary p-12 rounded-lg border border-border-primary text-center">
          <div className="text-4xl mb-4">⏳</div>
          <p className="text-text-tertiary">Loading Q-table...</p>
        </div>
      ) : qTable ? (
        <>
          {/* Q-Table Heatmap */}
          <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
            <h2 className="text-xl font-semibold text-text-primary mb-4">Q-Table Heatmap</h2>
            
            <div className="overflow-x-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr>
                    <th className="p-3 text-left text-text-tertiary border border-border-primary">State</th>
                    {qTable.actions.map((action, idx) => (
                      <th key={idx} className="p-3 text-center text-text-tertiary border border-border-primary">
                        {action}
                      </th>
                    ))}
                    <th className="p-3 text-center text-text-tertiary border border-border-primary">Best Action</th>
                  </tr>
                </thead>
                <tbody>
                  {qTable.states.map((state, stateIdx) => (
                    <tr key={stateIdx}>
                      <td className="p-3 text-text-primary border border-border-primary font-semibold">
                        {state}
                      </td>
                      {qTable.qtable[stateIdx].map((value, actionIdx) => (
                        <td
                          key={actionIdx}
                          className="p-3 text-center border border-border-primary font-mono"
                          style={{ backgroundColor: getColorForValue(value) }}
                        >
                          <span className="text-white font-semibold">
                            {value.toFixed(4)}
                          </span>
                        </td>
                      ))}
                      <td className="p-3 text-center border border-border-primary">
                        <span className="px-3 py-1 bg-primary text-white rounded-full text-sm font-semibold">
                          {qTable.best_actions[stateIdx]}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="mt-4 flex items-center justify-center space-x-4 text-sm">
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 rounded" style={{ backgroundColor: 'rgb(255, 100, 100)' }}></div>
                <span className="text-text-tertiary">Low Value</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 rounded" style={{ backgroundColor: 'rgb(100, 255, 100)' }}></div>
                <span className="text-text-tertiary">High Value</span>
              </div>
            </div>
          </div>

          {/* Learning Stats */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
              <h2 className="text-xl font-semibold text-text-primary mb-4">Learning Progress</h2>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-text-secondary">Epsilon (Exploration Rate)</span>
                    <span className="text-primary font-semibold">{qTable.epsilon.toFixed(4)}</span>
                  </div>
                  <div className="bg-bg-tertiary rounded-full h-3">
                    <div
                      className="bg-primary h-full rounded-full transition-all"
                      style={{ width: `${qTable.epsilon * 100}%` }}
                    ></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-text-secondary">Total Episodes</span>
                    <span className="text-primary font-semibold">{qTable.episodes}</span>
                  </div>
                </div>

                <div className="pt-4 border-t border-border-primary">
                  <p className="text-sm text-text-tertiary">
                    Lower epsilon means more exploitation (using learned knowledge) vs exploration (trying new actions).
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
              <h2 className="text-xl font-semibold text-text-primary mb-4">How It Works</h2>
              <div className="space-y-3 text-sm text-text-secondary">
                <div>
                  <span className="text-primary font-semibold">States:</span> Based on confidence levels of face and text predictions
                </div>
                <div>
                  <span className="text-primary font-semibold">Actions:</span> Trust Face, Trust Text, or Average Both
                </div>
                <div>
                  <span className="text-primary font-semibold">Learning:</span> Q-values updated based on prediction accuracy
                </div>
                <div>
                  <span className="text-primary font-semibold">Goal:</span> Learn which modality to trust in different situations
                </div>
              </div>
            </div>
          </div>

          {/* Action Descriptions */}
          <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
            <h2 className="text-xl font-semibold text-text-primary mb-4">Actions Explained</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-bg-tertiary rounded-lg">
                <h3 className="text-lg font-semibold text-primary mb-2">Trust Face</h3>
                <p className="text-sm text-text-secondary">
                  Use the face model's prediction as the final result. Best when face confidence is high.
                </p>
              </div>
              <div className="p-4 bg-bg-tertiary rounded-lg">
                <h3 className="text-lg font-semibold text-info mb-2">Trust Text</h3>
                <p className="text-sm text-text-secondary">
                  Use the text model's prediction as the final result. Best when text confidence is high.
                </p>
              </div>
              <div className="p-4 bg-bg-tertiary rounded-lg">
                <h3 className="text-lg font-semibold text-success mb-2">Average Both</h3>
                <p className="text-sm text-text-secondary">
                  Average the probabilities from both models. Best when both have similar confidence.
                </p>
              </div>
            </div>
          </div>
        </>
      ) : (
        <div className="bg-bg-secondary p-12 rounded-lg border border-border-primary text-center">
          <div className="text-6xl mb-4">🧠</div>
          <p className="text-xl text-text-tertiary">No Q-learning data available yet</p>
          <p className="text-sm text-text-secondary mt-2">
            Use multimodal detection and provide feedback to train the RL agent
          </p>
        </div>
      )}
    </div>
  );
};

export default RLVisualization;
