import { API_ENDPOINTS } from "@/config/constants"
import { DatasetPayload, Dataset } from "@/dtos/dataset.dto"
import { api } from "@/lib/fetcher"
import { ApiResponse } from "@/lib/types/api"

export const datasetService = {
  getAll: async (
    queryParams?: Record<string, string | number | boolean | undefined>
  ) => {
    const authResponse = await login("admin", "password")
    const response = await api.get<
      ApiResponse<{
        items: Dataset[]
        limit: number
        offset: number
        total: number
      }>
    >(API_ENDPOINTS.DATASETS, {
      headers: {
        Authorization: `Bearer ${authResponse.access_token}`,
      },
      params: queryParams,
    })

    return response
  },
  getById: async (id: string) => {
    const authResponse = await login("admin", "password")

    const response = await api.get<ApiResponse<Dataset>>(
      `${API_ENDPOINTS.DATASETS}/${id}/documents`,
      {
        headers: {
          Authorization: `Bearer ${authResponse.access_token}`,
        },
      }
    )
    return response
  },

  create: async (params: DatasetPayload) => {
    const authResponse = await login("admin", "password")
    const response = await api.post(`/datasets`, params, {
      headers: {
        Authorization: `Bearer ${authResponse.access_token}`,
      },
    })
    return response
  },

  update: async (id: string, params: DatasetPayload) => {
    const authResponse = await login("admin", "password")
    const response = await api.patch(`/datasets/${id}`, params, {
      headers: {
        Authorization: `Bearer ${authResponse.access_token}`,
      },
    })
    return response
  },

  delete: async (id: string) => {
    const authResponse = await login("admin", "password")

    const response = await api.delete(`/datasets/${id}`, {
      headers: {
        Authorization: `Bearer ${authResponse.access_token}`,
      },
    })

    return response
  },
}

export const login = async (username: string, password: string) => {
  const formData = new URLSearchParams()
  formData.append("username", username)
  formData.append("password", password)

  const response = await api.post<{
    access_token: string
  }>("/auth/login", formData, {
    method: "POST",
  })
  return response
}
