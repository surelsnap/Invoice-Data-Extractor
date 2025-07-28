import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import Results from './Results';

const FileUpload = () => {
  const [downloadLink, setDownloadLink] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png'],
      'application/pdf': ['.pdf']
    },
    maxFiles: 1,
    multiple: false,
    disabled: isLoading,
    onDrop: files => handleFileUpload(files[0])
  });

  const handleFileUpload = async file => {
    setIsLoading(true);
    setError('');
    setDownloadLink('');
    setUploadProgress(0);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(
        process.env.REACT_APP_API_URL + '/upload',
        formData,
        { 
          responseType: 'blob',
          onUploadProgress: progressEvent => {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setUploadProgress(percentCompleted);
          },
          timeout: 30000 // 30 seconds timeout
        }
      );

      const url = window.URL.createObjectURL(new Blob([response.data]));
      setDownloadLink(url);
    } catch (err) {
      let errorMessage = 'Failed to process invoice';
      
      if (err.response) {
        // Handle blob error responses
        if (err.response.data instanceof Blob) {
          const errorData = await new Response(err.response.data).json();
          errorMessage = errorData.detail || errorMessage;
        } else {
          errorMessage = err.response.data?.message || errorMessage;
        }
      } else if (err.request) {
        errorMessage = 'No response from server';
      } else if (err.code === 'ECONNABORTED') {
        errorMessage = 'Request timed out';
      }

      setError(errorMessage);
      
      // Revoke any existing URL
      if (downloadLink) {
        window.URL.revokeObjectURL(downloadLink);
        setDownloadLink('');
      }
    } finally {
      setIsLoading(false);
      setUploadProgress(0);
    }
  };

  return (
    <div className="file-upload-container">
      <div
        {...getRootProps()}
        className={`dropzone ${isLoading ? 'loading' : ''}`}
      >
        <input {...getInputProps()} />
        {isLoading ? (
          <div className="upload-progress">
            <div className="progress-bar" style={{ width: `${uploadProgress}%` }}></div>
            <span>Processing: {uploadProgress}%</span>
          </div>
        ) : (
          <p className="upload-prompt">
            Drag & drop invoice file, or click to select
            <br />
            <small>(Supports PDF, JPG, PNG)</small>
          </p>
        )}
      </div>

      <Results downloadLink={downloadLink} error={error} />
    </div>
  );
};

export default FileUpload;