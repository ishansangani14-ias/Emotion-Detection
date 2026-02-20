import { useState, useRef, useEffect } from 'react';
import Webcam from 'react-webcam';
import { detectFace } from '../services/api';

const EMOJI_MAP = {
  happy: { emoji: '😊', animation: 'bounce' },
  sad: { emoji: '😢', animation: 'fall' },
  angry: { emoji: '😠', animation: 'shake' },
  surprise: { emoji: '😲', animation: 'pop' },
  fear: { emoji: '😨', animation: 'pulse' },
  neutral: { emoji: '😐', animation: 'fade' },
  disgust: { emoji: '🤢', animation: 'distort' }
};

const RealtimeDetection = () => {
  const webcamRef = useRef(null);
  const [isDetecting, setIsDetecting] = useState(false);
  const [currentEmotion, setCurrentEmotion] = useState(null);
  const [confidence, setConfidence] = useState(0);
  const [probabilities, setProbabilities] = useState({});
  const detectionInterval = useRef(null);
  
  const startDetection = () => {
    setIsDetecting(true);
    
    detectionInterval.current = setInterval(async () => {
      if (webcamRef.current) {
        const imageSrc = webcamRef.current.getScreenshot();
        if (imageSrc) {
          try {
            // Convert base64 to blob
            const blob = await fetch(imageSrc).then(r => r.blob());
            const file = new File([blob], 'frame.jpg', { type: 'image/jpeg' });
            
            // Detect emotion
            const result = await detectFace(file);
            setCurrentEmotion(result.emotion);
            setConfidence(result.confidence);
            setProbabilities(result.probabilities);
          } catch (error) {
            console.error('Detection error:', error);
          }
        }
      }
    }, 500); // Detect every 500ms
  };
  
  const stopDetection = () => {
    setIsDetecting(false);
    if (detectionInterval.current) {
      clearInterval(detectionInterval.current);
    }
  };
  
  useEffect(() => {
    return () => {
      if (detectionInterval.current) {
        clearInterval(detectionInterval.current);
      }
    };
  }, []);
  
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-text-primary">Real-Time Emotion Detection</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Camera Section */}
        <div className="lg:col-span-2 space-y-4">
          <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
            <div className="relative">
              <Webcam
                ref={webcamRef}
                audio={false}
                screenshotFormat="image/jpeg"
                className="w-full rounded-lg"
                videoConstraints={{
                  width: 1280,
                  height: 720,
                  facingMode: "user"
                }}
              />
              
              {/* Emoji Overlay */}
              {isDetecting && currentEmotion && (
                <div className="absolute top-1/4 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                  <div className={`text-8xl animate-${EMOJI_MAP[currentEmotion]?.animation || 'pulse'}`}>
                    {EMOJI_MAP[currentEmotion]?.emoji}
                  </div>
                </div>
              )}
              
              {/* Live Indicator */}
              {isDetecting && (
                <div className="absolute top-4 left-4 bg-error px-3 py-1 rounded-full flex items-center space-x-2">
                  <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                  <span className="text-white text-sm font-semibold">LIVE</span>
                </div>
              )}
            </div>
            
            {/* Controls */}
            <div className="mt-4 flex space-x-4">
              {!isDetecting ? (
                <button
                  onClick={startDetection}
                  className="flex-1 px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors font-semibold"
                >
                  🎬 Start Live Detection
                </button>
              ) : (
                <button
                  onClick={stopDetection}
                  className="flex-1 px-6 py-3 bg-error text-white rounded-lg hover:bg-red-600 transition-colors font-semibold"
                >
                  ⏹ Stop Detection
                </button>
              )}
            </div>
          </div>
        </div>
        
        {/* Results Section */}
        <div className="space-y-4">
          {/* Current Emotion */}
          <div className="bg-bg-secondary p-6 rounded-lg border-2 border-primary">
            <h2 className="text-lg font-semibold text-text-tertiary mb-4">Current Emotion</h2>
            {currentEmotion ? (
              <>
                <div className="text-5xl text-center mb-2">
                  {EMOJI_MAP[currentEmotion]?.emoji}
                </div>
                <div className="text-3xl font-bold text-primary text-center uppercase mb-2">
                  {currentEmotion}
                </div>
                <div className="text-xl text-text-secondary text-center">
                  {(confidence * 100).toFixed(1)}% confidence
                </div>
                
                {/* Confidence Bar */}
                <div className="mt-4 bg-bg-tertiary rounded-full h-3 overflow-hidden">
                  <div
                    className="bg-primary h-full transition-all duration-300"
                    style={{ width: `${confidence * 100}%` }}
                  ></div>
                </div>
              </>
            ) : (
              <div className="text-center text-text-tertiary py-8">
                Start detection to see results
              </div>
            )}
          </div>
          
          {/* All Probabilities */}
          {Object.keys(probabilities).length > 0 && (
            <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
              <h2 className="text-lg font-semibold text-text-tertiary mb-4">All Emotions</h2>
              <div className="space-y-2">
                {Object.entries(probabilities)
                  .sort(([, a], [, b]) => b - a)
                  .map(([emotion, prob]) => (
                    <div key={emotion} className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl">{EMOJI_MAP[emotion]?.emoji}</span>
                        <span className="text-text-secondary capitalize">{emotion}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="w-24 bg-bg-tertiary rounded-full h-2">
                          <div
                            className="bg-primary h-full rounded-full transition-all duration-300"
                            style={{ width: `${prob * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-text-primary font-semibold w-12 text-right">
                          {(prob * 100).toFixed(1)}%
                        </span>
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* Tips */}
      <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
        <h2 className="text-lg font-semibold text-text-primary mb-3">💡 Tips for Best Results</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-text-secondary">
          <div>
            <span className="text-primary font-semibold">✓ Good Lighting:</span> Face well-lit, no shadows
          </div>
          <div>
            <span className="text-primary font-semibold">✓ Face Camera:</span> Look directly at camera
          </div>
          <div>
            <span className="text-primary font-semibold">✓ Clear Expressions:</span> Exaggerated emotions work best
          </div>
        </div>
      </div>
    </div>
  );
};

export default RealtimeDetection;
