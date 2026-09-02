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

export function SelectDemo({
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
