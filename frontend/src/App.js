import React from 'react';
import FileUpload from './components/FileUpload';
import Results from './components/Results';
import './styles.css';
function App() {
  return (
    <div className="container py-5">
      <h1 className="text-center mb-5">Invoice Data Extractor</h1>
      <div className="card shadow">
        <div className="card-body">
          <FileUpload />
        </div>
      </div>
    </div>
  );
}

export default App;