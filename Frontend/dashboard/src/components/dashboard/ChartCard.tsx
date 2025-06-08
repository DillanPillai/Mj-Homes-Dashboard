
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts';

interface ChartCardProps {
  title: string;
  subtitle: string;
  type: 'line' | 'pie' | 'bar';
}

const lineData = [
  { name: 'Jan', value: 750000 },
  { name: 'Feb', value: 765000 },
  { name: 'Mar', value: 780000 },
  { name: 'Apr', value: 775000 },
  { name: 'May', value: 785000 },
  { name: 'Jun', value: 790000 },
];

const pieData = [
  { name: 'Houses', value: 45, color: '#3B82F6' },
  { name: 'Apartments', value: 30, color: '#8B5CF6' },
  { name: 'Townhouses', value: 20, color: '#10B981' },
  { name: 'Other', value: 5, color: '#F59E0B' },
];

export const ChartCard = ({ title, subtitle, type }: ChartCardProps) => {
  const renderChart = () => {
    switch (type) {
      case 'line':
        return (
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={lineData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, 'Price']} />
              <Line type="monotone" dataKey="value" stroke="#3B82F6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        );
      case 'pie':
        return (
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                innerRadius={40}
                outerRadius={80}
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        );
      default:
        return null;
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">{title}</CardTitle>
        <p className="text-sm text-gray-500">{subtitle}</p>
      </CardHeader>
      <CardContent>
        {renderChart()}
        
        {type === 'pie' && (
          <div className="flex flex-wrap gap-3 mt-4">
            {pieData.map((item) => (
              <div key={item.name} className="flex items-center space-x-2">
                <div 
                  className="w-3 h-3 rounded-full" 
                  style={{ backgroundColor: item.color }}
                />
                <span className="text-sm text-gray-600">{item.name} ({item.value}%)</span>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};
