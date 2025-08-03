
import { OverviewSection } from './sections/OverviewSection';
import { SocialMediaSection } from './sections/SocialMediaSection';
import { TradeMeSection } from './sections/TradeMeSection';
import { CombinedInsightsSection } from './sections/CombinedInsightsSection';
import { DataUploadSection } from './sections/DataUploadSection';
import { SettingsSection } from './sections/SettingsSection';
import { PrivacyBanner } from './PrivacyBanner';

interface DashboardContentProps {
  activeSection: string;
}

export const DashboardContent = ({ activeSection }: DashboardContentProps) => {
  const renderContent = () => {
    switch (activeSection) {
      case 'overview':
        return (
          <>
            <PrivacyBanner />
            <OverviewSection />
          </>
        );
      case 'social-media':
        return <SocialMediaSection />;
      case 'trademe':
        return <TradeMeSection />;
      case 'combined-insights':
        return <CombinedInsightsSection />;
      case 'data-upload':
        return <DataUploadSection />;
      case 'settings':
        return <SettingsSection />;
      default:
        return (
          <>
            <PrivacyBanner />
            <OverviewSection />
          </>
        );
    }
  };

  return (
    <div className="p-6 space-y-6">
      {renderContent()}
    </div>
  );
};
