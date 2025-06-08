
import { TrendingUp, Clock, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export const CompetitorComparison = () => {
  return (
    <Card className="bg-gradient-to-br from-gray-50 to-blue-50 border-gray-200">
      <CardHeader>
        <CardTitle className="flex items-center text-gray-700">
          <TrendingUp className="w-5 h-5 mr-2" />
          Competitor Comparison
          <span className="ml-2 bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full">
            Coming Soon
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-center py-8">
          <Clock className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-600 mb-2">Feature in Development</h3>
          <p className="text-gray-500 max-w-md mx-auto">
            We're working on comprehensive competitor analysis tools that will allow you to compare 
            your performance against market leaders in real-time.
          </p>
          <div className="mt-6 bg-white p-4 rounded-lg border border-gray-200">
            <div className="flex items-start space-x-2">
              <AlertCircle className="w-5 h-5 text-blue-600 mt-0.5" />
              <div className="text-left">
                <h4 className="font-medium text-gray-800">Planned Features:</h4>
                <ul className="text-sm text-gray-600 mt-1 space-y-1">
                  <li>• Market share analysis</li>
                  <li>• Performance benchmarking</li>
                  <li>• Pricing strategy insights</li>
                  <li>• Lead generation comparison</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
