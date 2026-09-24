/**
 * Colab dither / pixel motif generator.
 * Implements references/layout-archetypes.md §4: 20px module, decorrelating
 * integer-hash cell selection, computed per-cell density (never hand-placed),
 * edge-anchored dissolve p(u) = a * u^2 (§4.3.1, base = 0), one colour per
 * instance, markers (+ x o) at ~1-per-8..12 filled cells, never adjacent.
 */
(function (global) {
  const M = 20; // base module, per §4.1

  // Avalanche hash, decorrelated in both axes. Never Math.random() — the
  // field must be reproducible. Exact function from layout-archetypes.md §4.2.
  function hash2(x, y) {
    let h = (x * 374761393 + y * 668265263) | 0;
    h = ((h ^ (h >>> 13)) * 1274126177) | 0;
    return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
  }

  /**
   * Render an edge-anchored dissolve field into `container` (a positioned
   * element). `box` is in canvas px, snapped to the 20px module.
   *
   * opts:
   *   dir        'right' | 'left' | 'top' | 'bottom'  — which side of the
   *              box is the dense / outer edge the field migrates toward.
   *   targetFill  mean fill fraction used to derive `a` (a = 3 * targetFill),
   *              per slide-library.md §3 construction note.
   *   color      one hex colour for the whole field (one colour per instance).
   *   opacity    composite alpha; caller supplies a value clearing the
   *              per-ground floor in token-system.md §4.4 / layout-archetypes §4.4.
   *   seed       decorrelates independent fields on the same slide.
   *   markers    false to disable; otherwise ~1 marker per `markerEvery` filled cells.
   *   exclude    array of {x,y,w,h} in canvas px (e.g. a text node's ink box) to
   *              keep clear of the field. Per §4.6, each is padded by `excludePad`
   *              (default 40px — 2 modules) before cells are blocked, so "never
   *              under text" is enforced by construction, not by eye.
   *   excludePad padding added to every exclude rect, in px (default 40).
   */
  function renderDitherField(container, box, opts) {
    const x0 = Math.round(box.x / M) * M;
    const y0 = Math.round(box.y / M) * M;
    const cols = Math.max(1, Math.round(box.w / M));
    const rows = Math.max(1, Math.round(box.h / M));
    const a = opts.a != null ? opts.a : 3 * (opts.targetFill != null ? opts.targetFill : 0.18);
    const dir = opts.dir || 'right';
    const seed = (opts.seed || 0) * 7919;
    const markerEvery = opts.markers === false ? Infinity : (opts.markerEvery || 10);
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

    const filled = [];
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const px = x0 + c * M, py = y0 + r * M;
        if (blocked(px, py)) continue; // keep-out zone — never a candidate, not just unlucky
        let u;
        if (dir === 'right') u = cols > 1 ? c / (cols - 1) : 1;
        else if (dir === 'left') u = cols > 1 ? 1 - c / (cols - 1) : 1;
        else if (dir === 'bottom') u = rows > 1 ? r / (rows - 1) : 1;
        else u = rows > 1 ? 1 - r / (rows - 1) : 1; // 'top'
        const p = Math.min(1, a * u * u); // p(u) = a * u^2, base = 0 (§4.3.1)
        const hv = hash2(c + seed, r + seed);
        if (hv < p) filled.push([c, r]);
      }
    }

    // Second pass: pick markers, never adjacent (8-neighbour), from an
    // independent hash so marker choice doesn't correlate with fill choice.
    const filledSet = new Set(filled.map(([c, r]) => c + ',' + r));
    const markerSet = new Set();
    for (const [c, r] of filled) {
      const hv2 = hash2(c * 92821 + seed, r * 68917 + seed);
      if (hv2 < 1 / markerEvery) {
        let adjacent = false;
        for (let dr = -1; dr <= 1 && !adjacent; dr++) {
          for (let dc = -1; dc <= 1; dc++) {
            if (dr === 0 && dc === 0) continue;
            if (markerSet.has((c + dc) + ',' + (r + dr))) { adjacent = true; break; }
          }
        }
        if (!adjacent) markerSet.add(c + ',' + r);
      }
    }

    const frag = document.createDocumentFragment();
    for (const [c, r] of filled) {
      const px = x0 + c * M, py = y0 + r * M;
      const key = c + ',' + r;
      if (markerSet.has(key)) {
        frag.appendChild(makeMarker(px, py, color, opacity, hash2(c * 5 + seed, r * 13 + seed)));
      } else {
        frag.appendChild(makeSquare(px, py, color, opacity));
      }
    }
    container.appendChild(frag);
    return { cells: filled.length, of: cols * rows, fill: filled.length / (cols * rows) };
  }

  function makeSquare(x, y, color, opacity) {
    const d = document.createElement('div');
    d.className = 'motif-cell';
    d.style.cssText = `position:absolute;left:${x}px;top:${y}px;width:${M}px;height:${M}px;background:${color};opacity:${opacity};`;
    return d;
  }

  function makeMarker(x, y, color, opacity, r) {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', M);
    svg.setAttribute('height', M);
    svg.style.cssText = `position:absolute;left:${x}px;top:${y}px;opacity:${opacity};`;
    const s = M;
    if (r < 0.34) {
      svg.innerHTML = `<rect x="${s * 0.42}" y="${s * 0.08}" width="${s * 0.16}" height="${s * 0.84}" fill="${color}"/><rect x="${s * 0.08}" y="${s * 0.42}" width="${s * 0.84}" height="${s * 0.16}" fill="${color}"/>`;
    } else if (r < 0.67) {
      svg.innerHTML = `<line x1="${s * 0.14}" y1="${s * 0.14}" x2="${s * 0.86}" y2="${s * 0.86}" stroke="${color}" stroke-width="${s * 0.14}"/><line x1="${s * 0.86}" y1="${s * 0.14}" x2="${s * 0.14}" y2="${s * 0.86}" stroke="${color}" stroke-width="${s * 0.14}"/>`;
    } else {
      svg.innerHTML = `<circle cx="${s / 2}" cy="${s / 2}" r="${s * 0.30}" fill="none" stroke="${color}" stroke-width="${s * 0.15}"/>`;
    }
    return svg;
  }

  global.ColabMotif = { hash2, renderDitherField, MODULE: M };
})(window);
