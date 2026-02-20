import { useState, useEffect } from 'react';
import axios from 'axios';

const Settings = () => {
  const [settings, setSettings] = useState({
    detectionThreshold: 0.5,
    autoSave: true,
    enableSound: false,
    darkMode: true,
    rlEnabled: true,
    learningRate: 0.1,
    epsilon: 0.3
  });

  const [saved, setSaved] = useState(false);
  const [apiStatus, setApiStatus] = useState('checking');
  const [clearing, setClearing] = useState(false);

  // Load settings from localStorage on mount
  useEffect(() => {
    const savedSettings = localStorage.getItem('eip_settings');
    if (savedSettings) {
      try {
        const parsed = JSON.parse(savedSettings);
        setSettings(parsed);
      } catch (error) {
        console.error('Error loading settings:', error);
      }
    }
    
    // Check API status
    checkApiStatus();
  }, []);

  const checkApiStatus = async () => {
    try {
      const response = await axios.get('http://localhost:8000/health', { timeout: 3000 });
      if (response.data.status === 'healthy') {
        setApiStatus('connected');
      } else {
        setApiStatus('error');
      }
    } catch (error) {
      setApiStatus('disconnected');
    }
  };

  const handleChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
    setSaved(false);
  };

  const handleSave = () => {
    try {
      // Save to localStorage
      localStorage.setItem('eip_settings', JSON.stringify(settings));
      setSaved(true);
      
      // Show success message
      console.log('Settings saved successfully:', settings);
      
      // Hide success message after 3 seconds
      setTimeout(() => setSaved(false), 3000);
    } catch (error) {
      console.error('Error saving settings:', error);
      alert('Failed to save settings. Please try again.');
    }
  };

  const handleReset = () => {
    if (window.confirm('Reset all settings to default values?')) {
      const defaultSettings = {
        detectionThreshold: 0.5,
        autoSave: true,
        enableSound: false,
        darkMode: true,
        rlEnabled: true,
        learningRate: 0.1,
        epsilon: 0.3
      };
      setSettings(defaultSettings);
      localStorage.setItem('eip_settings', JSON.stringify(defaultSettings));
      
      // Show feedback
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
      
      console.log('Settings reset to defaults');
    }
  };

  const handleClearHistory = async () => {
    if (window.confirm('⚠️ Are you sure you want to clear all detection history?\n\nThis will permanently delete:\n• All detection records\n• Analytics data\n• RL training history\n\nThis action CANNOT be undone!')) {
      setClearing(true);
      try {
        // Call API to clear history
        await axios.delete('http://localhost:8000/api/history/clear');
        
        // Also clear any local data
        localStorage.removeItem('detection_history');
        
        alert('✅ History cleared successfully!');
        console.log('History cleared');
      } catch (error) {
        console.error('Error clearing history:', error);
        alert('⚠️ Failed to clear history. The API might be unavailable.');
      } finally {
        setClearing(false);
      }
    }
  };

  const handleExportSettings = () => {
    const dataStr = JSON.stringify(settings, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'eip-settings.json';
    link.click();
    URL.revokeObjectURL(url);
    console.log('Settings exported');
  };

  const handleImportSettings = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const imported = JSON.parse(e.target.result);
          setSettings(imported);
          localStorage.setItem('eip_settings', JSON.stringify(imported));
          setSaved(true);
          setTimeout(() => setSaved(false), 3000);
          console.log('Settings imported successfully');
        } catch (error) {
          alert('Invalid settings file. Please check the file format.');
          console.error('Import error:', error);
        }
      };
      reader.readAsText(file);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-text-primary">Settings</h1>

      {/* Detection Settings */}
      <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
        <h2 className="text-xl font-semibold text-text-primary mb-4">🎯 Detection Settings</h2>
        
        <div className="space-y-4">
          <div>
            <label className="block text-text-secondary mb-2">
              Confidence Threshold: {(settings.detectionThreshold * 100).toFixed(0)}%
            </label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.05"
              value={settings.detectionThreshold}
              onChange={(e) => handleChange('detectionThreshold', parseFloat(e.target.value))}
              className="w-full h-2 bg-bg-tertiary rounded-lg appearance-none cursor-pointer accent-primary"
            />
            <p className="text-sm text-text-tertiary mt-1">
              Minimum confidence level required to display detection results
            </p>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <div className="text-text-primary font-semibold">Auto-save Detections</div>
              <div className="text-sm text-text-tertiary">Automatically save all detections to history</div>
            </div>
            <button
              onClick={() => handleChange('autoSave', !settings.autoSave)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                settings.autoSave ? 'bg-primary' : 'bg-bg-tertiary'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  settings.autoSave ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <div className="text-text-primary font-semibold">Enable Sound Notifications</div>
              <div className="text-sm text-text-tertiary">Play sound when emotion is detected</div>
            </div>
            <button
              onClick={() => handleChange('enableSound', !settings.enableSound)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                settings.enableSound ? 'bg-primary' : 'bg-bg-tertiary'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  settings.enableSound ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
        </div>
      </div>

      {/* RL Settings */}
      <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
        <h2 className="text-xl font-semibold text-text-primary mb-4">🎮 Reinforcement Learning</h2>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-text-primary font-semibold">Enable RL Fusion</div>
              <div className="text-sm text-text-tertiary">Use reinforcement learning for multimodal fusion</div>
            </div>
            <button
              onClick={() => handleChange('rlEnabled', !settings.rlEnabled)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                settings.rlEnabled ? 'bg-primary' : 'bg-bg-tertiary'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  settings.rlEnabled ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>

          {settings.rlEnabled && (
            <>
              <div>
                <label className="block text-text-secondary mb-2">
                  Learning Rate (α): {settings.learningRate.toFixed(2)}
                </label>
                <input
                  type="range"
                  min="0.01"
                  max="0.5"
                  step="0.01"
                  value={settings.learningRate}
                  onChange={(e) => handleChange('learningRate', parseFloat(e.target.value))}
                  className="w-full h-2 bg-bg-tertiary rounded-lg appearance-none cursor-pointer accent-primary"
                />
                <p className="text-sm text-text-tertiary mt-1">
                  Controls how quickly the agent learns from new experiences
                </p>
              </div>

              <div>
                <label className="block text-text-secondary mb-2">
                  Exploration Rate (ε): {settings.epsilon.toFixed(2)}
                </label>
                <input
                  type="range"
                  min="0.1"
                  max="1.0"
                  step="0.05"
                  value={settings.epsilon}
                  onChange={(e) => handleChange('epsilon', parseFloat(e.target.value))}
                  className="w-full h-2 bg-bg-tertiary rounded-lg appearance-none cursor-pointer accent-primary"
                />
                <p className="text-sm text-text-tertiary mt-1">
                  Balance between exploration (random) and exploitation (learned)
                </p>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Appearance */}
      <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
        <h2 className="text-xl font-semibold text-text-primary mb-4">🎨 Appearance</h2>
        
        <div className="flex items-center justify-between">
          <div>
            <div className="text-text-primary font-semibold">Dark Mode</div>
            <div className="text-sm text-text-tertiary">Currently enabled (Light mode coming soon)</div>
          </div>
          <button
            onClick={() => handleChange('darkMode', !settings.darkMode)}
            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
              settings.darkMode ? 'bg-primary' : 'bg-bg-tertiary'
            }`}
            disabled
          >
            <span
              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                settings.darkMode ? 'translate-x-6' : 'translate-x-1'
              }`}
            />
          </button>
        </div>
        
        <div className="mt-4 p-3 bg-bg-tertiary rounded-lg border border-border-primary">
          <p className="text-sm text-text-tertiary">
            💡 Light mode is coming in a future update. For now, enjoy the sleek dark theme!
          </p>
        </div>
      </div>

      {/* Data Management */}
      <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
        <h2 className="text-xl font-semibold text-text-primary mb-4">💾 Data Management</h2>
        
        <div className="space-y-4">
          <button
            onClick={handleClearHistory}
            disabled={clearing}
            className="w-full px-6 py-3 bg-error text-white rounded-lg hover:bg-red-600 transition-colors font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {clearing ? '⏳ Clearing...' : '🗑️ Clear All Detection History'}
          </button>
          
          <div className="text-sm text-text-tertiary">
            This will permanently delete all stored detections, analytics data, and RL training history.
          </div>

          <div className="grid grid-cols-2 gap-4 mt-4">
            <button
              onClick={handleExportSettings}
              className="px-4 py-2 bg-bg-tertiary text-text-primary rounded-lg hover:bg-border-primary transition-colors border border-border-primary"
            >
              📥 Export Settings
            </button>
            
            <label className="px-4 py-2 bg-bg-tertiary text-text-primary rounded-lg hover:bg-border-primary transition-colors border border-border-primary cursor-pointer text-center">
              📤 Import Settings
              <input
                type="file"
                accept=".json"
                onChange={handleImportSettings}
                className="hidden"
              />
            </label>
          </div>
        </div>
      </div>

      {/* Save/Reset Buttons */}
      <div className="space-y-4">
        {saved && (
          <div className="p-4 bg-success/20 border border-success rounded-lg">
            <p className="text-success font-semibold">✓ Settings saved successfully!</p>
          </div>
        )}
        
        <div className="flex space-x-4">
          <button
            onClick={handleSave}
            className="flex-1 px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors font-semibold"
          >
            {saved ? '✓ Saved!' : '💾 Save Settings'}
          </button>
          
          <button
            onClick={handleReset}
            className="px-6 py-3 bg-bg-tertiary text-text-primary rounded-lg hover:bg-bg-primary transition-colors border border-border-primary font-semibold"
          >
            🔄 Reset to Defaults
          </button>
        </div>
      </div>

      {/* System Info */}
      <div className="bg-bg-secondary p-6 rounded-lg border border-border-primary">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-text-primary">ℹ️ System Information</h2>
          <button
            onClick={checkApiStatus}
            className="px-3 py-1 text-sm bg-bg-tertiary text-text-secondary rounded hover:bg-border-primary transition-colors"
          >
            🔄 Refresh
          </button>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <div className="text-text-tertiary">Platform Version</div>
            <div className="text-text-primary font-semibold">2.0.0</div>
          </div>
          
          <div>
            <div className="text-text-tertiary">API Status</div>
            <div className={`font-semibold ${
              apiStatus === 'connected' ? 'text-success' :
              apiStatus === 'checking' ? 'text-warning' :
              'text-error'
            }`}>
              ● {apiStatus === 'connected' ? 'Connected' : 
                 apiStatus === 'checking' ? 'Checking...' : 
                 'Disconnected'}
            </div>
          </div>
          
          <div>
            <div className="text-text-tertiary">Face Model</div>
            <div className="text-text-primary font-semibold">CNN v1.0</div>
          </div>
          
          <div>
            <div className="text-text-tertiary">Text Model</div>
            <div className="text-text-primary font-semibold">TF-IDF + LR v1.0</div>
          </div>

          <div>
            <div className="text-text-tertiary">RL Agent</div>
            <div className="text-text-primary font-semibold">
              {settings.rlEnabled ? '✓ Enabled' : '✗ Disabled'}
            </div>
          </div>

          <div>
            <div className="text-text-tertiary">Auto-Save</div>
            <div className="text-text-primary font-semibold">
              {settings.autoSave ? '✓ Enabled' : '✗ Disabled'}
            </div>
          </div>

          <div>
            <div className="text-text-tertiary">Detection Threshold</div>
            <div className="text-text-primary font-semibold">
              {(settings.detectionThreshold * 100).toFixed(0)}%
            </div>
          </div>

          <div>
            <div className="text-text-tertiary">Sound Notifications</div>
            <div className="text-text-primary font-semibold">
              {settings.enableSound ? '✓ Enabled' : '✗ Disabled'}
            </div>
          </div>
        </div>

        <div className="mt-4 p-3 bg-bg-tertiary rounded-lg">
          <div className="text-xs text-text-tertiary">
            <div>Backend: http://localhost:8000</div>
            <div>Frontend: http://localhost:3000</div>
            <div>Last Updated: {new Date().toLocaleString()}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
