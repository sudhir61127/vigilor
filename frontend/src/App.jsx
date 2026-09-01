import { useMemo, useState } from "react";

const defaultProfile = { name: "Aarav", age: 32, monthly_income: 120000, monthly_expenses: 75000, emergency_fund: 180000, risk_tolerance: "moderate", tax_bracket: 20, dependents: 1, assets: [{ name: "Index funds", value: 650000, category: "equity" }, { name: "Savings", value: 120000, category: "cash" }], liabilities: [{ name: "Car loan", balance: 420000, interest_rate: 10.5, monthly_payment: 12500 }], goals: [{ name: "Home down payment", target_amount: 2000000, current_amount: 400000, years_remaining: 5, priority: 1 }] };
const rupees = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 });
const API = "http://localhost:8000/api/v1";

export default function App() {
  const [profile, setProfile] = useState(defaultProfile);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const numbers = useMemo(() => ({ income: profile.monthly_income, expenses: profile.monthly_expenses, reserve: profile.emergency_fund }), [profile]);
  const update = (key, value) => setProfile(p => ({ ...p, [key]: key === "name" || key === "risk_tolerance" ? value : Number(value) }));
  async function analyse() {
    setLoading(true);
    try { const r = await fetch(`${API}/analysis`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(profile) }); setAnalysis(await r.json()); }
    catch { setAnalysis({ error: "Could not reach the API. Start FastAPI on port 8000." }); }
    finally { setLoading(false); }
  }
  const twin = analysis?.digital_twin;
  return <main>
    <nav><span className="brand">FINARCH <i>AI</i></span><span>Decision engine</span><button onClick={analyse}>{loading ? "Analyzing…" : "Run analysis"}</button></nav>
    <section className="hero"><p className="eyebrow">YOUR AUTONOMOUS FINANCIAL DECISION ENGINE</p><h1>What is the best thing<br />to do with your money <em>now?</em></h1><p>Model your financial life, compare trade-offs, and get an explainable next action.</p></section>
    <section className="layout"><aside><h2>Financial snapshot</h2><label>Name<input value={profile.name} onChange={e => update("name", e.target.value)} /></label><label>Monthly income<input type="number" value={numbers.income} onChange={e => update("monthly_income", e.target.value)} /></label><label>Monthly expenses<input type="number" value={numbers.expenses} onChange={e => update("monthly_expenses", e.target.value)} /></label><label>Emergency reserve<input type="number" value={numbers.reserve} onChange={e => update("emergency_fund", e.target.value)} /></label><label>Risk tolerance<select value={profile.risk_tolerance} onChange={e => update("risk_tolerance", e.target.value)}><option>conservative</option><option>moderate</option><option>aggressive</option></select></label><button className="primary" onClick={analyse}>Generate my plan</button></aside>
      <div className="content">{!analysis && <div className="empty"><div className="orb">₹</div><h2>Your financial twin is waiting</h2><p>Use the sample profile or edit your snapshot, then run a decision analysis.</p></div>}{analysis?.error && <div className="empty"><h2>{analysis.error}</h2></div>}{twin && <><div className="metrics"><Metric label="Net worth" value={rupees.format(twin.net_worth)} /><Metric label="Monthly surplus" value={rupees.format(twin.monthly_cash_flow)} /><Metric label="Health score" value={`${twin.financial_health_score}/100`} /><Metric label="Emergency cover" value={`${twin.emergency_months} mo`} /></div><article className="recommendation"><p className="eyebrow">TOP DECISION · {analysis.recommendations.confidence_score}% CONFIDENCE</p><h2>{analysis.recommendations.top_recommendation.action}</h2><p>{analysis.recommendations.top_recommendation.why}</p><div className="impact">{analysis.recommendations.top_recommendation.expected_impact}</div><small>Trade-off: {analysis.recommendations.top_recommendation.tradeoff}</small></article><div className="two"><article><h3>Risk lens <b>{analysis.risk.level}</b></h3><p>Overall risk score: {analysis.risk.overall_risk_score}/100</p><p>Liquidity risk: {analysis.risk.liquidity_risk}</p><p>Diversification: {analysis.risk.diversification}</p></article><article><h3>Alternatives</h3>{analysis.recommendations.alternatives.slice(0, 4).map(a => <p className="alternative" key={a.action}>{a.action}<span>›</span></p>)}</article></div><p className="disclaimer">{analysis.recommendations.disclaimer}</p></>}</div>
    </section></main>;
}
function Metric({ label, value }) { return <article className="metric"><span>{label}</span><strong>{value}</strong></article>; }
