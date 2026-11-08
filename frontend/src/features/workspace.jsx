'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useRef } from 'react';

const navigation = [{href:'/dashboard',label:'Your garden'},{href:'/onboarding',label:'Plot setup'}];

export default function Workspace({children}) {
  const path = usePathname();
  const drawer = useRef(null);
  const links = navigation.map(item => <Link key={item.href} href={item.href} aria-current={path === item.href ? 'page' : undefined} onClick={() => drawer.current?.close()}>{item.label}</Link>);
  return <div className="workspace">
    <aside className="workspace-sidebar"><nav aria-label="Garden navigation">{links}</nav></aside>
    <div className="workspace-content"><button className="secondary mobile-menu" onClick={() => drawer.current.showModal()}>Garden menu</button>
      <dialog ref={drawer} className="garden-drawer" aria-label="Garden menu"><button className="secondary" onClick={() => drawer.current.close()}>Close menu</button><nav aria-label="Mobile garden navigation">{links}</nav></dialog>
      {children}
    </div>
  </div>;
}
