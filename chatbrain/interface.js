import React, { useState, useCallback } from 'react';
import { Upload, Settings, ChevronRight, Plus } from 'lucide-react';

const ChatAnalyzer = () => {
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [analysisPhase, setAnalysisPhase] = useState('upload'); // upload, configure, analyzing, results
  const [users, setUsers] = useState({ user1: '', user2: '' });
  const [analysisResults, setAnalysisResults] = useState(null);

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setAnalysisPhase('configure');
    }
  }, []);

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setAnalysisPhase('configure');
    }
  };

  const startAnalysis = async () => {
    if (!file || !users.user1 || !users.user2) return;
    
    setAnalysisPhase('analyzing');
    // Simulation of analysis time
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Mock results - replace with actual API call
    setAnalysisResults({
      // ... analysis results structure
    });
    setAnalysisPhase('results');
  };

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 h-16 border-b border-gray-800 bg-black/95 backdrop-blur-sm z-50">
        <div className="max-w-screen-xl mx-auto h-full px-6 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <span className="text-xl font-medium">Chat Analysis</span>
            {analysisPhase !== 'upload' && (
              <span className="text-gray-500">|</span>
            )}
            {file && (
              <span className="text-gray-400 text-sm">{file.name}</span>
            )}
          </div>
          <button className="p-2 hover:bg-gray-900 rounded-full transition-colors">
            <Settings className="w-5 h-5 text-gray-400" />
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-24 pb-16 px-6">
        <div className="max-w-screen-xl mx-auto">
          {analysisPhase === 'upload' && (
            <div
              className={`relative border-2 border-dashed rounded-lg p-12 text-center transition-colors
                ${dragActive ? 'border-blue-500 bg-blue-500/5' : 'border-gray-700 hover:border-gray-600'}
              `}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <input
                type="file"
                className="hidden"
                onChange={handleFileSelect}
                accept=".txt"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="flex flex-col items-center cursor-pointer"
              >
                <Upload className="w-12 h-12 mb-4 text-gray-500" />
                <span className="text-xl mb-2">Drop your chat file here</span>
                <span className="text-gray-500">or click to browse</span>
              </label>
            </div>
          )}

          {analysisPhase === 'configure' && (
            <div className="space-y-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <label className="block text-sm text-gray-400">First Participant</label>
                  <input
                    type="text"
                    className="w-full bg-gray-900 border border-gray-800 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500 transition-colors"
                    placeholder="Enter name"
                    value={users.user1}
                    onChange={(e) => setUsers(prev => ({ ...prev, user1: e.target.value }))}
                  />
                </div>
                <div className="space-y-4">
                  <label className="block text-sm text-gray-400">Second Participant</label>
                  <input
                    type="text"
                    className="w-full bg-gray-900 border border-gray-800 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500 transition-colors"
                    placeholder="Enter name"
                    value={users.user2}
                    onChange={(e) => setUsers(prev => ({ ...prev, user2: e.target.value }))}
                  />
                </div>
              </div>

              <button
                className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-6 py-3 transition-colors"
                onClick={startAnalysis}
              >
                Begin Analysis
              </button>
            </div>
          )}

          {analysisPhase === 'analyzing' && (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mb-4"></div>
              <p className="text-gray-400">Analyzing conversation patterns...</p>
            </div>
          )}

          {analysisPhase === 'results' && (
            <div className="space-y-8">
              {/* Results Sections */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
                  <h3 className="text-lg font-medium mb-4">Conversation Overview</h3>
                  {/* Overview metrics */}
                </div>
                <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
                  <h3 className="text-lg font-medium mb-4">Emotional Analysis</h3>
                  {/* Emotional metrics */}
                </div>
                <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
                  <h3 className="text-lg font-medium mb-4">Interaction Patterns</h3>
                  {/* Pattern metrics */}
                </div>
              </div>

              {/* Detailed Analysis */}
              <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
                <h3 className="text-lg font-medium mb-6">Key Insights</h3>
                <div className="space-y-4">
                  {/* Map through insights */}
                  {[1,2,3].map((_, i) => (
                    <div key={i} className="flex items-start space-x-3 text-gray-300">
                      <ChevronRight className="w-5 h-5 mt-0.5 text-blue-500" />
                      <p>Insight {i + 1}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="fixed bottom-0 left-0 right-0 h-16 border-t border-gray-800 bg-black/95 backdrop-blur-sm">
        <div className="max-w-screen-xl mx-auto h-full px-6 flex items-center justify-between">
          <span className="text-gray-500 text-sm">Powered by Advanced Analytics</span>
          {analysisPhase === 'results' && (
            <button 
              className="flex items-center space-x-2 px-4 py-2 bg-gray-900 rounded-lg hover:bg-gray-800 transition-colors"
              onClick={() => setAnalysisPhase('upload')}
            >
              <Plus className="w-4 h-4" />
              <span>New Analysis</span>
            </button>
          )}
        </div>
      </footer>
    </div>
  );
};

export default ChatAnalyzer;