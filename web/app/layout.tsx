import { Geist, Geist_Mono, Inter } from "next/font/google"

import "./globals.css"
import { ThemeProvider } from "@/components/theme-provider"
import { cn } from "@/lib/utils"
import { TooltipProvider } from "radix-ui/tooltip"
import { Metadata } from "next"
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/shared/app-sidebar"
import QueryProviders from "./providers"
import { Toaster } from "@/components/ui/sonner"

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" })

const fontMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
})

export const metadata: Metadata = {
  title: "Chatbot",
  description:
    "This is a chatbot application built with Next.js and TypeScript.",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={cn(
        "antialiased",
        fontMono.variable,
        "font-sans",
        inter.variable
      )}
    >
      <body>
        <QueryProviders>
          <ThemeProvider>
            <SidebarProvider>
              <TooltipProvider>
                <AppSidebar />
                <main className="flex max-h-screen min-h-screen w-full flex-col px-2">
                  {children}
                </main>
                <Toaster />
              </TooltipProvider>
            </SidebarProvider>
          </ThemeProvider>
        </QueryProviders>
      </body>
    </html>
  )
}
