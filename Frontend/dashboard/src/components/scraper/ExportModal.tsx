
import React, { useState } from "react";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { ExportFormat } from "@/types/scraper";
import { FileDown, Database, ChartBar, ExternalLink } from "lucide-react";

interface ExportModalProps {
  jobId: number;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onExport: (jobId: number, format: ExportFormat) => void;
}

const ExportModal: React.FC<ExportModalProps> = ({ 
  jobId,
  open,
  onOpenChange,
  onExport
}) => {
  const [format, setFormat] = useState<ExportFormat>('csv');

  const handleExport = () => {
    onExport(jobId, format);
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Export Job Data</DialogTitle>
          <DialogDescription>
            Choose a format to export the data from job #{jobId}
          </DialogDescription>
        </DialogHeader>
        
        <div className="py-4">
          <RadioGroup value={format} onValueChange={(value) => setFormat(value as ExportFormat)} className="gap-4">
            <div className="flex items-center space-x-2 border rounded-lg p-3 hover:bg-accent/10 transition-colors">
              <RadioGroupItem value="csv" id="csv" />
              <Label htmlFor="csv" className="flex items-center gap-2 cursor-pointer">
                <FileDown className="h-4 w-4" />
                <div>
                  <p className="font-medium">CSV File</p>
                  <p className="text-xs text-muted-foreground">Export as a CSV spreadsheet</p>
                </div>
              </Label>
            </div>
            
            <div className="flex items-center space-x-2 border rounded-lg p-3 hover:bg-accent/10 transition-colors">
              <RadioGroupItem value="sql" id="sql" />
              <Label htmlFor="sql" className="flex items-center gap-2 cursor-pointer">
                <Database className="h-4 w-4" />
                <div>
                  <p className="font-medium">SQL Database</p>
                  <p className="text-xs text-muted-foreground">Export to SQL database</p>
                </div>
              </Label>
            </div>
            
            <div className="flex items-center space-x-2 border rounded-lg p-3 hover:bg-accent/10 transition-colors">
              <RadioGroupItem value="r" id="r" />
              <Label htmlFor="r" className="flex items-center gap-2 cursor-pointer">
                <ChartBar className="h-4 w-4" />
                <div>
                  <p className="font-medium">R Format</p>
                  <p className="text-xs text-muted-foreground">Export for R analysis</p>
                </div>
              </Label>
            </div>
            
            <div className="flex items-center space-x-2 border rounded-lg p-3 hover:bg-accent/10 transition-colors">
              <RadioGroupItem value="powerbi" id="powerbi" />
              <Label htmlFor="powerbi" className="flex items-center gap-2 cursor-pointer">
                <ExternalLink className="h-4 w-4" />
                <div>
                  <p className="font-medium">Power BI</p>
                  <p className="text-xs text-muted-foreground">Export for Power BI dashboard</p>
                </div>
              </Label>
            </div>
          </RadioGroup>
        </div>
        
        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>Cancel</Button>
          <Button onClick={handleExport}>Export Data</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default ExportModal;
