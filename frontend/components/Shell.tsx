"use client";
import { usePathname } from "next/navigation";
import Link from "next/link";
const pages = ["dashboard","file-system","ai-models","datasets","knowledge","questions","retrieval","context","ai-runtime","verification","memory","lineage","workflows","monitoring","governance","file-detail","block-explorer","graph-explorer","ai-search","admin"];
export default function Shell({ children }: { children: React.ReactNode }) {
  const path = usePathname();
  const show = path !== "/";
  return (
    <div className="flex min-h-screen">
      {show && <aside className="w-56 bg-gray-900 text-white p-4 space-y-2">
        <div className="font-bold text-lg mb-4">VFS AI</div>
        {pages.map(p => <Link key={p} href={`/${p}`} className="block hover:text-blue-300 capitalize">{p.replace("-"," ")}</Link>)}
      </aside>}
      <div className="flex-1 flex flex-col">
        <header className="bg-white shadow p-4 font-semibold">VFS AI Knowledge System</header>
        <main className="flex-1 p-6">{children}</main>
        <footer className="bg-gray-100 p-3 text-center text-sm text-gray-500">© 2026 VFS AI Engine</footer>
      </div>
    </div>
  );
}
