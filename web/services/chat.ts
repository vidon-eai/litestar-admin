import { customFetch } from "@/lib/fetcher"
import { login } from "./dataset"

const DATASET_ID = "01a06267-e871-7b43-89e1-7598df9bf25f"

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
      dataset_id: dataset_id || DATASET_ID,
      question: question,
      llm: llm || "ollama:qwen3:8b",
    }),
  })

  return response
}
