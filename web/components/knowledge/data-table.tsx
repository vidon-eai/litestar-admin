"use client"

import { datasetListOptions } from "@/services/dataset"
import { useSuspenseQuery } from "@tanstack/react-query"
import DatasetCard from "./dataset-card"

export function DatasetDataTable() {
  const { data } = useSuspenseQuery(datasetListOptions)

  return (
    <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
      {data.data.items.map((dataset) => (
        <DatasetCard key={dataset.id} dataset={dataset} />
      ))}
    </div>
  )
}
