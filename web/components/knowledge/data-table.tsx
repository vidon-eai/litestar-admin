"use client"

import { Dataset } from "@/dtos/dataset.dto"
import { useDatasets } from "@/hooks/use-dataset"
import { ApiError } from "@/lib/fetcher"
import { useSearchParams } from "next/navigation"
import { useState } from "react"
import DatasetCard from "./dataset-card"
import { DatasetForm } from "./dataset-form"

export function DatasetDataTable() {
  const [dataset, setDataset] = useState<Dataset>()
  const searchParams = useSearchParams()
  const page = searchParams.get("page") ?? 1
  const pageSize = searchParams.get("pageSize") ?? 10 
  const {
    data: datasets,
    isLoading,
    isError,
    error,
  } = useDatasets({
    page,
    pageSize,
    orderBy: "created_at",
    sortOrder: "desc",
  })

  if (isError) {
    const apiError = error as ApiError
    console.log("錯誤訊息:", apiError.message) // 這裡會印出 "Invalid enum value 100"
    console.log("錯誤細節:", apiError.detail) // 這裡會拿到 detail 陣列

    return (
      <div className="rounded border border-red-200 bg-red-50 p-4 text-red-500">
        <p className="font-bold">請求發生錯誤 ({apiError.status})</p>
        <p>{apiError.message}</p>
      </div>
    )
  }

  if (isLoading) return null

  return (
    <div className="flex flex-col gap-2">
      <DatasetForm dataset={dataset} />
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        {datasets?.data?.items.map((dataset) => (
          <DatasetCard
            key={dataset.id}
            dataset={dataset}
            setDataset={setDataset}
          />
        ))}
      </div>
    </div>
  )
}
