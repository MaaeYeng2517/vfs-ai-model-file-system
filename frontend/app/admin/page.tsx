"use client";
import { useState } from "react";
export default function Admin() {
  const [u, setU] = useState(""); const [p, setP] = useState("");
  return (
    <main className="p-8 max-w-md mx-auto">
      <h1 className="text-2xl mb-4">Admin Login</h1>
      <input className="border p-2 w-full mb-2" placeholder="username" value={u} onChange={e=>setU(e.target.value)} />
      <input className="border p-2 w-full mb-2" type="password" placeholder="password" value={p} onChange={e=>setP(e.target.value)} />
      <button className="bg-blue-600 text-white px-4 py-2 rounded w-full">Login</button>
    </main>
  );
}
