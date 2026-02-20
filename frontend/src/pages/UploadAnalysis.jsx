import { useState } from 'react';
import { detectFace, detectBatch } from '../services/api';

const UploadAnalysis = () => {
  const [files, setFiles] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const EMOJI_MAP = {
    happy: '😊',
    sad: '😢',
    angry: '😠',
    surprise: '😲',
    fear: '😨',
    neutral: '😐',
    disgust: '🤢'
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFiles(e.target.files);
    }
  };

  const handleFiles = (fileList) => {
    const newFiles = Array.from(fileList).filter(file => 
      file.type.startsWith('image/')
    );
    setFiles(prev => [...prev, ...newFiles]);
  };

  const handleAnalyze = async () => {
    if (files.length === 0) return;

    setLoading(true);
    setResults([]);

    try {
      if (files.length === 1) {
        // Single file
        const result = await detectFace(files[0]);
        setResults([{ ...result, filename: files[0].name }]);
      } else {
        // Multiple files
        const batchResult = await detectBatch(files);
        const resultsWithNames = batchResult.results.map((result, idx) => ({
          ...result,
          filename: files[idx].name
        }));
        setResults(resultsWithNames);
      }
    } catch (error) {
      console.error('Analysis error:', error);
      alert('Failed to analyze images. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const clearAll = () => {
    setFiles([]);
    setResults([]);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-text-primary">Upload & Analyze Images</h1>

      {/* Upload Section */}
      <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
        <h2 className="text-xl font-semibold text-text-primary mb-4">Upload Images</h2>
        
        <div
          className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
            dragActive 
              ? 'border-primary bg-primary/10' 
              : 'border-border-primary hover:border-primary'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            id="file-upload"
            multiple
            accept="image/*"
            onChange={handleChange}
            className="hidden"
          />
          
          <label htmlFor="file-upload" className="cursor-pointer">
            <div className="text-6xl mb-4">📁</div>
            <p className="text-xl text-text-primary mb-2">
              Click to upload or drag and drop
            </p>
            <p className="text-text-tertiary">
              PNG, JPG, JPEG, BMP (max 16MB per file)
            </p>
            <p className="text-text-tertiary mt-2">
              Upload single or multiple images
            </p>
          </label>
        </div>

        {/* Selected Files */}
        {files.length > 0 && (
          <div className="mt-6">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold text-text-primary">
                Selected: {files.length} image{files.length > 1 ? 's' : ''}
              </h3>
              <button
                onClick={clearAll}
                className="text-error hover:text-red-400 transition-colors"
              >
                Clear All
              </button>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {files.map((file, idx) => (
                <div key={idx} className="relative bg-bg-tertiary rounded-lg p-3">
                  <img
                    src={URL.createObjectURL(file)}
                    alt={file.name}
                    className="w-full h-32 object-cover rounded mb-2"
                  />
                  <p className="text-xs text-text-secondary truncate">{file.name}</p>
                  <button
                    onClick={() => setFiles(files.filter((_, i) => i !== idx))}
                    className="absolute top-1 right-1 bg-error text-white rounded-full w-6 h-6 flex items-center justify-center hover:bg-red-600"
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>

            <div className="mt-4 flex space-x-4">
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="flex-1 px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors font-semibold disabled:opacity-50"
              >
                {loading ? '⏳ Analyzing...' : `🔮 Analyze ${files.length} Image${files.length > 1 ? 's' : ''}`}
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Results Section */}
      {results.length > 0 && (
        <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
          <h2 className="text-xl font-semibold text-text-primary mb-4">
            Results ({results.length} image{results.length > 1 ? 's' : ''})
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {results.map((result, idx) => (
              <div key={idx} className="bg-bg-tertiary rounded-lg p-4 border border-border-primary">
                <div className="text-center mb-3">
                  <div className="text-5xl mb-2">{EMOJI_MAP[result.emotion]}</div>
                  <div className="text-2xl font-bold text-primary uppercase">
                    {result.emotion}
                  </div>
                  <div className="text-lg text-text-secondary">
                    {(result.confidence * 100).toFixed(1)}%
                  </div>
                </div>
                
                <div className="bg-bg-secondary rounded-full h-2 mb-3">
                  <div
                    className="bg-primary h-full rounded-full"
                    style={{ width: `${result.confidence * 100}%` }}
                  ></div>
                </div>
                
                <p className="text-xs text-text-tertiary truncate">{result.filename}</p>
                
                {/* Top 3 emotions */}
                <div className="mt-3 space-y-1">
                  {Object.entries(result.probabilities || {})
                    .sort(([, a], [, b]) => b - a)
                    .slice(0, 3)
                    .map(([emotion, prob]) => (
                      <div key={emotion} className="flex justify-between text-xs">
                        <span className="text-text-tertiary capitalize">{emotion}</span>
                        <span className="text-text-primary">{(prob * 100).toFixed(1)}%</span>
                      </div>
                    ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Info */}
      <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
        <h2 className="text-lg font-semibold text-text-primary mb-3">💡 Tips</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-text-secondary">
          <div>
            <span className="text-primary font-semibold">✓ Good Lighting:</span> Clear, well-lit faces
          </div>
          <div>
            <span className="text-primary font-semibold">✓ Face Visible:</span> Front-facing, unobstructed
          </div>
          <div>
            <span className="text-primary font-semibold">✓ Clear Expression:</span> Exaggerated emotions work best
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadAnalysis;
