"use client"

import { datasetOptions } from "@/services/dataset"
import { useSuspenseQuery } from "@tanstack/react-query"

interface KnowledgeListProps {
  datasetId: string
}

export function KnowledgeList({ datasetId }: KnowledgeListProps) {
  const { data } = useSuspenseQuery(datasetOptions(datasetId))
  return (
    <div className="flex h-full flex-col justify-center">
      <div className="flex-1">
        {data.data.collections.map((collection) => (
          <div key={collection.id} className="mb-4">
            <h2 className="text-lg font-semibold">{collection.name}</h2>
          </div>
        ))}
      </div>
    </div>
  )
}
