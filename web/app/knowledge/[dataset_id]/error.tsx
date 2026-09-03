// app/dataset/[datasetId]/error.tsx
"use client"

import { useEffect } from "react"

export default function DatasetError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // 可在此處發送錯誤日誌到 Sentry 或 console
    console.error("Data fetching error:", error)
  }, [error])

  return (
    <div className="flex h-full flex-col items-center justify-center p-6 text-center">
      <h2 className="text-xl font-bold text-red-600">數據載入失敗</h2>
      <p className="mt-2 text-sm text-gray-600">
        {JSON.stringify(error) || "發生未知錯誤"}
      </p>
      <button
        onClick={() => reset()}
        className="mt-4 rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
      >
        重新嘗試
      </button>
    </div>
  )
}
