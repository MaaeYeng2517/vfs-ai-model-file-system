"use client";
import { useState } from "react";
export default function CrudForm({ onSubmit }: { onSubmit: (v: string) => void }) {
  const [val, setVal] = useState("");
  return (
    <form className="mb-4 flex gap-2" onSubmit={e => { e.preventDefault(); onSubmit(val); setVal(""); }}>
      <input className="border p-2 flex-1" value={val} onChange={e => setVal(e.target.value)} placeholder="New item" />
      <button className="bg-blue-600 text-white px-4 py-2 rounded">Add</button>
    </form>
  );
}
