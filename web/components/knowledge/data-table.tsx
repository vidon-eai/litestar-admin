"use client"

import { datasetListOptions } from "@/services/dataset"
import { useSuspenseQuery } from "@tanstack/react-query"

export function DatasetDataTable() {
  const { data } = useSuspenseQuery(datasetListOptions)

  return (
    <div className="flex h-full flex-col justify-center">
      {JSON.stringify(data)}
    </div>
  )
}
