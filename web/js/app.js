import { LENSA, LEGENDA } from './config.js';

const state = { active: 'dasar', layers: {}, desaIndex: null };
const loadingEl = document.getElementById('loading');
const infoContent = document.getElementById('info-content');
const infoPanel = document.getElementById('info-panel');

// Init map
const map = new maplibregl.Map({
  container: 'peta',
  style: {
    version: 8,
    sources: {
      'osm': {
        type: 'raster',
        tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
        tileSize: 256,
        attribution: '&copy; <a href="https://openstreetmap.org">OSM</a>'
      }
    },
    layers: [{
      id: 'osm-layer',
      type: 'raster',
      source: 'osm',
      minzoom: 0,
      maxzoom: 19
    }]
  },
  center: [106.15, -6.15],
  zoom: 11,
  attributionControl: false
});

map.addControl(new maplibregl.NavigationControl(), 'bottom-right');

// Loading state
function showLoading(v) {
  loadingEl.classList.toggle('hidden', !v);
  if (v) loadingEl.querySelector('span').textContent = 'Memuat data…';
  else loadingEl.querySelector('span').textContent = 'Selesai';
}

// Load GeoJSON layer
async function loadLayer(lensaId, layerCfg) {
  const srcId = `src-${layerCfg.id}`;
  const layerId = `lyr-${layerCfg.id}`;

  if (map.getLayer(layerId)) return;

  try {
    const resp = await fetch(layerCfg.file);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();

    map.addSource(srcId, { type: 'geojson', data });

    const paint = JSON.parse(JSON.stringify(layerCfg.paint));
    map.addLayer({
      id: layerId,
      type: layerCfg.type,
      source: srcId,
      paint,
      layout: layerCfg.type === 'line' && layerCfg.paint['line-dasharray']
        ? { 'line-dasharray': layerCfg.paint['line-dasharray'] }
        : {}
    });

    if (layerCfg.popup && layerCfg.popup.length > 0) {
      map.on('click', layerId, (e) => {
        if (!e.features?.[0]) return;
        const props = e.features[0].properties;
        let html = '<h3>' + (props[layerCfg.popup[0]] || '(tanpa nama)') + '</h3><table>';
        for (const k of layerCfg.popup.slice(0, 6)) {
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
    console.warn(`Gagal muat ${layerCfg.id}:`, err.message);
    if (!state.layers[lensaId]?.length) {
      infoContent.innerHTML = '<h3>Gagal memuat data</h3><p style="color:var(--text2)">Terjadi kesalahan saat memuat layer. Coba refresh halaman.</p>';
      infoPanel.classList.remove('hidden');
    }
  }
}

// Show lensa
async function showLensa(lensaId) {
  showLoading(true);

  // Hide all layers
  for (const [lid, layerIds] of Object.entries(state.layers)) {
    const vis = lid === lensaId ? 'visible' : 'none';
    for (const lyrId of layerIds) {
      if (map.getLayer(lyrId)) map.setLayoutProperty(lyrId, 'visibility', vis);
    }
  }

  // Load & show current lensa
  const lensa = LENSA[lensaId];
  if (!state.layers[lensaId]) {
    state.layers[lensaId] = [];
    const promises = lensa.layers.map(l => loadLayer(lensaId, l));
    await Promise.all(promises);
  } else {
    for (const lyrId of state.layers[lensaId]) {
      if (map.getLayer(lyrId)) map.setLayoutProperty(lyrId, 'visibility', 'visible');
    }
  }

  // Legend
  const legendEl = document.getElementById('legenda');
  const legendItems = LEGENDA[lensaId];
  if (legendItems) {
    legendEl.innerHTML = '<h3>' + lensa.label + '</h3>' +
      legendItems.map(l => `<div class="legend-item"><span style="display:inline-block;width:12px;height:12px;border-radius:3px;background:${l.color};flex-shrink:0"></span>${l.label}</div>`).join('');
  } else {
    legendEl.innerHTML = '';
  }

  state.active = lensaId;
  showLoading(false);
}

// Navigation
document.querySelectorAll('.lensa-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.lensa-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    showLensa(btn.dataset.lensa);
  });
});

// Info panel close
document.getElementById('info-tutup').addEventListener('click', () => {
  infoPanel.classList.add('hidden');
});

// Search
const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');
let searchTimeout;

async function initSearch() {
  const resp = await fetch('data/desa_index.json');
  state.desaIndex = await resp.json();
}

searchInput.addEventListener('input', () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    const q = searchInput.value.trim().toLowerCase();
    if (!q || q.length < 2) { searchResults.classList.add('hidden'); return; }
    const matches = state.desaIndex
      .filter(d => d.nama.toLowerCase().includes(q) || d.kecamatan.toLowerCase().includes(q))
      .slice(0, 20);

    if (!matches.length) {
      searchResults.innerHTML = '<div class="search-empty">Tidak ditemukan</div>';
      searchResults.classList.remove('hidden');
      return;
    }
    searchResults.innerHTML = matches.map(d =>
      `<div class="search-item" data-lat="${d.lat}" data-lng="${d.lng}">
        ${d.nama}<span class="kec">${d.kecamatan}</span>
      </div>`
    ).join('');
    searchResults.classList.remove('hidden');

    searchResults.querySelectorAll('.search-item').forEach(el => {
      el.addEventListener('click', () => {
        const lat = parseFloat(el.dataset.lat);
        const lng = parseFloat(el.dataset.lng);
        map.flyTo({ center: [lng, lat], zoom: 14 });
        searchResults.classList.add('hidden');
        searchInput.value = el.childNodes[0].textContent.trim();
      });
    });
  }, 200);
});

document.addEventListener('click', (e) => {
  if (!e.target.closest('#search-box')) searchResults.classList.add('hidden');
});

// Share
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

// URL state
function updateUrl() {
  const center = map.getCenter();
  const url = new URL(window.location);
  url.searchParams.set('lensa', state.active);
  url.searchParams.set('lat', center.lat.toFixed(4));
  url.searchParams.set('lng', center.lng.toFixed(4));
  url.searchParams.set('zoom', map.getZoom().toFixed(1));
  window.history.replaceState({}, '', url);
}

map.on('moveend', updateUrl);

// Init from URL or default
const params = new URLSearchParams(window.location.search);
const initLensa = params.get('lensa') || 'dasar';
const initLat = parseFloat(params.get('lat')) || -6.15;
const initLng = parseFloat(params.get('lng')) || 106.15;
const initZoom = parseFloat(params.get('zoom')) || 11;

map.setCenter([initLng, initLat]);
map.setZoom(initZoom);

// Validate lensa param
const validLensa = LENSA[initLensa] ? initLensa : 'dasar';
document.querySelector(`[data-lensa="${validLensa}"]`)?.classList.add('active');

map.on('load', () => {
  showLensa(validLensa);
  initSearch();
});
