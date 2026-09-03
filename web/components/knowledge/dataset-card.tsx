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
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { deleteDataset } from "@/services/dataset"
import { toast } from "sonner"
export default function DatasetCard({ dataset }) {
  const queryClient = useQueryClient()
  const mutation = useMutation({
    mutationFn: deleteDataset,
    onMutate: () => {},
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["datasets"] })
      toast.success("Dataset has been deleted")
    },
    onError: () => {
      toast.error("Failed to delete dataset")
    },
  })

  const handleDelete = () => {
    mutation.mutate({
      dataset_id: dataset.id,
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
          <Button variant="destructive" onClick={handleDelete}>
            <IconTrash />
          </Button>
        </CardAction>
      </CardHeader>
      <CardFooter className="flex items-center justify-between">
        <div></div>
        <Button asChild>
          <Link href={`/knowledge/${dataset.id}`}>View</Link>
        </Button>
      </CardFooter>
    </Card>
  )
}
