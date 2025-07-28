import React from 'react';
import PropTypes from 'prop-types';

const Results = ({ downloadLink, error }) => {
  if (error) {
    return (
      <div className="alert alert-danger mt-4">
        <strong>Error:</strong> {error}
      </div>
    );
  }

  if (downloadLink) {
    return (
      <div className="mt-4 text-center">
        <a
          href={downloadLink}
          download="invoice_data.xlsx"
          className="btn btn-success btn-lg"
        >
          Download Excel File
        </a>
        <p className="mt-2 text-muted">
          File will be automatically downloaded
        </p>
      </div>
    );
  }

  return null;
};

Results.propTypes = {
  downloadLink: PropTypes.string,
  error: PropTypes.string
};

export default Results;