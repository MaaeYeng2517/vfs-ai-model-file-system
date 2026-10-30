"use client";
import DataTable from "../../components/DataTable";
import CrudForm from "../../components/CrudForm";
const sample = [{id:1,name:"sample",status:"active"}];
export default function Page() {
  return <main className="p-8"><h1 className="text-2xl mb-4 capitalize">verification</h1><CrudForm onSubmit={()=>{}} /><DataTable rows={sample} /></main>;
}
