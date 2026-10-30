"use client";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
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
    <div className="h-64 mt-8"><ResponsiveContainer width="100%" height="100%"><PieChart><Pie data={[{name:"txt",value:30},{name:"json",value:20},{name:"xml",value:15},{name:"yml",value:10}]} dataKey="value" nameKey="name" outerRadius={80}>{["#3b82f6","#10b981","#f59e0b","#ef4444"].map((c,i)=><Cell key={i} fill={c}/>)}</Pie></PieChart></ResponsiveContainer></div></main>
  );
}
