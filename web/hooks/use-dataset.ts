import { DatasetPayload } from "@/dtos/dataset.dto"
import { datasetService } from "@/services/dataset.service"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"

export const DATASET_KEYS = {
  all: ["datasets"] as const,
  list: (params: Record<string, string | number | boolean | undefined>) =>
    [...DATASET_KEYS.all, "list", params] as const,
  details: () => [...DATASET_KEYS.all, "detail"] as const,
  detail: (id: string) => [...DATASET_KEYS.details(), id] as const,
}

export const useDatasets = (
  params: Record<string, string | number | boolean | undefined>
) => {
  return useQuery({
    queryKey: DATASET_KEYS.list(params),
    queryFn: () => datasetService.getAll(params),
  })
}

export const useDataset = (datasetId: string) => {
  return useQuery({
    queryKey: DATASET_KEYS.detail(datasetId ?? ""),
    queryFn: () => datasetService.getById(datasetId),
    enabled: Boolean(datasetId),
  })
}

export const useCreateDataset = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (datasetPayload: DatasetPayload) =>
      datasetService.create(datasetPayload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: DATASET_KEYS.all })
    },
  })
}

export const useUpdateDataset = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({
      datasetId,
      datasetPayload,
    }: {
      datasetId: string
      datasetPayload: DatasetPayload
    }) => datasetService.update(datasetId, datasetPayload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: DATASET_KEYS.all })
    },
  })
}

export const useDeleteDataset = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => datasetService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: DATASET_KEYS.all })
    },
  })
}
