
import { TrendingUp, Target, Users, BarChart3 } from 'lucide-react';
import { KPICard } from '../KPICard';
import { ChartCard } from '../ChartCard';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ProximityFilters } from '../filters/ProximityFilters';
import { DemographicFilters } from '../filters/DemographicFilters';
import { RegionFilters } from '../filters/RegionFilters';
import { CompetitorComparison } from '../CompetitorComparison';
import { MetricTooltip } from '../MetricTooltip';
import { useState } from 'react';

export const CombinedInsightsSection = () => {
  const [filters, setFilters] = useState({});

  const handleFiltersChange = (newFilters: any) => {
    setFilters({ ...filters, ...newFilters });
    console.log('Applied filters:', { ...filters, ...newFilters });
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Combined Insights</h1>
        <p className="text-gray-500 mt-1">Unified analytics from all your data sources</p>
      </div>

      {/* Filters Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <RegionFilters onFiltersChange={handleFiltersChange} />
        <ProximityFilters onFiltersChange={handleFiltersChange} />
        <DemographicFilters onFiltersChange={handleFiltersChange} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPICard
          title={
            <div className="flex items-center">
              Cross-Platform Leads
              <MetricTooltip 
                metric="Cross-Platform Leads" 
                description="Total qualified leads generated across all marketing channels and platforms" 
              />
            </div>
          }
          value="567"
          change="+24.3%"
          changeType="positive"
          icon={Target}
        />
        <KPICard
          title={
            <div className="flex items-center">
              Conversion Rate
              <MetricTooltip 
                metric="Conversion Rate" 
                description="Percentage of leads that convert to actual sales or signed contracts" 
              />
            </div>
          }
          value="12.8%"
          change="+2.1%"
          changeType="positive"
          icon={TrendingUp}
        />
        <KPICard
          title={
            <div className="flex items-center">
              Total Audience
              <MetricTooltip 
                metric="Total Audience" 
                description="Combined reach across all social media platforms and marketing channels" 
              />
            </div>
          }
          value="28.4K"
          change="+16.7%"
          changeType="positive"
          icon={Users}
        />
        <KPICard
          title={
            <div className="flex items-center">
              ROI
              <MetricTooltip 
                metric="Return on Investment" 
                description="Return on investment calculated from marketing spend versus revenue generated" 
              />
            </div>
          }
          value="234%"
          change="+45.2%"
          changeType="positive"
          icon={BarChart3}
        />
      </div>

      <Card className="bg-gradient-to-br from-purple-50 to-blue-50 border-purple-200">
        <CardHeader>
          <CardTitle className="text-purple-900">High-Potential Zones Heatmap</CardTitle>
          <p className="text-purple-700">Areas with highest engagement and conversion potential</p>
        </CardHeader>
        <CardContent>
          <div className="bg-white rounded-lg p-6 border border-purple-200">
            <div className="grid grid-cols-3 gap-4 text-center">
              <div className="bg-red-100 p-4 rounded-lg">
                <h3 className="font-semibold text-red-800">Central Auckland</h3>
                <p className="text-red-600">High Activity</p>
                <p className="text-sm text-red-500">92% engagement</p>
              </div>
              <div className="bg-orange-100 p-4 rounded-lg">
                <h3 className="font-semibold text-orange-800">North Shore</h3>
                <p className="text-orange-600">Medium Activity</p>
                <p className="text-sm text-orange-500">67% engagement</p>
              </div>
              <div className="bg-yellow-100 p-4 rounded-lg">
                <h3 className="font-semibold text-yellow-800">West Auckland</h3>
                <p className="text-yellow-600">Growing Interest</p>
                <p className="text-sm text-yellow-500">45% engagement</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Competitor Comparison Section */}
      <CompetitorComparison />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard
          title="Multi-Platform Performance"
          subtitle="Combined metrics"
          type="line"
        />
        <ChartCard
          title="Lead Sources"
          subtitle="By platform"
          type="pie"
        />
      </div>
    </div>
  );
};
