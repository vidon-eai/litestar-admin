import { customFetch } from "@/lib/fetcher"
import { queryOptions } from "@tanstack/react-query"
import { login } from "./dataset"

export const chatOptions = queryOptions({
  queryKey: ["chat"],
  queryFn: async () => {
    const authResponse = await login("admin", "password")

    const dataset_id = "01a05bcb-089b-7d01-a0fa-b7f3d3b9ddd8"
    const response = await customFetch(`/datasets/chat`, {
      method: "POST",
      headers: {
        accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${authResponse.access_token}`,
      },
      body: JSON.stringify({
        dataset_id: dataset_id,
        question: "請問這個知識庫的主要內容是什麼？",
        llm: "ollama:qwen2.5:7b-instruct-q4_K_M",
      }),
    })

    return response
  },
})

export const sendMessage = async ({
  question,
  dataset_id,
  llm,
}: {
  question: string
  dataset_id?: string
  llm?: string
}) => {
  const authResponse = await login("admin", "password")

  const response = await customFetch(`/datasets/chat`, {
    method: "POST",
    headers: {
      accept: "application/json",
      "Content-Type": "application/json",
      Authorization: `Bearer ${authResponse.access_token}`,
    },
    body: JSON.stringify({
      dataset_id: dataset_id || "01a05bcb-089b-7d01-a0fa-b7f3d3b9ddd8",
      question: question,
      llm: llm || "ollama:qwen2.5:7b-instruct-q4_K_M",
    }),
  })

  return response
}
