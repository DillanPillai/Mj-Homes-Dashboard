import { CheckCircle, Clock, AlertTriangle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export const DatasetStatus = () => {
  const datasets = [
    { name: 'TradeMe', status: 'approved', icon: CheckCircle, color: 'text-green-600' },
    { name: 'Tenancy Services', status: 'pending', icon: Clock, color: 'text-yellow-600' },
    { name: 'Stats NZ', status: 'approved', icon: CheckCircle, color: 'text-green-600' },
    { name: 'Auckland Council', status: 'review', icon: AlertTriangle, color: 'text-orange-600' },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Dataset Approval Status</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {datasets.map((dataset) => {
            const Icon = dataset.icon;
            return (
              <div key={dataset.name} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <span className="font-medium">{dataset.name}</span>
                <div className="flex items-center space-x-2">
                  <Icon className={`w-5 h-5 ${dataset.color}`} />
                  <span className={`text-sm capitalize ${dataset.color}`}>
                    {dataset.status}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
        <div className="mt-4 text-xs text-gray-500">
          Only datasets with public APIs and compliant data sources are approved for use.
        </div>
      </CardContent>
    </Card>
  );
};
