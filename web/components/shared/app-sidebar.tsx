"use client"

import * as React from "react"
import { IconBrandLine, IconLibrary } from '@tabler/icons-react';
import {
  Sidebar,
  SidebarContent,
} from "@/components/ui/sidebar"
import { NavMain } from "./nav-main"

const data = {
  navMain: [
    {
      title: "Chat",
      url: "/chat",
      icon: IconBrandLine,
    },
    {
      title: "Knowledge",
      url: "/knowledge",
      icon: IconLibrary,
    },
  ],
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="offcanvas" {...props}>
      <SidebarContent>
        <NavMain items={data.navMain} />
      </SidebarContent>
    </Sidebar>
  )
}
