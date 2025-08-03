
import { MapPin } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Label } from '@/components/ui/label';

interface RegionFiltersProps {
  onFiltersChange: (filters: any) => void;
}

export const RegionFilters = ({ onFiltersChange }: RegionFiltersProps) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center text-lg">
          <MapPin className="w-5 h-5 mr-2" />
          New Zealand Regions
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          <Label className="text-sm font-medium">Select Region</Label>
          <Select onValueChange={(value) => onFiltersChange({ region: value })} defaultValue="auckland">
            <SelectTrigger>
              <SelectValue placeholder="Select region" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="auckland">Auckland</SelectItem>
              <SelectItem value="wellington">Wellington</SelectItem>
              <SelectItem value="christchurch">Christchurch</SelectItem>
              <SelectItem value="hamilton">Hamilton</SelectItem>
              <SelectItem value="tauranga">Tauranga</SelectItem>
              <SelectItem value="dunedin">Dunedin</SelectItem>
              <SelectItem value="palmerston-north">Palmerston North</SelectItem>
              <SelectItem value="napier-hastings">Napier-Hastings</SelectItem>
              <SelectItem value="nelson">Nelson</SelectItem>
              <SelectItem value="rotorua">Rotorua</SelectItem>
              <SelectItem value="new-plymouth">New Plymouth</SelectItem>
              <SelectItem value="whangarei">Whangarei</SelectItem>
              <SelectItem value="invercargill">Invercargill</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </CardContent>
    </Card>
  );
};
