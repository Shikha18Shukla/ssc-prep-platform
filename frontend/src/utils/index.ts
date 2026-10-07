/**
 * Shared utility functions.
 */

/**
 * Format seconds into a MM:SS display string.
 */
export function formatTime(totalSeconds: number): string {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
}

/**
 * Calculate total test duration in seconds.
 * Each question is allocated 36 seconds.
 */
export function calculateTestDuration(questionCount: number): number {
  return questionCount * 36;
}

/**
 * Concatenate CSS class names, filtering out falsy values.
 */
export function cn(...classes: (string | boolean | undefined | null)[]): string {
  return classes.filter(Boolean).join(" ");
}
