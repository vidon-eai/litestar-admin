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

export const fetchDatasets = async () => {
  const authResponse = await login("admin", "password")

  const response = await customFetch<ApiResponse<DatasetDetail>>(`/datasets`, {
    method: "GET",
    headers: {
      accept: "application/json",
      "Content-Type": "application/json",
      Authorization: `Bearer ${authResponse.access_token}`,
    },
  })

  return response
}

export const datasetListOptions = queryOptions({
  // 將 dataset_id 加入 queryKey，避免不同 dataset 的快取互相衝突
  queryKey: ["datasets"],
  queryFn: async () => {
    const response = await fetchDatasets()

    return response
  },
})

export const datasetOptions = (dataset_id: string) =>
  queryOptions({
    // 將 dataset_id 加入 queryKey，避免不同 dataset 的快取互相衝突
    queryKey: ["datasets", dataset_id],
    queryFn: async () => {
      const authResponse = await login("admin", "password")

      const response = await customFetch<ApiResponse<DatasetDetail>>(
        `/datasets/${dataset_id}/documents`,
        {
          method: "GET",
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
            Authorization: `Bearer ${authResponse.access_token}`,
          },
        }
      )

      return response
    },
  })
