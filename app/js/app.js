import { LENSA, LEGENDA } from './config.js';

const state = {
  activeSet: new Set(),
  layers: {},
  customLayers: {},
  desaIndex: null,
  customSeq: 0,
};
const loadingEl = document.getElementById('loading');
const infoContent = document.getElementById('info-content');
const infoPanel = document.getElementById('info-panel');

// ── Map init ──
const map = new maplibregl.Map({
  container: 'peta',
  style: {
    version: 8,
    sources: {
      osm: {
        type: 'raster',
        tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
        tileSize: 256,
        attribution: '&copy; <a href="https://openstreetmap.org">OSM</a>',
      },
    },
    layers: [
      { id: 'osm-layer', type: 'raster', source: 'osm', minzoom: 0, maxzoom: 19 },
    ],
  },
  center: [106.15, -6.15],
  zoom: 11,
  attributionControl: false,
});

map.addControl(new maplibregl.NavigationControl(), 'bottom-right');

// ── Loading ──
function setLoading(v) {
  loadingEl.classList.toggle('hidden', !v);
  loadingEl.querySelector('span').textContent = v ? 'Memuat data…' : 'Selesai';
}

// ── Generate nav from config ──
function buildNav() {
  const nav = document.getElementById('lensa-nav');
  nav.innerHTML = '';
  for (const [id, cfg] of Object.entries(LENSA)) {
    const btn = document.createElement('button');
    btn.className = 'lensa-btn';
    btn.dataset.lensa = id;
    btn.setAttribute('aria-pressed', 'false');
    btn.innerHTML = `<span class="icon" aria-hidden="true">${cfg.icon || ''}</span><span class="label">${cfg.label}</span>`;
    btn.addEventListener('click', () => toggleLensa(id));
    nav.appendChild(btn);
  }
}

// ── Toggle ──
async function toggleLensa(id) {
  const on = !state.activeSet.has(id);
  const lensa = LENSA[id];
  if (!lensa) return;

  if (on) {
    state.activeSet.add(id);
  } else {
    state.activeSet.delete(id);
  }

  if (!state.layers[id]) {
    setLoading(true);
    state.layers[id] = [];
    const promises = lensa.layers.map((l) => loadLayer(id, l));
    await Promise.all(promises);
    setLoading(false);
  }

  const vis = on ? 'visible' : 'none';
  for (const lyrId of state.layers[id] || []) {
    if (map.getLayer(lyrId)) map.setLayoutProperty(lyrId, 'visibility', vis);
  }

  updateButtons();
  updateLegend();
  updateUrl();
}

// ── Load single layer ──
async function loadLayer(lensaId, cfg) {
  const srcId = `src-${cfg.id}`;
  const layerId = `lyr-${cfg.id}`;
  if (map.getLayer(layerId)) return;

  try {
    const resp = await fetch(cfg.file);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();
    map.addSource(srcId, { type: 'geojson', data });
    const paint = JSON.parse(JSON.stringify(cfg.paint));
    map.addLayer({
      id: layerId,
      type: cfg.type,
      source: srcId,
      paint,
      layout: cfg.type === 'line' && cfg.paint['line-dasharray']
        ? { 'line-dasharray': cfg.paint['line-dasharray'] }
        : {},
    });

    if (cfg.popup && cfg.popup.length) {
      map.on('click', layerId, (e) => {
        if (!e.features?.[0]) return;
        const props = e.features[0].properties;
        let html = `<h3>${props[cfg.popup[0]] || '(tanpa nama)'}</h3><table>`;
        for (const k of cfg.popup.slice(0, 6)) {
          if (props[k]) html += `<tr><td>${k}</td><td>${props[k]}</td></tr>`;
        }
        html += '</table>';
        infoContent.innerHTML = html;
        infoPanel.classList.remove('hidden');
      });
      map.on('mouseenter', layerId, () => { map.getCanvas().style.cursor = 'pointer'; });
      map.on('mouseleave', layerId, () => { map.getCanvas().style.cursor = ''; });
    }

    state.layers[lensaId] = state.layers[lensaId] || [];
    state.layers[lensaId].push(layerId);
  } catch (err) {
    console.warn(`Gagal muat ${cfg.id}: ${err.message}`);
    if (!state.layers[lensaId]?.length) {
      infoContent.innerHTML =
        '<h3>Gagal memuat data</h3><p style="color:var(--text2)">Terjadi kesalahan. Coba refresh.</p>';
      infoPanel.classList.remove('hidden');
    }
  }
}

// ── UI state ──
function updateButtons() {
  document.querySelectorAll('.lensa-btn').forEach((btn) => {
    const id = btn.dataset.lensa;
    const on = state.activeSet.has(id);
    btn.classList.toggle('active', on);
    btn.setAttribute('aria-pressed', on);
  });
}

function updateLegend() {
  const el = document.getElementById('legenda');
  const parts = [];
  for (const id of state.activeSet) {
    const items = LEGENDA[id];
    const label = LENSA[id]?.label;
    if (items && label) {
      parts.push(`<h3>${label}</h3>`);
      for (const l of items) {
        parts.push(
          `<div class="legend-item"><span style="display:inline-block;width:12px;height:12px;border-radius:3px;background:${l.color};flex-shrink:0"></span>${l.label}</div>`,
        );
      }
    }
  }
  el.innerHTML = parts.join('');
}

// ── Custom layers ──

async function addCustomLayer(url) {
  // validate URL
  let parsed;
  try {
    parsed = new URL(url);
  } catch {
    alert('URL tidak valid. Masukkan URL GeoJSON publik yang valid.');
    return;
  }
  if (!parsed.protocol.startsWith('http')) {
    alert('Hanya URL HTTP/HTTPS yang didukung.');
    return;
  }

  setLoading(true);
  let resp;
  try {
    resp = await fetch(url, { signal: AbortSignal.timeout(30000) });
  } catch (err) {
    setLoading(false);
    if (err.name === 'AbortError') {
      alert('Waktu habis. Server terlalu lambat.');
    } else {
      alert('Gagal menjangkau URL. Periksa koneksi atau CORS.');
    }
    return;
  }
  if (!resp.ok) {
    setLoading(false);
    alert(`Server merespon dengan kode ${resp.status} ${resp.statusText}.`);
    return;
  }

  // size check
  const cLen = resp.headers.get('Content-Length');
  if (cLen && parseInt(cLen) > 50 * 1024 * 1024) {
    setLoading(false);
    alert('File terlalu besar (maks 50MB).');
    return;
  }

  let data;
  try {
    data = await resp.json();
  } catch {
    setLoading(false);
    alert('Respon bukan JSON valid. Pastikan URL mengarah ke file GeoJSON.');
    return;
  }

  // validate GeoJSON
  if (!data.type || !data.features) {
    setLoading(false);
    alert('Data bukan GeoJSON FeatureCollection yang valid.');
    return;
  }
  if (!data.features.length) {
    setLoading(false);
    alert('GeoJSON kosong (tidak memiliki fitur).');
    return;
  }
  if (data.features.length > 50000) {
    setLoading(false);
    alert('Terlalu banyak fitur (maks 50.000).');
    return;
  }

  // detect geometry type
  const types = new Set();
  for (const f of data.features) {
    if (f.geometry) types.add(f.geometry.type.replace(/^Multi/, ''));
  }
  const baseType = types.has('Polygon')
    ? 'fill'
    : types.has('LineString')
      ? 'line'
      : types.has('Point')
        ? 'circle'
        : 'fill';
  const color = '#3b82f6';
  const opacity = 0.5;

  const seq = ++state.customSeq;
  const id = `custom-${seq}`;
  const srcId = `src-${id}`;
  const outlineId = `${id}-outline`;

  map.addSource(srcId, { type: 'geojson', data });

  const layerOpts = {
    id,
    source: srcId,
    paint:
      baseType === 'fill'
        ? { 'fill-color': color, 'fill-opacity': opacity }
        : baseType === 'line'
          ? { 'line-color': color, 'line-width': 2, 'line-opacity': opacity }
          : { 'circle-color': color, 'circle-radius': 6, 'circle-opacity': opacity },
  };
  if (baseType === 'fill') {
    layerOpts.type = 'fill';
    map.addLayer(layerOpts);
    map.addLayer({
      id: outlineId,
      type: 'line',
      source: srcId,
      paint: { 'line-color': '#1e3a5f', 'line-width': 1 },
    });
  } else if (baseType === 'line') {
    layerOpts.type = 'line';
    map.addLayer(layerOpts);
  } else {
    layerOpts.type = 'circle';
    map.addLayer(layerOpts);
  }

  // derive name
  const name = new URL(url).pathname.split('/').pop() || url.slice(0, 40);

  state.customLayers[id] = {
    url,
    name,
    color,
    opacity,
    visible: true,
    baseType,
    outlineId: baseType === 'fill' ? outlineId : null,
  };

  // zoom to
  try {
    const bounds = new maplibregl.LngLatBounds();
    for (const f of data.features) {
      if (f.geometry?.type === 'Point') {
        bounds.extend(f.geometry.coordinates);
      } else if (f.geometry?.type === 'MultiPoint') {
        for (const c of f.geometry.coordinates) bounds.extend(c);
      } else if (f.geometry?.coordinates) {
        _walkCoords(f.geometry.coordinates, bounds);
      }
    }
    if (!bounds.isEmpty()) {
      map.fitBounds(bounds, { padding: 60, maxZoom: 14 });
    }
  } catch { /* skip fit */ }

  setLoading(false);
  renderCustomLayerUI(id);
  updateUrl();
}

function _walkCoords(coords, bounds) {
  if (typeof coords[0] === 'number') {
    bounds.extend(coords);
  } else if (Array.isArray(coords)) {
    for (const c of coords) _walkCoords(c, bounds);
  }
}

function renderCustomLayerUI(id) {
  const list = document.getElementById('custom-list');
  const layer = state.customLayers[id];
  if (!layer) return;

  const div = document.createElement('div');
  div.className = 'custom-item';
  div.dataset.id = id;
  div.innerHTML = `
    <div class="custom-item-header">
      <input type="checkbox" checked aria-label="Tampilkan layer">
      <span class="custom-item-name" title="${layer.name}">${layer.name}</span>
    </div>
    <div class="custom-controls">
      <input type="color" value="${layer.color}" aria-label="Warna">
      <input type="range" min="0" max="1" step="0.05" value="${layer.opacity}" aria-label="Opacity">
      <button class="custom-zoom" aria-label="Zoom ke layer" title="Zoom">&#x1F50D;</button>
      <button class="custom-remove" aria-label="Hapus layer" title="Hapus">&times;</button>
    </div>
  `;

  const cb = div.querySelector('input[type="checkbox"]');
  cb.addEventListener('change', () => toggleCustomLayer(id, cb.checked));

  const cp = div.querySelector('input[type="color"]');
  cp.addEventListener('input', () => colorCustomLayer(id, cp.value));

  const range = div.querySelector('input[type="range"]');
  range.addEventListener('input', () => opacityCustomLayer(id, parseFloat(range.value)));

  div.querySelector('.custom-zoom').addEventListener('click', () => zoomCustomLayer(id));
  div.querySelector('.custom-remove').addEventListener('click', () => removeCustomLayer(id));

  list.appendChild(div);
}

function toggleCustomLayer(id, vis) {
  const layer = state.customLayers[id];
  if (!layer) return;
  layer.visible = vis;
  const v = vis ? 'visible' : 'none';
  if (map.getLayer(id)) map.setLayoutProperty(id, 'visibility', v);
  if (layer.outlineId && map.getLayer(layer.outlineId)) {
    map.setLayoutProperty(layer.outlineId, 'visibility', v);
  }
  updateUrl();
}

function colorCustomLayer(id, color) {
  const layer = state.customLayers[id];
  if (!layer) return;
  layer.color = color;
  const paint =
    layer.baseType === 'fill'
      ? { 'fill-color': color, 'fill-opacity': layer.opacity }
      : layer.baseType === 'line'
        ? { 'line-color': color, 'line-width': 2, 'line-opacity': layer.opacity }
        : { 'circle-color': color, 'circle-radius': 6, 'circle-opacity': layer.opacity };
  if (map.getLayer(id)) map.setPaintProperty(id, Object.keys(paint)[0], Object.values(paint)[0]);
  updateUrl();
}

function opacityCustomLayer(id, opacity) {
  const layer = state.customLayers[id];
  if (!layer) return;
  layer.opacity = opacity;
  const key = layer.baseType === 'fill' ? 'fill-opacity' : layer.baseType === 'line' ? 'line-opacity' : 'circle-opacity';
  if (map.getLayer(id)) map.setPaintProperty(id, key, opacity);
  updateUrl();
}

function zoomCustomLayer(id) {
  const srcId = `src-${id}`;
  const src = map.getSource(srcId);
  if (!src) return;
  try {
    const data = src._data || src.serialize();
    const bounds = new maplibregl.LngLatBounds();
    if (data.features) {
      for (const f of data.features) {
        if (f.geometry?.type === 'Point') {
          bounds.extend(f.geometry.coordinates);
        } else if (f.geometry?.coordinates) {
          _walkCoords(f.geometry.coordinates, bounds);
        }
      }
    }
    if (!bounds.isEmpty()) map.fitBounds(bounds, { padding: 60, maxZoom: 16 });
  } catch { /* skip */ }
}

function removeCustomLayer(id) {
  const layer = state.customLayers[id];
  if (!layer) return;
  const srcId = `src-${id}`;
  try {
    if (map.getLayer(id)) map.removeLayer(id);
    if (layer.outlineId && map.getLayer(layer.outlineId)) map.removeLayer(layer.outlineId);
    if (map.getSource(srcId)) map.removeSource(srcId);
  } catch { /* cleanup */ }
  delete state.customLayers[id];

  const el = document.querySelector(`.custom-item[data-id="${id}"]`);
  if (el) el.remove();

  updateUrl();
}

// URL serialization
function serializeCustom() {
  const arr = [];
  for (const layer of Object.values(state.customLayers)) {
    arr.push({
      u: layer.url,
      c: layer.color,
      o: layer.opacity,
      v: layer.visible,
    });
  }
  return arr.length ? JSON.stringify(arr) : '';
}

function deserializeCustom(str) {
  if (!str) return;
  let list;
  try {
    list = JSON.parse(str);
  } catch {
    return;
  }
  if (!Array.isArray(list)) return;
  for (const item of list) {
    if (!item.u) continue;
    addCustomLayer(item.u).then(() => {
      // apply persisted style after add
      const layers = Object.entries(state.customLayers);
      const added = layers[layers.length - 1];
      if (added) {
        const [id, layer] = added;
        if (item.c && item.c !== '#3b82f6') {
          layer.color = item.c;
          colorCustomLayer(id, item.c);
        }
        if (item.o !== undefined && item.o !== 0.5) {
          layer.opacity = item.o;
          opacityCustomLayer(id, item.o);
        }
        if (item.v === false) {
          layer.visible = false;
          toggleCustomLayer(id, false);
          const cb = document.querySelector(`.custom-item[data-id="${id}"] input[type="checkbox"]`);
          if (cb) cb.checked = false;
        }
      }
    });
  }
}

// ── Share ──
document.getElementById('btn-share').addEventListener('click', async () => {
  const url = window.location.href;
  try {
    await navigator.clipboard.writeText(url);
    const btn = document.getElementById('btn-share');
    btn.textContent = '✓';
    setTimeout(() => { btn.textContent = '🔗'; }, 2000);
  } catch {
    prompt('Salin tautan ini:', url);
  }
});

// ── URL state ──
function updateUrl() {
  const center = map.getCenter();
  const url = new URL(window.location);

  // lensa state
  const activeArr = [...state.activeSet];
  url.searchParams.set('lensa', activeArr.join(','));

  url.searchParams.set('lat', center.lat.toFixed(4));
  url.searchParams.set('lng', center.lng.toFixed(4));
  url.searchParams.set('zoom', map.getZoom().toFixed(1));

  // custom layers
  const customStr = serializeCustom();
  if (customStr) {
    url.searchParams.set('custom', customStr);
  } else {
    url.searchParams.delete('custom');
  }

  window.history.replaceState({}, '', url);
}

map.on('moveend', updateUrl);
map.on('styledata', updateUrl);

// ── Info panel close ──
document.getElementById('info-tutup').addEventListener('click', () => {
  infoPanel.classList.add('hidden');
});

// ── Search (generic, no hardcoded region ref) ──
const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');
let searchTimeout;

async function initSearch() {
  try {
    const resp = await fetch('data/desa_index.json');
    if (resp.ok) {
      state.desaIndex = await resp.json();
      searchInput.placeholder = 'Cari desa/kecamatan…';
    }
  } catch {
    // search unavailable, degrade gracefully
  }
}

searchInput.addEventListener('input', () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    const q = searchInput.value.trim().toLowerCase();
    if (!q || q.length < 2 || !state.desaIndex) {
      searchResults.classList.add('hidden');
      return;
    }
    const matches = state.desaIndex
      .filter((d) => d.nama.toLowerCase().includes(q) || d.kecamatan.toLowerCase().includes(q))
      .slice(0, 20);

    if (!matches.length) {
      searchResults.innerHTML = '<div class="search-empty">Tidak ditemukan</div>';
      searchResults.classList.remove('hidden');
      return;
    }
    searchResults.innerHTML = matches
      .map(
        (d) =>
          `<div class="search-item" data-lat="${d.lat}" data-lng="${d.lng}">
            ${d.nama}<span class="kec">${d.kecamatan}</span>
          </div>`,
      )
      .join('');
    searchResults.classList.remove('hidden');

    searchResults.querySelectorAll('.search-item').forEach((el) => {
      el.addEventListener('click', () => {
        map.flyTo({ center: [parseFloat(el.dataset.lng), parseFloat(el.dataset.lat)], zoom: 14 });
        searchResults.classList.add('hidden');
        searchInput.value = el.childNodes[0].textContent.trim();
      });
    });
  }, 200);
});

document.addEventListener('click', (e) => {
  if (!e.target.closest('#search-box')) searchResults.classList.add('hidden');
});

// ── Custom add button ──
document.getElementById('custom-add').addEventListener('click', () => {
  const url = document.getElementById('custom-url').value.trim();
  if (!url) return;
  addCustomLayer(url);
  document.getElementById('custom-url').value = '';
});

document.getElementById('custom-url').addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    document.getElementById('custom-add').click();
  }
});

// ── Init from URL ──
const params = new URLSearchParams(window.location.search);
const initLensaParam = params.get('lensa') || '';
const initLat = parseFloat(params.get('lat')) || -6.15;
const initLng = parseFloat(params.get('lng')) || 106.15;
const initZoom = parseFloat(params.get('zoom')) || 11;
const initCustom = params.get('custom') || '';

map.setCenter([initLng, initLat]);
map.setZoom(initZoom);

map.on('load', () => {
  buildNav();
  // activate initial lensa
  const ids = initLensaParam ? initLensaParam.split(',').filter((id) => LENSA[id]) : [];
  if (ids.length) {
    Promise.all(ids.map((id) => toggleLensa(id)));
  } else {
    // first lensa as default
    const firstId = Object.keys(LENSA)[0];
    if (firstId) toggleLensa(firstId);
  }
  initSearch();
  // restore custom layers from URL
  if (initCustom) deserializeCustom(initCustom);
});
