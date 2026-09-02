import { customFetch } from "@/lib/fetcher"
import { ApiResponse, DatasetDetail } from "@/types"
import { queryOptions } from "@tanstack/react-query"

export const getDatasets = async () => customFetch("/datasets")

export const login = async (username: string, password: string) => {
  const formData = new URLSearchParams()
  formData.append("username", username)
  formData.append("password", password)

  const response = await customFetch<{
    access_token: string
  }>("/auth/login", {
    method: "POST",
    headers: {
      accept: "application/json",
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData,
  })
  return response
}

export const datasetOptions = queryOptions({
  queryKey: ["datasets"],
  queryFn: async () => {
    const authResponse = await login("admin", "password")

    const dataset_id = '01a05bcb-089b-7d01-a0fa-b7f3d3b9ddd8'
    const response = await customFetch<ApiResponse<DatasetDetail>>(`/datasets/${dataset_id}/documents`, {
      method: "GET",
      headers: {
        accept: "application/json",
        "Content-Type": "application/json",
        'Authorization': `Bearer ${authResponse.access_token}`
      },
    })

    return response
  },
})
