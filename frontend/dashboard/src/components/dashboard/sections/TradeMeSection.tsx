
import { Building, Eye, Star, DollarSign } from 'lucide-react';
import { KPICard } from '../KPICard';
import { ChartCard } from '../ChartCard';
import { ProximityFilters } from '../filters/ProximityFilters';
import { DemographicFilters } from '../filters/DemographicFilters';
import { RegionFilters } from '../filters/RegionFilters';
import { MetricTooltip } from '../MetricTooltip';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { RentalMarketSection } from './RentalMarketSection';
import { useState } from 'react';

export const TradeMeSection = () => {
  const [filters, setFilters] = useState({});

  const handleFiltersChange = (newFilters: any) => {
    setFilters({ ...filters, ...newFilters });
    console.log('Applied filters:', { ...filters, ...newFilters });
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">TradeMe Analytics</h1>
        <p className="text-gray-500 mt-1">Monitor your TradeMe property listings performance</p>
      </div>

      {/* Filters Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <RegionFilters onFiltersChange={handleFiltersChange} />
        <ProximityFilters onFiltersChange={handleFiltersChange} />
        <DemographicFilters onFiltersChange={handleFiltersChange} />
      </div>

      <Tabs defaultValue="sales" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="sales">Sales Analytics</TabsTrigger>
          <TabsTrigger value="rental">Rental Market</TabsTrigger>
        </TabsList>
        
        <TabsContent value="sales" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <KPICard
              title={
                <div className="flex items-center">
                  Active Listings
                  <MetricTooltip 
                    metric="Active Listings" 
                    description="Total number of properties currently listed for sale on TradeMe" 
                  />
                </div>
              }
              value="47"
              change="+3"
              changeType="positive"
              icon={Building}
            />
            <KPICard
              title={
                <div className="flex items-center">
                  Total Views
                  <MetricTooltip 
                    metric="Total Views" 
                    description="Combined page views across all your property listings" 
                  />
                </div>
              }
              value="15.2K"
              change="+12.8%"
              changeType="positive"
              icon={Eye}
            />
            <KPICard
              title={
                <div className="flex items-center">
                  Watchlist Adds
                  <MetricTooltip 
                    metric="Watchlist Adds" 
                    description="Number of users who have added your properties to their watchlist" 
                  />
                </div>
              }
              value="234"
              change="+18.5%"
              changeType="positive"
              icon={Star}
            />
            <KPICard
              title={
                <div className="flex items-center">
                  Avg. Price
                  <MetricTooltip 
                    metric="Average Price" 
                    description="Average listing price across all your active properties" 
                  />
                </div>
              }
              value="$892K"
              change="+5.2%"
              changeType="positive"
              icon={DollarSign}
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ChartCard
              title="Listing Views Trend"
              subtitle="Last 30 days"
              type="line"
            />
            <ChartCard
              title="Property Categories"
              subtitle="Current listings"
              type="pie"
            />
          </div>
        </TabsContent>
        
        <TabsContent value="rental">
          <RentalMarketSection />
        </TabsContent>
      </Tabs>
    </div>
  );
};
