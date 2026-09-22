import { AnalyzeResponse } from '../types';
const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL !== undefined && import.meta.env.VITE_API_BASE_URL !== null)
  ? import.meta.env.VITE_API_BASE_URL
  : (import.meta.env.PROD ? '' : 'http://localhost:8000');

export class ApiError extends Error {
  status?: number;

  constructor(message: string, status?: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

export async function analyzeReportsApi(files: File[]): Promise<AnalyzeResponse> {
  const formData = new FormData();
  files.forEach((file) => {
    formData.append('files', file, file.name);
  });

  try {
    const response = await fetch(`${API_BASE_URL}/api/reports/analyze`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      let errorMessage = 'Extraction failed. Please verify your PDF file is a valid blood report.';
      try {
        const errorJson = await response.json();
        if (errorJson && errorJson.detail) {
          errorMessage = typeof errorJson.detail === 'string' 
            ? errorJson.detail 
            : JSON.stringify(errorJson.detail);
        }
      } catch {
        // use default
      }
      throw new ApiError(errorMessage, response.status);
    }

    return await response.json();
  } catch (error: any) {
    if (error instanceof ApiError) {
      throw error;
    }
    // Network or server unreachable
    throw new ApiError(
      'Unable to connect to the backend server. Please verify that the backend service is running.',
      0
    );
  }
}

export async function fetchSampleDataApi(): Promise<AnalyzeResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/reports/sample-data`);
    if (!response.ok) {
      let errorMsg = 'Failed to load sample demonstration data.';
      try {
        const errJson = await response.json();
        if (errJson?.detail) errorMsg = errJson.detail;
      } catch {}
      throw new ApiError(errorMsg, response.status);
    }
    return await response.json();
  } catch (error: any) {
    if (error instanceof ApiError) throw error;
    throw new ApiError('Unable to connect to the backend server to load sample data.', 0);
  }
}

export function getSamplePdfDownloadUrl(filename: string): string {
  return `${API_BASE_URL}/api/reports/download-sample/${encodeURIComponent(filename)}`;
}

export async function fetchSampleFileAsRealFile(filename: string): Promise<File> {
  const url = getSamplePdfDownloadUrl(filename);
  const response = await fetch(url);
  if (!response.ok) {
    throw new ApiError(`Failed to retrieve sample report file: ${filename}`, response.status);
  }
  const blob = await response.blob();
  return new File([blob], filename, { type: 'application/pdf' });
}
