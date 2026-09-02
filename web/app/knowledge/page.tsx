import { KnowledgeList } from "@/components/knowledge/list"
import { getQueryClient } from "@/lib/react-query"
import { datasetOptions } from "@/services/dataset"
import { dehydrate, HydrationBoundary, noop } from "@tanstack/react-query"

export default async function Page() {
  const queryClient = getQueryClient()

  void queryClient.query(datasetOptions).catch(noop)

  return (
    <div className="flex h-full flex-col justify-center">
      <HydrationBoundary state={dehydrate(queryClient)}>
        <KnowledgeList />
      </HydrationBoundary>
    </div>
  )
}
