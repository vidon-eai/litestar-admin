"use client"

import {
  Conversation,
  ConversationContent,
  ConversationEmptyState,
  ConversationScrollButton,
} from "@/components/ai-elements/conversation"
import {
  Message,
  MessageContent,
  MessageResponse,
} from "@/components/ai-elements/message"
import { MessageSquare } from "lucide-react"

const ConversationDemo = ({
  messages,
}: {
  messages: {
    id: string
    role: "user" | "assistant"
    parts: { type: "text"; text: string }[]
  }[]
}) => {
  return (
    <Conversation
      className={`${messages.length === 0 ? "flex-none" : "flex-1"}`}
    >
      <ConversationContent>
        {messages.length === 0 ? (
          <ConversationEmptyState
            icon={<MessageSquare className="size-12" />}
            title="Start a conversation"
            description="Type a message below to begin chatting"
          />
        ) : (
          messages.map((message) => (
            <Message from={message.role} key={message.id}>
              <MessageContent>
                {message.parts.map((part, i) => {
                  switch (part.type) {
                    case "text": // we don't use any reasoning or tool calls in this example
                      return (
                        <MessageResponse key={`${message.id}-${i}`}>
                          {part.text}
                        </MessageResponse>
                      )
                    default:
                      return null
                  }
                })}
              </MessageContent>
            </Message>
          ))
        )}
      </ConversationContent>
      <ConversationScrollButton />
    </Conversation>
  )
}

export default ConversationDemo
