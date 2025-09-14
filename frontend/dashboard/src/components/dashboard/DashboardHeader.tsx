// DashboardHeader.tsx
// If you're on Next.js app router, keep this. In Vite it doesn't hurt.
"use client"

import { LogOut, User, Menu } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { useAuth } from "@/contexts/AuthContext"
import { useToast } from "@/hooks/use-toast"
import * as React from "react"

interface DashboardHeaderProps {
  onToggleSidebar?: () => void
}

export const DashboardHeader: React.FC<DashboardHeaderProps> = ({
  onToggleSidebar,
}) => {
  const { user, logout } = useAuth()
  const { toast } = useToast()

  const getInitials = React.useCallback(() => {
    const name = (user as any)?.name as string | undefined
    if (name && name.trim().length > 0) {
      return name
        .trim()
        .split(/\s+/)
        .map((n) => n[0]?.toUpperCase())
        .join("")
        .slice(0, 2)
    }
    const email = (user as any)?.email as string | undefined
    return email?.[0]?.toUpperCase() ?? "U"
  }, [user])

  const handleLogout = async () => {
    // if your logout is async, await it so the toast doesn't get lost on navigation
    try {
      await Promise.resolve(logout())
      toast({
        title: "Logged out",
        description: "You have been successfully logged out.",
        variant: "destructive",
        // Fallback class override in case variant isn't forwarded by <Toaster />
        className:
          "bg-destructive text-destructive-foreground border-destructive",
      })
    } catch (e) {
      toast({
        title: "Logout failed",
        description: "Please try again.",
        variant: "destructive",
      })
    }
  }

  return (
    <header className="fixed left-0 right-0 top-0 z-40 border-b border-gray-200 bg-white px-6 py-4 shadow-sm">
      <div className="flex items-center justify-between">
        {/* Left: burger + brand */}
        <div className="flex items-center space-x-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={onToggleSidebar ?? (() => {})}
            className="p-2"
            aria-label="Toggle sidebar"
          >
            <Menu className="h-5 w-5" />
          </Button>

          <div>
            <h1 className="text-xl font-bold text-gray-900">MJ Home Dashboard</h1>
            <p className="text-sm text-gray-500">
              Real Estate Market Insights and Targeted Marketing Strategy
            </p>
          </div>
        </div>

        {/* Right: profile menu */}
        <div className="flex items-center space-x-4">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="flex items-center space-x-2 px-3">
                <Avatar className="h-8 w-8">
                  <AvatarImage src="/placeholder.svg" alt="User" />
                  <AvatarFallback>{getInitials()}</AvatarFallback>
                </Avatar>
                <div className="hidden text-left md:block">
                  <p className="text-sm font-medium">
                    {(user as any)?.name ?? "User"}
                  </p>
                  <p className="text-xs text-gray-500">Admin</p>
                </div>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56 bg-white">
              <DropdownMenuItem>
                <User className="mr-2 h-4 w-4" />
                Profile
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              {/* Radix <DropdownMenuItem> fires onSelect more reliably than onClick */}
              <DropdownMenuItem
                onSelect={(e) => {
                  e.preventDefault()
                  handleLogout()
                }}
                className="text-red-600 focus:text-red-700"
              >
                <LogOut className="mr-2 h-4 w-4" />
                Log Out
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  )
}
