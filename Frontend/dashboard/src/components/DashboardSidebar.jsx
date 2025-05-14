
import React from "react";
import { Link, useLocation } from "react-router-dom";
import { useTheme } from "@/contexts/ThemeContext";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { 
  Home, BarChart2, History, Settings, 
  Users, LogOut, Menu, X 
} from "lucide-react";
import MJHomeLogo from "./MJHomeLogo";
import ThemeToggle from "./ThemeToggle";

const DashboardSidebar = () => {
  const [isOpen, setIsOpen] = React.useState(true);
  const { theme } = useTheme();
  const { logout, user } = useAuth();
  const location = useLocation();

  const navItems = [
    { icon: Home, label: "Dashboard", path: "/" },
    { icon: BarChart2, label: "New Scraper", path: "/new-scraper" },
    { icon: History, label: "History", path: "/history" },
    { icon: Settings, label: "Settings", path: "/settings" },
    { icon: Users, label: "Team", path: "/team" },
  ];

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="md:hidden fixed inset-0 bg-black/50 z-30"
          onClick={() => setIsOpen(false)}
        ></div>
      )}

      {/* Mobile toggle button */}
      <button
        className="md:hidden fixed top-4 left-4 z-40 bg-white p-2 rounded-md shadow-md border border-gray-200"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle sidebar"
      >
        {isOpen ? (
          <X className="h-5 w-5 text-gray-700" />
        ) : (
          <Menu className="h-5 w-5 text-gray-700" />
        )}
      </button>

      {/* Sidebar */}
      <aside
        className={`bg-card border-r border-border h-screen fixed md:static top-0 left-0 z-30 transition-transform duration-300 transform ${
          isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
        } flex-shrink-0 w-64`}
      >
        <div className="h-full flex flex-col">
          {/* Logo */}
          <div className="p-4 flex justify-center border-b border-border">
            <MJHomeLogo />
          </div>

          {/* Nav items */}
          <nav className="flex-1 py-6 px-3">
            <div className="space-y-1">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center px-3 py-2 rounded-md text-sm ${
                    isActive(item.path)
                      ? "bg-mjhome-orange/10 text-mjhome-deep-orange"
                      : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                  }`}
                  onClick={() => setIsOpen(false)}
                >
                  <item.icon className="h-4 w-4 mr-2 flex-shrink-0" />
                  <span>{item.label}</span>
                </Link>
              ))}
            </div>
          </nav>

          {/* User section */}
          <div className="p-4 border-t border-border mt-auto">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <div className="h-8 w-8 bg-mjhome-orange/20 text-mjhome-deep-orange rounded-full flex items-center justify-center">
                  {user?.name?.charAt(0)?.toUpperCase() || "U"}
                </div>
                <div className="ml-2 overflow-hidden">
                  <p className="text-sm font-medium truncate">{user?.name || "User"}</p>
                  <p className="text-xs text-muted-foreground truncate">{user?.email || ""}</p>
                </div>
              </div>
              <ThemeToggle />
            </div>
            <Button
              onClick={logout}
              variant="outline"
              className="w-full flex items-center justify-center gap-1 border-mjhome-orange/30 text-mjhome-orange hover:bg-mjhome-orange/10"
            >
              <LogOut className="h-4 w-4" />
              <span>Sign out</span>
            </Button>
          </div>
        </div>
      </aside>
    </>
  );
};

export default DashboardSidebar;
