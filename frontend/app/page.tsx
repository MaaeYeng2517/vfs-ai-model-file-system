export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-white">
      <header className="p-6 flex justify-between items-center">
        <div className="font-bold text-xl">VFS AI Knowledge</div>
        <nav className="space-x-4"><a href="/dashboard" className="hover:underline">Dashboard</a><a href="/admin" className="hover:underline">Admin</a></nav>
      </header>
      <section className="text-center py-20">
        <h1 className="text-5xl font-bold mb-4">AI Knowledge Management System</h1>
        <p className="text-gray-600 mb-8">Virtual File System + AI + Knowledge Base</p>
        <a href="/dashboard" className="bg-blue-600 text-white px-6 py-3 rounded-lg">Get Started</a>
      </section>
      <section className="max-w-5xl mx-auto grid grid-cols-3 gap-6 p-8">
        {[{n:"VFS Core",d:"File storage & versioning",i:"📁"},{n:"AI Runtime",d:"Model execution",i:"🤖"},{n:"Knowledge Base",d:"Docs & chunks",i:"📚"},{n:"Workflow Engine",d:"Automation",i:"⚙️"},{n:"Monitoring",d:"Metrics & health",i:"📊"},{n:"Governance",d:"Audit & compliance",i:"🛡️"}].map(f=>(
          <div key={f.n} className="bg-white rounded-xl shadow p-6"><div className="text-3xl mb-2">{f.i}</div><h3 className="font-semibold mb-2">{f.n}</h3><p className="text-sm text-gray-500">{f.d}</p></div>
        ))}
      </section>

      <section className="max-w-5xl mx-auto p-8">
        <h2 className="text-2xl font-bold mb-4">Blog & Knowledge</h2>
        <div className="grid grid-cols-3 gap-4">
          {["VFS Core Intro","AI Retrieval Tips","Knowledge Graph Basics"].map(t=>(
            <div key={t} className="bg-white rounded-xl shadow p-4"><h3 className="font-semibold">{t}</h3><p className="text-sm text-gray-500">Latest article</p></div>
          ))}
        </div>
      </section>
      <footer className="text-center p-6 text-gray-400">© 2026 VFS AI Engine</footer>
    </main>
  );
}
