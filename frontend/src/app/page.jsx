import Link from 'next/link';
import ServiceStatus from '../features/service-status';

export default function Home() {
  return <>
    <section className="hero"><p className="eyebrow">FOR HOME GARDENERS & SMALL GROWERS</p>
      <h1>A place to start<br />your growing season.</h1>
      <p>Keep your plot details and growing notes together. Plantly is being built to turn reviewed research into a plan for your season.</p>
      <Link className="button" href="/dashboard">Open your garden</Link>
    </section>
    <section className="narrow"><h2>Start with what you know.</h2><p>Your own inputs come first. Missing soil measurements stay unknown, and recommendations stay unavailable until the evidence is reviewed.</p>
      <ServiceStatus />
    </section>
  </>;
}
