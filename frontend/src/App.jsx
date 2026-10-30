import { useEffect, useState } from "react";

export default function App() {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [health, setHealth] = useState(null);
  const [usage, setUsage] = useState([]);
  const [q, setQ] = useState("");

  const load = async () => {
    const r = await fetch("/api/vfs/files");
    setFiles(await r.json());
  };
  const loadUsage = async () => {
    const r = await fetch("/api/vfs/usage");
    setUsage(await r.json());
  };
  useEffect(() => {
    load();
    loadUsage();
    fetch("/health").then(r => r.json()).then(setHealth).catch(() => setHealth({ status: "down" }));
  }, []);

  const onUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const form = new FormData();
    form.append("file", file);
    setUploading(true);
    await fetch("/api/vfs/upload", { method: "POST", body: form });
    setUploading(false);
    load();
  };

  const logQuery = async () => {
    if (!q.trim()) return;
    await fetch("/api/vfs/usage", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: q, file_ids: files.map(f => f.id) }),
    });
    setQ("");
    loadUsage();
  };

  return (
    <div style={{ padding: 24, fontFamily: "sans-serif" }}>
      <h1>VFS AI Engine — Tracking</h1>
      <section style={{ marginBottom: 16, padding: 12, border: "1px solid #ddd", borderRadius: 8 }}>
        <h2>System Status</h2>
        <p>Backend: {health ? health.status : "checking..."}</p>
        <p>Files tracked: {files.length}</p>
        <p>Total bytes: {files.reduce((a, f) => a + (f.size || 0), 0)}</p>
      </section>
      <section style={{ marginBottom: 16 }}>
        <h2>File Explorer</h2>
        <input type="file" onChange={onUpload} disabled={uploading} />
        <ul>
          {files.map(f => (
            <li key={f.id}>
              {f.name} ({f.size} bytes, {f.mime_type}){" "}
              <a href={`/api/vfs/download/${f.id}`}>download</a>{" "}
              <button onClick={async () => { await fetch(`/api/vfs/files/${f.id}`, { method: "DELETE" }); load(); }}>delete</button>
            </li>
          ))}
        </ul>
      </section>
      <section>
        <h2>Query → File Trace</h2>
        <input value={q} onChange={e => setQ(e.target.value)} placeholder="question" />
        <button onClick={logQuery}>log</button>
        <ul>
          {usage.map((u, i) => (
            <li key={i}>{u.query} → files: {(u.file_ids || []).join(", ")}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}
EOF
echo ok