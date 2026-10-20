import test from 'node:test';
import assert from 'node:assert/strict';
import { isTauriDesktop, openInExternalBrowser } from '../src/lib/tauri-bridge.ts';
import { getSessionExportCode, importSessionFromCode } from '../src/lib/supabase.ts';

test('Tauri Bridge: isTauriDesktop returns boolean without error in Node/browser', () => {
  // In Node environment, window is undefined -> false
  assert.equal(isTauriDesktop(), false);
});

test('Tauri Bridge: openInExternalBrowser handles empty URL gracefully', async () => {
  const res = await openInExternalBrowser('');
  assert.equal(res, false);
});

test('Desktop Session Sync: importSessionFromCode rejects invalid payload', async () => {
  await assert.rejects(
    async () => {
      await importSessionFromCode('invalid_code_xyz_123');
    },
    {
      message: /Código de sesión inválido/
    }
  );
});

test('Desktop Session Sync: importSessionFromCode validates required fields', async () => {
  const badPayload = btoa(JSON.stringify({ some: 'other' }));
  await assert.rejects(
    async () => {
      await importSessionFromCode(badPayload);
    },
    {
      message: /Formato de sesión no reconocido/
    }
  );
});
