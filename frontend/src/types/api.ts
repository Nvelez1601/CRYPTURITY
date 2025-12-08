export interface ApiSuccess<T> {
  status: 'success';
  message: string;
  data: T;
}

export interface ApiError {
  status: 'error';
  message: string;
  errors?: unknown;
}
