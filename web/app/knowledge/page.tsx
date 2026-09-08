import { DatasetDataTable } from "@/components/knowledge/data-table"
import { getQueryClient } from "@/lib/react-query"
import { datasetListOptions } from "@/services/dataset.service"
import { dehydrate, HydrationBoundary, noop } from "@tanstack/react-query"

interface PageProps {
  searchParams: Promise<Record<string, string | number | boolean>>
}

export default async function Page({ searchParams }: PageProps) {
  return (
    <div className="p-4">
      <DatasetDataTable />
    </div>
  )
}
