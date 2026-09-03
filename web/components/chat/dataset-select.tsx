import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { fetchDatasets } from "@/services/dataset"
import { useQuery } from "@tanstack/react-query"

export function SelectDataset({
  setDatasetId,
  datasetId,
}: {
  setDatasetId: (id: string) => void
  datasetId?: string
}) {
  const datasetsQuery = useQuery({
    queryKey: ["datasets"],
    queryFn: fetchDatasets,
  })
  return (
    <Select
      onValueChange={(val) => {
        if (val) setDatasetId(val)
      }}
      value={datasetId || ""}
    >
      <SelectTrigger className="w-full max-w-48">
        <SelectValue placeholder="Select a dataset" />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          {datasetsQuery.data?.data.items.map((dataset) => (
            <SelectItem key={dataset.id} value={dataset.id}>
              {dataset.name}
            </SelectItem>
          ))}
        </SelectGroup>
      </SelectContent>
    </Select>
  )
}

export function SelectModel({
  setModel,
  model,
}: {
  setModel: (value: string) => void
  model?: string
}) {
  const modelOptions = [
    { value: "ollama:qwen2.5:7b-instruct-q4_K_M", label: "Qwen2.5:7B" },
    { value: "ollama:qwen3:8b", label: "Qwen3:8B" },
  ]
  return (
    <Select
      onValueChange={(val) => {
        if (val) setModel(val)
      }}
      value={model || ""}
    >
      <SelectTrigger className="w-full max-w-48">
        <SelectValue placeholder="Select a model" />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          {modelOptions.map((model) => (
            <SelectItem key={model.value} value={model.value}>
              {model.label}
            </SelectItem>
          ))}
        </SelectGroup>
      </SelectContent>
    </Select>
  )
}
