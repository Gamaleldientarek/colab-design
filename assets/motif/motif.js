/**
 * Colab dither / pixel motif generator.
 *
 * Implements references/layout-archetypes.md §4 — the 20px module (§4.1),
 * the decorrelating integer-hash cell selection (§4.2), computed per-cell
 * density p(u) = a * u^2 with base = 0 for an edge-anchored dissolve
 * (§4.3.1), the per-ground opacity floor (§4.4, enforced by the caller
 * supplying a compliant `opacity`), and marker placement (+  x  o at cell
 * intersections, never adjacent) — plus the poster-specific additions in
 * references/pixel-dither-posters.md §3: grid-past-edge sampling (§3.1)
 * and a field that is exportable as individual module positions rather
 * than a raster gradient standing in for one (§3.2).
 *
 * One engine, any canvas size. `box` and every `exclude` rect are plain
 * {x, y, w, h} in canvas px — the function never reads or assumes a
 * canvas width/height, so the same code renders a field on a 1920x1080
 * slide and on a 2480x3508 A4 poster. Nothing below changed for existing
 * callers unless they opt into a new option (see each option's default).
 *
 * ColabMotif.renderDitherField(container, box, opts)
 *
 *   container  A positioned DOM element (its own or an ancestor's
 *              position:absolute/relative) that filled-cell <div>s and
 *              marker <svg>s are appended to.
 *
 *   box        { x, y, w, h } in canvas px — the field zone. Snapped to
 *              the 20px module grid (§4.1). On a poster this is the fixed
 *              field zone from pixel-dither-posters.md §5/§9 — not the
 *              whole canvas.
 *
 *   opts:
 *     dir             'right' | 'left' | 'top' | 'bottom' |
 *                      'top-right' | 'top-left' |
 *                      'bottom-right' | 'bottom-left'
 *                      Which edge (the four originals — unchanged) or
 *                      corner (four new — for a poster's corner-anchored
 *                      field zone, pixel-dither-posters.md §9.1: "u = 0 at
 *                      the field zone's inner (bottom-left) edge, u = 1
 *                      toward the top-right corner") the field migrates
 *                      toward. A corner value's u is the field's own
 *                      construction rule generalised to two axes: radial
 *                      (Euclidean) distance from the sparse corner,
 *                      normalised by the (possibly extended) diagonal —
 *                      layout-archetypes.md §4.3.1 only derives the
 *                      single-axis form, so this is this engine's
 *                      documented extension of it, not a separately
 *                      ratified rule. Default 'right'.
 *     a               Explicit peak coefficient for p(u) = a * u^2
 *                      (§4.3.1, base = 0). The poster spec uses a = 0.70
 *                      (pixel-dither-posters.md §3, §9.1/§9.2). If
 *                      omitted, derived from targetFill (unchanged legacy
 *                      behaviour): a = 3 * targetFill.
 *     targetFill      Mean fill fraction used to derive `a` when `a` is
 *                      not given directly. Default 0.18 (unchanged).
 *     extendPastEdge  Fraction, 0.2-0.5 (pixel-dither-posters.md §3.1).
 *                      Extends the notional sampling grid past the dense
 *                      edge/corner by this fraction of the field's own
 *                      span before u is computed, so u = 1 falls outside
 *                      the rendered box and the visible edge still reads
 *                      as climbing rather than capped. Default 0 — exactly
 *                      the original, un-extended math, so no existing
 *                      field changes unless it opts in.
 *     color           One hex colour for the whole field. One colour per
 *                      instance (SKILL.md, layout-archetypes.md §4).
 *     opacity         Composite alpha. The caller supplies a value that
 *                      clears the per-ground floor: 40% on Deep Jade,
 *                      50% on Pine (layout-archetypes.md §4.4,
 *                      pixel-dither-posters.md §7) — this function does
 *                      not compute or enforce the floor itself. Default
 *                      0.6.
 *     seed            Decorrelates independent fields that share a canvas
 *                      or a template (e.g. the EN and AR re-solve of the
 *                      same poster).
 *     markers         false disables all markers. Otherwise the legacy
 *                      multi-marker slide behaviour applies (~1 marker per
 *                      `markerEvery` filled cells, never 8-neighbour
 *                      adjacent) unless `maxMarkers` is set. Default true
 *                      (unchanged).
 *     markerEvery     Legacy multi-marker density, used only when
 *                      `maxMarkers` is not set. Default 10 (unchanged).
 *     maxMarkers      Caps the field to at most this many markers total,
 *                      chosen deterministically — nearest the dense
 *                      edge/corner first, never adjacent — instead of
 *                      probabilistically. This is the poster template's
 *                      "exactly one accent marker, near the field's
 *                      densest corner" (pixel-dither-posters.md §4 item 3,
 *                      §9.1). Unset by default, so every existing slide
 *                      field keeps the untouched probabilistic behaviour.
 *     markerShape     'plus' | 'cross' | 'ring' — forces every marker in
 *                      this field to one glyph instead of the legacy
 *                      per-marker hash-bucketed pick (still the default
 *                      when unset). Poster examples specify an exact glyph
 *                      per instance (pixel-dither-posters.md §9.1's "one
 *                      o ring", §9.4's "one x"), which the original
 *                      random pick could not guarantee.
 *     exclude         Array of {x, y, w, h} in canvas px (e.g. a text
 *                      node's ink box) to keep clear of the field — the
 *                      §4.6 keep-out zone.
 *     excludePad      Padding added to every exclude rect, in px. Default
 *                      40 (2 modules).
 *
 *   Returns { cells, of, fill, modules, markers }:
 *     cells    Count of filled cells (plain + marker).
 *     of       Total candidate cells in the box (cols * rows).
 *     fill     cells / of.
 *     modules  Array of every filled cell's { x, y } canvas px (plain and
 *               marker cells both) — the pixel-dither-posters.md §3.2
 *               requirement that a poster field be "exportable as a list
 *               of individual module positions", not a raster gradient
 *               standing in for one.
 *     markers  Array of { x, y } canvas px for the marker subset of
 *               `modules`.
 */
(function (global) {
  const M = 20; // base module, per layout-archetypes.md §4.1

  // Avalanche hash, decorrelated in both axes. Never Math.random() — the
  // field must be reproducible. Exact function from layout-archetypes.md §4.2.
  function hash2(x, y) {
    let h = (x * 374761393 + y * 668265263) | 0;
    h = ((h ^ (h >>> 13)) * 1274126177) | 0;
    return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
  }

  // u = 0 at the field's sparse boundary, u = 1 at its dense edge/corner.
  // `ext` (extendPastEdge) pushes u = 1 past the box, per §3.1. Reduces
  // exactly to the original single-axis formulas when ext = 0.
  function computeU(c, r, cols, rows, dir, ext) {
    const singleCol = cols <= 1;
    const singleRow = rows <= 1;
    let dist, span;
    switch (dir) {
      case 'left':
        if (singleCol) return 1;
        dist = (cols - 1) - c; span = cols - 1; break;
      case 'top':
        if (singleRow) return 1;
        dist = (rows - 1) - r; span = rows - 1; break;
      case 'bottom':
        if (singleRow) return 1;
        dist = r; span = rows - 1; break;
      case 'top-right':
      case 'top-left':
      case 'bottom-right':
      case 'bottom-left': {
        if (singleCol && singleRow) return 1;
        let dx, dy;
        if (dir === 'top-right') { dx = c; dy = (rows - 1) - r; }
        else if (dir === 'top-left') { dx = (cols - 1) - c; dy = (rows - 1) - r; }
        else if (dir === 'bottom-right') { dx = c; dy = r; }
        else { dx = (cols - 1) - c; dy = r; } // 'bottom-left'
        dist = Math.sqrt(dx * dx + dy * dy);
        span = Math.sqrt((cols - 1) * (cols - 1) + (rows - 1) * (rows - 1));
        break;
      }
      case 'right':
      default:
        if (singleCol) return 1;
        dist = c; span = cols - 1; break;
    }
    if (span <= 0) return 1;
    const extendedSpan = span * (1 + (ext || 0));
    return Math.min(1, dist / extendedSpan);
  }

  function renderDitherField(container, box, opts) {
    const x0 = Math.round(box.x / M) * M;
    const y0 = Math.round(box.y / M) * M;
    const cols = Math.max(1, Math.round(box.w / M));
    const rows = Math.max(1, Math.round(box.h / M));
    const a = opts.a != null ? opts.a : 3 * (opts.targetFill != null ? opts.targetFill : 0.18);
    const dir = opts.dir || 'right';
    const ext = opts.extendPastEdge || 0;
    const seed = (opts.seed || 0) * 7919;
    const markerEvery = opts.markers === false ? Infinity : (opts.markerEvery || 10);
    const maxMarkers = opts.markers === false ? 0 : opts.maxMarkers;
    const color = opts.color;
    const opacity = opts.opacity != null ? opts.opacity : 0.6;
    const excludePad = opts.excludePad != null ? opts.excludePad : 40;
    const excludes = (opts.exclude || []).map(function (ex) {
      return { x0: ex.x - excludePad, y0: ex.y - excludePad, x1: ex.x + ex.w + excludePad, y1: ex.y + ex.h + excludePad };
    });

    function blocked(px, py) {
      for (const ex of excludes) {
        if (px < ex.x1 && px + M > ex.x0 && py < ex.y1 && py + M > ex.y0) return true;
      }
      return false;
    }

    const filled = []; // {c, r, u}
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const px = x0 + c * M, py = y0 + r * M;
        if (blocked(px, py)) continue; // keep-out zone — never a candidate, not just unlucky
        const u = computeU(c, r, cols, rows, dir, ext);
        const p = Math.min(1, a * u * u); // p(u) = a * u^2, base = 0 (§4.3.1)
        const hv = hash2(c + seed, r + seed);
        if (hv < p) filled.push({ c, r, u });
      }
    }

    // Marker selection. Two modes:
    //  - maxMarkers set: deterministic, nearest the dense edge/corner
    //    first, never 8-neighbour adjacent to a chosen marker. The poster
    //    template's "exactly one accent marker" (pixel-dither-posters.md
    //    §4 item 3).
    //  - maxMarkers unset: legacy per-cell probabilistic pick from an
    //    independent hash, unchanged from the original engine.
    const markerSet = new Set();
    function isAdjacent(c, r) {
      for (let dr = -1; dr <= 1; dr++) {
        for (let dc = -1; dc <= 1; dc++) {
          if (dr === 0 && dc === 0) continue;
          if (markerSet.has((c + dc) + ',' + (r + dr))) return true;
        }
      }
      return false;
    }
    if (maxMarkers != null) {
      const byDensity = filled.slice().sort((p, q) => q.u - p.u); // densest first
      for (const f of byDensity) {
        if (markerSet.size >= maxMarkers) break;
        if (!isAdjacent(f.c, f.r)) markerSet.add(f.c + ',' + f.r);
      }
    } else {
      for (const f of filled) {
        const hv2 = hash2(f.c * 92821 + seed, f.r * 68917 + seed);
        if (hv2 < 1 / markerEvery && !isAdjacent(f.c, f.r)) {
          markerSet.add(f.c + ',' + f.r);
        }
      }
    }

    const frag = document.createDocumentFragment();
    const modules = [];
    const markers = [];
    for (const f of filled) {
      const px = x0 + f.c * M, py = y0 + f.r * M;
      const key = f.c + ',' + f.r;
      modules.push({ x: px, y: py });
      if (markerSet.has(key)) {
        markers.push({ x: px, y: py });
        const shape = opts.markerShape || pickMarkerShape(hash2(f.c * 5 + seed, f.r * 13 + seed));
        frag.appendChild(makeMarker(px, py, color, opacity, shape));
      } else {
        frag.appendChild(makeSquare(px, py, color, opacity));
      }
    }
    container.appendChild(frag);
    return { cells: filled.length, of: cols * rows, fill: filled.length / (cols * rows), modules, markers };
  }

  function makeSquare(x, y, color, opacity) {
    const d = document.createElement('div');
    d.className = 'motif-cell';
    d.style.cssText = `position:absolute;left:${x}px;top:${y}px;width:${M}px;height:${M}px;background:${color};opacity:${opacity};`;
    return d;
  }

  // Unchanged 0.34 / 0.67 thresholds from the original hash-bucketed pick —
  // kept as a function so an explicit `markerShape` option (new) can bypass
  // it deterministically without changing the default random distribution.
  function pickMarkerShape(r) {
    if (r < 0.34) return 'plus';
    if (r < 0.67) return 'cross';
    return 'ring';
  }

  function makeMarker(x, y, color, opacity, shape) {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', M);
    svg.setAttribute('height', M);
    svg.style.cssText = `position:absolute;left:${x}px;top:${y}px;opacity:${opacity};`;
    const s = M;
    if (shape === 'plus') {
      svg.innerHTML = `<rect x="${s * 0.42}" y="${s * 0.08}" width="${s * 0.16}" height="${s * 0.84}" fill="${color}"/><rect x="${s * 0.08}" y="${s * 0.42}" width="${s * 0.84}" height="${s * 0.16}" fill="${color}"/>`;
    } else if (shape === 'cross') {
      svg.innerHTML = `<line x1="${s * 0.14}" y1="${s * 0.14}" x2="${s * 0.86}" y2="${s * 0.86}" stroke="${color}" stroke-width="${s * 0.14}"/><line x1="${s * 0.86}" y1="${s * 0.14}" x2="${s * 0.14}" y2="${s * 0.86}" stroke="${color}" stroke-width="${s * 0.14}"/>`;
    } else {
      svg.innerHTML = `<circle cx="${s / 2}" cy="${s / 2}" r="${s * 0.30}" fill="none" stroke="${color}" stroke-width="${s * 0.15}"/>`;
    }
    return svg;
  }

  global.ColabMotif = { hash2, renderDitherField, MODULE: M };
})(window);
