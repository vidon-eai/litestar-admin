import { KnowledgeList } from "@/components/knowledge/list"
import { getQueryClient } from "@/lib/react-query"
import { datasetOptions } from "@/services/dataset"
import { dehydrate, HydrationBoundary, noop } from "@tanstack/react-query"

interface PageProps {
  params: Promise<{
    dataset_id: string
  }>
}

export default async function Page({ params }: PageProps) {
  const { dataset_id } = await params
  const queryClient = getQueryClient()

  void queryClient.query(datasetOptions(dataset_id)).catch(noop)

  return (
    <div className="flex h-full flex-col justify-center">
      <HydrationBoundary state={dehydrate(queryClient)}>
        <KnowledgeList datasetId={dataset_id} />
      </HydrationBoundary>
    </div>
  )
}
