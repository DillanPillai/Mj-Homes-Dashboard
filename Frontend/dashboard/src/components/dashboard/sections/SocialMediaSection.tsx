
import { Share2, Heart, MessageCircle, TrendingUp } from 'lucide-react';
import { KPICard } from '../KPICard';
import { ChartCard } from '../ChartCard';

export const SocialMediaSection = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Social Media Analytics</h1>
        <p className="text-gray-500 mt-1">Track your social media performance and engagement</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPICard
          title="Total Followers"
          value="12.4K"
          change="+15.2%"
          changeType="positive"
          icon={Share2}
        />
        <KPICard
          title="Engagement Rate"
          value="5.8%"
          change="+0.7%"
          changeType="positive"
          icon={Heart}
        />
        <KPICard
          title="Comments"
          value="1,247"
          change="+22.1%"
          changeType="positive"
          icon={MessageCircle}
        />
        <KPICard
          title="Reach Growth"
          value="34.7%"
          change="+8.9%"
          changeType="positive"
          icon={TrendingUp}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard
          title="Engagement Over Time"
          subtitle="Last 30 days"
          type="line"
        />
        <ChartCard
          title="Content Performance"
          subtitle="By post type"
          type="pie"
        />
      </div>
    </div>
  );
};
