export const LENSA = {
  demo: {
    id: 'demo',
    label: 'Demo',
    icon: '🧪',
    color: '#3b82f6',
    layers: [
      {
        id: 'area-demo',
        file: 'sample-data/area.geojson',
        type: 'fill',
        paint: { 'fill-color': '#3b82f6', 'fill-opacity': 0.4 },
        popup: ['name'],
      },
      {
        id: 'area-demo-outline',
        file: 'sample-data/area.geojson',
        type: 'line',
        paint: { 'line-color': '#1d4ed8', 'line-width': 1.5 },
        popup: [],
      },
      {
        id: 'titik-demo',
        file: 'sample-data/titik.geojson',
        type: 'circle',
        paint: { 'circle-color': '#ef4444', 'circle-radius': 6, 'circle-opacity': 0.8 },
        popup: ['name', 'category'],
      },
    ],
  },
};

export const LEGENDA = {
  demo: [
    { label: 'Area Demo', color: '#3b82f6' },
    { label: 'Titik Demo', color: '#ef4444' },
  ],
};
