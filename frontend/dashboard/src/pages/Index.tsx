
import { useState } from 'react';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { DashboardSidebar } from '@/components/dashboard/DashboardSidebar';
import { DashboardContent } from '@/components/dashboard/DashboardContent';
import { DashboardFooter } from '@/components/dashboard/DashboardFooter';
import { BackToTopButton } from '@/components/dashboard/BackToTopButton';

const Index = () => {
  const [activeSection, setActiveSection] = useState('overview');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <DashboardHeader onToggleSidebar={() => setSidebarCollapsed(!sidebarCollapsed)} />
      
      <div className="flex flex-1 pt-[73px]">
        <DashboardSidebar 
          activeSection={activeSection}
          onSectionChange={setActiveSection}
          collapsed={sidebarCollapsed}
        />
        
        <main className={`flex-1 transition-all duration-300 ${sidebarCollapsed ? 'ml-16' : 'ml-64'} min-h-[calc(100vh-73px)] flex flex-col`}>
          <div className="flex-1">
            <DashboardContent activeSection={activeSection} />
          </div>
          <DashboardFooter />
        </main>
      </div>
      
      <BackToTopButton />
    </div>
  );
};

export default Index;
