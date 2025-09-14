// DashboardSidebar.tsx
"use client"

import * as React from "react"
import { BarChart3, TrendingUp, Upload, Settings } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

interface DashboardSidebarProps {
  activeSection: string
  onSectionChange: (section: string) => void
  collapsed: boolean
}

type NavItem = {
  id: string
  label: string
  icon: React.ComponentType<React.SVGProps<SVGSVGElement>>
}

const navigationItems: NavItem[] = [
  { id: "overview",           label: "Overview",          icon: BarChart3 },
  { id: "combined-insights",  label: "Combined Insights", icon: TrendingUp },
  { id: "data-upload",        label: "Data Upload",       icon: Upload },
  { id: "settings",           label: "Settings",          icon: Settings },
]

export const DashboardSidebar: React.FC<DashboardSidebarProps> = ({
  activeSection,
  onSectionChange,
  collapsed,
}) => {
  return (
    <aside
      className={cn(
        "fixed left-0 top-[73px] bottom-0 z-30 border-r border-gray-200 bg-white transition-all duration-300",
        collapsed ? "w-16" : "w-64"
      )}
      aria-label="Sidebar"
    >
      <div className="flex h-full flex-col">
        {/* Navigation */}
        <TooltipProvider delayDuration={150}>
          <nav className="flex-1 space-y-2 p-4">
            {navigationItems.map((item) => {
              const Icon = item.icon
              const isActive = activeSection === item.id

              const button = (
                <Button
                  key={item.id}
                  type="button"
                  variant={isActive ? "default" : "ghost"}
                  className={cn(
                    "w-full justify-start",
                    collapsed ? "px-2" : "px-4",
                    isActive && "bg-blue-600 text-white hover:bg-blue-700"
                  )}
                  onClick={() => onSectionChange(item.id)}
                  aria-current={isActive ? "page" : undefined}
                  aria-label={collapsed ? item.label : undefined}
                >
                  <Icon className={cn("h-5 w-5", collapsed ? "" : "mr-3")} />
                  {!collapsed && <span>{item.label}</span>}
                </Button>
              )

              return collapsed ? (
                <Tooltip key={item.id}>
                  <TooltipTrigger asChild>{button}</TooltipTrigger>
                  <TooltipContent side="right">{item.label}</TooltipContent>
                </Tooltip>
              ) : (
                button
              )
            })}
          </nav>
        </TooltipProvider>

        {/* User Info at Bottom */}
        {!collapsed && (
          <div className="border-t border-gray-200 p-4">
            <div className="space-y-1 text-xs text-gray-500">
              <p>Logged in as</p>
              <p className="font-medium text-gray-900">Mike Johnson</p>
              <p>Real Estate Analyst</p>
            </div>
          </div>
        )}
      </div>
    </aside>
  )
}
