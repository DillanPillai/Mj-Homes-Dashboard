
import React from "react";
import { Badge } from "@/components/ui/badge";
import { Calendar, Check, ExternalLink, Download, Info } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

const ScraperHistory = () => {
  // Mock data
  const recentJobs = [
    {
      id: 1,
      url: "https://example-property.com/listings",
      date: "May 10, 2025",
      status: "completed",
      records: 128,
      scriptType: "Basic Scraper",
      location: "New York",
      price: 350000,
      interest: "high"
    },
    {
      id: 2,
      url: "https://another-realty.com/rentals",
      date: "May 8, 2025",
      status: "failed",
      records: 0,
      scriptType: "Advanced",
      location: "Los Angeles",
      price: 420000,
      interest: "medium"
    }
  ];

  const handleViewData = (jobId) => {
    toast.info("View Data", {
      description: `Viewing data for job #${jobId}`,
    });
  };

  const handleDownload = (jobId) => {
    toast.success("CSV Downloaded", {
      description: `CSV data for job #${jobId} downloaded successfully`,
    });
  };

  const getStatusBadge = (status) => {
    if (status === "completed") {
      return (
        <Badge className="bg-green-500 hover:bg-green-600 text-white flex items-center gap-1 px-3 py-1 rounded-full">
          <Check className="h-3 w-3" /> Completed
        </Badge>
      );
    } else {
      return (
        <Badge className="bg-red-500 hover:bg-red-600 text-white flex items-center gap-1 px-3 py-1 rounded-full">
          <Info className="h-3 w-3" /> Failed
        </Badge>
      );
    }
  };

  const getInterestBadge = (interest) => {
    const classes = {
      high: "bg-blue-500 text-white",
      medium: "bg-amber-500 text-white",
      low: "bg-slate-500 text-white"
    };
    
    return (
      <Badge className={`${classes[interest] || ""} px-3 py-0.5 rounded-full`}>
        {interest} interest
      </Badge>
    );
  };

  return (
    <div className="space-y-4">
      {recentJobs.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground">
          <p>You haven't run any scraping jobs yet.</p>
        </div>
      ) : (
        recentJobs.map((job) => (
          <div 
            key={job.id} 
            className="rounded-lg overflow-hidden border border-border/40 bg-card"
          >
            {/* Top section with URL and status */}
            <div className="p-4 flex flex-wrap items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <span className="font-medium text-foreground truncate max-w-[300px]">
                  {job.url}
                </span>
                <span className="mx-2">·</span>
                {getStatusBadge(job.status)}
              </div>
              <div className="flex gap-2">
                <Button 
                  variant="outline" 
                  size="sm" 
                  className="flex items-center gap-1"
                  onClick={() => handleViewData(job.id)}
                >
                  <ExternalLink className="h-4 w-4" />
                  View Data
                </Button>
                <Button 
                  variant="outline" 
                  size="sm" 
                  className="flex items-center gap-1"
                  onClick={() => handleDownload(job.id)}
                >
                  <Download className="h-4 w-4" />
                  Download
                </Button>
              </div>
            </div>
            
            {/* Bottom section with metadata */}
            <div className="p-3 bg-muted/20 border-t border-border/20">
              <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
                <div className="flex items-center">
                  <Calendar className="h-3.5 w-3.5 mr-1.5" />
                  <span>{job.date}</span>
                </div>
                
                <div className="flex items-center">
                  <span className="font-mono">{job.records} records</span>
                </div>
                
                <Badge variant="outline" className="rounded-full px-2">
                  {job.scriptType}
                </Badge>
                
                <div className="ml-auto flex items-center gap-3">
                  <span className="font-medium">{job.location}</span>
                  <span className="font-mono">${job.price.toLocaleString()}</span>
                  {getInterestBadge(job.interest)}
                </div>
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default ScraperHistory;
