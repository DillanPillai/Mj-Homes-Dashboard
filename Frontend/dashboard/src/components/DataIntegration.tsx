
import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { toast } from "sonner";
import { Badge } from "@/components/ui/badge";
import { Database, ChartBar, FileSearch, Check, BarChart3 } from "lucide-react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { exportToPowerBI } from "@/services/scraperService";

const DataIntegration = () => {
  const [isPowerBIDialogOpen, setIsPowerBIDialogOpen] = useState(false);

  const handleConnectPowerBI = () => {
    setIsPowerBIDialogOpen(true);
  };

  const handleRunRScript = () => {
    toast.success("R Script Execution", {
      description: "R script execution simulated successfully",
      icon: <Check className="h-4 w-4 text-green-500" />,
    });
  };

  const handleSQLQuery = () => {
    toast.success("SQL Query", {
      description: "SQL query execution completed",
      icon: <Check className="h-4 w-4 text-green-500" />,
    });
  };

  const handleExportToPowerBI = () => {
    exportToPowerBI(1); // Mock export with job ID 1
    setIsPowerBIDialogOpen(false);
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Python Integration */}
        <div className="glass-card p-5 rounded-xl transition-all hover:shadow-lg hover:translate-y-[-2px]">
          <div className="flex items-center gap-2 mb-2">
            <Database className="h-5 w-5 text-primary" />
            <h3 className="font-medium">Python</h3>
            <Badge variant="default" className="ml-auto bg-green-500/90 hover:bg-green-500 text-white">Active</Badge>
          </div>
          <p className="text-sm text-muted-foreground mb-3">
            Web scraping engine powered by Python
          </p>
          <Button variant="outline" size="sm" className="w-full hover:bg-primary/10">
            Configure
          </Button>
        </div>

        {/* R Integration */}
        <div className="glass-card p-5 rounded-xl transition-all hover:shadow-lg hover:translate-y-[-2px]">
          <div className="flex items-center gap-2 mb-2">
            <ChartBar className="h-5 w-5 text-accent" />
            <h3 className="font-medium">R</h3>
          </div>
          <p className="text-sm text-muted-foreground mb-3">
            Statistical analysis and data processing with R
          </p>
          <Button 
            variant="outline" 
            size="sm" 
            className="w-full hover:bg-accent/10"
            onClick={handleRunRScript}
          >
            Run R Script
          </Button>
        </div>

        {/* SQL Integration */}
        <div className="glass-card p-5 rounded-xl transition-all hover:shadow-lg hover:translate-y-[-2px]">
          <div className="flex items-center gap-2 mb-2">
            <FileSearch className="h-5 w-5 text-primary" />
            <h3 className="font-medium">SQL</h3>
          </div>
          <p className="text-sm text-muted-foreground mb-3">
            Data storage and retrieval with SQL
          </p>
          <Button 
            variant="outline" 
            size="sm" 
            className="w-full hover:bg-primary/10"
            onClick={handleSQLQuery}
          >
            Query Data
          </Button>
        </div>
      </div>

      <Separator className="my-6" />

      {/* Power BI Integration */}
      <div className="glass-card flex flex-col sm:flex-row items-center justify-between gap-4 p-5 rounded-xl hover:shadow-lg transition-all hover:translate-y-[-2px]">
        <div>
          <div className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5 text-accent" />
            <h3 className="font-medium">Power BI Integration</h3>
          </div>
          <p className="text-sm text-muted-foreground mt-1">
            Connect your scraped data to Power BI for advanced visualization
          </p>
        </div>
        <Button 
          onClick={handleConnectPowerBI}
          className="shrink-0 shadow-md bg-gradient-to-r from-primary to-accent text-white hover:shadow-lg transition-all"
        >
          Connect Power BI
        </Button>
      </div>

      {/* Power BI Mock Data Dialog */}
      <Dialog open={isPowerBIDialogOpen} onOpenChange={setIsPowerBIDialogOpen}>
        <DialogContent className="sm:max-w-[600px]">
          <DialogHeader>
            <DialogTitle>Power BI Integration</DialogTitle>
            <DialogDescription>
              Export mock data to Power BI for visualization
            </DialogDescription>
          </DialogHeader>
          
          <div className="py-4">
            <h4 className="font-medium mb-3">Available Mock Data Sets</h4>
            <div className="space-y-3">
              {/* Mock Data Item */}
              <div className="border rounded-lg p-4 hover:bg-accent/5 transition-colors">
                <div className="flex justify-between items-center mb-2">
                  <span className="font-medium">E-commerce Product Data</span>
                  <Badge className="bg-blue-500">128 records</Badge>
                </div>
                <p className="text-sm text-muted-foreground mb-3">
                  Sample product data with prices, categories, and sales metrics
                </p>
                <Button size="sm" variant="outline" className="w-full" onClick={handleExportToPowerBI}>
                  Export to Power BI
                </Button>
              </div>
              
              {/* Mock Data Item */}
              <div className="border rounded-lg p-4 hover:bg-accent/5 transition-colors">
                <div className="flex justify-between items-center mb-2">
                  <span className="font-medium">Real Estate Listings</span>
                  <Badge className="bg-amber-500">64 records</Badge>
                </div>
                <p className="text-sm text-muted-foreground mb-3">
                  Property data with locations, prices, and buyer interest
                </p>
                <Button size="sm" variant="outline" className="w-full" onClick={handleExportToPowerBI}>
                  Export to Power BI
                </Button>
              </div>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default DataIntegration;
