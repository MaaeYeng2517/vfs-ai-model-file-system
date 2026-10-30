"use client";
import { useCallback } from "react";
import { useState } from "react";
import ReactFlow, { Background, Controls, addEdge, useNodesState, useEdgesState } from "reactflow";
import "reactflow/dist/style.css";

const initialNodes = [{ id: "1", position: { x: 0, y: 0 }, data: { label: "File" } }, { id: "2", position: { x: 200, y: 0 }, data: { label: "Chunk" } }];
const initialEdges = [{ id: "e1-2", source: "1", target: "2" }];

export default function GraphExplorer() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), [setEdges]);
  const [n, setN] = useState(3);
  const [e, setE] = useState(2);
  const addEdgeBtn = () => { if(nodes.length>=2){ const a=nodes[nodes.length-2].id; const b=nodes[nodes.length-1].id; setEdges((eds)=>[...eds,{id:`e${e}`,source:a,target:b}]); setE(e+1);} };
  const addNode = () => { setNodes((nds) => [...nds, { id: String(n), position: { x: Math.random()*400, y: Math.random()*400 }, data: { label: `Node ${n}` } }]); setN(n+1); };
  return (
    <main className="h-screen">
      <button onClick={addNode} className="absolute z-10 m-2 bg-blue-600 text-white px-3 py-1 rounded">Add Node</button>
      <button onClick={addEdgeBtn} className="absolute z-10 m-2 ml-28 bg-green-600 text-white px-3 py-1 rounded">Add Edge</button>
      <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} onConnect={onConnect} fitView>
        <Background />
        <Controls />
      </ReactFlow>
    </main>
  );
}
