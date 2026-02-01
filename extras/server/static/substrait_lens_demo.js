(() => {
  const init = () => {
    const sub = document.getElementById('substrateCanvas');
    const subSelect = document.getElementById('substraitSelect');
    const lensSelect = document.getElementById('lensSelect');
    const readout = document.getElementById('hoverReadout');
    const imageUpload = document.getElementById('imageUpload');

    if (!sub || !subSelect || !lensSelect || !readout) return;

    const subctx = sub.getContext('2d');
    if (!subctx) return;

    const rawBytesEl = document.getElementById('rawBytes');
    const rawBitsEl = document.getElementById('rawBits');
    const subBytesEl = document.getElementById('subBytes');
    const savedPctEl = document.getElementById('savedPct');
    const ramUsageEl = document.getElementById('ramUsage');
    const hddUsageEl = document.getElementById('hddUsage');
    const sourceNoteEl = document.getElementById('substrate-source-note');
    const lensSchemaEl = document.getElementById('lensSchema');
    const lensBadge = document.getElementById('lensBadge');
    const lensBadgeCtx = lensBadge ? lensBadge.getContext('2d') : null;

    // API-backed stats (refreshed per substrait/lens); fallback to local estimates
    let apiSubstrateStats = null;

    function localEstimate(currentSub, currentLens) {
      const subKey = (currentSub || '').toLowerCase();
      const lensKey = (currentLens || '').toLowerCase();
      const complexity = {
        sine: 0.8,
        spiral: 1.15,
        logistic: 0.9,
        zxy: 1.0,
        zxy2: 1.1,
        musicscale: 0.95,
        snail: 1.05,
        goldenratio: 1.2,
        momentum: 0.92,
        logic: 0.75,
        image: 1.25,
      }[subKey] || 1.0;
      const total = Math.max(320, Math.round(900 * complexity));
      const raw_bytes = total * 3 * 8;
      const raw_bits = raw_bytes * 8;
      const expr_scale = {
        sine: 1.0,
        spiral: 1.12,
        logistic: 1.05,
        zxy: 1.08,
        zxy2: 1.12,
        musicscale: 1.02,
        snail: 1.1,
        goldenratio: 1.15,
        momentum: 1.04,
        logic: 0.95,
        image: 1.2,
      }[subKey] || 1.0;
      const expr_bytes = Math.max(24, Math.ceil(Math.log2(total + 2) * 6 * expr_scale));
      const lens_weight = {
        color: 1.0,
        sound: 1.15,
        note: 1.2,
        vector: 1.1,
        angle: 1.05,
        hue: 1.0,
        value: 1.02,
        highlight: 1.05,
        shadow: 1.05,
        tone: 1.1,
        chord: 1.15,
        harmonic: 1.18,
      }[lensKey] || 1.0;
      const lens_bytes = Math.max(18, Math.ceil((Math.log2(total + 2)) * lens_weight * 4.2));
      const sub_bytes = expr_bytes + lens_bytes;
      const saved_pct = Math.max(0, (1 - sub_bytes / raw_bytes) * 100);
      return { raw_bytes, raw_bits, sub_bytes, saved_pct };
    }

    async function fetchSubstrateStats(currentSub = substraitType, currentLens = lensType) {
      const applyStats = (data, note, isError = false) => {
        apiSubstrateStats = data;
        if (rawBytesEl && rawBitsEl && subBytesEl && savedPctEl && ramUsageEl && hddUsageEl) {
          rawBytesEl.textContent = formatBytes(data.raw_bytes);
          rawBitsEl.textContent = formatBits(data.raw_bits);
          subBytesEl.textContent = formatBytes(data.sub_bytes);
          savedPctEl.textContent = `${data.saved_pct.toFixed(1)}%`;
          hddUsageEl.textContent = formatBytes(data.raw_bytes);
          ramUsageEl.textContent = formatBytes(data.sub_bytes);
        }
        if (sourceNoteEl) {
          sourceNoteEl.textContent = note;
          sourceNoteEl.style.color = isError ? '#ffb3c1' : '#cfe9ff';
        }
      };

      try {
        const params = new URLSearchParams({ substrait: currentSub, lens: currentLens });
        const res = await fetch(`/api/demo/substrate?${params.toString()}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        applyStats(data, `Data source: core-backed metrics for ${currentSub} + ${currentLens}`);
      } catch (err) {
        console.warn('Substrate demo API unavailable, using local estimates.', err);
        const est = localEstimate(currentSub, currentLens);
        applyStats(est, 'Data source: local estimates (API unavailable)', true);
      }
    }

    const lensLabelFromMode = (mode) => mode
      .replace(/-/g, ' ')
      .replace(/\b\w/g, (c) => c.toUpperCase());

    const PHI = (1 + Math.sqrt(5)) / 2;
    const LENSES = {
      sine: {
        id: 'sine',
        label: 'Sine Wave',
        type: '1D periodic',
        dimensions: ['time', 'amplitude', 'phase'],
        parameters: { frequency: 1, amplitude: 1, phase: 0, harmonics: [1, 2, 3] },
        attributes: ['smooth', 'oscillatory', 'continuous'],
        lensModes: ['waveform', 'spectrum', 'phase-space', 'wavelength', 'frequency', 'phase', 'amplitude', 'color'],
      },
      spiral: {
        id: 'spiral',
        label: 'Spiral Wave',
        type: '2D radial',
        dimensions: ['radius', 'angle', 'amplitude'],
        parameters: { turns: 3, radialGrowth: 'linear', modulation: 'none' },
        attributes: ['cyclical', 'expanding', 'phase-linked'],
        lensModes: ['polar-plot', 'radius-vs-angle'],
      },
      logistic: {
        id: 'logistic',
        label: 'Logistic Curve',
        type: '1D growth',
        dimensions: ['time', 'population', 'carryingCapacity'],
        parameters: { r: 2.5, K: 1.0, x0: 0.1 },
        attributes: ['saturating', 'nonlinear', 'sigmoid'],
        lensModes: ['time-series', 'phase-diagram'],
      },
      zxy: {
        id: 'zxy',
        label: 'z = x·y',
        type: '2D surface',
        dimensions: ['x', 'y', 'z'],
        parameters: { domain: [-2, 2], resolution: 64, symmetry: 'saddle' },
        attributes: ['bilinear', 'saddle', 'hyperbolic'],
        lensModes: ['height-map', 'contour-lines'],
      },
      zxy2: {
        id: 'zxy2',
        label: 'z = x·y²',
        type: '2D surface',
        dimensions: ['x', 'y', 'z'],
        parameters: { domain: [-2, 2], resolution: 64, curvatureBias: 'y-dominant' },
        attributes: ['anisotropic', 'parabolic-in-y'],
        lensModes: ['height-map', 'curvature-profile'],
      },
      musicscale: {
        id: 'musicscale',
        label: 'Musical Scale',
        type: 'discrete harmonic',
        dimensions: ['note', 'frequency', 'octave', 'chord', 'harmonic'],
        parameters: { tuning: '12-TET', root: 'C4', scaleType: 'major', chordTypes: ['triad', '7th', 'sus2', 'sus4'], harmonics: [1, 2, 3, 4, 5, 6] },
        attributes: ['quantized', 'harmonic', 'stackable'],
        lensModes: ['piano-roll', 'circle-of-fifths', 'harmonic-lattice'],
      },
      snail: {
        id: 'snail',
        label: 'Snail Shell',
        type: 'logarithmic spiral',
        dimensions: ['radius', 'angle', 'growthFactor'],
        parameters: { growthRate: 0.18, whorls: 4, thickness: 0.2 },
        attributes: ['self-similar', 'organic', 'logarithmic'],
        lensModes: ['shell-profile', 'growth-trajectory'],
      },
      goldenratio: {
        id: 'goldenratio',
        label: 'Golden Ratio Spiral',
        type: 'phi-spiral',
        dimensions: ['radius', 'angle', 'phi-step'],
        parameters: { phi: PHI, squares: 8, orientation: 'counterclockwise' },
        attributes: ['self-similar', 'discrete-continuous bridge'],
        lensModes: ['square-tiling', 'continuous-spiral'],
      },
      momentum: {
        id: 'momentum',
        label: 'Momentum',
        type: 'phase-space',
        dimensions: ['position', 'momentum', 'time'],
        parameters: { mass: 1, potential: 'harmonic', damping: 0.0 },
        attributes: ['conserved', 'directional', 'vectorial'],
        lensModes: ['phase-portrait', 'energy-levels'],
      },
      logic: {
        id: 'logic',
        label: 'Logic Gate',
        type: 'discrete boolean',
        dimensions: ['inputA', 'inputB', 'output'],
        parameters: { gateType: ['AND', 'OR', 'XOR', 'NAND'], truthTable: true },
        attributes: ['binary', 'composable', 'deterministic'],
        lensModes: ['truth-table', 'circuit-diagram'],
      },
      image: {
        id: 'image',
        label: 'Image Substrait',
        type: '2D raster',
        dimensions: ['x', 'y', 'color', 'layer'],
        parameters: { resolution: [512, 512], channels: ['R', 'G', 'B', 'A'], layers: ['base', 'mask', 'detail'] },
        attributes: ['sampled', 'layered', 'composite'],
        lensModes: ['channel-view', 'layer-stack'],
      },
    };

    const lensOptionsBySubstrait = Object.fromEntries(
      Object.entries(LENSES).map(([key, meta]) => {
        const opts = (meta.lensModes || []).map((m) => ({ value: m, label: lensLabelFromMode(m) }));
        return [key, opts.length ? opts : [{ value: 'hue', label: 'Hue' }]];
      })
    );
    lensOptionsBySubstrait.default = [{ value: 'hue', label: 'Hue' }];

    const substraitLabels = {
      sine: 'Sine wave',
      spiral: 'Spiral wave',
      logistic: 'Logistic curve',
      zxy: 'Saddle (z = x·y)',
      zxy2: 'Bowl-saddle (z = x·y²)',
      musicscale: 'Musical scale',
      snail: 'Snail shell',
      goldenratio: 'Golden ratio spiral',
      momentum: 'Momentum',
      logic: 'Logic gate',
      image: 'Image substrait',
    };

    function pushLimited(arr, item, limit) {
      arr.push(item);
      while (arr.length > limit) arr.shift();
    }

    function applyHoverEffect(subType, lensType, x, y, hue, angle) {
      const a = angle != null ? angle : 0;
      const h = hue != null ? hue : 200;
      // Lens-driven animations (overlay on top of substrait-specific trails)
      switch (lensType) {
        case 'waveform':
        case 'amplitude':
          pushLimited(colorWake, { x, y, hue: h, life: 1 }, 120);
          break;
        case 'spectrum':
        case 'frequency':
          pushLimited(colorRipples, { x, y, hue: h, life: 1 }, 26);
          break;
        case 'phase-space':
        case 'phase-diagram':
        case 'vector':
        case 'angle':
          pushLimited(rocketTrail, { x, y, angle: a, life: 1 }, 36);
          break;
        case 'polar-plot':
        case 'radius-vs-angle':
        case 'shell-profile':
        case 'continuous-spiral':
          pushLimited(soundRipples, { x, y, baseRadius: 6, expand: 90, life: 1 }, 38);
          break;
        case 'time-series':
        case 'height-map':
        case 'contour-lines':
        case 'curvature-profile':
          pushLimited(colorRipples, { x, y, hue: h, life: 1 }, 22);
          break;
        case 'piano-roll':
        case 'harmonic-lattice':
        case 'circle-of-fifths':
        case 'tone':
        case 'note':
        case 'chord':
        case 'harmonic':
          pushLimited(soundRipples, { x, y, baseRadius: 4, expand: 110, life: 1 }, 44);
          break;
        case 'truth-table':
        case 'circuit-diagram':
          pushLimited(rocketTrail, { x, y, angle: a + 15, life: 1 }, 28);
          break;
        case 'channel-view':
        case 'layer-stack':
          pushLimited(colorWake, { x, y, hue: h, life: 1 }, 120);
          break;
        default:
          break;
      }

      switch (subType) {
        case 'sine':
          pushLimited(colorRipples, { x, y, hue: h, life: 1 }, 22);
          pushLimited(colorWake, { x, y, hue: h, life: 1 }, 120);
          break;
        case 'spiral':
          pushLimited(rainbowTrail, { x, y, hue: h, life: 1 }, 120);
          pushLimited(soundRipples, { x, y, baseRadius: 6, expand: 90, life: 1 }, 40);
          pushLimited(rocketTrail, { x, y, angle: a + 25, life: 1 }, 32);
          break;
        case 'logistic':
          pushLimited(colorRipples, { x, y, hue: h, life: 1 }, 18);
          pushLimited(rocketTrail, { x, y, angle: a, life: 1 }, 28);
          break;
        case 'zxy':
          pushLimited(colorRipples, { x, y, hue: h, life: 1 }, 26);
          pushLimited(soundRipples, { x, y, baseRadius: 5, expand: 70, life: 1 }, 40);
          break;
        case 'zxy2':
          pushLimited(soundRipples, { x, y, baseRadius: 4, expand: 55, life: 1 }, 40);
          pushLimited(colorWake, { x, y, hue: h, life: 1 }, 90);
          break;
        case 'musicscale':
          pushLimited(soundRipples, { x, y, baseRadius: 8, expand: 110, life: 1 }, 48);
          pushLimited(colorRipples, { x, y, hue: h, life: 1 }, 20);
          break;
        case 'snail':
          pushLimited(colorWake, { x, y, hue: h, life: 1 }, 140);
          pushLimited(rocketTrail, { x, y, angle: a - 40, life: 1 }, 32);
          break;
        case 'goldenratio':
          pushLimited(colorRipples, { x, y, hue: h, life: 1 }, 24);
          pushLimited(soundRipples, { x, y, baseRadius: 7, expand: 95, life: 1 }, 44);
          break;
        case 'momentum':
          pushLimited(rocketTrail, { x, y, angle: a, life: 1 }, 36);
          pushLimited(colorWake, { x, y, hue: h, life: 1 }, 120);
          break;
        case 'logic':
          pushLimited(rocketTrail, { x, y, angle: a, life: 1 }, 28);
          break;
        case 'image':
        default:
          pushLimited(colorRipples, { x, y, hue: h, life: 1 }, 18);
          break;
      }
    }

    function formatParamValue(v) {
      if (Array.isArray(v)) return `[${v.join(', ')}]`;
      if (typeof v === 'object') return '{…}';
      return `${v}`;
    }

    function summarizeParams(params, limit = 4) {
      const entries = Object.entries(params || {}).slice(0, limit);
      return entries.map(([k, v]) => `${k}: ${formatParamValue(v)}`).join(', ');
    }

    function updateLensSchemaDisplay(subType, lensType) {
      if (!lensSchemaEl) return;
      const meta = LENSES[subType];
      if (!meta) {
        lensSchemaEl.textContent = 'Pick a substrait and lens to see its dimensions, modes, and parameters.';
        return;
      }
      const dims = meta.dimensions?.join(', ') || '—';
      const modes = meta.lensModes?.join(' • ') || '—';
      const attrs = meta.attributes?.join(', ') || '—';
      const params = summarizeParams(meta.parameters || {});
      lensSchemaEl.innerHTML = `
        <strong>${meta.label}</strong> <span style="color:#8fd3ff;">(${meta.type})</span><br>
        <span class="muted">Lens:</span> ${lensType} • <span class="muted">Dims:</span> ${dims}<br>
        <span class="muted">Modes:</span> ${modes}<br>
        <span class="muted">Attrs:</span> ${attrs}<br>
        <span class="muted">Params:</span> ${params || '—'}`;
    }

    function tickLensBadge(meta, lens) {
      if (!lensBadgeCtx || !lensBadge) return;
      const w = lensBadge.width;
      const h = lensBadge.height;
      const now = performance.now();
      lensBadgeCtx.clearRect(0, 0, w, h);

      const bg = lensBadgeCtx.createLinearGradient(0, 0, w, h);
      bg.addColorStop(0, 'rgba(38,64,92,0.55)');
      bg.addColorStop(1, 'rgba(20,28,42,0.65)');
      lensBadgeCtx.fillStyle = bg;
      lensBadgeCtx.fillRect(0, 0, w, h);

      const hueBase = (now / 40) % 360;
      lensBadgeCtx.strokeStyle = `hsla(${hueBase},85%,65%,0.6)`;
      lensBadgeCtx.lineWidth = 2;
      lensBadgeCtx.beginPath();
      lensBadgeCtx.roundRect(6, 6, w - 12, h - 12, 10);
      lensBadgeCtx.stroke();

      // Axes representing dimensions
      if (meta && meta.dimensions) {
        const cx = w * 0.28;
        const cy = h * 0.6;
        const radius = Math.min(w, h) * 0.28;
        const dims = meta.dimensions.length;
        for (let i = 0; i < dims; i++) {
          const a = (i / dims) * Math.PI * 2 + (now / 1800);
          const x2 = cx + Math.cos(a) * radius;
          const y2 = cy + Math.sin(a) * radius;
          lensBadgeCtx.strokeStyle = `hsla(${(hueBase + i * 30) % 360},90%,70%,0.7)`;
          lensBadgeCtx.lineWidth = 1.8;
          lensBadgeCtx.beginPath();
          lensBadgeCtx.moveTo(cx, cy);
          lensBadgeCtx.lineTo(x2, y2);
          lensBadgeCtx.stroke();
          lensBadgeCtx.beginPath();
          lensBadgeCtx.arc(x2, y2, 4, 0, Math.PI * 2);
          lensBadgeCtx.fillStyle = `hsla(${(hueBase + i * 30) % 360},90%,70%,0.9)`;
          lensBadgeCtx.fill();
        }
      }

      // Particles/trailing visualizations
      if (lensBadgeParticles.length < 28) {
        const angle = (now / 22 + lensBadgeParticles.length * 9) % 360;
        const speed = 0.6 + Math.random() * 0.5;
        const hue = (hueBase + (lens === 'angle' || lens === 'vector' ? 180 : 0) + Math.random() * 24) % 360;
        lensBadgeParticles.push({
          x: w * 0.55 + Math.random() * (w * 0.35),
          y: h * 0.2 + Math.random() * (h * 0.6),
          angle,
          vel: speed,
          hue,
          life: 1,
          dir: Math.random() > 0.5 ? 1 : -1,
        });
      }

      lensBadgeParticles = lensBadgeParticles.filter((p) => p.life > 0);
      lensBadgeParticles.forEach((p) => {
        const a = (p.angle * Math.PI) / 180;
        p.x += Math.cos(a) * p.vel * p.dir;
        p.y += Math.sin(a) * p.vel * p.dir;
        p.life -= 0.01;
        const alpha = p.life * 0.7;
        lensBadgeCtx.fillStyle = `hsla(${p.hue},90%,65%,${alpha})`;
        lensBadgeCtx.beginPath();
        lensBadgeCtx.arc(p.x, p.y, 3 + (1 - p.life) * 3, 0, Math.PI * 2);
        lensBadgeCtx.fill();
        lensBadgeCtx.strokeStyle = `hsla(${p.hue},90%,75%,${alpha * 0.5})`;
        lensBadgeCtx.beginPath();
        lensBadgeCtx.arc(p.x, p.y, 7 + (1 - p.life) * 10, 0, Math.PI * 2);
        lensBadgeCtx.stroke();
      });

      lensBadgePulse += 0.03;
      const pulse = 4 + Math.sin(lensBadgePulse) * 2;
      lensBadgeCtx.strokeStyle = `hsla(${hueBase + 40},90%,80%,0.5)`;
      lensBadgeCtx.lineWidth = 1.2;
      lensBadgeCtx.beginPath();
      lensBadgeCtx.roundRect(12, 12, w - 24, h - 24, 10 + pulse);
      lensBadgeCtx.stroke();

      if (meta) lensBadgeMeta = meta;
    }

    function refreshLensOptions(subType) {
      const opts = lensOptionsBySubstrait[subType] || lensOptionsBySubstrait.default;
      lensSelect.innerHTML = '';
      opts.forEach((o) => {
        const opt = document.createElement('option');
        opt.value = o.value;
        opt.textContent = o.label;
        lensSelect.appendChild(opt);
      });
      lensType = opts.length ? opts[0].value : '';
      lensSelect.value = lensType;
      lensSelect.disabled = false;
    }

    let t = 0;
    // Ensure defaults are set (fallback to first options if empty)
    if (!subSelect.value && subSelect.options.length) {
      subSelect.value = subSelect.options[0].value;
    }
    let substraitType = subSelect.value;
    let lensType = '';

    let rainbowTrail = [];
    let vectorArrow = null;
    let soundRipples = [];
    let rocketTrail = [];
    let colorRipples = [];
    let colorWake = [];
    let uploadedImage = null;
    let uploadedImageBytes = 0;
    let imageProfile = null;
    let imageSampleData = null;
    let imageBounds = null;
    let lensBadgeParticles = [];
    let lensBadgePulse = 0;
    let lensBadgeMeta = null;

    const PHYSICAL_WIDTH_METERS = 2.0; // visualize canvas as 2 meters wide for wavelength scaling
    const PIXELS_PER_METER = () => sub.width / PHYSICAL_WIDTH_METERS;
    const MIN_WAVELENGTH_M = 0.05; // 5 cm
    const MAX_WAVELENGTH_M = 2.5;  // 2.5 m
    const MIDDLE_C_HZ = 261.63;
    const MAX_TONE_HZ = 2093; // C7 upper bound for clarity
    const BASS_MIN_HZ = 65;   // C2-ish for low end
    const OCT_SPAN_UP = 3;    // up to ~C7
    const OCT_SPAN_DOWN = 2;  // down to ~C2

    function spacingForSubstrait(subType) {
      switch (subType) {
        case 'musicscale':
        case 'logic':
        case 'logistic':
          return 10; // tighter sampling for stepped/sigmoid shapes
        case 'zxy':
        case 'zxy2':
        case 'spiral':
        case 'snail':
        case 'goldenratio':
          return 12;
        default:
          return 14;
      }
    }
    let gridPoints = [];
    let hoverPoint = null;
    let scanActive = false;
    let scanIndex = 0;

    let fitScale = 1;
    let fitOffset = 0;
    let fitCenter = 0;

    function formatBytes(bytes) {
      if (bytes >= 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
      if (bytes >= 1024) return `${(bytes / 1024).toFixed(1)} KB`;
      return `${bytes.toFixed(0)} B`;
    }

    function formatBits(bits) {
      if (bits >= 1024 * 1024) return `${(bits / (1024 * 1024)).toFixed(2)} Mb`;
      if (bits >= 1024) return `${(bits / 1024).toFixed(1)} Kb`;
      return `${bits.toFixed(0)} b`;
    }

    function updateStoragePanel() {
      if (!rawBytesEl || !rawBitsEl || !subBytesEl || !savedPctEl || !ramUsageEl || !hddUsageEl) return;
      if (!apiSubstrateStats) {
        rawBytesEl.textContent = '—';
        rawBitsEl.textContent = '—';
        subBytesEl.textContent = '—';
        savedPctEl.textContent = '—';
        hddUsageEl.textContent = '—';
        ramUsageEl.textContent = '—';
        return;
      }

      rawBytesEl.textContent = formatBytes(apiSubstrateStats.raw_bytes);
      rawBitsEl.textContent = formatBits(apiSubstrateStats.raw_bits);
      subBytesEl.textContent = formatBytes(apiSubstrateStats.sub_bytes);
      savedPctEl.textContent = `${apiSubstrateStats.saved_pct.toFixed(1)}%`;
      hddUsageEl.textContent = formatBytes(apiSubstrateStats.raw_bytes);
      ramUsageEl.textContent = formatBytes(apiSubstrateStats.sub_bytes);
    }

    function quantizeToNote(rawFreq) {
      const names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
      const midi = Math.round(69 + 12 * Math.log2(rawFreq / 440));
      const noteIndex = ((midi % 12) + 12) % 12;
      const octave = Math.floor(midi / 12) - 1;
      const freq = 440 * Math.pow(2, (midi - 69) / 12);
      const label = `${names[noteIndex]}${octave}`;
      return { freq, label };
    }

    function curvatureSign(x, tNow, type) {
      const y0 = curveY(Math.max(0, x - 1), tNow, type);
      const y1 = curveY(x, tNow, type);
      const y2 = curveY(Math.min(sub.width, x + 1), tNow, type);
      const second = y2 - 2 * y1 + y0;
      if (second > 0.5) return 'concave up';
      if (second < -0.5) return 'concave down';
      return 'near inflection';
    }

    function quadrantFromAngle(angle) {
      const a = (angle + 360) % 360;
      if (a >= 45 && a < 135) return 'Q1';
      if (a >= 135 && a < 225) return 'Q2';
      if (a >= 225 && a < 315) return 'Q3';
      return 'Q4';
    }

    function hslToRgb(h, s, l) {
      // h: 0-360, s/l: 0-100
      const _h = h / 360;
      const _s = s / 100;
      const _l = l / 100;

      const hue2rgb = (p, q, t) => {
        if (t < 0) t += 1;
        if (t > 1) t -= 1;
        if (t < 1/6) return p + (q - p) * 6 * t;
        if (t < 1/2) return q;
        if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
        return p;
      };

      let r, g, b;
      if (_s === 0) {
        r = g = b = _l; // achromatic
      } else {
        const q = _l < 0.5 ? _l * (1 + _s) : _l + _s - _l * _s;
        const p = 2 * _l - q;
        r = hue2rgb(p, q, _h + 1/3);
        g = hue2rgb(p, q, _h);
        b = hue2rgb(p, q, _h - 1/3);
      }

      return {
        r: Math.round(r * 255),
        g: Math.round(g * 255),
        b: Math.round(b * 255)
      };
    }

    function rgbToHex({ r, g, b }) {
      const toHex = (v) => v.toString(16).padStart(2, '0');
      return `#${toHex(r)}${toHex(g)}${toHex(b)}`.toUpperCase();
    }

    function rgbToHue(r, g, b) {
      const rn = r / 255;
      const gn = g / 255;
      const bn = b / 255;
      const max = Math.max(rn, gn, bn);
      const min = Math.min(rn, gn, bn);
      const delta = max - min;
      let h = 0;
      if (delta === 0) h = 0;
      else if (max === rn) h = ((gn - bn) / delta) % 6;
      else if (max === gn) h = (bn - rn) / delta + 2;
      else h = (rn - gn) / delta + 4;
      h = Math.round((h * 60 + 360) % 360);
      return h;
    }

    let audioCtx;
    let lastBeep = 0;
    const SPEED_OF_SOUND = 343; // meters per second

    function rebuildImageProfile() {
      if (!uploadedImage) { imageProfile = null; imageSampleData = null; imageBounds = null; return; }
      const off = document.createElement('canvas');
      off.width = sub.width;
      off.height = sub.height;
      const octx = off.getContext('2d');
      if (!octx) { imageProfile = null; imageSampleData = null; imageBounds = null; return; }

      // cover-fit the image into canvas
      const imgAspect = uploadedImage.width / uploadedImage.height;
      const canvasAspect = off.width / off.height;
      let drawW, drawH, dx, dy;
      if (imgAspect > canvasAspect) {
        drawH = off.height;
        drawW = drawH * imgAspect;
        dx = (off.width - drawW) / 2;
        dy = 0;
      } else {
        drawW = off.width;
        drawH = drawW / imgAspect;
        dx = 0;
        dy = (off.height - drawH) / 2;
      }

      octx.clearRect(0, 0, off.width, off.height);
      octx.drawImage(uploadedImage, dx, dy, drawW, drawH);

      const imageData = octx.getImageData(0, 0, off.width, off.height);
      imageSampleData = imageData;
      imageBounds = { dx, dy, dw: drawW, dh: drawH, width: off.width, height: off.height };

      const data = imageData.data;
      const profile = new Array(off.width).fill(0);
      for (let x = 0; x < off.width; x++) {
        let sum = 0;
        for (let y = 0; y < off.height; y++) {
          const idx = (y * off.width + x) * 4;
          const r = data[idx];
          const g = data[idx + 1];
          const b = data[idx + 2];
          const lum = 0.2126 * r + 0.7152 * g + 0.0722 * b; // linear-ish luma
          sum += lum;
        }
        const avg = sum / off.height; // 0..255
        const norm = avg / 255;
        // Map luma to vertical displacement around center: bright => upper, dark => lower
        const yRaw = sub.height / 2 - (norm - 0.5) * sub.height * 0.8;
        profile[x] = yRaw;
      }
      imageProfile = profile;
    }

    function sampleImagePixel(canvasX, canvasY) {
      if (!imageSampleData || !imageBounds) return null;
      const { width, height } = imageBounds;
      const xi = Math.max(0, Math.min(width - 1, Math.floor(canvasX)));
      const yi = Math.max(0, Math.min(height - 1, Math.floor(canvasY)));
      const idx = (yi * width + xi) * 4;
      const d = imageSampleData.data;
      const r = d[idx];
      const g = d[idx + 1];
      const b = d[idx + 2];
      const toHex = (v) => v.toString(16).padStart(2, '0');
      const hex = `#${toHex(r)}${toHex(g)}${toHex(b)}`.toUpperCase();
      return { r, g, b, hex, x: xi, y: yi };
    }

    

    function resumeAudio() {
      if (audioCtx && audioCtx.state === 'suspended' && audioCtx.resume) {
        audioCtx.resume().catch(() => {});
      }
    }

    // Create audio context lazily; resume on first user gesture so browsers allow playback.
    function getCtx() {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      resumeAudio();
      return audioCtx;
    }

    function playBeep(freq) {
      const now = performance.now();
      if (now - lastBeep < 80) return;
      lastBeep = now;
      const ctxA = getCtx();
      const o = ctxA.createOscillator();
      const g = ctxA.createGain();
      o.type = 'sine';
      o.frequency.value = freq;
      g.gain.value = 0.08;
      o.connect(g).connect(ctxA.destination);
      o.start();
      o.stop(ctxA.currentTime + 0.12);
    }

    function playChord(frequencies) {
      const now = performance.now();
      if (now - lastBeep < 120) return;
      lastBeep = now;
      const ctxA = getCtx();
      const gain = ctxA.createGain();
      gain.gain.value = 0.06;
      gain.connect(ctxA.destination);
      const duration = 0.22;
      frequencies.forEach((f) => {
        const o = ctxA.createOscillator();
        o.type = 'sine';
        o.frequency.value = f;
        o.connect(gain);
        o.start();
        o.stop(ctxA.currentTime + duration);
      });
      setTimeout(() => gain.disconnect(), duration * 1000 + 50);
    }

    function slopeMag(x, tNow, type) {
      const y1 = curveY(Math.max(0, x - 1), tNow, type);
      const y2 = curveY(Math.min(sub.width, x + 1), tNow, type);
      return Math.abs(y2 - y1) / 2;
    }

    function rawCurveY(x, tNow, type) {
      if (type === 'sine') {
        return 120 + Math.sin((x + tNow) * 0.02) * 60;
      }
      if (type === 'spiral') {
        // Archimedean spiral height projection
        const theta = (x / sub.width) * Math.PI * 4 + tNow * 0.002;
        const r = 16 + 7 * theta;
        return sub.height * 0.5 - r * Math.sin(theta * 0.9);
      }
      if (type === 'logistic') {
        const L = 1;
        const k = 0.045;
        const x0 = sub.width / 2;
        return 220 - (L / (1 + Math.exp(-k * (x - x0)))) * 200;
      }
      if (type === 'zxy') {
        // Represent z = x·y as the interaction of two axes via angle transition.
        // Map x along [-90°, 90°] so cos(theta) is the x-axis projection and sin(theta) the y-axis projection.
        const theta = (((x / sub.width) * 2 - 1) + Math.sin(tNow * 0.0006) * 0.12) * (Math.PI / 2);
        const xComp = Math.cos(theta); // x projection
        const yComp = Math.sin(theta); // y projection
        const z = xComp * yComp;       // z = x * y = 0.5*sin(2θ), smooth transition of angles
        return sub.height / 2 - z * (sub.height * 0.45);
      }
      if (type === 'zxy2') {
        // Parabolic flavor: reuse angular projection but square the y component (y^2 >= 0)
        const theta = (((x / sub.width) * 2 - 1) + Math.sin(tNow * 0.0006) * 0.12) * (Math.PI / 2);
        const xComp = Math.cos(theta);
        const yComp = Math.sin(theta);
        const z = xComp * (yComp * yComp); // z = x * y^2
        return sub.height / 2 - z * (sub.height * 0.45);
      }
      if (type === 'musicscale') {
        // Constant upward stair centered on Middle C (0). Left side goes negative, right side positive.
        // No motion wobble; steeper near low/high ends.
        const semitones = [-12, -10, -8, -7, -5, -3, -1, 0, 2, 4, 5, 7, 9, 11, 12];
        const seg = sub.width / semitones.length;
        const idx = Math.min(semitones.length - 1, Math.max(0, Math.floor(x / seg)));
        const base = semitones[idx]; // 0 == Middle C
        const norm = Math.abs(base) / Math.max(1, Math.max(...semitones.map((s) => Math.abs(s))));
        const edgeBoost = 1 + 0.5 * norm; // steeper near edges (low/high)
        const stepHeight = 8.5; // vertical gain per semitone
        const centerY = sub.height * 0.65;
        return centerY - base * stepHeight * edgeBoost;
      }
      if (type === 'snail') {
        // Logarithmic spiral projection (snail shell) using sin/cos components
        const theta = (x / sub.width) * Math.PI * 5 + tNow * 0.0015;
        const a = 8, b = 0.18;                    // spiral growth constants
        const r = a * Math.exp(b * theta);        // log spiral radius
        const wobble = 0.22 * r * Math.sin(theta * 1.4); // subtle thickness ripple
        // Project with both sin and cos to capture the spiral roll
        const yProj = r * Math.sin(theta) + 0.35 * r * Math.cos(theta) + wobble;
        return sub.height * 0.6 - yProj * 0.8;
      }
      if (type === 'goldenratio') {
        // Golden ratio spiral: radii constrained to [-66, +33], stepped by φ multiples.
        const phi = (1 + Math.sqrt(5)) / 2;
        const baseNeg = -66;
        const basePos = 33;
        const radii = [
          baseNeg,
          baseNeg / phi,
          baseNeg / (phi * phi),
          baseNeg / (phi * phi * phi),
          baseNeg / (phi * phi * phi * phi),
          basePos / (phi * phi * phi),
          basePos / (phi * phi),
          basePos / phi,
          basePos,
        ];
        // Interval widths follow φ^n progression (1.618-based) instead of uniform slices.
        const intervals = [
          1,
          phi,
          phi * phi,
          phi * phi * phi,
          phi * phi * phi * phi,
          phi * phi * phi,
          phi * phi,
          phi,
        ];
        const totalInterval = intervals.reduce((a, b) => a + b, 0);
        let u = ((x / sub.width) + 0.04 * Math.sin(tNow * 0.0004)) % 1;
        if (u < 0) u += 1; // keep within [0,1)

        let acc = 0;
        let idx = 0;
        let local = 0;
        for (; idx < intervals.length; idx++) {
          const slice = intervals[idx] / totalInterval;
          if (u <= acc + slice || idx === intervals.length - 1) {
            local = (u - acc) / slice;
            break;
          }
          acc += slice;
        }
        const ease = local * local * (3 - 2 * local); // smoothstep
        const rStart = radii[idx];
        const rEnd = radii[idx + 1];
        const r = rStart + (rEnd - rStart) * ease;
        const angleBase = idx * (Math.PI / 2);
        const angle = angleBase + ease * (Math.PI / 2);
        const scale = (sub.height * 0.022);
        const yProj = r * (Math.sin(angle) + 0.42 * Math.cos(angle));
        return sub.height * 0.6 - yProj * scale;
      }
      if (type === 'momentum') {
        // Momentum curve: accelerating then easing (sigmoid of a quadratic path)
        const xn = x / sub.width;
        const v = xn * xn * 1.6; // acceleration phase
        const eased = 1 / (1 + Math.exp(-10 * (v - 0.6)));
        const overshoot = 0.08 * Math.sin(xn * Math.PI * 2);
        return sub.height * 0.72 - (eased + overshoot) * sub.height * 0.5;
      }
      if (type === 'circuit') {
        // Stepped trace pattern (square segments across lanes)
        const lanes = 4;
        const laneH = sub.height / (lanes + 1);
        const segW = sub.width / 14;
        const seg = Math.floor(x / segW);
        const lane = seg % lanes;
        const yBase = laneH * (lane + 1);
        const within = (x % segW) / segW;
        const rise = Math.sin(Math.PI * within);
        const jog = ((seg % 2 === 0) ? -1 : 1) * laneH * 0.22 * rise;
        const micro = 4 * Math.sin(within * Math.PI * 6) * (1 - Math.abs(0.5 - within));
        return yBase + jog + micro;
      }
      if (type === 'logic') {
        // Logic gate profile: trapezoid rising to output high
        const xn = x / sub.width;
        const shoulder = Math.max(0, Math.min(1, (xn - 0.18) / 0.18));
        const fall = Math.max(0, Math.min(1, (0.88 - xn) / 0.18));
        const plateau = Math.min(shoulder, fall);
        const bevel = 0.08 * Math.sin(xn * Math.PI * 2);
        return sub.height * 0.72 - (plateau + bevel) * sub.height * 0.48;
      }
      if (type === 'image' && imageProfile && imageProfile.length) {
        const xi = Math.max(0, Math.min(sub.width - 1, Math.floor(x)));
        return imageProfile[xi];
      }
      return 120;
    }

    function curveY(x, tNow, type) {
      return rawCurveY(x, tNow, type);
    }

    function slopeAngleDeg(x, tNow, type) {
      const y1 = curveY(Math.max(0, x - 1), tNow, type);
      const y2 = curveY(Math.min(sub.width, x + 1), tNow, type);
      const angle = Math.atan2(y2 - y1, 2);
      return (angle * 180 / Math.PI + 360) % 360;
    }

    function colorHueAt(x, y, tNow) {
      const ySign = (y - sub.height / 2) / (sub.height / 2); // -1 bottom, +1 top
      const slopeMix = slopeAngleDeg(x, tNow, substraitType) / 360;
      const xMix = (x / sub.width) % 1;
      const jitter = (slopeMix + xMix) % 1; // keeps full spectrum represented along x/slope

      // Map vertical position to spectrum: bottom violet (~270), middle green (~120), top red (~0)
      const bottomHue = 270; // violet
      const midHue = 120;    // green
      const topHue = 0;      // red

      let baseHue;
      if (ySign >= 0) {
        // interpolate mid -> top
        const t = Math.min(1, ySign);
        baseHue = midHue + (topHue - midHue) * t; // 120 -> 0
      } else {
        // interpolate bottom -> mid
        const t = Math.min(1, -ySign);
        baseHue = bottomHue + (midHue - bottomHue) * t; // 270 -> 120
      }

      // Add a small rainbow sweep to ensure full spectrum appears as you move along x/slope
      const sweep = 60; // ±30 degrees sweep
      const hue = (baseHue + sweep * (jitter - 0.5) + 360) % 360;
      return hue;
    }

    function lensValue(x, y, type) {
      const normY = 1 - (y / sub.height);
      const normX = x / sub.width;
      const slopeDeg = slopeAngleDeg(x, t, substraitType) / 360;
      const angleDeg = slopeAngleDeg(x, t, substraitType);

      if (type === 'hue' || type === 'value' || type === 'highlight' || type === 'shadow') {
        const hue = Math.floor(colorHueAt(x, y, t));
        const sat = 82;
        const baseLum = 58;
        const lum = type === 'value' ? Math.min(78, baseLum + 14) : type === 'highlight' ? Math.min(86, baseLum + 22) : type === 'shadow' ? Math.max(30, baseLum - 22) : baseLum;
        const rgb = hslToRgb(hue, sat, lum);
        const hex = rgbToHex(rgb);
        const label = type === 'hue' ? 'Hue' : type === 'value' ? 'Value' : type === 'highlight' ? 'Highlight' : 'Shadow';
        return {
          text: `${label}: hsl(${hue},${sat}%,${lum}%) | rgb(${rgb.r}, ${rgb.g}, ${rgb.b}) | ${hex}`,
          color: `hsl(${hue},${sat}%,${lum}%)`,
          hue
        };
      }

      // Dimensional lens modes
      if (type === 'waveform') {
        const amp = rawCurveY(x, t, substraitType);
        const phase = ((x / sub.width) * 360) % 360;
        return { text: `Waveform: amp=${amp.toFixed(2)}, phase=${phase.toFixed(1)}°`, color: '#9be8ff', hue: angleDeg };
      }

      if (type === 'spectrum') {
        const freq = 40 + 460 * (Math.abs(rawCurveY(x, t, substraitType)) / (sub.height / 2));
        const mag = Math.abs(slopeDeg * 2 - 1);
        return { text: `Spectrum: f≈${freq.toFixed(1)} Hz, mag=${mag.toFixed(2)}`, color: '#ffd166', hue: (freq / 500) * 360 };
      }

      if (type === 'phase-space') {
        const pos = rawCurveY(x, t, substraitType);
        const vel = slopeDeg * 2 - 1;
        return { text: `Phase-space: pos=${pos.toFixed(2)}, vel=${vel.toFixed(3)}`, color: '#c3f4ff', hue: (vel * 180 + 360) % 360 };
      }

      if (type === 'wavelength') {
        const yRel = (sub.height / 2 - y) / (sub.height / 2);
        const freq = MIDDLE_C_HZ * Math.pow(2, yRel * OCT_SPAN_UP);
        const wavelength = SPEED_OF_SOUND / freq;
        return { text: `Wavelength: λ=${wavelength.toFixed(3)} m (f=${freq.toFixed(1)} Hz)`, color: '#8fd3ff', hue: (freq / MAX_TONE_HZ) * 360 };
      }

      if (type === 'frequency') {
        const yRel = (sub.height / 2 - y) / (sub.height / 2);
        const freq = MIDDLE_C_HZ * Math.pow(2, yRel * OCT_SPAN_UP);
        return { text: `Frequency: ${freq.toFixed(1)} Hz (center = C4)`, color: '#ffb86c', hue: (freq / MAX_TONE_HZ) * 360 };
      }

      if (type === 'phase') {
        const phase = ((x / sub.width) * 360) % 360;
        return { text: `Phase: ${phase.toFixed(1)}° (x-proportional)`, color: '#9be8ff', hue: phase };
      }

      if (type === 'amplitude') {
        const amp = rawCurveY(x, t, substraitType);
        return { text: `Amplitude: ${amp.toFixed(2)} (centered)`, color: '#9ae6b4', hue: angleDeg };
      }

      if (type === 'color') {
        const hue = Math.floor(colorHueAt(x, y, t));
        const rgb = hslToRgb(hue, 82, 58);
        const hex = rgbToHex(rgb);
        return { text: `Color lens: hue=${hue}°, rgb(${rgb.r},${rgb.g},${rgb.b}) ${hex}`, color: hex, hue };
      }

      if (type === 'polar-plot' || type === 'radius-vs-angle') {
        const cx = sub.width / 2;
        const cy = sub.height / 2;
        const dx = x - cx;
        const dy = cy - y;
        const r = Math.sqrt(dx * dx + dy * dy);
        const a = (Math.atan2(dy, dx) * 180 / Math.PI + 360) % 360;
        const text = type === 'polar-plot'
          ? `Polar plot: r=${r.toFixed(1)}, θ=${a.toFixed(1)}°`
          : `Radius vs angle: r=${r.toFixed(1)} @ θ=${a.toFixed(1)}°`;
        return { text, color: '#f6d365', hue: a };
      }

      if (type === 'time-series') {
        const val = rawCurveY(x, t, substraitType);
        return { text: `Time-series: t=${t.toFixed(1)}, value=${val.toFixed(2)}`, color: '#9ae6b4', hue: angleDeg };
      }

      if (type === 'phase-diagram') {
        const pos = rawCurveY(x, t, substraitType);
        const vel = slopeDeg * 2 - 1;
        return { text: `Phase diagram: pos=${pos.toFixed(2)}, vel=${vel.toFixed(3)}`, color: '#9ae6b4', hue: (vel * 180 + 360) % 360 };
      }

      if (type === 'height-map' || type === 'contour-lines') {
        const hVal = rawCurveY(x, t, substraitType);
        const normalized = (hVal + sub.height / 2) / sub.height;
        if (type === 'contour-lines') {
          const level = Math.round(normalized * 10) / 10;
          return { text: `Contour: height=${hVal.toFixed(2)}, level=${level.toFixed(1)}`, color: '#8fd3ff', hue: level * 360 };
        }
        return { text: `Height map: ${hVal.toFixed(2)} (norm ${normalized.toFixed(2)})`, color: '#8fd3ff', hue: normalized * 360 };
      }

      if (type === 'curvature-profile') {
        const y0 = curveY(Math.max(0, x - 1), t, substraitType);
        const y1 = curveY(x, t, substraitType);
        const y2 = curveY(Math.min(sub.width, x + 1), t, substraitType);
        const second = y2 - 2 * y1 + y0;
        return { text: `Curvature: ${second.toFixed(3)}`, color: '#ffb3c1', hue: (second * 40 + 180) % 360 };
      }

      if (type === 'piano-roll') {
        const note = quantizeToNote(220 + normX * 660);
        return { text: `Piano roll: ${note.label} (${note.freq.toFixed(1)} Hz)`, color: '#ffb86c', freq: note.freq, hue: (note.freq / 880) * 360 };
      }

      if (type === 'circle-of-fifths') {
        const keys = ['C','G','D','A','E','B','F#','C#','G#','D#','A#','F'];
        const idx = Math.floor((normX) * 12) % 12;
        const key = keys[idx];
        return { text: `Circle of fifths: ${key} major`, color: '#ffb86c', hue: (idx / 12) * 360 };
      }

      if (type === 'harmonic-lattice') {
        const base = 110 + normX * 660;
        const ratios = [1, 3/2, 5/4];
        const freqs = ratios.map((r) => base * r);
        return { text: `Harmonic lattice: ${freqs.map(f=>f.toFixed(1)).join(' / ')} Hz`, color: '#ffb86c', freq: base, hue: (base / 800) * 360 };
      }

      if (type === 'shell-profile') {
        const cx = sub.width / 2;
        const cy = sub.height / 2;
        const dx = x - cx;
        const dy = cy - y;
        const r = Math.sqrt(dx * dx + dy * dy);
        const a = (Math.atan2(dy, dx) * 180 / Math.PI + 360) % 360;
        return { text: `Shell profile: r=${r.toFixed(1)}, θ=${a.toFixed(1)}°`, color: '#c3f4ff', hue: a };
      }

      if (type === 'growth-trajectory') {
        const growth = Math.log(1 + Math.abs(rawCurveY(x, t, substraitType)) + 1e-3);
        return { text: `Growth trajectory: ${growth.toFixed(3)}`, color: '#c3f4ff', hue: (growth * 120) % 360 };
      }

      if (type === 'square-tiling') {
        const step = (angleDeg + t) % 360;
        return { text: `Square tiling (φ): step=${step.toFixed(1)}°`, color: '#ffd166', hue: step };
      }

      if (type === 'continuous-spiral') {
        const radius = Math.abs(rawCurveY(x, t, substraitType)) + 1;
        const angle = (x / sub.width) * 360;
        return { text: `Continuous spiral: r=${radius.toFixed(2)}, θ=${angle.toFixed(1)}°`, color: '#ffd166', hue: angle };
      }

      if (type === 'phase-portrait') {
        const pos = rawCurveY(x, t, substraitType);
        const mom = slopeDeg * 2 - 1;
        return { text: `Phase portrait: pos=${pos.toFixed(2)}, p=${mom.toFixed(3)}`, color: '#9ae6b4', hue: (mom * 180 + 360) % 360 };
      }

      if (type === 'energy-levels') {
        const pos = rawCurveY(x, t, substraitType) / (sub.height / 2);
        const vel = (slopeDeg * 2 - 1);
        const m = 1;
        const k = 1;
        const energy = 0.5 * m * vel * vel + 0.5 * k * pos * pos;
        return { text: `Energy levels: E=${energy.toFixed(3)} (pos=${pos.toFixed(2)}, vel=${vel.toFixed(2)})`, color: '#9ae6b4', hue: (energy * 90) % 360 };
      }

      if (type === 'truth-table') {
        const a = normX > 0.33;
        const b = normX > 0.66;
        const gates = ['AND','OR','XOR','NAND'];
        const gate = gates[Math.floor((t / 60) % gates.length)];
        let out;
        if (gate === 'AND') out = a && b;
        else if (gate === 'OR') out = a || b;
        else if (gate === 'XOR') out = !!(a ^ b);
        else out = !(a && b);
        return { text: `Truth-table (${gate}): A=${a?1:0}, B=${b?1:0} → ${out?1:0}`, color: out ? '#8ee6a8' : '#ff6b6b', hue: out ? 120 : 0 };
      }

      if (type === 'circuit-diagram') {
        const gates = ['AND','OR','XOR','NAND'];
        const gate = gates[Math.floor((t / 60) % gates.length)];
        return { text: `Circuit: ${gate} gate (inputs along x)`, color: '#8fd3ff', hue: (gates.indexOf(gate) / gates.length) * 360 };
      }

      if (type === 'channel-view' || type === 'layer-stack') {
        const px = sampleImagePixel(x, y);
        if (!px) return { text: 'Load an image to view channels.', color: '#e8ecf3', hue: 200 };
        if (type === 'channel-view') {
          return { text: `Channel view: R=${px.r}, G=${px.g}, B=${px.b}, A=${px.a ?? 255}, hex=${px.hex}`, color: px.hex, hue: angleDeg };
        }
        return { text: `Layer stack: base RGB(${px.r},${px.g},${px.b})`, color: px.hex, hue: angleDeg };
      }

      if (type === 'sound' || type === 'note' || type === 'tone' || type === 'chord' || type === 'harmonic') {
        const rel = (sub.height / 2 - y) / (sub.height / 2); // +1 top (treble), -1 bottom (bass), 0 center
        const mag = Math.min(1, Math.abs(rel));

        let rawFreq;
        if (rel >= 0) {
          // Exponential up from C4 over OCT_SPAN_UP octaves when moving above center
          rawFreq = MIDDLE_C_HZ * Math.pow(2, mag * OCT_SPAN_UP);
        } else {
          // Exponential down from C4 over OCT_SPAN_DOWN octaves when moving below center
          rawFreq = MIDDLE_C_HZ / Math.pow(2, mag * OCT_SPAN_DOWN);
        }

        rawFreq = Math.max(BASS_MIN_HZ, Math.min(MAX_TONE_HZ, rawFreq));
        const wavelength = SPEED_OF_SOUND / rawFreq;

        if (type === 'note' || type === 'chord') {
          const note = quantizeToNote(rawFreq);
          const chord = [note.freq, note.freq * 1.25, note.freq * 1.5];
          const text = `Chord (root ${note.label}): ${note.freq.toFixed(1)} / ${(note.freq*1.25).toFixed(1)} / ${(note.freq*1.5).toFixed(1)} Hz | λ=${(SPEED_OF_SOUND / note.freq).toFixed(3)} m (center = C4, bass below, treble above)`;
          return { text, color: '#ffb86c', freq: note.freq, chord, wavelength: SPEED_OF_SOUND / note.freq };
        }

        if (type === 'harmonic') {
          const base = rawFreq;
          const harmonics = [base, base * 2, base * 3];
          const text = `Harmonics: ${harmonics.map((h) => h.toFixed(1)).join(' / ')} Hz | fundamental λ=${(SPEED_OF_SOUND / base).toFixed(3)} m`;
          return { text, color: '#ffb86c', freq: base, chord: harmonics, wavelength: SPEED_OF_SOUND / base };
        }

        if (type === 'tone' || type === 'sound') {
          const label = `Tone: ${rawFreq.toFixed(1)} Hz | λ=${wavelength.toFixed(3)} m (bass below, treble above)`;
          return { text: label, color: '#ffb86c', freq: rawFreq, wavelength };
        }
      }

      if (type === 'vector' || type === 'angle') {
        const angle = Math.floor(slopeAngleDeg(x, t, substraitType));
        const quad = quadrantFromAngle(angle);
        const curve = curvatureSign(x, t, substraitType);
        const label = type === 'angle' ? `Angle: ${angle}° | quad ${quad} | ${curve}` : `Vector angle: ${angle}° | quadrant: ${quad} | ${curve}`;
        return { text: label, color: '#9be8ff', angle };
      }

      if (type === 'ascii') {
        const code = 33 + Math.floor(normY * 60);
        const ch = String.fromCharCode(code);
        const dist0 = Math.abs(y - sub.height / 2).toFixed(1);
        const xPos = Math.round(x);
        const yPos = Math.round(y);
        return { text: `ASCII: ${ch} (code ${code}) | x=${xPos}, y=${yPos}, |y-mid|=${dist0}`, color: '#8fd3ff' };
      }

      return { text: '', color: '#e8ecf3', hue: angleDeg };
    }

    function lensHue(x, y, type) {
      if (type === 'hue' || type === 'value' || type === 'highlight' || type === 'shadow') {
        return Math.floor(colorHueAt(x, y, t));
      }

      if (type === 'sound' || type === 'note' || type === 'tone' || type === 'chord' || type === 'harmonic' || type === 'piano-roll' || type === 'harmonic-lattice' || type === 'circle-of-fifths' || type === 'wavelength' || type === 'frequency') {
        const angle = slopeAngleDeg(x, t, substraitType);
        const dist = Math.abs(y - sub.height / 2) / (sub.height / 2);
        const rawFreq = 110 + 1650 * (0.35 * dist + 0.65 * (angle / 360));
        return ((rawFreq - 110) / 1760) * 360;
      }

      if (type === 'vector' || type === 'angle' || type === 'phase-space' || type === 'phase-diagram' || type === 'phase-portrait') {
        return slopeAngleDeg(x, t, substraitType);
      }

      if (type === 'polar-plot' || type === 'radius-vs-angle' || type === 'shell-profile' || type === 'continuous-spiral') {
        const cx = sub.width / 2;
        const cy = sub.height / 2;
        const dx = x - cx;
        const dy = cy - y;
        const a = (Math.atan2(dy, dx) * 180 / Math.PI + 360) % 360;
        return a;
      }

      if (type === 'height-map' || type === 'contour-lines' || type === 'curvature-profile' || type === 'spectrum' || type === 'waveform' || type === 'time-series' || type === 'amplitude' || type === 'phase') {
        return Math.floor(colorHueAt(x, y, t));
      }

      if (type === 'truth-table' || type === 'circuit-diagram') {
        return 30;
      }

      if (type === 'channel-view' || type === 'layer-stack') {
        const px = sampleImagePixel(x, y);
        if (px) return rgbToHue(px.r, px.g, px.b);
        return 210;
      }

      if (type === 'ascii') {
        const code = 33 + Math.floor((1 - y / sub.height) * 60);
        return (code % 90) / 90 * 360;
      }

      return slopeAngleDeg(x, t, substraitType);
    }

    function drawInteractive() {
      subctx.clearRect(0, 0, sub.width, sub.height);

      // Optional uploaded image background
      if (uploadedImage) {
        const aspect = uploadedImage.width / uploadedImage.height;
        const targetW = sub.width;
        const targetH = targetW / aspect;
        const offsetY = (sub.height - targetH) / 2;
        subctx.globalAlpha = 0.45;
        subctx.drawImage(uploadedImage, 0, offsetY, targetW, targetH);
        subctx.globalAlpha = 1;
      }

      subctx.strokeStyle = 'rgba(255,255,255,0.07)';
      subctx.lineWidth = 1;

      const gridSpacing = spacingForSubstrait(substraitType);

      for (let gx = 0; gx <= sub.width; gx += gridSpacing) {
        subctx.beginPath();
        subctx.moveTo(gx, 0);
        subctx.lineTo(gx, sub.height);
        subctx.stroke();
      }

      for (let gy = 0; gy <= sub.height; gy += gridSpacing) {
        subctx.beginPath();
        subctx.moveTo(0, gy);
        subctx.lineTo(sub.width, gy);
        subctx.stroke();
      }

      // Zero line through center to mark reference (C4)
      subctx.save();
      subctx.beginPath();
      subctx.setLineDash([8, 8]);
      subctx.lineWidth = 2;
      subctx.strokeStyle = 'rgba(0,255,128,0.4)';
      subctx.moveTo(0, sub.height / 2);
      subctx.lineTo(sub.width, sub.height / 2);
      subctx.stroke();
      subctx.restore();

      gridPoints = [];
      // No fitting/normalization: use raw mathematical positions
      fitCenter = 0; fitScale = 1; fitOffset = 0;

      for (let gx = 0; gx <= sub.width; gx += gridSpacing) {
        const y = curveY(gx, t, substraitType);
        const slope = slopeMag(gx, t, substraitType);
        gridPoints.push({ x: gx, y, slope });
      }

      gridPoints.forEach((p) => {
        const depth = Math.min(1, p.slope / 18);
        subctx.beginPath();
        subctx.fillStyle = `rgba(0,0,0,${0.25 * depth})`;
        subctx.ellipse(p.x, p.y + 6, 10, 6, 0, 0, Math.PI * 2);
        subctx.fill();

        subctx.beginPath();
        const hue = lensHue(p.x, p.y, lensType);
        subctx.fillStyle = `hsl(${hue},80%,${50 + depth * 20}%)`;
        subctx.arc(p.x, p.y, 4 + depth * 2, 0, Math.PI * 2);
        subctx.fill();
      });

      // No auto firing; activation only on hover

      updateStoragePanel();

      if (hoverPoint) {
        subctx.beginPath();
        subctx.strokeStyle = '#ffffff';
        subctx.lineWidth = 2;
        subctx.arc(hoverPoint.x, hoverPoint.y, 7, 0, Math.PI * 2);
        subctx.stroke();
      }

      if (rainbowTrail.length) {
        rainbowTrail = rainbowTrail.filter((p) => p.life > 0);
        rainbowTrail.forEach((p) => {
          const alpha = p.life;
          const radius = 10 * p.life + 4;
          subctx.beginPath();
          subctx.fillStyle = `hsla(${p.hue},90%,60%,${alpha})`;
          subctx.arc(p.x, p.y, radius, 0, Math.PI * 2);
          subctx.fill();
          p.life -= 0.012;
        });
      }

      if (colorWake.length) {
        colorWake = colorWake.filter((p) => p.life > 0);
        subctx.lineWidth = 2;
        colorWake.forEach((p, idx) => {
          const alpha = 0.22 * p.life;
          const radius = 3 + 8 * p.life;
          const hue = p.hue;
          const grad = subctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, radius * 1.8);
          grad.addColorStop(0, `hsla(${hue},90%,70%,${alpha})`);
          grad.addColorStop(1, `hsla(${hue},80%,45%,0)`);
          subctx.beginPath();
          subctx.fillStyle = grad;
          subctx.arc(p.x, p.y, radius, 0, Math.PI * 2);
          subctx.fill();

          if (idx > 0) {
            const prev = colorWake[idx - 1];
            subctx.strokeStyle = `hsla(${hue},90%,70%,${alpha * 0.5})`;
            subctx.beginPath();
            subctx.moveTo(prev.x, prev.y);
            subctx.lineTo(p.x, p.y);
            subctx.stroke();
          }

          p.life -= 0.012;
        });
      }

      if (colorRipples.length) {
        colorRipples = colorRipples.filter((r) => r.life > 0);
        colorRipples.forEach((r) => {
          const alpha = 0.18 * r.life;
          const radius = 18 + 120 * (1 - r.life);
          const hue = r.hue;
          const grad = subctx.createRadialGradient(r.x, r.y, radius * 0.2, r.x, r.y, radius);
          grad.addColorStop(0, `hsla(${hue},92%,68%,${alpha})`);
          grad.addColorStop(0.5, `hsla(${hue},85%,52%,${alpha * 0.5})`);
          grad.addColorStop(1, `hsla(${hue},80%,40%,0)`);
          subctx.beginPath();
          subctx.fillStyle = grad;
          subctx.arc(r.x, r.y, radius, 0, Math.PI * 2);
          subctx.fill();
          r.life -= 0.018;
        });
      }

      if (soundRipples.length) {
        soundRipples = soundRipples.filter((r) => r.life > 0);
        soundRipples.forEach((r) => {
          const alpha = r.life * 0.45;
          const radius = r.baseRadius + r.expand * (1 - r.life);
          subctx.strokeStyle = `rgba(255, 184, 108, ${alpha})`;
          subctx.lineWidth = 2;
          subctx.beginPath();
          subctx.arc(r.x, r.y, radius, 0, Math.PI * 2);
          subctx.stroke();
          // secondary faint ring for clarity
          subctx.strokeStyle = `rgba(255, 184, 108, ${alpha * 0.4})`;
          subctx.beginPath();
          subctx.arc(r.x, r.y, radius * 1.1, 0, Math.PI * 2);
          subctx.stroke();
          r.life -= 0.018;
        });
      }

      if (rocketTrail.length) {
        rocketTrail = rocketTrail.filter((r) => r.life > 0);
        rocketTrail.forEach((r) => {
          const alpha = r.life * 0.4;
          const len = 20 * r.life + 10;
          const a = r.angle * Math.PI / 180;
          const x2 = r.x + Math.cos(a) * len;
          const y2 = r.y + Math.sin(a) * len;
          subctx.strokeStyle = `rgba(155,232,255,${alpha})`;
          subctx.lineWidth = 2;
          subctx.beginPath();
          subctx.moveTo(r.x, r.y);
          subctx.lineTo(x2, y2);
          subctx.stroke();
          r.life -= 0.02;
        });
      }

      if (vectorArrow && vectorArrow.life > 0) {
        const a = vectorArrow.angle * Math.PI / 180;
        const len = 42;
        const x1 = vectorArrow.x;
        const y1 = vectorArrow.y;

        subctx.save();
        subctx.translate(x1, y1);
        subctx.rotate(a);

        // Rocket body
        subctx.beginPath();
        subctx.moveTo(-12, -6);
        subctx.lineTo(len, 0);
        subctx.lineTo(-12, 6);
        subctx.closePath();
        subctx.fillStyle = 'rgba(155,232,255,0.9)';
        subctx.fill();

        // Nose highlight
        subctx.beginPath();
        subctx.moveTo(len, 0);
        subctx.lineTo(len - 6, -4);
        subctx.lineTo(len - 6, 4);
        subctx.closePath();
        subctx.fillStyle = 'rgba(255,215,0,0.9)';
        subctx.fill();

        // Flame
        subctx.beginPath();
        subctx.moveTo(-12, -5);
        subctx.lineTo(-22, 0);
        subctx.lineTo(-12, 5);
        subctx.closePath();
        subctx.fillStyle = 'rgba(255,140,0,0.75)';
        subctx.fill();

        subctx.restore();

        vectorArrow.life -= 0.03;
      }

      tickLensBadge(LENSES[substraitType], lensType);
      t += 1.4;
      requestAnimationFrame(drawInteractive);
    }

    subSelect.onchange = () => {
      substraitType = subSelect.value;
      refreshLensOptions(substraitType);
      rainbowTrail = [];
      vectorArrow = null;
      soundRipples = [];
      rocketTrail = [];
      colorRipples = [];
      colorWake = [];
      rebuildImageProfile();
      updateLensSchemaDisplay(substraitType, lensType);
      fetchSubstrateStats(substraitType, lensType);
    };

    lensSelect.onchange = () => {
      lensType = lensSelect.value;
      rainbowTrail = [];
      vectorArrow = null;
      soundRipples = [];
      rocketTrail = [];
      colorRipples = [];
      colorWake = [];
      updateLensSchemaDisplay(substraitType, lensType);
      fetchSubstrateStats(substraitType, lensType);
    };

    if (imageUpload) {
      imageUpload.addEventListener('change', (e) => {
        const file = e.target.files && e.target.files[0];
        if (!file) return;
        uploadedImageBytes = file.size;
        const reader = new FileReader();
        reader.onload = (evt) => {
          const img = new Image();
          img.onload = () => {
            uploadedImage = img;
            rebuildImageProfile();
          };
          img.src = evt.target.result;
        };
        reader.readAsDataURL(file);
      });
    }

    // Ensure audio context is unlocked on first user interaction
    ['pointerdown', 'touchstart', 'click'].forEach((evtName) => {
      window.addEventListener(evtName, resumeAudio, { once: true, capture: true });
    });

    sub.addEventListener('mousemove', (e) => {
      const rect = sub.getBoundingClientRect();
      const mx = (e.clientX - rect.left) * (sub.width / rect.width);
      const my = (e.clientY - rect.top) * (sub.height / rect.height);

      let x = mx;
      let y = my;

      if (gridPoints.length) {
        let best = Infinity;
        gridPoints.forEach((p) => {
          const d2 = (p.x - mx) ** 2 + (p.y - my) ** 2;
          if (d2 < best) {
            best = d2;
            x = p.x;
            y = p.y;
          }
        });
      } else {
        y = curveY(x, t, substraitType);
      }

      hoverPoint = { x, y };

      const lens = lensValue(x, y, lensType);
      const hoverHue = lens.hue ?? lensHue(x, y, lensType);
      const hoverAngle = slopeAngleDeg(x, t, substraitType);
      const xRel = Math.round(x - sub.width / 2);
      const rawY = rawCurveY(x, t, substraitType);
      let extra = '';
      if (substraitType === 'image') {
        const px = sampleImagePixel(x, y);
        if (px) {
          extra = ` | img(x=${px.x}, y=${px.y}, rgb(${px.r},${px.g},${px.b}), ${px.hex})`;
        }
      }
      const subLabel = substraitLabels[substraitType] || substraitType;
      readout.textContent = `${subLabel} • ${lens.text} | rel (x=${xRel}, y0=${rawY.toFixed(2)})${extra}`;
      readout.style.color = lens.color;

      const playableSoundLens = ['sound', 'note', 'tone', 'chord', 'harmonic', 'piano-roll', 'harmonic-lattice'];
      if (playableSoundLens.includes(lensType) && lens.freq) {
        if ((lensType === 'note' || lensType === 'chord' || lensType === 'harmonic') && lens.chord) {
          playChord(lens.chord);
        } else {
          playBeep(lens.freq);
        }
      }

      if (lensType === 'color') {
        const hue = lens.hue ?? lensHue(x, y, lensType);
        rainbowTrail.push({ x, y, hue, life: 1 });
        colorWake.push({ x, y, hue, life: 1 });
        colorRipples.push({ x, y, hue, life: 1 });
        if (rainbowTrail.length > 120) rainbowTrail.shift();
        if (colorWake.length > 90) colorWake.shift();
        if (colorRipples.length > 18) colorRipples.shift();
      }

      if (lensType === 'vector' || lensType === 'angle') {
        const angle = slopeAngleDeg(x, t, substraitType);
        vectorArrow = { x, y, angle, life: 1 };
      }

      if ((lensType === 'sound' || lensType === 'note') && lens.freq) {
        const wavelength = lens.wavelength || (SPEED_OF_SOUND / lens.freq);
        const wavelengthPx = wavelength * PIXELS_PER_METER();
        soundRipples.push({ x, y, baseRadius: 4, expand: Math.max(24, wavelengthPx * 0.5), life: 1 });
        if (soundRipples.length > 40) soundRipples.shift();
      }

      applyHoverEffect(substraitType, lensType, x, y, hoverHue, hoverAngle);
    });

    sub.addEventListener('mouseleave', () => {
      hoverPoint = null;
      scanActive = false;
      scanIndex = 0;
    });

    refreshLensOptions(substraitType);
    updateLensSchemaDisplay(substraitType, lensType);
    fetchSubstrateStats(substraitType, lensType);
    drawInteractive();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
