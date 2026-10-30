"use client";
import { useCallback } from "react";
import ReactFlow, { Background, Controls, addEdge, useNodesState, useEdgesState } from "reactflow";
import "reactflow/dist/style.css";

const initialNodes = [{ id: "1", position: { x: 0, y: 0 }, data: { label: "File" } }, { id: "2", position: { x: 200, y: 0 }, data: { label: "Chunk" } }];
const initialEdges = [{ id: "e1-2", source: "1", target: "2" }];

export default function GraphExplorer() {
  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), [setEdges]);
  return (
    <main className="h-screen">
      <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} onConnect={onConnect} fitView>
        <Background />
        <Controls />
      </ReactFlow>
    </main>
  );
}
