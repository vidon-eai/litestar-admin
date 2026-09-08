import { z } from 'zod';

export const QueryParamDtoSchema = z.object({
  page: z.number().default(1),
  pageSize: z.number().default(10)
});

export type QueryParamDto = z.infer<typeof QueryParamDtoSchema>;