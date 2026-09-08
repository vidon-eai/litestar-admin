import { z } from "zod"

export const DatasetSchema = z.object({
  id: z.uuidv7(),
  created_at: z.iso.datetime(),
  updated_at: z.iso.datetime(),
  created_by: z.uuidv7(),
  updated_by: z.uuidv7(),
  name: z.string(),
  description: z.string(),
})

export type Dataset = z.infer<typeof DatasetSchema>

export const DatasetPayloadSchema = z.object({
  created_by: z.uuidv7().optional(),
  name: z.string().min(1, "Name can not be empty."),
  description: z.string("Required"),
})

export type DatasetPayload = z.infer<typeof DatasetPayloadSchema>
