"use client";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
const data = [{ name: "Files", value: 120 }, { name: "Users", value: 8 }, { name: "Storage GB", value: 42 }, { name: "DB Tables", value: 24 }];
export default function Dashboard() {
  return (
    <main className="p-8">
      <h1 className="text-2xl mb-4">Dashboard</h1>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}><XAxis dataKey="name" /><YAxis /><Tooltip /><Bar dataKey="value" fill="#3b82f6" /></BarChart>
        </ResponsiveContainer>
      </div>
    </main>
  );
}
