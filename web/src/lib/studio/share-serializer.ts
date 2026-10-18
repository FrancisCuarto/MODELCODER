import type { ModelSpec } from './types.ts';

/**
 * Serializes a ModelSpec to a URL-safe Base64 string that can be placed in window.location.hash.
 * Does not require external libraries and operates safely in all modern browsers and Node environments.
 */
export function serializeSpecToHash(spec: ModelSpec): string {
  try {
    const jsonStr = JSON.stringify(spec);
    if (typeof Buffer !== 'undefined') {
      return Buffer.from(jsonStr, 'utf-8')
        .toString('base64')
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');
    }
    const bytes = new TextEncoder().encode(jsonStr);
    let binary = '';
    for (let i = 0; i < bytes.length; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary)
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');
  } catch (err) {
    console.error('[ModelCoder] Failed to serialize spec to URL hash:', err);
    return '';
  }
}

/**
 * Deserializes and validates a ModelSpec from a URL-safe Base64 hash token.
 * Returns null if the token is invalid or corrupt.
 */
export function deserializeSpecFromHash(token: string): ModelSpec | null {
  if (!token || typeof token !== 'string') return null;

  try {
    // Strip optional leading # or model= prefixes
    let cleanToken = token.trim();
    if (cleanToken.startsWith('#')) cleanToken = cleanToken.slice(1);
    if (cleanToken.startsWith('model=')) cleanToken = cleanToken.slice(6);

    let base64 = cleanToken.replace(/-/g, '+').replace(/_/g, '/');
    while (base64.length % 4 !== 0) {
      base64 += '=';
    }

    let jsonStr = '';
    if (typeof Buffer !== 'undefined') {
      jsonStr = Buffer.from(base64, 'base64').toString('utf-8');
    } else {
      const binary = atob(base64);
      const bytes = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i++) {
        bytes[i] = binary.charCodeAt(i);
      }
      jsonStr = new TextDecoder().decode(bytes);
    }

    const parsed = JSON.parse(jsonStr);
    if (parsed && typeof parsed === 'object' && Array.isArray(parsed.components)) {
      return parsed as ModelSpec;
    }
  } catch (err) {
    console.warn('[ModelCoder] Invalid or corrupted model share token:', err);
  }
  return null;
}
