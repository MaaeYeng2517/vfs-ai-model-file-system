export default function DataTable({ rows }: { rows: any[] }) {
  if (!rows || rows.length === 0) return <p className="text-gray-500">No data</p>;
  const cols = Object.keys(rows[0]);
  return (
    <table className="w-full border-collapse border">
      <thead><tr>{cols.map(c => <th key={c} className="border p-2 bg-gray-100">{c}</th>)}</tr></thead>
      <tbody>{rows.map((r,i) => <tr key={i}>{cols.map(c => <td key={c} className="border p-2">{String(r[c])}</td>)}</tr>)}</tbody>
    </table>
  );
}
