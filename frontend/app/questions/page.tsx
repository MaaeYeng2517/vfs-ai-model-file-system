"use client";
import { useEffect, useState } from "react";
import DataTable from "../../components/DataTable";
import CrudForm from "../../components/CrudForm";
export default function Page() {
  const [rows, setRows] = useState<any[]>([]);
  const load = async () => { const r = await fetch("http://localhost:8000/questions"); setRows(await r.json()); };
  useEffect(() => { load(); }, []);
  return (
    <main className="p-8">
      <h1 className="text-2xl mb-4">Questions</h1>
      <CrudForm onSubmit={async v => { await fetch("http://localhost:8000/questions",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({original_text:v})}); await load(); }} />
      <DataTable rows={rows} />
    </main>
  );
}
