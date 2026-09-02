"use client"

import { useState } from "react"
import ChatInput from "./chat-input"
import ConversationDemo from "./conversation"

export default function Chat() {
    const [messages, setMessages] = useState<
    {
        id: string
        role: "user" | "assistant"
        parts: { type: "text"; text: string }[]
    }[]
  >([])


  return (
    <>
      <ConversationDemo messages={messages} />
      <ChatInput setMessages={setMessages} />
    </>
  )
}
