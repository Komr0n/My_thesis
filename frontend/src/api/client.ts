import axios from 'axios';

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const apiClient = axios.create({
  baseURL,
  timeout: 15000
});

export interface PipelineRequestOptions {
  imageBase64: string;
  recognize?: boolean;
  emotions?: boolean;
  topK?: number;
  threshold?: number;
}

export interface PipelineFace {
  bbox: number[];
  score: number;
  identity?: { person: string; similarity: number } | null;
  emotion?: { label: string; probabilities: Record<string, number> } | null;
  landmarks: Record<string, number[]>;
}

export interface PipelineResponse {
  faces: PipelineFace[];
  timing_ms: Record<string, number>;
}

export interface PersonsResponse {
  results: { id: number; name: string; notes?: string; embedding_count: number }[];
  total: number;
}

export async function runPipeline(options: PipelineRequestOptions) {
  const payload = {
    image_base64: options.imageBase64,
    recognize: options.recognize ?? true,
    emotions: options.emotions ?? true,
    top_k: options.topK,
    threshold: options.threshold
  };
  const response = await apiClient.post<PipelineResponse>('/pipeline', payload);
  return response.data;
}

export async function uploadPipeline(formData: FormData) {
  const response = await apiClient.post<PipelineResponse>('/pipeline', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
}

export async function enrollPerson(name: string, images: string[], notes?: string) {
  const response = await apiClient.post('/enroll', { name, images, notes });
  return response.data;
}

export async function fetchPersons() {
  const response = await apiClient.get<PersonsResponse>('/persons');
  return response.data;
}
