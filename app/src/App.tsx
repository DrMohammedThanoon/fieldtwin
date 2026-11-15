import { useEffect, useMemo, useRef, useState } from 'react'
import type { Map as MapLibreMap } from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import evidenceJson from './data/terrain_baseline.json'

type View = 'mission' | 'search' | 'comparison' | 'transfer'
type SiteId = keyof typeof evidenceJson.sites
type FeatureKey = 'slope_deg' | 'relief_p95_p05_m' | 'roughness_rms_m'
type Features = Record<FeatureKey, number>
type Candidate = { site_id: SiteId; features: Features; absolute_differences: Features; pareto_front: number }
type Evaluation = { window_m: number; grid_m: number; mars_reference_features: Features; candidates: Candidate[] }

const evidence = evidenceJson as typeof evidenceJson & { evaluations: Record<'1000' | '2000', Evaluation> }
const repo = 'https://github.com/DrMohammedThanoon/fieldtwin'
const doc = (path: string) => `${repo}/blob/main/${path}`
const views: { id: View; label: string; number: string }[] = [
  { id: 'mission', label: 'Mission', number: '01' },
  { id: 'search', label: 'Earth search', number: '02' },
  { id: 'comparison', label: 'Comparison', number: '03' },
  { id: 'transfer', label: 'Transfer / rover test', number: '04' },
]
const siteOrder: SiteId[] = ['PILOT_A', 'PILOT_B', 'PILOT_C', 'PILOT_D', 'ARADS_PLAYA', 'LASCAR_CONTROL']
const displayName: Record<SiteId, string> = {
  PILOT_A: 'Pilot A', PILOT_B: 'Pilot B', PILOT_C: 'Pilot C', PILOT_D: 'Pilot D',
  ARADS_PLAYA: 'ARADS Playa', LASCAR_CONTROL: 'Láscar control',
}
const roleName: Record<SiteId, string> = {
  PILOT_A: 'Exploratory candidate', PILOT_B: 'Exploratory candidate · route case',
  PILOT_C: 'Exploratory candidate', PILOT_D: 'Exploratory candidate',
  ARADS_PLAYA: 'Historical regional field-test context', LASCAR_CONTROL: 'Rugged negative control',
}
const featureLabels: { key: FeatureKey; title: string; unit: string; short: string }[] = [
  { key: 'slope_deg', title: 'Plane-fit slope', unit: '°', short: 'Slope' },
  { key: 'relief_p95_p05_m', title: 'P95–P05 local relief', unit: 'm', short: 'Relief' },
  { key: 'roughness_rms_m', title: 'Detrended RMS roughness', unit: 'm', short: 'Roughness' },
]
const citations = [
  { title: 'NASADEM HGT.001 · NASA LP DAAC', href: 'https://lpdaac.usgs.gov/products/nasadem_hgtv001/' },
  { title: 'CTX stereo DTM · USGS Astrogeology', href: 'https://stac.astrogeology.usgs.gov/docs/data/mars/ctxdtms/' },
  { title: 'MOLA MEGDR · NASA PDS', href: 'https://pds-geosciences.wustl.edu/missions/mgs/megdr.html' },
  { title: 'Data manifest and product identifiers', href: doc('data/SOURCES.md') },
  { title: 'Methods and measured results', href: doc('docs/PHASE4_BASELINE_RESULTS.md') },
]

function format(n: number, digits = 2) { return n.toFixed(digits) }
function isSiteId(value: string): value is SiteId { return Object.hasOwn(evidence.sites, value) }
function initialView(): View {
  const hash = window.location.hash.slice(1)
  return views.some((v) => v.id === hash) ? hash as View : 'mission'
}

function Icon({ name }: { name: 'arrow' | 'north' | 'external' }) {
  if (name === 'arrow') return <span aria-hidden="true">↗</span>
  if (name === 'north') return <span aria-hidden="true">✦</span>
  return <span aria-hidden="true">↗</span>
}

function Eyebrow({ children }: { children: React.ReactNode }) { return <p className="eyebrow">{children}</p> }
function SectionHead({ number, eyebrow, title, description }: { number: string; eyebrow: string; title: string; description: string }) {
  return <div className="section-head"><span className="section-number">{number}</span><div><Eyebrow>{eyebrow}</Eyebrow><h1>{title}</h1><p className="section-description">{description}</p></div></div>
}
function EvidenceLink({ href, children }: { href: string; children: React.ReactNode }) {
  return <a href={href} target="_blank" rel="noopener noreferrer">{children} <Icon name="external" /></a>
}
function Pill({ children, tone = 'neutral' }: { children: React.ReactNode; tone?: 'earth' | 'mars' | 'warn' | 'neutral' }) {
  return <span className={`pill pill-${tone}`}>{children}</span>
}

function EarthMap({ selected, onSelect }: { selected: SiteId; onSelect: (site: SiteId) => void }) {
  const container = useRef<HTMLDivElement>(null)
  const map = useRef<MapLibreMap | null>(null)
  const selectRef = useRef(onSelect)
  const [status, setStatus] = useState<'loading' | 'ready' | 'unavailable'>('loading')
  selectRef.current = onSelect

  useEffect(() => {
    if (!container.current) { setStatus('unavailable'); return }
    let disposed = false
    void import('maplibre-gl').then((maplibregl) => {
      if (disposed || !container.current) return
      let m: MapLibreMap
      try { m = new maplibregl.Map({
        container: container.current,
        style: { version: 8, sources: { osm: { type: 'raster', tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'], tileSize: 256, attribution: '© OpenStreetMap contributors' } }, layers: [{ id: 'osm', type: 'raster', source: 'osm' }] },
        center: [-69.4, -24.1], zoom: 7, maxZoom: 14,
        attributionControl: false,
      }) } catch { setStatus('unavailable'); return }
      map.current = m
      m.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-right')
      m.addControl(new maplibregl.AttributionControl({ compact: false }), 'bottom-right')
      m.on('load', () => {
        const features = siteOrder.map((id) => ({ type: 'Feature' as const, properties: { id, role: evidence.sites[id].role }, geometry: { type: 'Point' as const, coordinates: [evidence.sites[id].longitude_deg, evidence.sites[id].latitude_deg] } }))
        m.addSource('sites', { type: 'geojson', data: { type: 'FeatureCollection', features } })
        m.addLayer({ id: 'site-halos', type: 'circle', source: 'sites', paint: { 'circle-radius': 13, 'circle-color': '#0a1723', 'circle-opacity': 0.78 } })
        m.addLayer({ id: 'site-points', type: 'circle', source: 'sites', paint: { 'circle-radius': ['case', ['==', ['get', 'id'], selected], 8, 6], 'circle-color': ['match', ['get', 'role'], 'pilot', '#35c9b8', 'historical_rover_test_reference', '#f0c078', '#f48467'], 'circle-stroke-color': '#fff', 'circle-stroke-width': 2 } })
        m.on('click', 'site-points', (event) => { const id = event.features?.[0]?.properties?.id; if (typeof id === 'string' && isSiteId(id)) selectRef.current(id) })
        m.on('mouseenter', 'site-points', () => { m.getCanvas().style.cursor = 'pointer' })
        m.on('mouseleave', 'site-points', () => { m.getCanvas().style.cursor = '' })
        m.fitBounds([[-70.35, -24.75], [-67.45, -23.1]], { padding: 42, duration: 0 })
        setStatus('ready')
      })
      m.on('error', (event) => { if (event.error?.message && /tile|source|load|fetch|webgl/i.test(event.error.message)) setStatus('unavailable') })
    }).catch(() => { if (!disposed) setStatus('unavailable') })
    return () => { disposed = true; map.current?.remove(); map.current = null }
  }, [])

  useEffect(() => {
    const m = map.current
    if (m?.getLayer('site-points')) m.setPaintProperty('site-points', 'circle-radius', ['case', ['==', ['get', 'id'], selected], 8, 6])
  }, [selected])

  return <div className="map-shell">
    <div className="map-viewport" ref={container} role="img" aria-label="Interactive Earth map of six measured Atacama sample points. Equivalent candidate selection is available in the list below." />
    {status === 'loading' && <div className="map-message" role="status">Loading Earth basemap…</div>}
    {status === 'unavailable' && <div className="map-message map-message-error" role="status">Earth map tiles or WebGL are unavailable. All six measured sites and coordinates remain in the list below.</div>}
    <div className="map-label"><span className="live-dot" /> EARTH ONLY <span className="map-label-separator">·</span> Northern Chile</div>
  </div>
}

function Mission({ go }: { go: (view: View) => void }) {
  return <>
    <section className="mission-hero">
      <div className="hero-copy"><Eyebrow>NASA Space Apps Challenge 2026 / SamaBeyond</Eyebrow><h1>Where can Earth<br /><em>test a Mars question?</em></h1><p className="hero-lead">FieldTwin compares measured terrain at six Earth sites with a provisional Mars reference to explore DEM-informed rover route planning.</p><p className="hero-tagline">Find where Earth can test Mars — and prove where the analogy breaks.</p><button className="primary-button" onClick={() => go('search')}>Explore the Earth search <span aria-hidden="true">→</span></button></div>
      <div className="hero-visual" aria-label="Abstract graphic separating Earth and Mars terrain evidence"><div className="orbit orbit-one" /><div className="orbit orbit-two" /><div className="planet planet-mars"><span>MARS<br /><small>reference</small></span></div><div className="planet planet-earth"><span>EARTH<br /><small>six sites</small></span></div><div className="visual-axis">MEASURE · COMPARE · QUALIFY</div></div>
    </section>
    <div className="status-strip"><span className="status-dot" /><strong>Evidence status</strong><span>Exploratory terrain comparison</span><span className="strip-divider" /><span>No unique validated analog winner</span><span className="strip-divider" /><span>No physical rover test</span></div>
    <section className="content-section"><div className="split-heading"><div><Eyebrow>01 / The mission need</Eyebrow><h2>A route-planning question grounded in terrain.</h2></div><p>Can DEM-derived slope, relief and roughness help choose Earth settings for testing a rover route-planning method? The results support a bounded desktop comparison and a future test proposal.</p></div>
      <div className="three-grid">
        <article className="info-card"><span className="card-index">A / MARS REFERENCE</span><div className="card-symbol mars-symbol">◌</div><h3>Provisional CTX terrain</h3><p>USGS stereo-derived CTX DTM. The analyzed reference is in a Mars planetary coordinate system; its independent artifact and vertical-accuracy checks remain unresolved.</p><p className="card-foot">~20 m source posting · 1 km and 2 km windows</p></article>
        <article className="info-card"><span className="card-index">B / EARTH OBSERVATIONS</span><div className="card-symbol earth-symbol">◇</div><h3>Real NASADEM samples</h3><p>Four exploratory Atacama pilots, a historical ARADS regional reference and a rugged Láscar control. All six coordinates and measured features are traceable to the baseline export.</p><p className="card-foot">NASADEM_HGT.001 · three source tiles</p></article>
        <article className="info-card"><span className="card-index">C / DECISION METHOD</span><div className="card-symbol line-symbol">≋</div><h3>Transparent Pareto fronts</h3><p>Three unweighted absolute feature differences identify trade-offs. All four pilots are nondominated at both tested scales; no site is certified as the best field location.</p><p className="card-foot">Slope · relief · roughness</p></article>
      </div>
    </section>
    <section className="content-section compact"><div className="method-band"><div><Eyebrow>The evidence chain</Eyebrow><h2>From observation to a testable question</h2></div><ol><li>Mars CTX reference</li><li>NASADEM Earth samples</li><li>Scale-aware descriptors</li><li>Pareto trade-offs</li><li>Future rover test proposal</li></ol></div></section>
    <section className="content-section sources-preview"><div><Eyebrow>Source integrity</Eyebrow><h2>Every visible result has a trail.</h2><p>NASA PDS MOLA supplies regional Mars context only. The local terrain comparison uses a provisional USGS CTX DTM and real NASADEM elevation. A shared 100 m processing grid does not establish identical effective sensor resolution.</p></div><div className="source-list">{citations.map((c) => <EvidenceLink key={c.title} href={c.href}>{c.title}</EvidenceLink>)}</div></section>
  </>
}

function Search({ selected, setSelected, go, evaluation }: { selected: SiteId; setSelected: (id: SiteId) => void; go: (view: View) => void; evaluation: Evaluation }) {
  const [filter, setFilter] = useState<'all' | 'pilot' | 'context'>('all')
  const visible = siteOrder.filter((id) => filter === 'all' || (filter === 'pilot' ? evidence.sites[id].role === 'pilot' : evidence.sites[id].role !== 'pilot'))
  const site = evidence.sites[selected]
  const candidate = evaluation.candidates.find((c) => c.site_id === selected)
  return <div className="page-content"><SectionHead number="02" eyebrow="Bounded Earth study" title="Search the measured sites." description="Six real sampled points in northern Chile. The 9 × 9 pilot grid covered 81 defined sample locations; this was not a continuous or global terrain survey." />
    <div className="search-layout"><div><EarthMap selected={selected} onSelect={setSelected} /><div className="map-legend"><span><i className="legend-dot earth" /> Exploratory pilots</span><span><i className="legend-dot gold" /> ARADS context</span><span><i className="legend-dot coral" /> Láscar control</span></div><p className="caption">OpenStreetMap basemap is Earth geography only. The Mars reference is intentionally absent from this map. <EvidenceLink href={doc('data/SEARCH_SCOPE.md')}>Search scope</EvidenceLink></p></div>
      <aside className="selected-panel"><Eyebrow>Selected measured point</Eyebrow><div className="selected-title"><h2>{displayName[selected]}</h2><Pill tone={site.role === 'pilot' ? 'earth' : site.role === 'negative_control' ? 'mars' : 'warn'}>{roleName[selected]}</Pill></div><p className="coords">{format(site.latitude_deg, 6)}° lat<br />{format(site.longitude_deg, 6)}° lon</p><div className="divider" /><dl className="details"><div><dt>Elevation source</dt><dd>{site.source_product} · {site.source_file}</dd></div><div><dt>Analysis reference</dt><dd>{site.analysis_crs}</dd></div><div><dt>1 km Pareto front</dt><dd>{candidate?.pareto_front ?? 'Unavailable'}</dd></div><div><dt>Science status</dt><dd>Exploratory; field suitability unvalidated</dd></div></dl><button className="secondary-button full" onClick={() => go('comparison')}>Inspect the comparison <span aria-hidden="true">→</span></button></aside></div>
    <div className="list-head"><div><Eyebrow>Actual location inventory</Eyebrow><h2>Select a site</h2></div><div className="segmented" aria-label="Filter locations"><button className={filter === 'all' ? 'active' : ''} onClick={() => setFilter('all')}>All 6</button><button className={filter === 'pilot' ? 'active' : ''} onClick={() => setFilter('pilot')}>Pilots 4</button><button className={filter === 'context' ? 'active' : ''} onClick={() => setFilter('context')}>Context 2</button></div></div>
    <div className="site-grid">{visible.map((id) => { const s = evidence.sites[id]; return <button className={`site-card ${selected === id ? 'selected' : ''}`} key={id} onClick={() => setSelected(id)} aria-pressed={selected === id}><span className="site-card-top"><span className={`site-swatch ${s.role}`} /><span>{id.replaceAll('_', ' ')}</span><span aria-hidden="true">↗</span></span><strong>{displayName[id]}</strong><small>{format(s.latitude_deg, 4)}°, {format(s.longitude_deg, 4)}°</small><span className="site-role">{roleName[id]}</span></button> })}</div>
    <div className="note-grid"><div className="note-card"><Eyebrow>Sampling boundary</Eyebrow><p>Original pilot grid: latitude −24.9 to −24.1; longitude −69.9 to −69.1. Four pilot points were chosen for the six-site comparison. ARADS and Láscar used separate source tiles outside that grid.</p></div><div className="note-card"><Eyebrow>Search limitations</Eyebrow><p>No independently verified search polygon, geographic holdout or field-access assessment exists. The map shows measured points, not an evaluated surface between them.</p></div></div>
  </div>
}

function FeatureBars({ value, max, label }: { value: number; max: number; label: string }) {
  return <div className="bar-row"><span>{label}</span><div className="bar-track" role="img" aria-label={`${label}: ${format(value, 2)}`}><div style={{ width: `${Math.max(2, 100 * value / max)}%` }} /></div><strong>{format(value)}</strong></div>
}

function Comparison({ selected, setSelected, windowM, setWindowM, go }: { selected: SiteId; setSelected: (id: SiteId) => void; windowM: '1000' | '2000'; setWindowM: (value: '1000' | '2000') => void; go: (view: View) => void }) {
  const evaluation = evidence.evaluations[windowM]
  const candidate = evaluation.candidates.find((c) => c.site_id === selected)!
  const frontCounts = [1, 2, 3].map((front) => evaluation.candidates.filter((c) => c.pareto_front === front).length)
  const maxes = featureLabels.map((f) => Math.max(...evaluation.candidates.map((c) => c.absolute_differences[f.key])))
  return <div className="page-content"><SectionHead number="03" eyebrow="Measured terrain evidence" title="Compare the trade-offs." description="An unweighted Pareto comparison of absolute differences from the provisional Mars CTX reference. Front numbers describe this tested set, not field suitability." />
    <div className="toolbar"><div><span className="toolbar-label">Analysis window</span><div className="segmented" aria-label="Analysis window"><button className={windowM === '1000' ? 'active' : ''} onClick={() => setWindowM('1000')}>1 km</button><button className={windowM === '2000' ? 'active' : ''} onClick={() => setWindowM('2000')}>2 km</button></div></div><label className="site-select-label">Inspect a measured site<select value={selected} onChange={(e) => { if (isSiteId(e.target.value)) setSelected(e.target.value) }}>{siteOrder.map((id) => <option value={id} key={id}>{displayName[id]}</option>)}</select></label><span className="toolbar-note">100 m computational grid · different effective source resolutions</span></div>
    <div className="front-summary">{frontCounts.map((count, i) => <div className="front-stat" key={i}><span>FRONT 0{i + 1}</span><strong>{count}</strong><small>{i === 0 ? 'Four nondominated pilots' : i === 1 ? 'ARADS historical context' : 'Láscar rugged control'}</small></div>)}</div>
    <div className="comparison-layout"><section className="comparison-chart"><div className="panel-heading"><div><Eyebrow>Absolute difference from Mars</Eyebrow><h2>Three features, three units</h2></div><Pill>Measured / derived</Pill></div><p className="chart-intro">Shorter bars mean a smaller difference for that individual feature. Each feature has its own scale; bar length cannot be compared across feature panels.</p>{featureLabels.map((f, index) => <div className="feature-chart" key={f.key}><div className="feature-heading"><h3>{f.title}</h3><span>Difference · {f.unit}</span></div>{evaluation.candidates.map((c) => <FeatureBars key={c.site_id} label={displayName[c.site_id as SiteId]} value={c.absolute_differences[f.key]} max={maxes[index]} />)}</div>)}<p className="caption">Bars use zero as the origin and the largest observed difference in this six-site set as the panel maximum. <EvidenceLink href={doc('docs/METHODS.md')}>Methods</EvidenceLink></p></section>
      <aside className="comparison-side"><div className="metric-panel"><Eyebrow>Selected point / {windowM === '1000' ? '1 km' : '2 km'}</Eyebrow><h2>{displayName[selected]}</h2><Pill tone={candidate.pareto_front === 1 ? 'earth' : candidate.pareto_front === 2 ? 'warn' : 'mars'}>Pareto front {candidate.pareto_front}</Pill><div className="metric-table"><div className="metric-header"><span>Feature</span><span>Mars</span><span>Earth</span><span>|Δ|</span></div>{featureLabels.map((f) => <div className="metric-line" key={f.key}><span>{f.short} <small>{f.unit}</small></span><span>{format(evaluation.mars_reference_features[f.key])}</span><span>{format(candidate.features[f.key])}</span><strong>{format(candidate.absolute_differences[f.key])}</strong></div>)}</div><p className="caption">Values are rounded for display; fronts use full exported precision.</p></div><div className="caution-panel"><Eyebrow>Interpret with care</Eyebrow><p>All four pilots are nondominated at both windows. The selected front is not a rover-safety rating, a similarity percentage or a unique winner.</p><p>CTX stereo artifacts and independent elevation accuracy remain unresolved. Matching grid spacing does not prove matching effective source resolution.</p></div><button className="secondary-button full" onClick={() => go('transfer')}>Evaluate analog transfer <span aria-hidden="true">→</span></button></aside></div>
    <div className="note-grid"><div className="note-card"><Eyebrow>Uncertainty experiment</Eyebrow><p>In 100 hypothetical Mars elevation perturbation trials, complete Pareto ordering was unchanged in 21/100, 27/100 and 30/100 runs at assumed 1 m, 3 m and 5 m SD. These are not calibrated error probabilities.</p></div><div className="note-card"><Eyebrow>ML decision</Eyebrow><p>The physical baseline remains primary. ML-B V1 and V2 failed their scientific acceptance gates; the independent expert-rated site-ranking benchmark was never activated. <EvidenceLink href={doc('docs/PHASE5_SCIENTIFIC_CLOSEOUT.md')}>Closeout</EvidenceLink></p></div></div>
  </div>
}

const transferRows = [
  { area: 'Slope, relief, roughness', status: 'DEM-supported', detail: 'Comparable derived terrain descriptors at documented windows, with scale and source limits.' },
  { area: 'Grid route alternatives', status: 'DEM-supported', detail: 'Numerical paths under hypothetical grade limits; path feasibility is model dependent.' },
  { area: 'Rocks, soil, traction, slip', status: 'Needs evidence', detail: 'Independent ground survey, material observations and a specified rover are required.' },
  { area: 'Field access and safety', status: 'Needs evidence', detail: 'Permissions, site inspection, operational plans and safety review are absent.' },
  { area: 'Mars gravity and atmosphere', status: 'Cannot reproduce', detail: 'Earth field conditions cannot physically match these Martian conditions.' },
  { area: 'Temperature and communication delay', status: 'Cannot reproduce', detail: 'Environmental/operations effects require separate simulation and qualification.' },
]
const routeRows = [
  { place: 'Mars CTX', at3: '5 / 5', at10: '5 / 5', detour: '2.37%' },
  { place: 'Pilot B', at3: '5 / 5', at10: '5 / 5', detour: '5.92%' },
  { place: 'ARADS Playa', at3: '3 / 5', at10: '5 / 5', detour: '30.07%' },
  { place: 'Láscar control', at3: '0 / 5', at10: '0 / 5', detour: '—' },
]
function Transfer({ selected }: { selected: SiteId }) {
  return <div className="page-content"><SectionHead number="04" eyebrow="From comparison to experiment" title="Where the analogy breaks." description="Pilot B is the existing illustrative DEM-route case. The research proposes a future physical field test; no rover has traversed a FieldTwin route." />
    <div className="transfer-intro"><div><Eyebrow>Illustrative case / Pilot B</Eyebrow><h2>A testable route question,<br /><em>not a certified site.</em></h2><p>The route algorithm changed paths under assumed DEM-grid grade constraints. Pilot B was chosen for this explanation because the existing benchmark includes it, not because it was proven the best analog.</p></div><div className="transfer-stat"><span>60</span><strong>recorded DEM route searches</strong><small>20 distance-only + 40 grade-constrained</small></div></div>
    <div className="transfer-grid"><section className="table-panel"><div className="panel-heading"><div><Eyebrow>Numerical experiment</Eyebrow><h2>Route feasibility</h2></div><Pill tone="warn">Hypothetical limits</Pill></div><p className="chart-intro">Five predefined endpoint pairs per terrain, 1 km window, 100 m grid. Counts are feasible constrained routes. Mean detour at 3° includes feasible routes only.</p><div className="route-table" role="table" aria-label="Precomputed numerical route results"><div className="route-row route-header" role="row"><span role="columnheader">Terrain</span><span role="columnheader">3°</span><span role="columnheader">10°</span><span role="columnheader">3° detour</span></div>{routeRows.map((row) => <div className="route-row" role="row" key={row.place}><strong role="cell">{row.place}</strong><span role="cell">{row.at3}</span><span role="cell">{row.at10}</span><span role="cell">{row.detour}</span></div>)}</div><p className="caption">3° and 10° are experimental assumptions, not certified rover limits. “—” means no feasible 3° routes in these five pairs. <EvidenceLink href={doc('docs/PHASE4_BASELINE_RESULTS.md')}>Full benchmark</EvidenceLink></p></section>
      <section className="matrix-panel"><div className="panel-heading"><div><Eyebrow>Analog Transfer Matrix</Eyebrow><h2>What transfers?</h2></div></div><div className="matrix-list">{transferRows.map((row) => <div className="matrix-row" key={row.area}><div><h3>{row.area}</h3><p>{row.detail}</p></div><Pill tone={row.status === 'DEM-supported' ? 'earth' : row.status === 'Needs evidence' ? 'warn' : 'mars'}>{row.status}</Pill></div>)}</div><p className="caption"><EvidenceLink href={doc('docs/ANALOG_TRANSFER_MATRIX.md')}>Read the full transfer matrix</EvidenceLink></p></section></div>
    <section className="protocol-section"><div className="protocol-heading"><Eyebrow>Proposed / not performed</Eyebrow><h2>A future field protocol</h2><p>Selected map point: {displayName[selected]}. The existing numerical route example remains Pilot B regardless of map selection. Any physical test requires a fresh site-specific plan.</p></div><div className="protocol-steps"><div><span>01</span><h3>Verify the ground</h3><p>Confirm access, permissions and safety; independently survey terrain, rocks and soil at Pilot B.</p></div><div><span>02</span><h3>Specify the rover</h3><p>Define vehicle geometry, traction, sensors and certified operating limits before planning trial corridors.</p></div><div><span>03</span><h3>Measure the trial</h3><p>Compare planned with repeated traversed paths; record distance, grade, slip, energy, localization error and recoveries.</p></div><div><span>04</span><h3>Report the gap</h3><p>Quantify differences between DEM predictions and measured behavior, and disclose Earth-to-Mars limits.</p></div></div></section>
    <div className="note-grid"><div className="note-card"><Eyebrow>Stress test, not calibration</Eyebrow><p>4,840 original and synthetic-perturbation route searches tested numerical sensitivity. Assumed elevation errors are not measured DEM accuracy, and search frequencies are not rover-safety probabilities.</p></div><div className="note-card"><Eyebrow>Evidence and reproducibility</Eyebrow><p>Review the <EvidenceLink href={doc('docs/LIMITATIONS.md')}>limitations</EvidenceLink>, <EvidenceLink href={doc('docs/PHASE5_SCIENTIFIC_CLOSEOUT.md')}>scientific closeout</EvidenceLink> and <EvidenceLink href={repo}>source repository</EvidenceLink>.</p></div></div>
  </div>
}

function App() {
  const [view, setView] = useState<View>(initialView)
  const [selected, setSelected] = useState<SiteId>('PILOT_B')
  const [windowM, setWindowM] = useState<'1000' | '2000'>('1000')
  const evaluation = useMemo(() => evidence.evaluations[windowM], [windowM])
  useEffect(() => { const onHash = () => setView(initialView()); window.addEventListener('hashchange', onHash); return () => window.removeEventListener('hashchange', onHash) }, [])
  function go(next: View) { window.location.hash = next; setView(next); window.scrollTo({ top: 0, behavior: 'smooth' }) }
  return <div className="app"><a className="skip-link" href="#main-content">Skip to content</a><header className="site-header"><button className="brand" onClick={() => go('mission')} aria-label="FieldTwin, return to Mission"><span className="brand-mark"><Icon name="north" /></span><span>FIELD<span>TWIN</span><small>EARTH × MARS TERRAIN LAB</small></span></button><nav className="main-nav" aria-label="Main navigation">{views.map((item) => <button key={item.id} onClick={() => go(item.id)} aria-current={view === item.id ? 'page' : undefined}><span>{item.number}</span>{item.label}</button>)}</nav><a className="header-evidence" href={repo} target="_blank" rel="noopener noreferrer">View evidence <Icon name="external" /></a></header>
    <main id="main-content">{view === 'mission' ? <Mission go={go} /> : view === 'search' ? <Search selected={selected} setSelected={setSelected} go={go} evaluation={evaluation} /> : view === 'comparison' ? <Comparison selected={selected} setSelected={setSelected} windowM={windowM} setWindowM={setWindowM} go={go} /> : <Transfer selected={selected} />}</main>
    <footer className="site-footer"><div><strong>FIELD<span>TWIN</span></strong><p>Find where Earth can test Mars — and prove where the analogy breaks.</p></div><div><span>Scientific status</span><p>Exploratory · evidence-limited · no unique validated analog</p></div><div><span>Explore</span><div className="footer-links"><EvidenceLink href={doc('data/SOURCES.md')}>Data sources</EvidenceLink><EvidenceLink href={doc('docs/METHODS.md')}>Methods</EvidenceLink><EvidenceLink href={doc('docs/VALIDATION.md')}>Validation</EvidenceLink></div></div><small>© 2026 SamaBeyond / FieldTwin. Basemap © OpenStreetMap contributors.</small></footer>
  </div>
}

export default App
