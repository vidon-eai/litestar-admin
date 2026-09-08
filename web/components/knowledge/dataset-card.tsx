import Link from "next/link"
import { Button } from "../ui/button"
import {
  Card,
  CardAction,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "../ui/card"
import { IconTrash } from "@tabler/icons-react"
import { Dataset } from "@/dtos/dataset.dto"
import { useDeleteDataset } from "@/hooks/use-dataset"
import { toast } from "sonner"
export default function DatasetCard({
  dataset,
  setDataset,
}: {
  dataset: Dataset
  setDataset: (dataset: Dataset) => void
}) {
  const deleteDatasetMutation = useDeleteDataset()

  const handleDeleteDataset = () => {
    deleteDatasetMutation.mutate(dataset.id, {
      onSuccess: (data) => {
        console.log(data)
        toast.success("Dataset has been deleted")
      },
    })
  }

  return (
    <Card size="sm">
      <CardHeader>
        <CardTitle>{dataset.name}</CardTitle>
        <CardDescription>
          {dataset.description || "No description provided."}
        </CardDescription>
        <CardAction>
          <Button variant="destructive" onClick={handleDeleteDataset}>
            <IconTrash />
          </Button>
        </CardAction>
      </CardHeader>
      <CardFooter className="flex items-center justify-between">
        <Button onClick={() => setDataset(dataset)}>Select</Button>
        <Button asChild>
          <Link href={`/knowledge/${dataset.id}`}>View</Link>
        </Button>
      </CardFooter>
    </Card>
  )
}
