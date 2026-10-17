/**
 * MODELCODER — Social Graphics & Marketing Exporter (Stories 9:16 & Posts 1:1)
 * Generates high-impact 1080x1920 (Instagram Stories/TikTok) and 1080x1080 (Instagram Feed/Twitter)
 * graphics for user-created 3D models with official branding, customizable themes, and telemetry.
 */

export type SocialFormat = 'story' | 'post';

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
    cardBg: 'rgba(11, 16, 26, 0.88)',
    cardBorder: 'rgba(0, 240, 255, 0.35)',
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
    cardBg: 'rgba(18, 21, 28, 0.90)',
    cardBorder: 'rgba(255, 255, 255, 0.20)',
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
    cardBg: 'rgba(20, 10, 35, 0.88)',
    cardBorder: 'rgba(236, 72, 153, 0.38)',
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
    cardBg: 'rgba(24, 18, 10, 0.90)',
    cardBorder: 'rgba(245, 158, 11, 0.40)',
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
    cardBg: 'rgba(11, 16, 26, 0.90)',
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
  format?: SocialFormat;
  title: string;
  description: string;
  author?: string;
  theme: StoryTheme;
  showWatermark?: boolean;
  showDescription?: boolean;
  showStats?: boolean;
  showTechFrame?: boolean;
  stats: StoryModelStats;
  logoImage?: CanvasImageSource | null;
}

/**
 * Dimensions
 */
export const STORY_CANVAS_WIDTH = 1080;
export const STORY_CANVAS_HEIGHT = 1920;

export const POST_CANVAS_WIDTH = 1080;
export const POST_CANVAS_HEIGHT = 1080;

/**
 * Singleton cached logo image element
 */
let cachedLogoImage: HTMLImageElement | null = null;

export function getModelCoderLogo(): HTMLImageElement | null {
  if (typeof window === 'undefined' || typeof Image === 'undefined') return null;
  if (!cachedLogoImage) {
    cachedLogoImage = new Image();
    cachedLogoImage.src = '/logo.png';
  }
  return cachedLogoImage;
}

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
 * Draws the high-impact social graphic onto the target canvas.
 * Supports both Story 9:16 (1080x1920) and Post 1:1 (1080x1080).
 */
export function drawStoryCard(
  modelCanvas: HTMLCanvasElement | null,
  options: StoryOptions,
  targetCanvas?: HTMLCanvasElement
): HTMLCanvasElement {
  const isPost = options.format === 'post';
  const canvasWidth = isPost ? POST_CANVAS_WIDTH : STORY_CANVAS_WIDTH;
  const canvasHeight = isPost ? POST_CANVAS_HEIGHT : STORY_CANVAS_HEIGHT;

  const canvas = targetCanvas || document.createElement('canvas');
  canvas.width = canvasWidth;
  canvas.height = canvasHeight;

  const ctx = canvas.getContext('2d');
  if (!ctx) return canvas;

  const theme = STORY_THEMES[options.theme] || STORY_THEMES.cyber_dark;
  const showWatermark = options.showWatermark !== false;
  const showDescription = options.showDescription !== false;
  const showStats = options.showStats !== false;
  const showTechFrame = options.showTechFrame !== false;

  const logoImg = options.logoImage || getModelCoderLogo();

  // 1. BACKGROUND
  if (theme.isTransparent) {
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);
  } else if (theme.bgGradient) {
    const bgGrad = ctx.createLinearGradient(0, 0, 0, canvasHeight);
    bgGrad.addColorStop(0, theme.bgGradient[0]);
    bgGrad.addColorStop(0.5, theme.bgGradient[1]);
    bgGrad.addColorStop(1, theme.bgGradient[2]);
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, canvasWidth, canvasHeight);

    // Subtle background grid
    ctx.strokeStyle = theme.gridColor;
    ctx.lineWidth = 1;
    const gridSize = 64;
    for (let x = 0; x <= canvasWidth; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvasHeight);
      ctx.stroke();
    }
    for (let y = 0; y <= canvasHeight; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(canvasWidth, y);
      ctx.stroke();
    }
  }

  // 2. RADIAL AMBIENT GLOW BEHIND 3D MODEL
  const glowX = canvasWidth / 2;
  const glowY = isPost ? 470 : 800;
  const glowRadius = isPost ? 440 : theme.glowRadius;
  const radGlow = ctx.createRadialGradient(glowX, glowY, 40, glowX, glowY, glowRadius);
  radGlow.addColorStop(0, theme.glowColor);
  radGlow.addColorStop(0.5, theme.glowColor.replace(/[\d\.]+\)$/, '0.06)'));
  radGlow.addColorStop(1, 'rgba(0, 0, 0, 0)');
  ctx.fillStyle = radGlow;
  ctx.fillRect(0, glowY - glowRadius, canvasWidth, glowRadius * 2);

  // 3. TOP BRAND HEADER & WATERMARK
  if (showWatermark) {
    if (isPost) {
      // POST 1:1 HEADER
      const headerY = 50;
      const logoSize = 56;
      const logoX = 50;

      // Draw Logo Image if available
      if (logoImg && (logoImg as any).naturalWidth > 0) {
        try {
          ctx.drawImage(logoImg, logoX, headerY - 6, logoSize, logoSize);
        } catch {}
      }

      const textStartX = logoImg ? logoX + logoSize + 14 : logoX;

      // Brand Title
      ctx.font = '900 36px system-ui, -apple-system, sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.letterSpacing = '0.5px';
      ctx.fillText('MODELCODER', textStartX, headerY + 28);

      // Pill Tag beside brand
      const brandWidth = ctx.measureText('MODELCODER').width;
      const pillX = textStartX + brandWidth + 14;
      const pillY = headerY;
      drawRoundRect(ctx, pillX, pillY, 120, 34, 6);
      ctx.fillStyle = 'rgba(255, 184, 0, 0.12)';
      ctx.fill();
      ctx.strokeStyle = theme.secondaryColor;
      ctx.lineWidth = 1.2;
      ctx.stroke();

      ctx.font = '800 14px "Courier New", monospace, sans-serif';
      ctx.fillStyle = theme.secondaryColor;
      ctx.letterSpacing = '1.5px';
      ctx.fillText('3D STUDIO', pillX + 13, pillY + 22);

      // Subtitle below brand
      ctx.font = '700 14px "Courier New", monospace, sans-serif';
      ctx.fillStyle = theme.primaryColor;
      ctx.letterSpacing = '1.5px';
      ctx.fillText('CATÁLOGO 3D PROCEDURAL', textStartX, headerY + 46);

      // Right-side URL Stamp
      const stampX = canvasWidth - 50;
      ctx.textAlign = 'right';
      ctx.font = '800 18px "Courier New", monospace, sans-serif';
      ctx.fillStyle = theme.primaryColor;
      ctx.letterSpacing = '1.5px';
      ctx.fillText('modelcoder.vercel.app', stampX, headerY + 24);

      ctx.font = '600 13px system-ui, sans-serif';
      ctx.fillStyle = theme.textDimColor;
      ctx.letterSpacing = '0.5px';
      ctx.fillText('VERIFIED 3D ASSET', stampX, headerY + 44);
      ctx.textAlign = 'left';

      // Divider line
      ctx.strokeStyle = theme.cardBorder;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(50, headerY + 64);
      ctx.lineTo(canvasWidth - 50, headerY + 64);
      ctx.stroke();
    } else {
      // STORY 9:16 HEADER
      const headerY = 150;
      const logoSize = 68;
      const logoX = 70;

      // Draw Logo Image if available
      if (logoImg && (logoImg as any).naturalWidth > 0) {
        try {
          ctx.drawImage(logoImg, logoX, headerY - 6, logoSize, logoSize);
        } catch {}
      }

      const textStartX = logoImg ? logoX + logoSize + 18 : logoX;

      // Category badge
      ctx.font = '700 18px "Courier New", monospace, sans-serif';
      ctx.fillStyle = theme.primaryColor;
      ctx.letterSpacing = '2px';
      ctx.fillText('CATÁLOGO 3D PROCEDURAL · WEB EDITION', textStartX, headerY + 12);

      // Main Brand Title
      ctx.font = '900 52px system-ui, -apple-system, sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.letterSpacing = '1px';
      ctx.fillText('MODELCODER', textStartX, headerY + 60);

      // Pill Tag beside brand
      const brandTextWidth = ctx.measureText('MODELCODER').width;
      const pillX = textStartX + brandTextWidth + 18;
      const pillY = headerY + 24;
      drawRoundRect(ctx, pillX, pillY, 140, 38, 8);
      ctx.fillStyle = 'rgba(255, 184, 0, 0.12)';
      ctx.fill();
      ctx.strokeStyle = theme.secondaryColor;
      ctx.lineWidth = 1.5;
      ctx.stroke();

      ctx.font = '800 16px "Courier New", monospace, sans-serif';
      ctx.fillStyle = theme.secondaryColor;
      ctx.letterSpacing = '2px';
      ctx.fillText('3D STUDIO', pillX + 16, pillY + 25);

      // Brand Watermark URL Stamp
      const stampX = canvasWidth - 70;
      ctx.textAlign = 'right';
      ctx.font = '800 22px "Courier New", monospace, sans-serif';
      ctx.fillStyle = theme.primaryColor;
      ctx.letterSpacing = '2px';
      ctx.fillText('modelcoder.vercel.app', stampX, headerY + 40);

      ctx.font = '600 15px system-ui, sans-serif';
      ctx.fillStyle = theme.textDimColor;
      ctx.letterSpacing = '1px';
      ctx.fillText('VERIFIED PROCEDURAL ASSET', stampX, headerY + 64);
      ctx.textAlign = 'left';

      // Header divider line
      ctx.strokeStyle = theme.cardBorder;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(70, headerY + 84);
      ctx.lineTo(canvasWidth - 70, headerY + 84);
      ctx.stroke();
    }
  }

  // 4. TECH FRAME & CORNER CROSSHAIRS
  if (isPost) {
    // POST 1:1 FRAMING
    const frameX = 50;
    const frameY = 130;
    const frameW = canvasWidth - 100;
    const frameH = 670;

    if (showTechFrame) {
      const bracketLen = 28;
      ctx.strokeStyle = theme.primaryColor;
      ctx.lineWidth = 2;

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
      ctx.font = '700 14px "Courier New", monospace, sans-serif';
      ctx.fillStyle = theme.textDimColor;
      ctx.letterSpacing = '1.5px';
      ctx.fillText('VISOR 3D · PBR 1080P', frameX + 36, frameY + 20);

      ctx.textAlign = 'right';
      const genIdText = options.stats.generationId || 'GEN-3D';
      ctx.fillText(`ID: [${genIdText}]`, frameX + frameW - 36, frameY + 20);
      ctx.textAlign = 'left';
    }

    // 5. 3D MODEL RENDER (POST 1:1)
    if (modelCanvas) {
      const modelRenderSize = 650;
      const modelX = (canvasWidth - modelRenderSize) / 2;
      const modelY = frameY + (frameH - modelRenderSize) / 2 + 10;
      ctx.drawImage(modelCanvas, modelX, modelY, modelRenderSize, modelRenderSize);
    }

    // 6. BOTTOM MODEL DESCRIPTION CARD (POST 1:1)
    const cardX = 50;
    const cardY = 820;
    const cardW = canvasWidth - 100;
    const cardH = 210;

    drawRoundRect(ctx, cardX, cardY, cardW, cardH, 16);
    ctx.fillStyle = theme.cardBg;
    ctx.fill();
    ctx.strokeStyle = theme.cardBorder;
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Model Name
    const titleText = (options.title || 'MODELO 3D SIN TÍTULO').toUpperCase();
    ctx.font = '900 32px system-ui, -apple-system, sans-serif';
    ctx.fillStyle = theme.textColor;
    ctx.letterSpacing = '0.5px';
    ctx.fillText(titleText, cardX + 28, cardY + 44);

    // Author credit
    let descY = cardY + 84;
    if (options.author && options.author.trim() !== '') {
      const authorTag = `@${options.author.replace(/^@/, '')}`;
      ctx.font = '700 16px "Courier New", monospace, sans-serif';
      ctx.fillStyle = theme.secondaryColor;
      ctx.letterSpacing = '1.5px';
      ctx.fillText(`CREADO POR: ${authorTag}`, cardX + 28, cardY + 70);
      descY = cardY + 100;
    }

    // Description (1-2 lines for square post)
    if (showDescription && options.description && options.description.trim() !== '') {
      ctx.font = '400 19px system-ui, -apple-system, sans-serif';
      ctx.fillStyle = theme.textDimColor;
      ctx.letterSpacing = '0px';
      wrapAndDrawText(ctx, options.description.trim(), cardX + 28, descY, cardW - 56, 26, 2);
    }

    // Spec Chips Row
    if (showStats) {
      const statsY = cardY + cardH - 46;
      const chips = [
        `📦 ${options.stats.componentCount || 1} PIEZAS`,
        `🔺 ${options.stats.triangles || 0} TRIS`,
        `🧱 ${options.stats.materialsSummary || 'PBR'}`
      ];

      let chipX = cardX + 28;
      ctx.font = '800 14px "Courier New", monospace, sans-serif';
      ctx.letterSpacing = '1px';

      for (const chip of chips) {
        const chipMetrics = ctx.measureText(chip);
        const chipW = chipMetrics.width + 20;
        const chipH = 30;

        drawRoundRect(ctx, chipX, statsY, chipW, chipH, 5);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.06)';
        ctx.fill();
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.14)';
        ctx.lineWidth = 1;
        ctx.stroke();

        ctx.fillStyle = theme.primaryColor;
        ctx.fillText(chip, chipX + 10, statsY + 20);

        chipX += chipW + 12;
      }

      // Small footer stamp inside card
      ctx.textAlign = 'right';
      ctx.font = '700 14px "Courier New", monospace, sans-serif';
      ctx.fillStyle = theme.primaryColor;
      ctx.fillText('MODELCODER.VERCEL.APP', cardX + cardW - 28, statsY + 20);
      ctx.textAlign = 'left';
    }
  } else {
    // STORY 9:16 FRAMING
    const frameX = 70;
    const frameY = 270;
    const frameW = canvasWidth - 140; // 940 px
    const frameH = 960;

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
      ctx.font = '700 16px "Courier New", monospace, sans-serif';
      ctx.fillStyle = theme.textDimColor;
      ctx.letterSpacing = '1.5px';
      ctx.fillText('VISOR 3D · PBR 1080P', frameX + 44, frameY + 24);

      ctx.textAlign = 'right';
      const genIdText = options.stats.generationId || 'GEN-3D';
      ctx.fillText(`ID: [${genIdText}]`, frameX + frameW - 44, frameY + 24);
      ctx.textAlign = 'left';
    }

    // 5. 3D MODEL RENDER (STORY 9:16)
    if (modelCanvas) {
      const modelRenderSize = 920;
      const modelX = (canvasWidth - modelRenderSize) / 2;
      const modelY = frameY + (frameH - modelRenderSize) / 2 + 10;
      ctx.drawImage(modelCanvas, modelX, modelY, modelRenderSize, modelRenderSize);
    }

    // 6. BOTTOM MODEL DESCRIPTION CARD (STORY 9:16)
    const cardX = 70;
    const cardY = 1270;
    const cardW = canvasWidth - 140; // 940 px
    const cardH = 430;

    drawRoundRect(ctx, cardX, cardY, cardW, cardH, 20);
    ctx.fillStyle = theme.cardBg;
    ctx.fill();
    ctx.strokeStyle = theme.cardBorder;
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Model Name
    const titleText = (options.title || 'MODELO 3D SIN TÍTULO').toUpperCase();
    ctx.font = '900 44px system-ui, -apple-system, sans-serif';
    ctx.fillStyle = theme.textColor;
    ctx.letterSpacing = '0.5px';
    ctx.fillText(titleText, cardX + 36, cardY + 62);

    // Author credit tag
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

    // 7. BOTTOM CALL-TO-ACTION & WATERMARK FOOTER (STORY 9:16)
    const footerY = 1750;

    ctx.strokeStyle = theme.cardBorder;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(70, footerY);
    ctx.lineTo(canvasWidth - 70, footerY);
    ctx.stroke();

    ctx.textAlign = 'center';
    ctx.font = '800 22px system-ui, -apple-system, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.letterSpacing = '1.5px';
    ctx.fillText('DISEÑADO CON MODELCODER · CREÁ TUS MODELOS EN VIVO', canvasWidth / 2, footerY + 45);

    ctx.font = '700 20px "Courier New", monospace, sans-serif';
    ctx.fillStyle = theme.primaryColor;
    ctx.letterSpacing = '2.5px';
    ctx.fillText('MODELCODER.VERCEL.APP', canvasWidth / 2, footerY + 80);
    ctx.textAlign = 'left';
  }

  return canvas;
}

/**
 * Backwards compatible export
 */
export const drawSocialCard = drawStoryCard;

/**
 * Exports a canvas as a high-definition PNG Blob.
 */
export function exportStoryToBlob(canvas: HTMLCanvasElement): Promise<Blob> {
  return new Promise((resolve, reject) => {
    canvas.toBlob((blob) => {
      if (blob) {
        resolve(blob);
      } else {
        reject(new Error('No se pudo generar el archivo PNG de la imagen.'));
      }
    }, 'image/png', 1.0);
  });
}

/**
 * Triggers direct browser download of the image.
 */
export function downloadStoryImage(canvas: HTMLCanvasElement, filename: string = 'modelcoder_share.png'): void {
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
 * Copies the story/post image directly into the user's system clipboard (PNG Blob).
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
 * Native web share for mobile devices.
 */
export async function shareStory(
  canvas: HTMLCanvasElement,
  filename: string = 'modelcoder_share.png',
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
