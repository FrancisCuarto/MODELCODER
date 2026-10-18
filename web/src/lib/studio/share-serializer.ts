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

/**
 * Compresses a ModelSpec using native Deflate and encodes to URL-safe Base64 with a 'z:' prefix.
 * Achieves 70-85% size reduction compared to uncompressed JSON.
 */
export async function compressSpecToHash(spec: ModelSpec): Promise<string> {
  try {
    const jsonStr = JSON.stringify(spec);
    const rawBytes = new TextEncoder().encode(jsonStr);

    if (typeof CompressionStream !== 'undefined') {
      const stream = new Response(new Blob([rawBytes]).stream().pipeThrough(new CompressionStream('deflate-raw')));
      const compressedBuffer = await stream.arrayBuffer();
      const compressedBytes = new Uint8Array(compressedBuffer);
      let binary = '';
      for (let i = 0; i < compressedBytes.length; i++) {
        binary += String.fromCharCode(compressedBytes[i]);
      }
      const b64 = (typeof btoa !== 'undefined' ? btoa(binary) : Buffer.from(binary, 'binary').toString('base64'))
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');
      return 'z:' + b64;
    }
  } catch (err) {
    console.warn('[ModelCoder] Deflate compression failed, falling back to raw hash:', err);
  }
  return serializeSpecToHash(spec);
}

/**
 * Asynchronously deserializes a ModelSpec from a hash token.
 * Automatically handles both compressed ('z:...') and legacy uncompressed tokens.
 */
export async function deserializeSpec(token: string): Promise<ModelSpec | null> {
  if (!token || typeof token !== 'string') return null;

  let cleanToken = token.trim();
  if (cleanToken.startsWith('#')) cleanToken = cleanToken.slice(1);
  if (cleanToken.startsWith('model=')) cleanToken = cleanToken.slice(6);

  if (cleanToken.startsWith('z:')) {
    try {
      const b64 = cleanToken.slice(2).replace(/-/g, '+').replace(/_/g, '/');
      const padLen = (4 - (b64.length % 4)) % 4;
      const padded = b64 + '='.repeat(padLen);

      let binary = '';
      if (typeof atob !== 'undefined') {
        binary = atob(padded);
      } else if (typeof Buffer !== 'undefined') {
        binary = Buffer.from(padded, 'base64').toString('binary');
      }

      const compressedBytes = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i++) {
        compressedBytes[i] = binary.charCodeAt(i);
      }

      if (typeof DecompressionStream !== 'undefined') {
        const stream = new Response(new Blob([compressedBytes]).stream().pipeThrough(new DecompressionStream('deflate-raw')));
        const decompressedBuffer = await stream.arrayBuffer();
        const jsonStr = new TextDecoder().decode(decompressedBuffer);
        const parsed = JSON.parse(jsonStr);
        if (parsed && typeof parsed === 'object' && Array.isArray(parsed.components)) {
          return parsed as ModelSpec;
        }
      }
    } catch (err) {
      console.warn('[ModelCoder] Failed to decompress z: token:', err);
    }
  }

  return deserializeSpecFromHash(token);
}

