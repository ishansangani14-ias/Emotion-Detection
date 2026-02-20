import { useState } from 'react';
import { detectText } from '../services/api';

const TextAnalysis = () => {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const EMOJI_MAP = {
    happy: '😊',
    sad: '😢',
    angry: '😠',
    surprise: '😲',
    fear: '😨',
    neutral: '😐',
    disgust: '🤢'
  };

  const handleAnalyze = async () => {
    if (!text.trim()) {
      setError('Please enter some text');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await detectText(text);
      setResult(data);
    } catch (err) {
      setError('Failed to analyze text. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-text-primary">Text Emotion Analysis</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Section */}
        <div className="space-y-4">
          <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
            <h2 className="text-xl font-semibold text-text-primary mb-4">Enter Text</h2>
            
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Type your message here... (e.g., 'I am so happy today!')"
              className="w-full h-48 p-4 bg-bg-tertiary text-text-primary rounded-lg border border-border-primary focus:border-primary focus:outline-none resize-none"
            />

            <div className="mt-4 flex space-x-4">
              <button
                onClick={handleAnalyze}
                disabled={loading || !text.trim()}
                className="flex-1 px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? '⏳ Analyzing...' : '🔮 Analyze Emotion'}
              </button>
              
              <button
                onClick={() => {
                  setText('');
                  setResult(null);
                  setError(null);
                }}
                className="px-6 py-3 bg-bg-tertiary text-text-secondary rounded-lg hover:bg-border-primary transition-colors"
              >
                Clear
              </button>
            </div>

            {error && (
              <div className="mt-4 p-3 bg-error/20 border border-error rounded-lg text-error">
                {error}
              </div>
            )}
          </div>

          {/* Example Texts */}
          <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
            <h3 className="text-lg font-semibold text-text-primary mb-3">Try These Examples:</h3>
            <div className="space-y-2">
              {[
                "I am so happy today! Everything is going great!",
                "I feel sad and lonely. Nothing seems to work out.",
                "This makes me so angry! I can't believe this happened!",
                "Wow! I didn't expect that at all! Amazing!",
                "I'm scared about what might happen next.",
                "This is disgusting and unacceptable behavior."
              ].map((example, idx) => (
                <button
                  key={idx}
                  onClick={() => setText(example)}
                  className="w-full text-left p-3 bg-bg-tertiary text-text-secondary rounded-lg hover:bg-border-primary hover:text-text-primary transition-colors text-sm"
                >
                  "{example}"
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Results Section */}
        <div className="space-y-4">
          {result ? (
            <>
              {/* Main Result */}
              <div className="bg-bg-secondary p-6 rounded-lg border-2 border-primary">
                <h2 className="text-lg font-semibold text-text-tertiary mb-4">Detected Emotion</h2>
                
                <div className="text-center">
                  <div className="text-7xl mb-4">
                    {EMOJI_MAP[result.emotion] || '😐'}
                  </div>
                  <div className="text-4xl font-bold text-primary uppercase mb-2">
                    {result.emotion}
                  </div>
                  <div className="text-2xl text-text-secondary mb-4">
                    {(result.confidence * 100).toFixed(1)}% confidence
                  </div>
                  
                  {/* Confidence Bar */}
                  <div className="bg-bg-tertiary rounded-full h-4 overflow-hidden">
                    <div
                      className="bg-primary h-full transition-all duration-300"
                      style={{ width: `${result.confidence * 100}%` }}
                    ></div>
                  </div>
                </div>
              </div>

              {/* All Probabilities */}
              <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
                <h2 className="text-lg font-semibold text-text-tertiary mb-4">All Emotions</h2>
                <div className="space-y-3">
                  {Object.entries(result.probabilities || {})
                    .sort(([, a], [, b]) => b - a)
                    .map(([emotion, prob]) => (
                      <div key={emotion} className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <span className="text-3xl">{EMOJI_MAP[emotion]}</span>
                          <span className="text-text-secondary capitalize">{emotion}</span>
                        </div>
                        <div className="flex items-center space-x-3">
                          <div className="w-32 bg-bg-tertiary rounded-full h-2">
                            <div
                              className="bg-primary h-full rounded-full transition-all duration-300"
                              style={{ width: `${prob * 100}%` }}
                            ></div>
                          </div>
                          <span className="text-text-primary font-semibold w-16 text-right">
                            {(prob * 100).toFixed(1)}%
                          </span>
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            </>
          ) : (
            <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary h-full flex items-center justify-center">
              <div className="text-center text-text-tertiary">
                <div className="text-6xl mb-4">💬</div>
                <p className="text-lg">Enter text and click "Analyze Emotion" to see results</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Info Section */}
      <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
        <h2 className="text-lg font-semibold text-text-primary mb-3">💡 How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-text-secondary">
          <div>
            <span className="text-primary font-semibold">TF-IDF Vectorization:</span> Converts text into numerical features
          </div>
          <div>
            <span className="text-primary font-semibold">Logistic Regression:</span> Classifies emotions based on text patterns
          </div>
          <div>
            <span className="text-primary font-semibold">7 Emotions:</span> Detects happy, sad, angry, surprise, fear, neutral, disgust
          </div>
        </div>
      </div>
    </div>
  );
};

export default TextAnalysis;
