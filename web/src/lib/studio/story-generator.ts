/**
 * MODELCODER — Instagram Story (9:16) Graphic Generator & Social Exporter
 * Generates high-impact 1080x1920 Instagram Story cards for user-created 3D models,
 * featuring brand watermarks, technical specifications, and customizable themes.
 */

export type StoryTheme =
  | 'cyber_dark'
  | 'carbon_minimal'
  | 'neon_synth'
  | 'gold_luxury'
  | 'transparent_sticker';

export interface StoryThemeDefinition {
  id: StoryTheme;
  label: string;
  badge: string;
  bgGradient?: [string, string, string];
  glowColor: string;
  glowRadius: number;
  gridColor: string;
  primaryColor: string;
  secondaryColor: string;
  cardBg: string;
  cardBorder: string;
  textColor: string;
  textDimColor: string;
  isTransparent?: boolean;
}

export const STORY_THEMES: Record<StoryTheme, StoryThemeDefinition> = {
  cyber_dark: {
    id: 'cyber_dark',
    label: 'Cyber Dark',
    badge: '🌌 CYBERPUNK',
    bgGradient: ['#06080e', '#0d131f', '#121927'],
    glowColor: 'rgba(0, 240, 255, 0.16)',
    glowRadius: 580,
    gridColor: 'rgba(0, 240, 255, 0.05)',
    primaryColor: '#00f0ff',
    secondaryColor: '#ffb800',
    cardBg: 'rgba(11, 16, 26, 0.84)',
    cardBorder: 'rgba(0, 240, 255, 0.32)',
    textColor: '#ffffff',
    textDimColor: '#94a3b8'
  },
  carbon_minimal: {
    id: 'carbon_minimal',
    label: 'Carbon Minimal',
    badge: '🖤 TITANIUM',
    bgGradient: ['#090a0d', '#13151c', '#0f1015'],
    glowColor: 'rgba(255, 255, 255, 0.09)',
    glowRadius: 500,
    gridColor: 'rgba(255, 255, 255, 0.035)',
    primaryColor: '#f8fafc',
    secondaryColor: '#94a3b8',
    cardBg: 'rgba(18, 21, 28, 0.86)',
    cardBorder: 'rgba(255, 255, 255, 0.18)',
    textColor: '#ffffff',
    textDimColor: '#a1a1aa'
  },
  neon_synth: {
    id: 'neon_synth',
    label: 'Neon Synth',
    badge: '💜 SYNTHWAVE',
    bgGradient: ['#0a0414', '#1e0836', '#120624'],
    glowColor: 'rgba(236, 72, 153, 0.22)',
    glowRadius: 620,
    gridColor: 'rgba(217, 70, 239, 0.06)',
    primaryColor: '#f43f5e',
    secondaryColor: '#a855f7',
    cardBg: 'rgba(20, 10, 35, 0.85)',
    cardBorder: 'rgba(236, 72, 153, 0.36)',
    textColor: '#ffffff',
    textDimColor: '#cbd5e1'
  },
  gold_luxury: {
    id: 'gold_luxury',
    label: 'Gold Sci-Fi',
    badge: '✨ AMBER GOLD',
    bgGradient: ['#0a0805', '#1a140c', '#100c07'],
    glowColor: 'rgba(245, 158, 11, 0.19)',
    glowRadius: 580,
    gridColor: 'rgba(245, 158, 11, 0.05)',
    primaryColor: '#fbbf24',
    secondaryColor: '#f59e0b',
    cardBg: 'rgba(24, 18, 10, 0.86)',
    cardBorder: 'rgba(245, 158, 11, 0.38)',
    textColor: '#ffffff',
    textDimColor: '#d6d3d1'
  },
  transparent_sticker: {
    id: 'transparent_sticker',
    label: 'Sticker Transparente',
    badge: '🏁 STICKER',
    isTransparent: true,
    glowColor: 'rgba(0, 240, 255, 0.08)',
    glowRadius: 400,
    gridColor: 'transparent',
    primaryColor: '#00f0ff',
    secondaryColor: '#ffb800',
    cardBg: 'rgba(11, 16, 26, 0.88)',
    cardBorder: 'rgba(0, 240, 255, 0.45)',
    textColor: '#ffffff',
    textDimColor: '#94a3b8'
  }
};

export interface StoryModelStats {
  triangles: number | string;
  vertices: number | string;
  componentCount: number | string;
  materialsSummary?: string;
  generationId?: string;
}

export interface StoryOptions {
  title: string;
  description: string;
  author?: string;
  theme: StoryTheme;
  showWatermark?: boolean;
  showDescription?: boolean;
  showStats?: boolean;
  showTechFrame?: boolean;
  stats: StoryModelStats;
}

/**
 * Standard Instagram Stories dimensions
 */
export const STORY_CANVAS_WIDTH = 1080;
export const STORY_CANVAS_HEIGHT = 1920;

/**
 * Draws rounded rectangle path on a 2D canvas context.
 */
export function drawRoundRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  width: number,
  height: number,
  radius: number
): void {
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.lineTo(x + width - radius, y);
  ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
  ctx.lineTo(x + width, y + height - radius);
  ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
  ctx.lineTo(x + radius, y + height);
  ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
  ctx.lineTo(x, y + radius);
  ctx.quadraticCurveTo(x, y, x + radius, y);
  ctx.closePath();
}

/**
 * Wraps text into lines and renders it. Returns number of lines rendered.
 */
export function wrapAndDrawText(
  ctx: CanvasRenderingContext2D,
  text: string,
  x: number,
  y: number,
  maxWidth: number,
  lineHeight: number,
  maxLines: number = 3
): number {
  if (!text || text.trim() === '') return 0;
  const words = text.split(/\s+/);
  let line = '';
  let linesRendered = 0;
  let currentY = y;

  for (let n = 0; n < words.length; n++) {
    const testLine = line + words[n] + ' ';
    const metrics = ctx.measureText(testLine);
    const testWidth = metrics.width;

    if (testWidth > maxWidth && n > 0) {
      if (linesRendered === maxLines - 1) {
        // Last line: append ellipsis
        ctx.fillText(line.trim() + '...', x, currentY);
        linesRendered++;
        return linesRendered;
      }
      ctx.fillText(line.trim(), x, currentY);
      linesRendered++;
      line = words[n] + ' ';
      currentY += lineHeight;
    } else {
      line = testLine;
    }
  }

  if (line.trim() && linesRendered < maxLines) {
    ctx.fillText(line.trim(), x, currentY);
    linesRendered++;
  }

  return linesRendered;
}

/**
 * Draws the high-impact Instagram Story card onto the target canvas (1080x1920).
 */
export function drawStoryCard(
  modelCanvas: HTMLCanvasElement | null,
  options: StoryOptions,
  targetCanvas?: HTMLCanvasElement
): HTMLCanvasElement {
  const canvas = targetCanvas || document.createElement('canvas');
  canvas.width = STORY_CANVAS_WIDTH;
  canvas.height = STORY_CANVAS_HEIGHT;

  const ctx = canvas.getContext('2d');
  if (!ctx) return canvas;

  const theme = STORY_THEMES[options.theme] || STORY_THEMES.cyber_dark;
  const showWatermark = options.showWatermark !== false;
  const showDescription = options.showDescription !== false;
  const showStats = options.showStats !== false;
  const showTechFrame = options.showTechFrame !== false;

  // 1. BACKGROUND
  if (theme.isTransparent) {
    ctx.clearRect(0, 0, STORY_CANVAS_WIDTH, STORY_CANVAS_HEIGHT);
  } else if (theme.bgGradient) {
    const bgGrad = ctx.createLinearGradient(0, 0, 0, STORY_CANVAS_HEIGHT);
    bgGrad.addColorStop(0, theme.bgGradient[0]);
    bgGrad.addColorStop(0.5, theme.bgGradient[1]);
    bgGrad.addColorStop(1, theme.bgGradient[2]);
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, STORY_CANVAS_WIDTH, STORY_CANVAS_HEIGHT);

    // Subtle background grid
    ctx.strokeStyle = theme.gridColor;
    ctx.lineWidth = 1;
    const gridSize = 64;
    for (let x = 0; x <= STORY_CANVAS_WIDTH; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, STORY_CANVAS_HEIGHT);
      ctx.stroke();
    }
    for (let y = 0; y <= STORY_CANVAS_HEIGHT; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(STORY_CANVAS_WIDTH, y);
      ctx.stroke();
    }
  }

  // 2. RADIAL AMBIENT GLOW BEHIND 3D MODEL
  const glowX = STORY_CANVAS_WIDTH / 2;
  const glowY = 800;
  const radGlow = ctx.createRadialGradient(glowX, glowY, 40, glowX, glowY, theme.glowRadius);
  radGlow.addColorStop(0, theme.glowColor);
  radGlow.addColorStop(0.5, theme.glowColor.replace(/[\d\.]+\)$/, '0.06)'));
  radGlow.addColorStop(1, 'rgba(0, 0, 0, 0)');
  ctx.fillStyle = radGlow;
  ctx.fillRect(0, glowY - theme.glowRadius, STORY_CANVAS_WIDTH, theme.glowRadius * 2);

  // 3. TOP BRAND HEADER & WATERMARK (Safe for Instagram UI)
  if (showWatermark) {
    const headerY = 160;

    // Small category badge
    ctx.font = '700 20px "Courier New", monospace, sans-serif';
    ctx.fillStyle = theme.primaryColor;
    ctx.letterSpacing = '3px';
    ctx.fillText('// 3D MODEL CATALOG // WEB GENERATOR', 70, headerY);

    // Main Brand Title
    ctx.font = '900 62px system-ui, -apple-system, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.letterSpacing = '1px';
    ctx.fillText('MODELCODER', 70, headerY + 68);

    // Pill Tag beside brand
    const brandTextWidth = ctx.measureText('MODELCODER').width;
    const pillX = 70 + brandTextWidth + 24;
    const pillY = headerY + 18;
    drawRoundRect(ctx, pillX, pillY, 150, 42, 8);
    ctx.fillStyle = 'rgba(0, 240, 255, 0.12)';
    ctx.fill();
    ctx.strokeStyle = theme.primaryColor;
    ctx.lineWidth = 1.5;
    ctx.stroke();

    ctx.font = '800 18px "Courier New", monospace, sans-serif';
    ctx.fillStyle = theme.primaryColor;
    ctx.letterSpacing = '2px';
    ctx.fillText('3D STUDIO', pillX + 16, pillY + 27);

    // Brand Watermark URL Stamp
    const stampX = STORY_CANVAS_WIDTH - 70;
    ctx.textAlign = 'right';
    ctx.font = '800 22px "Courier New", monospace, sans-serif';
    ctx.fillStyle = theme.primaryColor;
    ctx.letterSpacing = '2px';
    ctx.fillText('modelcoder.vercel.app', stampX, headerY + 48);

    ctx.font = '600 16px system-ui, sans-serif';
    ctx.fillStyle = theme.textDimColor;
    ctx.letterSpacing = '1px';
    ctx.fillText('VERIFIED PROCEDURAL ASSET', stampX, headerY + 76);
    ctx.textAlign = 'left';

    // Header divider line
    ctx.strokeStyle = theme.cardBorder;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(70, headerY + 100);
    ctx.lineTo(STORY_CANVAS_WIDTH - 70, headerY + 100);
    ctx.stroke();
  }

  // 4. TECH FRAME & CORNER CROSSHAIRS
  const frameX = 70;
  const frameY = 300;
  const frameW = STORY_CANVAS_WIDTH - 140; // 940 px
  const frameH = 920;

  if (showTechFrame) {
    const bracketLen = 36;
    ctx.strokeStyle = theme.primaryColor;
    ctx.lineWidth = 2.5;

    // Top-Left ⌜
    ctx.beginPath();
    ctx.moveTo(frameX, frameY + bracketLen);
    ctx.lineTo(frameX, frameY);
    ctx.lineTo(frameX + bracketLen, frameY);
    ctx.stroke();

    // Top-Right ⌝
    ctx.beginPath();
    ctx.moveTo(frameX + frameW - bracketLen, frameY);
    ctx.lineTo(frameX + frameW, frameY);
    ctx.lineTo(frameX + frameW, frameY + bracketLen);
    ctx.stroke();

    // Bottom-Left ⌞
    ctx.beginPath();
    ctx.moveTo(frameX, frameY + frameH - bracketLen);
    ctx.lineTo(frameX, frameY + frameH);
    ctx.lineTo(frameX + bracketLen, frameY + frameH);
    ctx.stroke();

    // Bottom-Right ⌟
    ctx.beginPath();
    ctx.moveTo(frameX + frameW - bracketLen, frameY + frameH);
    ctx.lineTo(frameX + frameW, frameY + frameH);
    ctx.lineTo(frameX + frameW, frameY + frameH - bracketLen);
    ctx.stroke();

    // Telemetry labels
    ctx.font = '700 15px "Courier New", monospace, sans-serif';
    ctx.fillStyle = theme.textDimColor;
    ctx.letterSpacing = '1.5px';
    ctx.fillText('// 3D_VIEWPORT: ORTHO_PBR // 1080P_HD', frameX + 44, frameY + 22);

    ctx.textAlign = 'right';
    const genIdText = options.stats.generationId || 'GEN-3D';
    ctx.fillText(`SEED: [${genIdText}]`, frameX + frameW - 44, frameY + 22);
    ctx.textAlign = 'left';
  }

  // 5. 3D MODEL RENDER
  if (modelCanvas) {
    const modelRenderSize = 900;
    const modelX = (STORY_CANVAS_WIDTH - modelRenderSize) / 2;
    const modelY = frameY + (frameH - modelRenderSize) / 2 + 10;
    ctx.drawImage(modelCanvas, modelX, modelY, modelRenderSize, modelRenderSize);
  }

  // 6. BOTTOM MODEL DESCRIPTION CARD (Glass Card)
  const cardX = 70;
  const cardY = 1270;
  const cardW = STORY_CANVAS_WIDTH - 140; // 940 px
  const cardH = 430;

  // Glass card background
  drawRoundRect(ctx, cardX, cardY, cardW, cardH, 20);
  ctx.fillStyle = theme.cardBg;
  ctx.fill();
  ctx.strokeStyle = theme.cardBorder;
  ctx.lineWidth = 1.5;
  ctx.stroke();

  // Model Name / Title
  const titleText = (options.title || 'MODELO 3D SIN TÍTULO').toUpperCase();
  ctx.font = '900 44px system-ui, -apple-system, sans-serif';
  ctx.fillStyle = theme.textColor;
  ctx.letterSpacing = '0.5px';
  ctx.fillText(titleText, cardX + 36, cardY + 62);

  // Author credit tag (if specified)
  let descOffsetY = cardY + 115;
  if (options.author && options.author.trim() !== '') {
    const authorTag = `@${options.author.replace(/^@/, '')}`;
    ctx.font = '700 20px "Courier New", monospace, sans-serif';
    ctx.fillStyle = theme.secondaryColor;
    ctx.letterSpacing = '2px';
    ctx.fillText(`CREADO POR: ${authorTag}`, cardX + 36, cardY + 98);
    descOffsetY = cardY + 140;
  }

  // Model Description
  if (showDescription && options.description && options.description.trim() !== '') {
    ctx.font = '400 24px system-ui, -apple-system, sans-serif';
    ctx.fillStyle = theme.textDimColor;
    ctx.letterSpacing = '0px';
    const lines = wrapAndDrawText(ctx, options.description.trim(), cardX + 36, descOffsetY, cardW - 72, 36, 3);
    descOffsetY += lines * 36 + 18;
  }

  // Technical Specs Chips Row
  if (showStats) {
    const statsY = cardY + cardH - 64;
    const chips = [
      `📦 ${options.stats.componentCount || 1} PIEZAS`,
      `🔺 ${options.stats.triangles || 0} TRIS`,
      `🧱 ${options.stats.materialsSummary || 'PBR'}`
    ];

    let chipX = cardX + 36;
    ctx.font = '800 17px "Courier New", monospace, sans-serif';
    ctx.letterSpacing = '1px';

    for (const chip of chips) {
      const chipMetrics = ctx.measureText(chip);
      const chipW = chipMetrics.width + 26;
      const chipH = 36;

      drawRoundRect(ctx, chipX, statsY, chipW, chipH, 6);
      ctx.fillStyle = 'rgba(255, 255, 255, 0.06)';
      ctx.fill();
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.14)';
      ctx.lineWidth = 1;
      ctx.stroke();

      ctx.fillStyle = theme.primaryColor;
      ctx.fillText(chip, chipX + 13, statsY + 24);

      chipX += chipW + 16;
    }
  }

  // 7. BOTTOM CALL-TO-ACTION & WATERMARK FOOTER
  const footerY = 1750;

  // Divider
  ctx.strokeStyle = theme.cardBorder;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(70, footerY);
  ctx.lineTo(STORY_CANVAS_WIDTH - 70, footerY);
  ctx.stroke();

  // CTA text
  ctx.textAlign = 'center';
  ctx.font = '800 22px system-ui, -apple-system, sans-serif';
  ctx.fillStyle = '#ffffff';
  ctx.letterSpacing = '1.5px';
  ctx.fillText('DISEÑADO CON MODELCODER • CREÁ TUS MODELOS EN VIVO', STORY_CANVAS_WIDTH / 2, footerY + 45);

  ctx.font = '700 20px "Courier New", monospace, sans-serif';
  ctx.fillStyle = theme.primaryColor;
  ctx.letterSpacing = '2.5px';
  ctx.fillText('MODELCODER.VERCEL.APP', STORY_CANVAS_WIDTH / 2, footerY + 80);
  ctx.textAlign = 'left';

  return canvas;
}

/**
 * Exports a canvas as a high-definition PNG Blob.
 */
export function exportStoryToBlob(canvas: HTMLCanvasElement): Promise<Blob> {
  return new Promise((resolve, reject) => {
    canvas.toBlob((blob) => {
      if (blob) {
        resolve(blob);
      } else {
        reject(new Error('No se pudo generar el archivo PNG de la historia.'));
      }
    }, 'image/png', 1.0);
  });
}

/**
 * Triggers direct browser download of the Instagram Story image.
 */
export function downloadStoryImage(canvas: HTMLCanvasElement, filename: string = 'modelcoder_historia_ig.png'): void {
  const safeFilename = filename.toLowerCase().endsWith('.png') ? filename : `${filename}.png`;
  const dataUrl = canvas.toDataURL('image/png');
  const a = document.createElement('a');
  a.href = dataUrl;
  a.download = safeFilename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

/**
 * Copies the story image directly into the user's system clipboard (PNG Blob).
 * Supported in Chrome, Edge, Firefox, Safari.
 */
export async function copyStoryToClipboard(canvas: HTMLCanvasElement): Promise<boolean> {
  if (typeof navigator === 'undefined' || !navigator.clipboard || typeof ClipboardItem === 'undefined') {
    throw new Error('Tu navegador no soporta la copia directa de imágenes al portapapeles.');
  }

  const blob = await exportStoryToBlob(canvas);
  await navigator.clipboard.write([
    new ClipboardItem({ 'image/png': blob })
  ]);
  return true;
}

/**
 * Native web share for mobile devices (opens native Instagram Story / WhatsApp share sheet).
 */
export async function shareStory(
  canvas: HTMLCanvasElement,
  filename: string = 'historia_modelcoder.png',
  title: string = 'Mi Modelo 3D en ModelCoder',
  text: string = 'Mirá el modelo 3D que creé con texturas PBR y exportación GLB en ModelCoder Studio!'
): Promise<boolean> {
  if (typeof navigator === 'undefined' || !navigator.share) {
    throw new Error('La función de compartir no está disponible en este navegador o dispositivo.');
  }

  const blob = await exportStoryToBlob(canvas);
  const file = new File([blob], filename, { type: 'image/png' });

  if (navigator.canShare && !navigator.canShare({ files: [file] })) {
    throw new Error('Este dispositivo no soporta compartir imágenes directamente.');
  }

  await navigator.share({
    title,
    text,
    files: [file]
  });
  return true;
}
