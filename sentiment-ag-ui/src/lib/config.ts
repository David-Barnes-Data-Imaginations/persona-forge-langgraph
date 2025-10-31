/**
 * Centralized configuration for the SentimentSuite frontend
 */

export const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8001";

/**
 * Helper to construct backend API URLs
 */
export const getBackendUrl = (path: string): string => {
  // Ensure path starts with /
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${BACKEND_URL}${normalizedPath}`;
};
