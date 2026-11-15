import { useEffect, useMemo, useState } from 'react'
import evidenceJson from './data/terrain_baseline.json'
import { EarthMap, BASEMAPS } from './EarthMap'
import type { Marker, BasemapId } from './EarthMap'
import './sb.css'

type View = 'mission' | 'search' | 'comparison' | 'transfer'
type SiteId = keyof typeof evidenceJson.sites
type FeatureKey = 'slope_deg' | 'relief_p95_p05_m' | 'roughness_rms_m'
type Features = Record<FeatureKey, number>
type Candidate = { site_id: SiteId; features: Features; absolute_differences: Features; pareto_front: number }
type Evaluation = { window_m: number; grid_m: number; mars_reference_features: Features; candidates: Candidate[] }
type Tone = 'earth' | 'mars' | 'warn' | 'neutral'

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
const displayName: Record<SiteId, string> = { PILOT_A: 'Pilot A', PILOT_B: 'Pilot B', PILOT_C: 'Pilot C', PILOT_D: 'Pilot D', ARADS_PLAYA: 'ARADS Playa', LASCAR_CONTROL: 'Láscar control' }
const roleName: Record<SiteId, string> = {
  PILOT_A: 'Exploratory candidate', PILOT_B: 'Exploratory candidate · route case', PILOT_C: 'Exploratory candidate', PILOT_D: 'Exploratory candidate',
  ARADS_PLAYA: 'Historical regional field-test context', LASCAR_CONTROL: 'Rugged negative control',
}
const roleColor = (id: SiteId) => { const r = evidence.sites[id].role; return r === 'pilot' ? '#2f8f86' : r === 'negative_control' ? '#ff8b5d' : '#e3b955' }
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
const protocol = [
  ['01', 'Verify the ground', 'Confirm access, permissions and safety; independently survey terrain, rocks and soil at Pilot B.'],
  ['02', 'Specify the rover', 'Define vehicle geometry, traction, sensors and certified operating limits before planning trial corridors.'],
  ['03', 'Measure the trial', 'Compare planned with repeated traversed paths; record distance, grade, slip, energy, localization error and recoveries.'],
  ['04', 'Report the gap', 'Quantify differences between DEM predictions and measured behavior, and disclose Earth-to-Mars limits.'],
]

const fmt = (n: number, digits = 2) => n.toFixed(digits)
const isSiteId = (value: string): value is SiteId => Object.hasOwn(evidence.sites, value)
function initialView(): View { const h = window.location.hash.slice(1); return views.some((v) => v.id === h) ? h as View : 'mission' }

function Ext({ href, children }: { href: string; children: React.ReactNode }) { return <a href={href} target="_blank" rel="noopener noreferrer">{children} <span aria-hidden="true">↗</span></a> }
function Pill({ children, tone = 'neutral' }: { children: React.ReactNode; tone?: Tone }) { return <span className={`sb-pill ${tone}`}>{children}</span> }
function Title({ eyebrow, children, lead }: { eyebrow: string; children: React.ReactNode; lead: string }) {
  return <div className="sb-title"><div><div className="sb-eyebrow">{eyebrow}</div><h1>{children}</h1></div><p>{lead}</p></div>
}
const accent = (s: string) => <span style={{ color: 'var(--orange)' }}>{s}</span>

function Mission({ go }: { go: (v: View) => void }) {
  const nWindows = Object.keys(evidence.evaluations).length
  return <>
    <div className="sb-hero">
      <div>
        <div className="sb-eyebrow">NASA Space Apps Challenge 2026 / SamaBeyond</div>
        <h1 className="sb-h sb-h-sm">Where can Earth <em>test a Mars question?</em></h1>
        <p className="sb-lead">FieldTwin compares measured terrain at six Earth sites with a provisional Mars reference to explore DEM-informed rover route planning.</p>
        <p className="sb-note" style={{ marginTop: 14 }}>Find where Earth can test Mars — and prove where the analogy breaks.</p>
        <div className="sb-cards" style={{ marginTop: 26 }}>
          <button className="sb-btn" onClick={() => go('search')}>Explore the Earth search ↗</button>
          <a className="sb-btn secondary" href={repo} target="_blank" rel="noopener noreferrer">View evidence ↗</a>
        </div>
        <div className="sb-kpis">
          <div className="sb-kpi"><b>{siteOrder.length}</b><span>Measured Earth sites</span></div>
          <div className="sb-kpi"><b>{featureLabels.length}</b><span>Terrain features</span></div>
          <div className="sb-kpi"><b>{nWindows}</b><span>Analysis windows</span></div>
        </div>
        <div className="sb-meta"><div><b>01 / MEASURE</b><br />SLOPE · RELIEF · ROUGHNESS</div><div><b>02 / COMPARE</b><br />PARETO TRADE-OFFS</div><div><b>03 / QUALIFY</b><br />WHERE THE ANALOGY BREAKS</div></div>
      </div>
      <div className="sb-visual" aria-label="Abstract graphic separating Earth and Mars terrain evidence" role="img">
        <div className="sb-stars" /><div className="sb-ring" />
        <div className="sb-globe big" style={{ backgroundImage: 'url(planetary/mars_hi.jpg)' }} />
        <div className="sb-orbit"><div className="sb-globe earth" /></div>
        <div className="sb-vlabel">MARS · REFERENCE (CTX DTM)<br />EARTH · SIX MEASURED SITES<br />GRAPHIC IS ILLUSTRATIVE, NOT DATA</div>
      </div>
    </div>
    <div className="sb-layout" style={{ paddingTop: 10 }}>
      <Title eyebrow="01 / The mission need" lead="Can DEM-derived slope, relief and roughness help choose Earth settings for testing a rover route-planning method? The results support a bounded desktop comparison and a future test proposal.">A route-planning question {accent('grounded in terrain.')}</Title>
      <div className="sb-dgrid">
        <div className="sb-panel"><h3>A / Mars reference</h3><b>Provisional CTX terrain</b><p>USGS stereo-derived CTX DTM. The analyzed reference is in a Mars planetary coordinate system; its independent artifact and vertical-accuracy checks remain unresolved.</p><p className="sb-tiny">~20 m source posting · 1 km and 2 km windows</p></div>
        <div className="sb-panel"><h3>B / Earth observations</h3><b>Real NASADEM samples</b><p>Four exploratory Atacama pilots, a historical ARADS regional reference and a rugged Láscar control. All six coordinates and measured features are traceable to the baseline export.</p><p className="sb-tiny">NASADEM_HGT.001 · three source tiles</p></div>
        <div className="sb-panel"><h3>C / Decision method</h3><b>Transparent Pareto fronts</b><p>Three unweighted absolute feature differences identify trade-offs. All four pilots are nondominated at both tested scales; no site is certified as the best field location.</p><p className="sb-tiny">Slope · relief · roughness</p></div>
      </div>
      <div className="sb-panel" style={{ marginTop: 14 }}><h3>The evidence chain</h3>
        <ol className="sb-chain">{['Mars CTX reference', 'NASADEM Earth samples', 'Scale-aware descriptors', 'Pareto trade-offs', 'Future rover test proposal'].map((s, i) => <li key={s}><span>{String(i + 1).padStart(2, '0')}</span>{s}</li>)}</ol></div>
      <div className="sb-columns rev" style={{ marginTop: 14, gridTemplateColumns: 'minmax(0,1fr) minmax(0,1fr)' }}>
        <div className="sb-panel"><h3>Source integrity</h3><p>NASA PDS MOLA supplies regional Mars context only. The local terrain comparison uses a provisional USGS CTX DTM and real NASADEM elevation. A shared 100 m processing grid does not establish identical effective sensor resolution.</p></div>
        <div className="sb-panel"><h3>Every visible result has a trail</h3><ul className="sb-srcs" style={{ listStyle: 'none', paddingLeft: 0 }}>{citations.map((c) => <li key={c.title}><Ext href={c.href}>{c.title}</Ext></li>)}</ul></div>
      </div>
    </div>
  </>
}

function Search({ selected, setSelected, go, evaluation }: { selected: SiteId; setSelected: (id: SiteId) => void; go: (v: View) => void; evaluation: Evaluation }) {
  const [filter, setFilter] = useState<'all' | 'pilot' | 'context'>('all')
  const [basemap, setBasemap] = useState<BasemapId>('topo')
  const [showPoints, setShowPoints] = useState(true)
  const visible = siteOrder.filter((id) => filter === 'all' || (filter === 'pilot' ? evidence.sites[id].role === 'pilot' : evidence.sites[id].role !== 'pilot'))
  const site = evidence.sites[selected]
  const candidate = evaluation.candidates.find((c) => c.site_id === selected)
  const markers = useMemo<Marker[]>(() => visible.map((id) => ({ id, lat: evidence.sites[id].latitude_deg, lon: evidence.sites[id].longitude_deg, label: displayName[id], color: roleColor(id), r: 7 })), [filter]) // eslint-disable-line react-hooks/exhaustive-deps
  return <div className="sb-layout">
    <Title eyebrow="Bounded Earth study" lead="Six real sampled points in northern Chile. The 9 × 9 pilot grid covered 81 defined sample locations; this was not a continuous or global terrain survey.">Search the {accent('measured sites.')}</Title>
    <div className="sb-columns">
      <aside className="sb-side">
        <h3>Measured points</h3>
        <div className="sb-seg" role="group" aria-label="Filter locations">{([['all', 'All 6'], ['pilot', 'Pilots 4'], ['context', 'Context 2']] as const).map(([k, l]) => <button key={k} aria-pressed={filter === k} onClick={() => setFilter(k)}>{l.toUpperCase()}</button>)}</div>
        <div className="sb-list" role="list">{visible.map((id) => <button key={id} role="listitem" className={`sb-choice ${selected === id ? 'selected' : ''}`} aria-pressed={selected === id} onClick={() => setSelected(id)}>
          <b><i className="sb-dot" style={{ background: roleColor(id) }} />{displayName[id]}</b><small>{fmt(evidence.sites[id].latitude_deg, 4)}°, {fmt(evidence.sites[id].longitude_deg, 4)}° · {roleName[id]}</small></button>)}</div>
        <dl className="sb-dl">
          <div><dt>Elevation source</dt><dd>{site.source_product} · {site.source_file}</dd></div>
          <div><dt>Analysis reference</dt><dd>{site.analysis_crs}</dd></div>
          <div><dt>1 km Pareto front</dt><dd>{candidate?.pareto_front ?? 'Unavailable'}</dd></div>
          <div><dt>Science status</dt><dd>Exploratory; field suitability unvalidated</dd></div>
        </dl>
        <button className="sb-btn" onClick={() => go('comparison')}>Inspect the comparison ↗</button>
      </aside>
      <div className="sb-view">
        <EarthMap basemap={basemap} markers={showPoints ? markers : []} selectedId={selected} onSelect={(id) => { if (isSiteId(id)) setSelected(id) }} zoom={8} />
        <div className="sb-shade" />
        <div className="sb-layers" role="group" aria-label="Map layers">
          <div className="sb-layers-seg">{BASEMAPS.map((b) => <button key={b.id} aria-pressed={basemap === b.id} onClick={() => setBasemap(b.id)}>{b.label.toUpperCase()}</button>)}</div>
          <label className="sb-layers-chk"><input type="checkbox" checked={showPoints} onChange={(e) => setShowPoints(e.target.checked)} /> MEASURED POINTS</label>
        </div>
        <div className="sb-ovt"><span>EARTH ONLY · NORTHERN CHILE</span><b>{displayName[selected]}</b></div>
        <div className="sb-ovf"><span className="sb-legendbar"><i className="sb-dot" style={{ background: '#2f8f86' }} /> Exploratory pilots <i className="sb-dot" style={{ background: '#e3b955' }} /> ARADS context <i className="sb-dot" style={{ background: '#ff8b5d' }} /> Láscar control</span><span>{fmt(site.latitude_deg, 6)}° lat · {fmt(site.longitude_deg, 6)}° lon</span></div>
      </div>
    </div>
    <div className="sb-announce">Basemaps (OpenStreetMap, NASA GIBS ASTER relief and MODIS imagery, OpenTopoMap) show Earth only. The Mars reference is intentionally absent from this map. <Ext href={doc('data/SEARCH_SCOPE.md')}>Search scope</Ext></div>
    <div className="sb-dgrid" style={{ gridTemplateColumns: '1fr 1fr', marginTop: 14 }}>
      <div className="sb-panel"><h3>Sampling boundary</h3><p>Original pilot grid: latitude −24.9 to −24.1; longitude −69.9 to −69.1. Four pilot points were chosen for the six-site comparison. ARADS and Láscar used separate source tiles outside that grid.</p></div>
      <div className="sb-panel"><h3>Search limitations</h3><p>No independently verified search polygon, geographic holdout or field-access assessment exists. The map shows measured points, not an evaluated surface between them.</p></div>
    </div>
  </div>
}

function Comparison({ selected, setSelected, windowM, setWindowM, go }: { selected: SiteId; setSelected: (id: SiteId) => void; windowM: '1000' | '2000'; setWindowM: (v: '1000' | '2000') => void; go: (v: View) => void }) {
  const evaluation = evidence.evaluations[windowM]
  const candidate = evaluation.candidates.find((c) => c.site_id === selected)!
  const frontCounts = [1, 2, 3].map((front) => evaluation.candidates.filter((c) => c.pareto_front === front).length)
  const maxes = featureLabels.map((f) => Math.max(...evaluation.candidates.map((c) => c.absolute_differences[f.key])))
  const tone: Tone = candidate.pareto_front === 1 ? 'earth' : candidate.pareto_front === 2 ? 'warn' : 'mars'
  return <div className="sb-layout">
    <Title eyebrow="Measured terrain evidence" lead="An unweighted Pareto comparison of absolute differences from the provisional Mars CTX reference. Front numbers describe this tested set, not field suitability.">Compare the {accent('trade-offs.')}</Title>
    <div className="sb-toolbar">
      <div><span className="sb-eyebrow" style={{ color: 'var(--muted)' }}>Analysis window</span>
        <div className="sb-seg" style={{ marginBottom: 0, marginTop: 6 }} role="group" aria-label="Analysis window"><button aria-pressed={windowM === '1000'} onClick={() => setWindowM('1000')}>1 KM</button><button aria-pressed={windowM === '2000'} onClick={() => setWindowM('2000')}>2 KM</button></div></div>
      <label className="sb-select"><span className="sb-eyebrow" style={{ color: 'var(--muted)' }}>Inspect a measured site</span>
        <select value={selected} onChange={(e) => { if (isSiteId(e.target.value)) setSelected(e.target.value) }}>{siteOrder.map((id) => <option value={id} key={id}>{displayName[id]}</option>)}</select></label>
      <span className="sb-tiny">100 m computational grid · different effective source resolutions</span>
    </div>
    <div className="sb-stats">{frontCounts.map((count, i) => <div className="sb-stat" key={i}><small>Front 0{i + 1}</small><b style={{ fontSize: 28 }}>{count}</b><small>{i === 0 ? 'Four nondominated pilots' : i === 1 ? 'ARADS historical context' : 'Láscar rugged control'}</small></div>)}</div>
    <div className="sb-columns rev" style={{ marginTop: 14 }}>
      <section className="sb-panel"><h3>Absolute difference from Mars · measured / derived</h3>
        <p>Shorter bars mean a smaller difference for that individual feature. Each feature has its own scale; bar length cannot be compared across feature panels.</p>
        {featureLabels.map((f, index) => <div key={f.key} style={{ marginTop: 18 }}>
          <div className="sb-fh"><b>{f.title}</b><span>Difference · {f.unit}</span></div>
          {evaluation.candidates.map((c) => { const id = c.site_id as SiteId; const v = c.absolute_differences[f.key]; return <button key={id} className={`sb-brow ${selected === id ? 'selected' : ''}`} onClick={() => setSelected(id)} aria-pressed={selected === id} aria-label={`${displayName[id]} ${f.title}: ${fmt(v)} ${f.unit}`}>
            <span>{displayName[id]}</span><span className="sb-btrack"><i style={{ width: `${Math.max(2, 100 * v / maxes[index])}%`, background: roleColor(id) }} /></span><b>{fmt(v)}</b></button> })}
        </div>)}
        <p className="sb-tiny" style={{ marginTop: 14 }}>Bars use zero as the origin and the largest observed difference in this six-site set as the panel maximum. <Ext href={doc('docs/METHODS.md')}>Methods</Ext></p>
      </section>
      <aside>
        <div className="sb-panel"><h3>Selected point / {windowM === '1000' ? '1 km' : '2 km'}</h3><b style={{ fontSize: 22 }}>{displayName[selected]}</b> <Pill tone={tone}>Pareto front {candidate.pareto_front}</Pill>
          <div className="sb-crit hd" style={{ gridTemplateColumns: '1fr 60px 60px 60px', marginTop: 14 }}><span>Feature</span><span>Mars</span><span>Earth</span><span>|Δ|</span></div>
          {featureLabels.map((f) => <div className="sb-crit" style={{ gridTemplateColumns: '1fr 60px 60px 60px' }} key={f.key}><span>{f.short} <small>{f.unit}</small></span><span>{fmt(evaluation.mars_reference_features[f.key])}</span><span>{fmt(candidate.features[f.key])}</span><b style={{ color: 'var(--green)' }}>{fmt(candidate.absolute_differences[f.key])}</b></div>)}
          <p className="sb-tiny" style={{ marginTop: 10 }}>Values are rounded for display; fronts use full exported precision.</p></div>
        <div className="sb-announce" style={{ marginTop: 14 }}><b>Interpret with care.</b> All four pilots are nondominated at both windows. The selected front is not a rover-safety rating, a similarity percentage or a unique winner. CTX stereo artifacts and independent elevation accuracy remain unresolved. Matching grid spacing does not prove matching effective source resolution.</div>
        <button className="sb-btn secondary" style={{ marginTop: 14, width: '100%', justifyContent: 'center' }} onClick={() => go('transfer')}>Evaluate analog transfer ↗</button>
      </aside>
    </div>
    <div className="sb-dgrid" style={{ gridTemplateColumns: '1fr 1fr', marginTop: 14 }}>
      <div className="sb-panel"><h3>Uncertainty experiment</h3><p>In 100 hypothetical Mars elevation perturbation trials, complete Pareto ordering was unchanged in 21/100, 27/100 and 30/100 runs at assumed 1 m, 3 m and 5 m SD. These are not calibrated error probabilities.</p></div>
      <div className="sb-panel"><h3>ML decision</h3><p>The physical baseline remains primary. ML-B V1 and V2 failed their scientific acceptance gates; the independent expert-rated site-ranking benchmark was never activated. <Ext href={doc('docs/PHASE5_SCIENTIFIC_CLOSEOUT.md')}>Closeout</Ext></p></div>
    </div>
  </div>
}

function Transfer({ selected }: { selected: SiteId }) {
  return <div className="sb-layout">
    <Title eyebrow="From comparison to experiment" lead="Pilot B is the existing illustrative DEM-route case. The research proposes a future physical field test; no rover has traversed a FieldTwin route.">Where the analogy {accent('breaks.')}</Title>
    <div className="sb-panel sb-intro"><div><div className="sb-eyebrow">Illustrative case / Pilot B</div><h2>A testable route question, <span style={{ color: 'var(--orange)' }}>not a certified site.</span></h2>
      <p>The route algorithm changed paths under assumed DEM-grid grade constraints. Pilot B was chosen for this explanation because the existing benchmark includes it, not because it was proven the best analog.</p></div>
      <div className="sb-stat sb-bigstat"><b>60</b><small>recorded DEM route searches</small><small>20 distance-only + 40 grade-constrained</small></div></div>
    <div className="sb-g2" style={{ gridTemplateColumns: '1fr 1fr' }}>
      <section className="sb-panel"><h3>Route feasibility · hypothetical limits</h3>
        <p>Five predefined endpoint pairs per terrain, 1 km window, 100 m grid. Counts are feasible constrained routes. Mean detour at 3° includes feasible routes only.</p>
        <div className="sb-tablewrap"><table className="ds" aria-label="Precomputed numerical route results"><thead><tr><th>Terrain</th><th>3°</th><th>10°</th><th>3° detour</th></tr></thead><tbody>{routeRows.map((r) => <tr key={r.place}><td><b>{r.place}</b></td><td>{r.at3}</td><td>{r.at10}</td><td>{r.detour}</td></tr>)}</tbody></table></div>
        <p className="sb-tiny">3° and 10° are experimental assumptions, not certified rover limits. “—” means no feasible 3° routes in these five pairs. <Ext href={doc('docs/PHASE4_BASELINE_RESULTS.md')}>Full benchmark</Ext></p></section>
      <section className="sb-panel"><h3>Analog Transfer Matrix · what transfers?</h3>
        {transferRows.map((row) => <div className="sb-matrix" key={row.area}><div><b>{row.area}</b><p>{row.detail}</p></div><Pill tone={row.status === 'DEM-supported' ? 'earth' : row.status === 'Needs evidence' ? 'warn' : 'mars'}>{row.status}</Pill></div>)}
        <p className="sb-tiny"><Ext href={doc('docs/ANALOG_TRANSFER_MATRIX.md')}>Read the full transfer matrix</Ext></p></section>
    </div>
    <div className="sb-panel" style={{ marginTop: 14 }}><div className="sb-eyebrow">Proposed / not performed</div><h2 style={{ margin: '8px 0' }}>A future field protocol</h2>
      <p>Selected map point: {displayName[selected]}. The existing numerical route example remains Pilot B regardless of map selection. Any physical test requires a fresh site-specific plan.</p>
      <div className="sb-steps">{protocol.map(([n, t, d]) => <div key={n}><span>{n}</span><b>{t}</b><p>{d}</p></div>)}</div></div>
    <div className="sb-dgrid" style={{ gridTemplateColumns: '1fr 1fr', marginTop: 14 }}>
      <div className="sb-panel"><h3>Stress test, not calibration</h3><p>4,840 original and synthetic-perturbation route searches tested numerical sensitivity. Assumed elevation errors are not measured DEM accuracy, and search frequencies are not rover-safety probabilities.</p></div>
      <div className="sb-panel"><h3>Evidence and reproducibility</h3><p>Review the <Ext href={doc('docs/LIMITATIONS.md')}>limitations</Ext>, <Ext href={doc('docs/PHASE5_SCIENTIFIC_CLOSEOUT.md')}>scientific closeout</Ext> and <Ext href={repo}>source repository</Ext>.</p></div>
    </div>
  </div>
}

export default function App() {
  const [view, setView] = useState<View>(initialView)
  const [selected, setSelected] = useState<SiteId>('PILOT_B')
  const [windowM, setWindowM] = useState<'1000' | '2000'>('1000')
  const [theme, setTheme] = useState<'dark' | 'light'>(() => { try { return localStorage.getItem('sb-theme-v3') === 'light' ? 'light' : 'dark' } catch { return 'dark' } })
  const evaluation = useMemo(() => evidence.evaluations[windowM], [windowM])
  useEffect(() => { document.documentElement.dataset.theme = theme; try { localStorage.setItem('sb-theme-v3', theme) } catch { /* storage unavailable */ } }, [theme])
  useEffect(() => { const onHash = () => setView(initialView()); window.addEventListener('hashchange', onHash); return () => window.removeEventListener('hashchange', onHash) }, [])
  function go(next: View) { window.location.hash = next; setView(next); window.scrollTo({ top: 0 }) }
  return <div className="sb"><a className="sb-skip" href="#main-content">Skip to content</a><div className="sb-shell">
    <header className="sb-nav">
      <button className="sb-logo" onClick={() => go('mission')} aria-label="SamaBeyond FieldTwin, return to Mission"><svg width="34" height="30" viewBox="0 0 34 30" aria-hidden="true"><ellipse cx="17" cy="15" rx="15" ry="8" transform="rotate(-18 17 15)" fill="none" stroke="#e8672b" strokeWidth="1.2" strokeDasharray="38 12" /><circle cx="26.5" cy="6.5" r="2.4" fill="#e8672b" /><circle cx="17" cy="15" r="6" fill="none" stroke="#e8672b" strokeWidth="1.4" /><path d="M12 14c2-2 3 2 5 0s3-2 5 0M12 17c2-2 3 2 5 0s3-2 5 0" fill="none" stroke="#e8672b" strokeWidth="1" /></svg><span className="sb-wm">Sama<span>Beyond</span></span></button>
      <nav className="sb-links" aria-label="Main navigation">{views.map((v) => <button key={v.id} onClick={() => go(v.id)} aria-current={view === v.id ? 'page' : undefined}>{v.number} / {v.label.toUpperCase()}</button>)}</nav>
      <div className="sb-navr"><div className="sb-indicator">EXPLORATORY · NOT FIELD-VALIDATED</div>
        <button className="sb-theme" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')} aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`} title="Toggle theme"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" strokeWidth="1.4" /><path d="M8 1.5a6.5 6.5 0 0 1 0 13z" fill="currentColor" /></svg></button></div>
    </header>
    <div className="sb-announce" role="note"><b>Evidence status:</b> exploratory terrain comparison · no unique validated analog winner · no physical rover test.</div>
    <main id="main-content" className="sb-step" key={view}>{view === 'mission' ? <Mission go={go} /> : view === 'search' ? <Search selected={selected} setSelected={setSelected} go={go} evaluation={evaluation} /> : view === 'comparison' ? <Comparison selected={selected} setSelected={setSelected} windowM={windowM} setWindowM={setWindowM} go={go} /> : <Transfer selected={selected} />}</main>
    <footer className="sb-foot"><span>SAMABEYOND · FIELDTWIN · NASA SPACE APPS 2026 · BASEMAPS: © OPENSTREETMAP CONTRIBUTORS, NASA GIBS, © OPENTOPOMAP · MARS IMAGE: SOLAR SYSTEM SCOPE, CC BY 4.0, FROM NASA DATA</span><span><Ext href={doc('data/SOURCES.md')}>Data sources</Ext> · <Ext href={doc('docs/METHODS.md')}>Methods</Ext> · <Ext href={doc('docs/VALIDATION.md')}>Validation</Ext> · <Ext href={repo}>Repository</Ext></span></footer>
  </div></div>
}
