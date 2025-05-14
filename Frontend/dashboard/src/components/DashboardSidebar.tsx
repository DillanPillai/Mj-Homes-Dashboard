
import React from "react";
import { Button } from "@/components/ui/button";
import { 
  LayoutDashboard, 
  Search, 
  ListCheck, 
  Settings, 
  Users
} from "lucide-react";
import ThemeToggle from "@/components/ThemeToggle";
import { useAuth } from "@/contexts/AuthContext";
import { Link } from "react-router-dom";
import MJHomeLogo from "./MJHomeLogo";

interface SidebarItemProps {
  icon: React.ReactNode;
  label: string;
  active?: boolean;
  href: string;
}

const SidebarItem = ({ icon, label, active = false, href }: SidebarItemProps) => (
  <Link to={href} className="w-full">
    <Button
      variant={active ? "default" : "ghost"}
      size="lg"
      className={`w-full justify-start gap-3 mb-1 ${
        active 
          ? "bg-primary text-primary-foreground" 
          : "hover:bg-secondary"
      }`}
    >
      {icon}
      <span>{label}</span>
      {active && <div className="absolute left-0 top-1/2 h-8 w-1 -translate-y-1/2 rounded-r-md bg-accent" />}
    </Button>
  </Link>
);

const DashboardSidebar = () => {
  const { user, logout } = useAuth();
  
  return (
    <div className="h-screen w-64 flex flex-col bg-sidebar dark:bg-sidebar border-r border-border p-4">
      <div className="flex justify-center mb-6 py-2">
        <MJHomeLogo />
      </div>
      
      <div className="space-y-6 flex-1">
        <div>
          <p className="text-xs font-semibold text-muted-foreground mb-2 px-4">MAIN</p>
          <nav className="space-y-0.5">
            <SidebarItem 
              icon={<LayoutDashboard size={18} />} 
              label="Dashboard" 
              active={true}
              href="/"
            />
            <SidebarItem 
              icon={<Search size={18} />} 
              label="New Scraper"
              href="/new-scraper"
            />
            <SidebarItem 
              icon={<ListCheck size={18} />} 
              label="History"
              href="/history"
            />
          </nav>
        </div>
        
        <div>
          <p className="text-xs font-semibold text-muted-foreground mb-2 px-4">MANAGE</p>
          <nav className="space-y-0.5">
            <SidebarItem 
              icon={<Settings size={18} />} 
              label="Settings"
              href="/settings"
            />
            <SidebarItem 
              icon={<Users size={18} />} 
              label="Team"
              href="/team"
            />
          </nav>
        </div>
      </div>
      
      <div className="border-t border-border pt-4 mt-6 space-y-4">
        <div className="flex items-center justify-between px-2">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
              <span className="font-medium text-sm">{user?.name?.charAt(0) || 'U'}</span>
            </div>
            <div>
              <p className="text-sm font-medium">{user?.name || 'User'}</p>
              <p className="text-xs text-muted-foreground">{user?.email || 'user@example.com'}</p>
            </div>
          </div>
          <ThemeToggle />
        </div>
        
        <Button variant="outline" size="sm" className="w-full" onClick={logout}>
          Sign out
        </Button>
      </div>
    </div>
  );
};

export default DashboardSidebar;
