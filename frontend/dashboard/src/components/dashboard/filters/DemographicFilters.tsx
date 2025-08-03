
import { Users, DollarSign, Home } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Label } from '@/components/ui/label';

interface DemographicFiltersProps {
  onFiltersChange: (filters: any) => void;
}

export const DemographicFilters = ({ onFiltersChange }: DemographicFiltersProps) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center text-lg">
          <Users className="w-5 h-5 mr-2" />
          Demographic Filters
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="space-y-2">
            <Label className="text-sm font-medium">Age Groups</Label>
            <Select onValueChange={(value) => onFiltersChange({ ageGroup: value })}>
              <SelectTrigger>
                <SelectValue placeholder="Select age group" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="18-30">18-30 years</SelectItem>
                <SelectItem value="31-45">31-45 years</SelectItem>
                <SelectItem value="46-60">46-60 years</SelectItem>
                <SelectItem value="60+">60+ years</SelectItem>
                <SelectItem value="all">All ages</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div className="space-y-2">
            <Label className="flex items-center text-sm font-medium">
              <DollarSign className="w-4 h-4 mr-2" />
              Income Range
            </Label>
            <Select onValueChange={(value) => onFiltersChange({ income: value })}>
              <SelectTrigger>
                <SelectValue placeholder="Select income" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="under-50k">Under $50k</SelectItem>
                <SelectItem value="50k-100k">$50k - $100k</SelectItem>
                <SelectItem value="100k-150k">$100k - $150k</SelectItem>
                <SelectItem value="150k+">$150k+</SelectItem>
                <SelectItem value="all">All incomes</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div className="space-y-2">
            <Label className="flex items-center text-sm font-medium">
              <Home className="w-4 h-4 mr-2" />
              Household Size
            </Label>
            <Select onValueChange={(value) => onFiltersChange({ household: value })}>
              <SelectTrigger>
                <SelectValue placeholder="Select type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="single">Single</SelectItem>
                <SelectItem value="couple">Couple</SelectItem>
                <SelectItem value="family">Family</SelectItem>
                <SelectItem value="all">All types</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
