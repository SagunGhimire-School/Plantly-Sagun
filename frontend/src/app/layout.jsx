import Link from 'next/link';
import Providers from './providers';
import './globals.css';

export const metadata = { title: 'Plantly', description: 'A place for your plots, seasons and growing notes.' };

export default function RootLayout({ children }) {
  return <html lang="en"><body>
    <a className="skip" href="#main">Skip to content</a>
    <header className="site-header"><Link href="/" className="wordmark">Plantly<span aria-hidden="true">.</span></Link>
      <nav aria-label="Main navigation"><Link href="/pricing">Pricing</Link><Link href="/dashboard">Your garden</Link></nav>
    </header>
    <main id="main"><Providers>{children}</Providers></main>
    <footer><strong>Plantly</strong><p>Local development preview. Scientific planning is not available yet.</p></footer>
  </body></html>;
}
