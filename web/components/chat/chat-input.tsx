"use client"

import {
  PromptInput,
  PromptInputBody,
  type PromptInputMessage,
  PromptInputSubmit,
  PromptInputTextarea,
  PromptInputFooter,
  PromptInputTools,
} from "@/components/ai-elements/prompt-input"
import { sendMessage } from "@/services/chat"
import { useMutation } from "@tanstack/react-query"
import { useState } from "react"
import { Shimmer } from "../ai-elements/shimmer"
import { SelectDemo } from "./ dataset-select"

const ChatInput = ({
  setMessages,
}: {
  setMessages?: React.Dispatch<
    React.SetStateAction<
      {
        id: string
        role: "user" | "assistant"
        parts: { type: "text"; text: string }[]
      }[]
    >
  >
}) => {
  const [text, setText] = useState<string>("")
  const [datasetId, setDatasetId] = useState<string>()
  const [status, setStatus] = useState<
    "submitted" | "streaming" | "ready" | "error"
  >("ready")

  const mutation = useMutation({
    mutationFn: sendMessage,
    onMutate: () => {
      setStatus("streaming")

      setMessages?.((prevMessages) => [
        ...prevMessages,
        {
          id: crypto.randomUUID(),
          role: "user",
          parts: [{ type: "text", text }],
        },
      ])
      setText("")
    },
    onSuccess: (data) => {
      const message = data?.data.messages.find(
        (m) => m.type === "ai" && m.tool_calls.length === 0
      )
      setMessages?.((prevMessages) => [
        ...prevMessages,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          parts: [{ type: "text", text: message?.content || "" }],
        },
      ])
      setStatus("ready")
    },
    onError: () => {
      setStatus("error")
    },
  })

  const handleSubmit = (message: PromptInputMessage) => {
    const hasText = Boolean(message.text)
    const hasAttachments = Boolean(message.files?.length)

    if (!(hasText || hasAttachments)) {
      return
    }

    mutation.mutate({
      question: message.text,
      dataset_id: datasetId,
    })
  }

  return (
    <>
      {status === "streaming" && <Shimmer duration={6}>Loading...</Shimmer>}
      <PromptInput
        onSubmit={handleSubmit}
        className="my-4 shrink-0"
        globalDrop
        multiple
      >
        <PromptInputBody>
          <PromptInputTextarea
            onChange={(e) => setText(e.target.value)}
            value={text}
          />
        </PromptInputBody>
        <PromptInputFooter>
          <PromptInputTools>
            <SelectDemo setDatasetId={setDatasetId} datasetId={datasetId} />
          </PromptInputTools>
          <PromptInputSubmit
            disabled={status === "streaming"}
            status={status}
          />
        </PromptInputFooter>
      </PromptInput>
    </>
  )
}

export default ChatInput
