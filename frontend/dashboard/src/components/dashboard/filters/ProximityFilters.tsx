
import { MapPin, Train, GraduationCap } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Label } from '@/components/ui/label';

interface ProximityFiltersProps {
  onFiltersChange: (filters: any) => void;
}

export const ProximityFilters = ({ onFiltersChange }: ProximityFiltersProps) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center text-lg">
          <MapPin className="w-5 h-5 mr-2" />
          Proximity Filters
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label className="flex items-center text-sm font-medium">
              <GraduationCap className="w-4 h-4 mr-2" />
              Distance to Schools
            </Label>
            <Select onValueChange={(value) => onFiltersChange({ schools: value })}>
              <SelectTrigger>
                <SelectValue placeholder="Select distance" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="1km">Within 1 km</SelectItem>
                <SelectItem value="5km">Within 5 km</SelectItem>
                <SelectItem value="10km">Within 10 km</SelectItem>
                <SelectItem value="any">Any distance</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div className="space-y-2">
            <Label className="flex items-center text-sm font-medium">
              <Train className="w-4 h-4 mr-2" />
              Distance to Public Transport
            </Label>
            <Select onValueChange={(value) => onFiltersChange({ transport: value })}>
              <SelectTrigger>
                <SelectValue placeholder="Select distance" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="500m">Within 500m</SelectItem>
                <SelectItem value="1km">Within 1 km</SelectItem>
                <SelectItem value="2km">Within 2 km</SelectItem>
                <SelectItem value="any">Any distance</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
