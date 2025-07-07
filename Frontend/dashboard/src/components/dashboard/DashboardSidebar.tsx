
import { 
  BarChart3, 
  Share2, 
  Building, 
  TrendingUp, 
  Upload, 
  Settings
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface DashboardSidebarProps {
  activeSection: string;
  onSectionChange: (section: string) => void;
  collapsed: boolean;
}

const navigationItems = [
  { id: 'overview', label: 'Overview', icon: BarChart3 },
  { id: 'social-media', label: 'Social Media', icon: Share2 },
  { id: 'trademe', label: 'TradeMe', icon: Building },
  { id: 'combined-insights', label: 'Combined Insights', icon: TrendingUp },
  { id: 'data-upload', label: 'Data Upload', icon: Upload },
  { id: 'settings', label: 'Settings', icon: Settings },
];

export const DashboardSidebar = ({
  activeSection,
  onSectionChange,
  collapsed
}: DashboardSidebarProps) => {
  return (
    <aside className={cn(
      "bg-white border-r border-gray-200 transition-all duration-300 fixed left-0 top-[73px] bottom-0 z-30",
      collapsed ? "w-16" : "w-64"
    )}>
      <div className="flex flex-col h-full">
        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeSection === item.id;
            
            return (
              <Button
                key={item.id}
                variant={isActive ? "default" : "ghost"}
                className={cn(
                  "w-full justify-start",
                  collapsed ? "px-2" : "px-4",
                  isActive && "bg-blue-600 text-white hover:bg-blue-700"
                )}
                onClick={() => onSectionChange(item.id)}
              >
                <Icon className={cn("w-5 h-5", collapsed ? "" : "mr-3")} />
                {!collapsed && <span>{item.label}</span>}
              </Button>
            );
          })}
        </nav>

        {/* User Info at Bottom */}
        {!collapsed && (
          <div className="p-4 border-t border-gray-200">
            <div className="text-xs text-gray-500 space-y-1">
              <p>Logged in as</p>
              <p className="font-medium text-gray-900">Mike Johnson</p>
              <p>Real Estate Analyst</p>
            </div>
          </div>
        )}
      </div>
    </aside>
  );
};
