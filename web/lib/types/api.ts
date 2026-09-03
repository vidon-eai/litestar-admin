import { z } from "zod"

export const ApiResponseSchema = <T extends z.ZodType>(dataSchema: T) =>
  z.object({
    code: z.number().int(),
    status_code: z.number().int(),
    data: dataSchema,
    is_success: z.boolean(),
    detail: z.string(),
    timestamp: z.coerce.date(),
  })

export type ApiResponse<T> = z.infer<
  ReturnType<typeof ApiResponseSchema<z.ZodType<T>>>
>
