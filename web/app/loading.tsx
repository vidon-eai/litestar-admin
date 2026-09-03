import { Spinner } from "@/components/ui/spinner"

export default function Loading() {
  return (
    <div className="flex h-full flex-col items-center justify-center p-4">
      <Spinner className="size-8" />
    </div>
  )
}
