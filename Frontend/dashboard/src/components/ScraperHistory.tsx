
import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Database, ArrowDown, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { ScrapingJob, ScraperFilters as FiltersType, ExportFormat } from "@/types/scraper";
import { fetchScrapingJobs, downloadJobData, viewJobData } from "@/services/scraperService";
import ScraperFilters from "@/components/scraper/ScraperFilters";
import ScraperJobCard from "@/components/scraper/ScraperJobCard";
import ExportModal from "@/components/scraper/ExportModal";

const ScraperHistory = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [jobs, setJobs] = useState<ScrapingJob[]>([]);
  const [filteredData, setFilteredData] = useState<ScrapingJob[]>([]);
  const [filters, setFilters] = useState<FiltersType>({
    interest: "",
    location: "",
    minPrice: "",
    maxPrice: "",
    showOnlyCompleted: false
  });
  const [exportJob, setExportJob] = useState<number | null>(null);
  const [isExportModalOpen, setIsExportModalOpen] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    fetchJobs();
  }, []);
  
  const fetchJobs = async () => {
    try {
      setIsLoading(true);
      const data = await fetchScrapingJobs();
      setJobs(data);
      setFilteredData(data);
    } catch (error) {
      console.error("Error fetching jobs:", error);
      toast({
        title: "Error",
        description: "Failed to fetch scraping history",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilterChange = (key: string, value: string | boolean) => {
    const updatedFilters = { ...filters, [key]: value };
    setFilters(updatedFilters);
    
    // Apply filters
    const filtered = jobs.filter(item => {
      // Filter by interest
      if (updatedFilters.interest && item.interest !== updatedFilters.interest.toLowerCase()) {
        return false;
      }
      
      // Filter by location
      if (updatedFilters.location && 
          !item.location.toLowerCase().includes(updatedFilters.location.toLowerCase())) {
        return false;
      }
      
      // Filter by min price
      if (updatedFilters.minPrice && item.price < parseInt(updatedFilters.minPrice)) {
        return false;
      }
      
      // Filter by max price
      if (updatedFilters.maxPrice && item.price > parseInt(updatedFilters.maxPrice)) {
        return false;
      }
      
      // Filter by status
      if (updatedFilters.showOnlyCompleted && item.status !== "completed") {
        return false;
      }
      
      return true;
    });
    
    setFilteredData(filtered);
  };

  const handleViewData = (jobId: number) => {
    viewJobData(jobId);
  };

  const handleDownload = (jobId: number) => {
    setExportJob(jobId);
    setIsExportModalOpen(true);
  };

  const handleExport = async (jobId: number, format: ExportFormat) => {
    try {
      await downloadJobData(jobId, format);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to download data",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="space-y-6">
      {/* Filters section */}
      <ScraperFilters 
        filters={filters} 
        handleFilterChange={handleFilterChange} 
      />

      {/* Results section */}
      <div>
        <h4 className="text-sm font-medium mb-4 flex items-center gap-2">
          <Database className="h-4 w-4" />
          Python Scraping Results
        </h4>
        
        {isLoading ? (
          <div className="flex justify-center py-10">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
          </div>
        ) : filteredData.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">
            No scraping jobs match your filters
          </div>
        ) : (
          <div className="space-y-3">
            {filteredData.map((job) => (
              <ScraperJobCard 
                key={job.id} 
                job={job} 
                onViewData={handleViewData}
                onDownload={handleDownload}
              />
            ))}
          </div>
        )}

        <div className="mt-5 flex justify-end">
          <Button 
            className="gap-2 bg-gradient-to-r from-primary to-accent text-white"
            onClick={fetchJobs}
          >
            Refresh Jobs
            <ArrowDown className="h-4 w-4 rotate-180" />
          </Button>
        </div>
      </div>

      {/* Export Modal */}
      {exportJob !== null && (
        <ExportModal
          jobId={exportJob}
          open={isExportModalOpen}
          onOpenChange={setIsExportModalOpen}
          onExport={handleExport}
        />
      )}
    </div>
  );
};

export default ScraperHistory;
