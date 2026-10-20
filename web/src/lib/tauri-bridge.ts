/**
 * ModelCoder Desktop (Tauri) Integration Bridge
 * Handles native OS interoperability, opening external links in system browser,
 * and seamless authentication sync between Web and Desktop.
 */

export function isTauriDesktop(): boolean {
  if (typeof window === 'undefined') return false;
  return (
    '__TAURI_INTERNALS__' in window ||
    '__TAURI__' in window ||
    window.location.hostname === 'tauri.localhost' ||
    window.location.protocol === 'tauri:'
  );
}

export function getTauriInvoke(): ((cmd: string, args?: any) => Promise<any>) | null {
  if (typeof window === 'undefined') return null;
  return (
    (window as any).__TAURI_INTERNALS__?.invoke ||
    (window as any).__TAURI__?.core?.invoke ||
    null
  );
}

/**
 * Opens any URL or external link in the user's default system browser (Chrome/Edge/Firefox)
 * when running inside Tauri, with graceful fallback for standard web browsers.
 */
export async function openInExternalBrowser(url: string): Promise<boolean> {
  if (!url) return false;
  const invoke = getTauriInvoke();
  if (invoke) {
    try {
      await invoke('open_external_url', { url });
      return true;
    } catch (err) {
      console.warn('[ModelCoder Desktop] invoke open_external_url failed:', err);
    }
  }

  // Fallback for regular web or if invoke is unavailable
  try {
    const win = window.open(url, '_blank', 'noopener,noreferrer');
    return !!win;
  } catch {
    window.location.href = url;
    return true;
  }
}

/**
 * Initializes global click interceptor for desktop app:
 * Any <a target="_blank"> or external http/https link is routed to OS default browser.
 */
export function initDesktopLinkInterceptor(): void {
  if (typeof window === 'undefined') return;

  // Intercept all clicks globally on document (capture phase)
  document.addEventListener(
    'click',
    (event: MouseEvent) => {
      if (!isTauriDesktop()) return;

      const anchor = (event.target as HTMLElement)?.closest('a');
      if (!anchor) return;

      const href = anchor.getAttribute('href');
      if (!href || href.startsWith('#') || href.startsWith('javascript:')) return;

      const target = anchor.getAttribute('target');
      const isHttp = href.startsWith('http://') || href.startsWith('https://');

      // Check if it's an external link or target="_blank"
      // Note: do not intercept local internal studio routes unless target is _blank
      if (target === '_blank' || (isHttp && !href.includes('tauri.localhost'))) {
        event.preventDefault();
        event.stopPropagation();
        openInExternalBrowser(href);
      }
    },
    true
  );

  // Intercept window.open calls
  if (isTauriDesktop()) {
    const originalWindowOpen = window.open;
    window.open = function (url?: string | URL, target?: string, features?: string): Window | null {
      if (url) {
        const urlStr = String(url);
        if (urlStr.startsWith('http://') || urlStr.startsWith('https://')) {
          openInExternalBrowser(urlStr);
          return null;
        }
      }
      return originalWindowOpen ? originalWindowOpen.call(window, url, target, features) : null;
    };
  }
}
