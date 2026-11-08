import Link from 'next/link';

export default function Pricing() {
  return <section className="narrow"><p className="eyebrow">PRICING</p><h1>Plans are still taking shape.</h1>
    <p>Plantly has no published subscription prices or trial offer yet. There is no checkout, and this local preview does not collect payment.</p>
    <div className="notice"><p>AI planning is not configured yet. Scientific recommendations, live weather and product prices are unavailable.</p></div>
    <Link className="button" href="/">Back to Plantly</Link>
  </section>;
}
