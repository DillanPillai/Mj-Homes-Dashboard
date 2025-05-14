
import React from "react";
import { Button } from "@/components/ui/button";
import { FileDown, Database, ChartBar, ExternalLink } from "lucide-react";
import { toast } from "sonner";

const DataIntegration = () => {
  const handleExport = (format) => {
    toast.success(`Export to ${format}`, {
      description: `Your data has been prepared for ${format}`,
    });
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      <IntegrationCard 
        title="CSV Export"
        description="Download data as spreadsheet"
        icon={<FileDown className="h-6 w-6" />}
        buttonText="Export CSV"
        onClick={() => handleExport('CSV')}
        className="bg-green-500/10 border-green-500/30"
        iconClass="text-green-500"
      />
      
      <IntegrationCard 
        title="SQL Database"
        description="Push data to SQL"
        icon={<Database className="h-6 w-6" />}
        buttonText="Connect SQL"
        onClick={() => handleExport('SQL')}
        className="bg-blue-500/10 border-blue-500/30"
        iconClass="text-blue-500"
      />
      
      <IntegrationCard 
        title="R Analysis"
        description="Export for R statistical analysis"
        icon={<ChartBar className="h-6 w-6" />}
        buttonText="Export to R"
        onClick={() => handleExport('R')}
        className="bg-purple-500/10 border-purple-500/30"
        iconClass="text-purple-500"
      />
      
      <IntegrationCard 
        title="Power BI"
        description="Create Power BI visualizations"
        icon={<ExternalLink className="h-6 w-6" />}
        buttonText="Connect to Power BI"
        onClick={() => handleExport('Power BI')}
        className="bg-orange-500/10 border-orange-500/30"
        iconClass="text-orange-500"
      />
    </div>
  );
};

const IntegrationCard = ({ 
  title, 
  description, 
  icon, 
  buttonText, 
  onClick,
  className = "",
  iconClass = ""
}) => {
  return (
    <div className={`p-4 rounded-lg border ${className}`}>
      <div className={`mb-3 ${iconClass}`}>
        {icon}
      </div>
      <h3 className="font-medium mb-1">{title}</h3>
      <p className="text-xs text-muted-foreground mb-3">{description}</p>
      <Button 
        variant="outline" 
        size="sm" 
        onClick={onClick}
        className="w-full"
      >
        {buttonText}
      </Button>
    </div>
  );
};

export default DataIntegration;
