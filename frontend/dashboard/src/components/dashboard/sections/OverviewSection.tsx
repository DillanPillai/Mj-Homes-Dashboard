
import { CalendarDays, MapPin, TrendingUp, DollarSign, Home, Users } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { KPICard } from '../KPICard';
import { ChartCard } from '../ChartCard';
import { ListingsTable } from '../ListingsTable';

export const OverviewSection = () => {
  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Overview</h1>
          <p className="text-gray-500 mt-1">Real estate market insights and analytics</p>
        </div>
        
        {/* Filters */}
        <div className="flex items-center space-x-3">
          <Button variant="outline" size="sm">
            <CalendarDays className="w-4 h-4 mr-2" />
            Last 30 Days
          </Button>
          <Button variant="outline" size="sm">
            <MapPin className="w-4 h-4 mr-2" />
            Auckland Region
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPICard
          title="Total Listings"
          value="1,247"
          change="+12.5%"
          changeType="positive"
          icon={Home}
        />
        <KPICard
          title="Average Price"
          value="$785,000"
          change="+3.2%"
          changeType="positive"
          icon={DollarSign}
        />
        <KPICard
          title="Active Customers"
          value="324"
          change="+8.7%"
          changeType="positive"
          icon={Users}
        />
        <KPICard
          title="Market Growth"
          value="15.3%"
          change="-2.1%"
          changeType="negative"
          icon={TrendingUp}
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard
          title="Property Price Trends"
          subtitle="Last 12 months"
          type="line"
        />
        <ChartCard
          title="Listings by Property Type"
          subtitle="Current month"
          type="pie"
        />
      </div>

      {/* Social Media Insights Card */}
      <Card className="bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
        <CardHeader>
          <CardTitle className="text-blue-900">Social Media Insights</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">2.4M</p>
              <p className="text-sm text-gray-600">Total Reach</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-purple-600">18.7K</p>
              <p className="text-sm text-gray-600">Engagements</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">342</p>
              <p className="text-sm text-gray-600">Leads Generated</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Recent Listings Table */}
      <ListingsTable />
    </div>
  );
};
