
import React from "react";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { FileText, ArrowDown } from "lucide-react";

interface FilterProps {
  filters: {
    interest: string;
    location: string;
    minPrice: string;
    maxPrice: string;
    showOnlyCompleted: boolean;
  };
  handleFilterChange: (key: string, value: string | boolean) => void;
}

const ScraperFilters: React.FC<FilterProps> = ({ filters, handleFilterChange }) => {
  return (
    <div className="glass-card p-4 rounded-lg bg-background/80 border border-border/40 shadow-sm">
      <details className="group">
        <summary className="flex cursor-pointer items-center justify-between font-medium">
          <h4 className="text-sm flex items-center gap-2">
            <FileText className="h-4 w-4" />
            Filter Results
          </h4>
          <span className="transition-transform group-open:rotate-180">
            <ArrowDown className="h-4 w-4" />
          </span>
        </summary>
        
        <div className="pt-4 pb-2 animate-fade-in">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <Label htmlFor="interest" className="text-xs mb-1.5 block">Customer Interest</Label>
              <select
                id="interest"
                className="flex h-9 w-full rounded-md border border-input bg-background/50 backdrop-blur-sm px-3 py-1 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                value={filters.interest}
                onChange={(e) => handleFilterChange("interest", e.target.value)}
              >
                <option value="">All</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>
            
            <div>
              <Label htmlFor="location" className="text-xs mb-1.5 block">Location</Label>
              <Input
                id="location"
                placeholder="Filter by location"
                value={filters.location}
                onChange={(e) => handleFilterChange("location", e.target.value)}
                className="h-9 bg-background/50 backdrop-blur-sm"
              />
            </div>
            
            <div className="grid grid-cols-2 gap-2">
              <div>
                <Label htmlFor="minPrice" className="text-xs mb-1.5 block">Min Price</Label>
                <Input
                  id="minPrice"
                  type="number"
                  placeholder="Min"
                  value={filters.minPrice}
                  onChange={(e) => handleFilterChange("minPrice", e.target.value)}
                  className="h-9 bg-background/50 backdrop-blur-sm"
                />
              </div>
              <div>
                <Label htmlFor="maxPrice" className="text-xs mb-1.5 block">Max Price</Label>
                <Input
                  id="maxPrice"
                  type="number"
                  placeholder="Max"
                  value={filters.maxPrice}
                  onChange={(e) => handleFilterChange("maxPrice", e.target.value)}
                  className="h-9 bg-background/50 backdrop-blur-sm"
                />
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <Switch 
              id="completed" 
              checked={filters.showOnlyCompleted}
              onCheckedChange={(checked) => handleFilterChange("showOnlyCompleted", checked)}
              className="data-[state=checked]:bg-green-500"
            />
            <Label htmlFor="completed" className="text-sm">Show only completed</Label>
          </div>
        </div>
      </details>
    </div>
  );
};

export default ScraperFilters;
