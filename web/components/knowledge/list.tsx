"use client"

import { useDataset } from "@/hooks/use-dataset"
import { useParams } from "next/navigation"

export function KnowledgeList() {
  const { dataset_id } = useParams()
  const { data: dataset, isError, error, isLoading } = useDataset(dataset_id + "")

  if(isError) {
    return error.message
  }

  if(isLoading) return <>Loading...</>

  return (
    <div className="flex h-full ">
      <div className="flex-1">
        {dataset?.data?.name}
      
      </div>
    </div>
  )
}
