"use client";
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
const cat = [{name:"Files",value:120},{name:"Questions",value:45},{name:"Answers",value:30},{name:"Workflows",value:8}];
const trend = [{day:"Mon",files:10,questions:5,users:2},{day:"Tue",files:15,questions:8,users:3},{day:"Wed",files:20,questions:6,users:4}];
export default function Page() {
  return (
    <main className="p-8 space-y-8">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <ResponsiveContainer width="100%" height={250}><BarChart data={cat}><XAxis dataKey="name"/><YAxis/><Tooltip/><Bar dataKey="value" fill="#2563eb"/></BarChart></ResponsiveContainer>
      <ResponsiveContainer width="100%" height={250}><LineChart data={trend}><CartesianGrid strokeDasharray="3 3"/><XAxis dataKey="day"/><YAxis/><Tooltip/><Line dataKey="files" stroke="#2563eb"/><Line dataKey="questions" stroke="#16a34a"/><Line dataKey="users" stroke="#dc2626"/></LineChart></ResponsiveContainer>
    </main>
  );
}
