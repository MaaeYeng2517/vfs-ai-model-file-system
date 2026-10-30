"use client";
import { useEffect, useState } from "react";
import DataTable from "../../components/DataTable";
export default function Page() {
  const [rows, setRows] = useState([]);
  useEffect(() => { fetch("http://localhost:8000/api/vfs/files").then(r=>r.json()).then(setRows).catch(()=>{}); }, []);
  return <main className="p-8"><h1 className="text-2xl mb-4">Files</h1><DataTable rows={rows} /></main>;
}
