const Theory = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-text-primary">System Theory & Architecture</h1>
      
      {/* Overview */}
      <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
        <h2 className="text-2xl font-semibold text-primary mb-4">🎯 System Overview</h2>
        <p className="text-text-secondary leading-relaxed">
          The Emotion Intelligence Platform is a multimodal AI system that combines facial expression analysis,
          natural language processing, and reinforcement learning to accurately detect and classify human emotions.
          The system uses deep learning models trained on large-scale datasets to achieve industry-level performance.
        </p>
      </div>

      {/* CNN Architecture */}
      <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
        <h2 className="text-2xl font-semibold text-primary mb-4">🧠 CNN Architecture (Face Detection)</h2>
        
        <div className="space-y-4">
          <div className="bg-bg-tertiary p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-text-primary mb-2">Model Structure</h3>
            <div className="space-y-2 text-text-secondary">
              <div className="flex items-center space-x-2">
                <span className="text-primary font-mono">→</span>
                <span>Input Layer: 48x48 grayscale images</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-primary font-mono">→</span>
                <span>Conv Block 1: 32 filters, 3x3 kernel + BatchNorm + ReLU + MaxPool</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-primary font-mono">→</span>
                <span>Conv Block 2: 64 filters, 3x3 kernel + BatchNorm + ReLU + MaxPool</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-primary font-mono">→</span>
                <span>Conv Block 3: 128 filters, 3x3 kernel + BatchNorm + ReLU + MaxPool</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-primary font-mono">→</span>
                <span>Conv Block 4: 256 filters, 3x3 kernel + BatchNorm + ReLU + MaxPool</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-primary font-mono">→</span>
                <span>Flatten Layer</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-primary font-mono">→</span>
                <span>Dense Layer: 512 units + Dropout(0.5)</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-primary font-mono">→</span>
                <span>Output Layer: 7 units (emotions) + Softmax</span>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-bg-tertiary p-4 rounded-lg">
              <h3 className="text-lg font-semibold text-text-primary mb-2">Training Details</h3>
              <ul className="space-y-1 text-sm text-text-secondary">
                <li>• Dataset: FER2013 (35,887 images)</li>
                <li>• Optimizer: Adam (lr=0.001)</li>
                <li>• Loss: Categorical Crossentropy</li>
                <li>• Batch Size: 64</li>
                <li>• Epochs: 50 with early stopping</li>
                <li>• Data Augmentation: rotation, shift, flip</li>
              </ul>
            </div>
            
            <div className="bg-bg-tertiary p-4 rounded-lg">
              <h3 className="text-lg font-semibold text-text-primary mb-2">Performance Metrics</h3>
              <ul className="space-y-1 text-sm text-text-secondary">
                <li>• Validation Accuracy: ~65%</li>
                <li>• Test Accuracy: ~63%</li>
                <li>• Inference Time: ~50ms</li>
                <li>• Model Size: 2.5MB</li>
                <li>• Parameters: ~1.2M</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* NLP Pipeline */}
      <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
        <h2 className="text-2xl font-semibold text-primary mb-4">📝 NLP Pipeline (Text Analysis)</h2>
        
        <div className="space-y-4">
          <div className="bg-bg-tertiary p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-text-primary mb-2">Processing Pipeline</h3>
            <div className="space-y-2 text-text-secondary">
              <div className="flex items-center space-x-2">
                <span className="text-primary font-mono">1.</span>
                <span>Text Preprocessing: lowercase, remove punctuation, tokenization</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-primary font-mono">2.</span>
                <span>Feature Extraction: TF-IDF vectorization (max 5000 features)</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-primary font-mono">3.</span>
                <span>Classification: Logistic Regression with L2 regularization</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-primary font-mono">4.</span>
                <span>Output: Emotion probabilities for 7 classes</span>
              </div>
            </div>
          </div>

          <div className="bg-bg-tertiary p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-text-primary mb-2">Key Features</h3>
            <ul className="space-y-1 text-sm text-text-secondary">
              <li>• Handles variable-length text input</li>
              <li>• Captures semantic meaning through TF-IDF</li>
              <li>• Fast inference (~10ms per text)</li>
              <li>• Robust to typos and informal language</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Reinforcement Learning */}
      <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
        <h2 className="text-2xl font-semibold text-primary mb-4">🎮 Reinforcement Learning Fusion</h2>
        
        <div className="space-y-4">
          <div className="bg-bg-tertiary p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-text-primary mb-2">Q-Learning Agent</h3>
            <p className="text-text-secondary mb-3">
              The RL agent learns optimal fusion strategies by treating multimodal fusion as a decision-making problem.
            </p>
            
            <div className="space-y-2 text-text-secondary text-sm">
              <div><span className="text-primary font-semibold">States:</span> Confidence levels (high-high, high-low, low-high, low-low)</div>
              <div><span className="text-primary font-semibold">Actions:</span> trust_face, trust_text, average</div>
              <div><span className="text-primary font-semibold">Reward:</span> +1 for correct, -1 for incorrect prediction</div>
              <div><span className="text-primary font-semibold">Policy:</span> ε-greedy (ε decays from 1.0 to 0.1)</div>
            </div>
          </div>

          <div className="bg-bg-tertiary p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-text-primary mb-2">Q-Table Update Rule</h3>
            <div className="bg-bg-primary p-3 rounded font-mono text-sm text-text-secondary">
              Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',a') - Q(s,a)]
            </div>
            <div className="mt-2 text-sm text-text-secondary">
              <div>α (learning rate) = 0.1</div>
              <div>γ (discount factor) = 0.9</div>
            </div>
          </div>

          <div className="bg-bg-tertiary p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-text-primary mb-2">Fusion Strategies</h3>
            <ul className="space-y-1 text-sm text-text-secondary">
              <li>• <span className="text-primary font-semibold">trust_face:</span> Use face model prediction</li>
              <li>• <span className="text-primary font-semibold">trust_text:</span> Use text model prediction</li>
              <li>• <span className="text-primary font-semibold">average:</span> Average both model probabilities</li>
            </ul>
          </div>
        </div>
      </div>

      {/* System Architecture */}
      <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
        <h2 className="text-2xl font-semibold text-primary mb-4">🏗️ System Architecture</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-bg-tertiary p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-text-primary mb-2">Frontend</h3>
            <ul className="space-y-1 text-sm text-text-secondary">
              <li>• React.js + Vite</li>
              <li>• Tailwind CSS</li>
              <li>• Chart.js for visualization</li>
              <li>• WebSocket for real-time</li>
              <li>• Webcam API integration</li>
            </ul>
          </div>
          
          <div className="bg-bg-tertiary p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-text-primary mb-2">Backend</h3>
            <ul className="space-y-1 text-sm text-text-secondary">
              <li>• FastAPI framework</li>
              <li>• TensorFlow/Keras models</li>
              <li>• OpenCV for preprocessing</li>
              <li>• SQLAlchemy ORM</li>
              <li>• Async request handling</li>
            </ul>
          </div>
          
          <div className="bg-bg-tertiary p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-text-primary mb-2">Database</h3>
            <ul className="space-y-1 text-sm text-text-secondary">
              <li>• PostgreSQL</li>
              <li>• Detection history storage</li>
              <li>• RL training logs</li>
              <li>• User feedback tracking</li>
              <li>• Analytics aggregation</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Emotion Classes */}
      <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
        <h2 className="text-2xl font-semibold text-primary mb-4">😊 Emotion Classes</h2>
        
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
          {[
            { emoji: '😊', name: 'Happy', desc: 'Joy, pleasure' },
            { emoji: '😢', name: 'Sad', desc: 'Sorrow, grief' },
            { emoji: '😠', name: 'Angry', desc: 'Rage, frustration' },
            { emoji: '😲', name: 'Surprise', desc: 'Shock, amazement' },
            { emoji: '😨', name: 'Fear', desc: 'Anxiety, terror' },
            { emoji: '😐', name: 'Neutral', desc: 'Calm, composed' },
            { emoji: '🤢', name: 'Disgust', desc: 'Revulsion, distaste' }
          ].map(emotion => (
            <div key={emotion.name} className="bg-bg-tertiary p-4 rounded-lg text-center">
              <div className="text-4xl mb-2">{emotion.emoji}</div>
              <div className="text-text-primary font-semibold mb-1">{emotion.name}</div>
              <div className="text-xs text-text-tertiary">{emotion.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Theory;
