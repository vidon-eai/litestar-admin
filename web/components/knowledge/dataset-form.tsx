import {
  Dataset,
  DatasetPayload,
  DatasetPayloadSchema,
} from "@/dtos/dataset.dto"
import { useCreateDataset, useUpdateDataset } from "@/hooks/use-dataset"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Field, FieldDescription, FieldGroup, FieldLabel } from "../ui/field"
import { Input } from "../ui/input"
import { Button } from "../ui/button"
import { Textarea } from "../ui/textarea"
import { useEffect } from "react"

export function DatasetForm({ dataset }: { dataset?: Dataset }) {
  const { mutate: createDataset, isPending: createPending } = useCreateDataset()
  const { mutate: updateDataset, isPending: updatePending } = useUpdateDataset()

  const {
    register,
    handleSubmit,
    reset,
    setValues,
    formState: { errors },
  } = useForm<DatasetPayload>({
    resolver: zodResolver(DatasetPayloadSchema), // 導入 Zod 驗證器
    defaultValues: {
      name: dataset?.name,
      description: dataset?.description,
    },
  })

  useEffect(() => {
    if (!dataset) return
    setValues(dataset)
  }, [dataset, setValues])

  // 2. 表單驗證通過後觸發 Mutation
  const onSubmit = (data: DatasetPayload) => {
    if (dataset) {
      updateDataset(
        {
          datasetId: dataset.id,
          datasetPayload: data,
        },
        {
          onSuccess: () => {
            reset()
          },
          onError: (err) => {
            alert(err.message)
          },
        }
      )
    } else {
      createDataset(data, {
        onSuccess: () => {
          reset()
        },
        onError: (err) => {
          alert(err.message)
        },
      })
    }
  }

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="max-w-md space-y-4 rounded border p-4"
    >
      <FieldGroup>
        <Field data-invalid={!!errors.name}>
          <FieldLabel htmlFor="name">
            Knowledge Name <span className="text-destructive">*</span>
          </FieldLabel>
          <Input
            {...register("name")}
            id="name"
            placeholder="Input knowledge name"
            aria-invalid={!!errors.name}
          />
          {errors.name && (
            <FieldDescription className="text-destructive">
              {errors.name.message}
            </FieldDescription>
          )}
        </Field>
        <Field data-invalid={!!errors.description}>
          <FieldLabel htmlFor="description">Description</FieldLabel>
          <Textarea
            {...register("description")}
            id="description"
            placeholder="Input knowledge description"
            aria-invalid={!!errors.description}
          />
          {errors.description && (
            <FieldDescription className="text-destructive">
              {errors.description.message}
            </FieldDescription>
          )}
        </Field>
      </FieldGroup>

      <Button type="submit" disabled={createPending || updatePending}>
        {createPending || updatePending
          ? "處理中..."
          : dataset
            ? "Update"
            : "Create"}
      </Button>
    </form>
  )
}
