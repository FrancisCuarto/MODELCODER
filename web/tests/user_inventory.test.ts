import test from 'node:test';
import assert from 'node:assert';
import {
  saveProjectDraft,
  getProjectDrafts,
  getProjectDraft,
  deleteProjectDraft,
  duplicateProjectDraft,
  saveAutoDraft,
  getAutoDraft,
  clearAutoDraft,
  toggleFavorite,
  isFavorite,
  getFavorites,
  saveCollection,
  getCollections,
  toggleModelInCollection,
  deleteCollection,
  importProjectFromJSON,
} from '../src/lib/user-inventory.ts';
import type { ModelSpec } from '../src/lib/studio/types.ts';

// Mock localStorage for Node.js test runner environment
const mockStorage: Record<string, string> = {};
(global as any).localStorage = {
  getItem: (key: string) => mockStorage[key] || null,
  setItem: (key: string, val: string) => { mockStorage[key] = val; },
  removeItem: (key: string) => { delete mockStorage[key]; },
  clear: () => {
    for (const k in mockStorage) delete mockStorage[k];
  }
};
(global as any).window = {
  dispatchEvent: () => true
};

const dummySpec: ModelSpec = {
  id: 'test.crate',
  name: 'Crate Test Alpha',
  category: 'furniture',
  description: 'Contenedor de prueba',
  units: 'meters',
  dimensions: { width: 1, depth: 1, height: 1 },
  palette: 'industrial_hazard',
  components: [
    {
      name: 'hull',
      shape: 'box',
      size: [1, 1, 1],
      position: [0, 0.5, 0],
      rotation: [0, 0, 0],
      scale: [1, 1, 1],
      color: '#ffffff'
    }
  ]
};

test('User Drafts 1: Guardar un borrador en curso y recuperarlo con su geometría exacta', () => {
  const draft = saveProjectDraft({
    name: 'Crate Test Alpha',
    category: 'furniture',
    description: 'Mi modelo a medias',
    spec: dummySpec,
    tri_count: 120
  });

  assert.ok(draft.id.startsWith('proj_'));
  assert.strictEqual(draft.name, 'Crate Test Alpha');
  assert.strictEqual(draft.components_count, 1);
  assert.strictEqual(draft.tri_count, 120);

  const fetched = getProjectDraft(draft.id);
  assert.ok(fetched);
  assert.strictEqual(fetched?.spec.components[0].name, 'hull');
});

test('User Drafts 2: Actualizar un borrador existente preserva su ID original', () => {
  const drafts = getProjectDrafts();
  const existingId = drafts[0].id;

  const updated = saveProjectDraft({
    id: existingId,
    name: 'Crate Test Alpha v2',
    spec: {
      ...dummySpec,
      name: 'Crate Test Alpha v2',
      components: [
        ...dummySpec.components,
        {
          name: 'lid',
          shape: 'box',
          size: [1, 0.1, 1],
          position: [0, 1.05, 0],
          rotation: [0, 0, 0],
          scale: [1, 1, 1],
          color: '#333333'
        }
      ]
    }
  });

  assert.strictEqual(updated.id, existingId);
  assert.strictEqual(updated.name, 'Crate Test Alpha v2');
  assert.strictEqual(updated.components_count, 2);
});

test('User Drafts 3: Duplicar un borrador genera una copia independiente', () => {
  const drafts = getProjectDrafts();
  const targetId = drafts[0].id;

  const clone = duplicateProjectDraft(targetId);
  assert.ok(clone);
  assert.notStrictEqual(clone?.id, targetId);
  assert.ok(clone?.name.includes('(Copia)'));
  assert.strictEqual(clone?.components_count, 2);
});

test('User Drafts 4: Autoguardado temporal funciona sin sobrescribir la lista de proyectos', () => {
  saveAutoDraft(dummySpec, 'data:image/png;base64,mock');
  const auto = getAutoDraft();
  assert.ok(auto);
  assert.strictEqual(auto?.spec.name, 'Crate Test Alpha');
  assert.strictEqual(auto?.thumbnail, 'data:image/png;base64,mock');

  clearAutoDraft();
  assert.strictEqual(getAutoDraft(), null);
});

test('Favorites System: Alternar favoritos y verificar estado', () => {
  assert.strictEqual(isFavorite('server_rack'), false);
  const isNowFav = toggleFavorite({ id: 'server_rack', name: 'Server Rack', category: 'electronics' });
  assert.strictEqual(isNowFav, true);
  assert.strictEqual(isFavorite('server_rack'), true);

  const list = getFavorites();
  assert.strictEqual(list.length, 1);
  assert.strictEqual(list[0].id, 'server_rack');

  // Toggle again to remove
  const isRemoved = toggleFavorite({ id: 'server_rack', name: 'Server Rack' });
  assert.strictEqual(isRemoved, false);
  assert.strictEqual(isFavorite('server_rack'), false);
});

test('Collections System: Crear colecciones y alternar modelos dentro de ellas', () => {
  const col = saveCollection({
    name: 'Bases Espaciales',
    description: 'Props de ingeniería',
    color: '#00f0ff'
  });

  assert.ok(col.id.startsWith('col_'));
  assert.strictEqual(col.name, 'Bases Espaciales');
  assert.strictEqual(col.model_ids.length, 0);

  const added = toggleModelInCollection(col.id, 'crate');
  assert.strictEqual(added, true);

  const updatedCol = getCollections().find((c) => c.id === col.id);
  assert.ok(updatedCol?.model_ids.includes('crate'));

  // Remove
  const removed = toggleModelInCollection(col.id, 'crate');
  assert.strictEqual(removed, false);
});

test('JSON Import: Importar un archivo JSON externo restaura el modelo en los borradores', () => {
  const jsonStr = JSON.stringify(dummySpec);
  const imported = importProjectFromJSON(jsonStr);

  assert.ok(imported.id);
  assert.strictEqual(imported.name, 'Crate Test Alpha');
  assert.strictEqual(imported.components_count, 1);
});
