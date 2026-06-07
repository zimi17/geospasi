# Roadmap

## v0.1 — Core Viewer (current)
- [x] MapLibre GL JS base map
- [x] GeoJSON layer loading
- [x] Popup info on feature click
- [x] Dark theme, responsive layout
- [x] Search (desa index)
- [x] Share URL with map state
- [x] Layer toggle (independent, multi-active)
- [x] Custom GeoJSON URL overlay with color/opacity/zoom/remove
- [x] GeoSERANG example — 7 lensa, 46 layers
- [x] WCAG accessibility compliance

## v0.2 — Quality & Documentation
- [ ] Acceptance test suite (manual test plan)
- [ ] CI/CD for core app demo
- [ ] npm/pip package? or keep zero-dep
- [ ] i18n (id/en)
- [ ] Keyboard navigation for layer panel

## v0.3 — Data Import
- [ ] Import GeoJSON via file upload (not just URL)
- [ ] Import KML/GPX (convert to GeoJSON client-side)
- [ ] Style presets for common data types
- [ ] CSV point import (lat/lon → GeoJSON)

## v0.4 — Advanced Viewer
- [ ] Layer reorder (drag & drop)
- [ ] Opacity slider for built-in layers
- [ ] Attribute table view
- [ ] Export visible layers as GeoJSON
- [ ] Print map

## Future — Server-Assisted Features
- [ ] PMTiles support for large datasets
- [ ] MBTiles offline tiles
- [ ] WMS/WFS source support
- [ ] Supabase integration for queryable data
