import { Home, TrendingUp, Clock, DollarSign } from 'lucide-react';
import { KPICard } from '../KPICard';
import { ChartCard } from '../ChartCard';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { RentPredictSection } from './RentPredictSection';

export const RentalMarketSection = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Rental Market Insights</h1>
        <p className="text-gray-500 mt-1">Comprehensive rental market analytics and trends</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPICard
          title="Average Rent"
          value="$650/wk"
          change="+3.2%"
          changeType="positive"
          icon={DollarSign}
        />
        <KPICard
          title="Rental Yield"
          value="4.8%"
          change="+0.3%"
          changeType="positive"
          icon={TrendingUp}
        />
        <KPICard
          title="Vacancy Rate"
          value="2.1%"
          change="-0.5%"
          changeType="positive"
          icon={Clock}
        />
        <KPICard
          title="Active Rentals"
          value="1,247"
          change="+8.7%"
          changeType="positive"
          icon={Home}
        />
      </div>

      <RentPredictSection />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard
          title="Rental Price Trends"
          subtitle="Last 12 months"
          type="line"
        />
        <ChartCard
          title="Property Type Distribution"
          subtitle="Current rental listings"
          type="pie"
        />
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Rental Market Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-green-50 p-4 rounded-lg border border-green-200">
              <h3 className="font-semibold text-green-800">Strong Demand</h3>
              <p className="text-sm text-green-600 mt-1">
                Low vacancy rates indicate high rental demand in the current market.
              </p>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
              <h3 className="font-semibold text-blue-800">Steady Growth</h3>
              <p className="text-sm text-blue-600 mt-1">
                Rental prices showing consistent upward trend over the past year.
              </p>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg border border-orange-200">
              <h3 className="font-semibold text-orange-800">Investment Opportunity</h3>
              <p className="text-sm text-orange-600 mt-1">
                Current yields remain attractive for property investors.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
