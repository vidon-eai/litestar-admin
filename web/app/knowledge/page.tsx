import { DatasetDataTable } from "@/components/knowledge/data-table"
import { getQueryClient } from "@/lib/react-query"
import { datasetListOptions } from "@/services/dataset"
import { dehydrate, HydrationBoundary, noop } from "@tanstack/react-query"
import { ErrorBoundary } from "next/dist/client/components/error-boundary"

export default async function Page() {
  const queryClient = getQueryClient()

  void queryClient.query(datasetListOptions).catch(noop)

  return (
    <div className="p-4">
      <HydrationBoundary state={dehydrate(queryClient)}>
        <DatasetDataTable />
      </HydrationBoundary>
    </div>
  )
}
