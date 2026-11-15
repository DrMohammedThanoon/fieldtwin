import { useEffect, useRef, useState } from 'react'
import type { Map as MapLibreMap } from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'

export type BasemapId = 'osm' | 'relief' | 'satellite' | 'topo'
type Basemap = { id: BasemapId; label: string; tiles: string; maxzoom: number; attribution: string; dim?: boolean }
const GIBS = 'https://gibs.earthdata.nasa.gov/wmts/epsg3857/best'
export const BASEMAPS: Basemap[] = [
  { id: 'osm', label: 'Streets', tiles: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png', maxzoom: 19, attribution: '© OpenStreetMap contributors', dim: true },
  { id: 'relief', label: 'NASA relief', tiles: `${GIBS}/ASTER_GDEM_Color_Shaded_Relief/default/GoogleMapsCompatible_Level12/{z}/{y}/{x}.jpg`, maxzoom: 12, attribution: 'NASA GIBS · ASTER GDEM shaded relief (NASA/METI)' },
  { id: 'satellite', label: 'NASA imagery', tiles: `${GIBS}/MODIS_Terra_CorrectedReflectance_TrueColor/default/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpg`, maxzoom: 9, attribution: 'NASA GIBS · MODIS Terra true colour (250 m)' },
  { id: 'topo', label: 'Topo', tiles: 'https://tile.opentopomap.org/{z}/{x}/{y}.png', maxzoom: 17, attribution: '© OpenTopoMap (CC-BY-SA) · © OpenStreetMap contributors' },
]
function addBase(m: MapLibreMap, id: BasemapId) {
  const b = BASEMAPS.find((x) => x.id === id) ?? BASEMAPS[0]
  if (m.getLayer('base')) m.removeLayer('base')
  if (m.getSource('base')) m.removeSource('base')
  m.addSource('base', { type: 'raster', tiles: [b.tiles], tileSize: 256, maxzoom: b.maxzoom, attribution: b.attribution })
  m.addLayer({ id: 'base', type: 'raster', source: 'base', paint: b.dim ? { 'raster-brightness-max': 0.55, 'raster-saturation': -0.5 } : {} })
}

export type Marker = { id: string; lat: number; lon: number; label: string; color?: string; r?: number }

export function EarthMap({ markers, selectedId, onSelect, zoom = 1.6, fit, follow = true, basemap = 'osm' }: { markers: Marker[]; selectedId: string; onSelect?: (id: string) => void; zoom?: number; fit?: [[number, number], [number, number]]; follow?: boolean; basemap?: BasemapId }) {
  const container = useRef<HTMLDivElement>(null)
  const map = useRef<MapLibreMap | null>(null)
  const glRef = useRef<typeof import('maplibre-gl') | null>(null)
  const pins = useRef<{ remove: () => void }[]>([])
  const selectRef = useRef(onSelect)
  const [status, setStatus] = useState<'loading' | 'ready' | 'unavailable'>('loading')
  selectRef.current = onSelect
  const latest = useRef({ markers, selectedId, zoom, fit, basemap })
  latest.current = { markers, selectedId, zoom, fit, basemap }
  useEffect(() => {
    if (!container.current) { setStatus('unavailable'); return }
    let disposed = false
    void import('maplibre-gl').then((gl) => {
      if (disposed || !container.current) return
      glRef.current = gl
      const s0 = latest.current.markers.find((x) => x.id === latest.current.selectedId)
      let m: MapLibreMap
      try { m = new gl.Map({ container: container.current, style: { version: 8, sources: {}, layers: [] }, center: s0 ? [s0.lon, s0.lat] : [20, 15], zoom: latest.current.zoom, maxZoom: 12, attributionControl: false }) } catch { setStatus('unavailable'); return }
      map.current = m
      m.addControl(new gl.NavigationControl({ showCompass: false }), 'top-right')
      m.addControl(new gl.AttributionControl({ compact: false }), 'bottom-right')
      m.on('load', () => { addBase(m, latest.current.basemap); if (latest.current.fit) m.fitBounds(latest.current.fit, { padding: 42, duration: 0 }); setStatus('ready') })
      m.on('error', (ev) => { if (ev.error?.message && /tile|source|webgl/i.test(ev.error.message)) setStatus('unavailable') })
    }).catch(() => { if (!disposed) setStatus('unavailable') })
    return () => { disposed = true; pins.current.forEach((p) => p.remove()); pins.current = []; map.current?.remove(); map.current = null }
  }, [])
  useEffect(() => { if (map.current && status !== 'loading' && map.current.getLayer('base')) { addBase(map.current, basemap); setStatus('ready') } }, [basemap])
  useEffect(() => { // DOM markers: keyboard-focusable and independent of the GeoJSON web worker
    const m = map.current, gl = glRef.current
    if (!m || !gl || status === 'loading') return
    pins.current.forEach((p) => p.remove())
    pins.current = markers.map((mk) => {
      const el = document.createElement('button')
      el.className = `sb-pin earthsel ${mk.id === selectedId ? 'selected' : ''}`
      el.title = mk.label
      el.setAttribute('aria-label', `${mk.label}, latitude ${mk.lat}, longitude ${mk.lon}`)
      el.setAttribute('aria-pressed', String(mk.id === selectedId))
      el.style.zIndex = mk.id === selectedId ? '3' : '1'
      const dot = document.createElement('i')
      dot.style.cssText = `width:${2 * (mk.r ?? 6) + 2}px;height:${2 * (mk.r ?? 6) + 2}px;background:${mk.color ?? '#d8dde1'}`
      el.appendChild(dot)
      el.addEventListener('click', (ev) => { ev.stopPropagation(); selectRef.current?.(mk.id) })
      return new gl.Marker({ element: el }).setLngLat([mk.lon, mk.lat]).addTo(m)
    })
    const s = markers.find((x) => x.id === selectedId)
    if (s && follow) m.flyTo({ center: [s.lon, s.lat], zoom: Math.max(m.getZoom(), zoom), duration: 600 })
  }, [markers, selectedId, zoom, status, follow])
  return <>
    <div className="sb-mapfill" ref={container} role="region" aria-label="Interactive Earth map of measured Atacama sites. The list beside the map offers the same selection." />
    {status === 'loading' && <div className="sb-mapmsg" role="status">Loading Earth basemap…</div>}
    {status === 'unavailable' && <div className="sb-mapmsg" role="status">Earth map tiles or WebGL are unavailable. Every site and its coordinates remain in the list.</div>}
  </>
}

