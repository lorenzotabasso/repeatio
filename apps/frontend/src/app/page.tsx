'use client';

import { useState, useEffect } from 'react';

interface ProcessingStatus {
  status: 'idle' | 'uploading' | 'processing' | 'completed' | 'error';
  message: string;
  progress?: number;
}

interface AudioFile {
  filename: string;
  size: number;
  created: number;
}

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [firstLanguage, setFirstLanguage] = useState('');
  const [secondLanguage, setSecondLanguage] = useState('');
  const [processingStatus, setProcessingStatus] = useState<ProcessingStatus>({
    status: 'idle',
    message: 'Ready to process CSV file'
  });
  const [generatedFiles, setGeneratedFiles] = useState<AudioFile[]>([]);

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'es', name: 'Spanish' },
    { code: 'fr', name: 'French' },
    { code: 'de', name: 'German' },
    { code: 'it', name: 'Italian' },
    { code: 'pt', name: 'Portuguese' },
    { code: 'ru', name: 'Russian' },
    { code: 'ja', name: 'Japanese' },
    { code: 'ko', name: 'Korean' },
    { code: 'zh', name: 'Chinese' }
  ];

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'text/csv') {
      setSelectedFile(file);
      setProcessingStatus({
        status: 'idle',
        message: `File selected: ${file.name}`
      });
    } else {
      setProcessingStatus({
        status: 'error',
        message: 'Please select a valid CSV file'
      });
    }
  };

  const fetchGeneratedFiles = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/audio/files`);
      if (response.ok) {
        const data = await response.json();
        setGeneratedFiles(data.files || []);
      }
    } catch (error) {
      console.error('Error fetching files:', error);
    }
  };

  const handleStartProcessing = async () => {
    if (!selectedFile) {
      setProcessingStatus({
        status: 'error',
        message: 'Please select a CSV file first'
      });
      return;
    }

    if (!firstLanguage || !secondLanguage) {
      setProcessingStatus({
        status: 'error',
        message: 'Please select both languages'
      });
      return;
    }

    if (firstLanguage === secondLanguage) {
      setProcessingStatus({
        status: 'error',
        message: 'Please select different languages'
      });
      return;
    }

    // Start processing
    setProcessingStatus({
      status: 'uploading',
      message: 'Uploading file...',
      progress: 0
    });

    try {
      const formData = new FormData();
      formData.append('csv_file', selectedFile);
      
      // Add request as a JSON string
      const requestData = {
        languages: [
          { column_index: 0, language_code: firstLanguage, flag: '🇮🇹' },
          { column_index: 1, language_code: secondLanguage, flag: '🇷🇺' }
        ],
        output_filename: `output_${Date.now()}.mp3`,
        pause_duration: 5000,
        silence_duration: 1000
      };
      
      formData.append('request', JSON.stringify(requestData));

      setProcessingStatus({
        status: 'processing',
        message: 'Processing CSV and generating audio...',
        progress: 25
      });

      const response = await fetch(`${API_BASE_URL}/api/v1/audio/csv-to-audio`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();

      if (result.success) {
        setProcessingStatus({
          status: 'completed',
          message: 'Audio generation completed successfully!',
          progress: 100
        });
        
        // Refresh the list of generated files
        await fetchGeneratedFiles();
      } else {
        throw new Error(result.error || 'Unknown error occurred');
      }

    } catch (error) {
      console.error('Processing error:', error);
      setProcessingStatus({
        status: 'error',
        message: `Error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`
      });
    }
  };

  const handleDownloadFile = (filename: string) => {
    window.open(`${API_BASE_URL}/api/v1/audio/download/${filename}`, '_blank');
  };

  const handleDeleteFile = async (filename: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/audio/files/${filename}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        await fetchGeneratedFiles();
      }
    } catch (error) {
      console.error('Error deleting file:', error);
    }
  };

  // Load generated files on component mount
  useEffect(() => {
    fetchGeneratedFiles();
  }, []);

  const getStatusColor = (status: ProcessingStatus['status']) => {
    switch (status) {
      case 'idle': return 'text-gray-600';
      case 'uploading': return 'text-blue-600';
      case 'processing': return 'text-yellow-600';
      case 'completed': return 'text-green-600';
      case 'error': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getStatusIcon = (status: ProcessingStatus['status']) => {
    switch (status) {
      case 'idle': return '📁';
      case 'uploading': return '📤';
      case 'processing': return '⚙️';
      case 'completed': return '✅';
      case 'error': return '❌';
      default: return '📁';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">
            CSV Audio Generator
          </h1>
          
          {/* File Upload Section */}
          <div className="mb-8">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select CSV File
            </label>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors">
              <input
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="cursor-pointer">
                <div className="text-gray-600">
                  {selectedFile ? (
                    <div>
                      <p className="text-green-600 font-medium">✓ {selectedFile.name}</p>
                      <p className="text-sm text-gray-500 mt-1">
                        Size: {(selectedFile.size / 1024).toFixed(1)} KB
                      </p>
                    </div>
                  ) : (
                    <div>
                      <p className="text-lg">📁 Click to select CSV file</p>
                      <p className="text-sm text-gray-500 mt-1">
                        or drag and drop here
                      </p>
                    </div>
                  )}
                </div>
              </label>
            </div>
          </div>

          {/* Language Selection */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                First Language
              </label>
              <select
                value={firstLanguage}
                onChange={(e) => setFirstLanguage(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select language</option>
                {languages.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Second Language
              </label>
              <select
                value={secondLanguage}
                onChange={(e) => setSecondLanguage(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select language</option>
                {languages.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Process Button */}
          <div className="mb-8">
            <button
              onClick={handleStartProcessing}
              disabled={processingStatus.status === 'uploading' || processingStatus.status === 'processing'}
              className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {processingStatus.status === 'uploading' || processingStatus.status === 'processing' 
                ? 'Processing...' 
                : 'Start Audio Generation'
              }
            </button>
          </div>

          {/* Status Display */}
          <div className="bg-gray-50 rounded-lg p-4 mb-8">
            <div className="flex items-center mb-2">
              <span className="text-2xl mr-3">{getStatusIcon(processingStatus.status)}</span>
              <span className={`font-medium ${getStatusColor(processingStatus.status)}`}>
                {processingStatus.message}
              </span>
            </div>
            
            {processingStatus.progress !== undefined && (
              <div className="mt-3">
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${processingStatus.progress}%` }}
                  ></div>
                </div>
                <p className="text-sm text-gray-600 mt-1">
                  Progress: {processingStatus.progress}%
                </p>
              </div>
            )}
          </div>

          {/* Generated Files Section */}
          <div className="border-t pt-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Generated Audio Files</h2>
            {generatedFiles.length === 0 ? (
              <p className="text-gray-500 text-center py-4">No audio files generated yet</p>
            ) : (
              <div className="space-y-3">
                {generatedFiles.map((file) => (
                  <div key={file.filename} className="flex items-center justify-between bg-gray-50 p-4 rounded-lg">
                    <div className="flex items-center">
                      <span className="text-2xl mr-3">🎵</span>
                      <div>
                        <p className="font-medium text-gray-800">{file.filename}</p>
                        <p className="text-sm text-gray-500">
                          Size: {(file.size / 1024).toFixed(1)} KB | 
                          Created: {new Date(file.created * 1000).toLocaleString()}
                        </p>
                      </div>
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleDownloadFile(file.filename)}
                        className="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700 transition-colors"
                      >
                        Download
                      </button>
                      <button
                        onClick={() => handleDeleteFile(file.filename)}
                        className="px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700 transition-colors"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
