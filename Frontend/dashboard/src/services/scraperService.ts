
import { ScrapingJob, ExportFormat } from "../types/scraper";
import { toast } from "sonner";

const API_URL = 'http://localhost:5000/api';

export const fetchScrapingJobs = async (): Promise<ScrapingJob[]> => {
  try {
    const response = await fetch(`${API_URL}/jobs`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch jobs');
    }
    
    return await response.json();
  } catch (error) {
    console.error("Error fetching jobs:", error);
    throw error;
  }
};

export const downloadJobData = async (jobId: number, format: ExportFormat = 'csv'): Promise<void> => {
  try {
    // In a real app, this would be a direct file download
    // For demo purposes, we'll just return a success message
    const response = await fetch(`${API_URL}/download/${jobId}?format=${format}`);
    
    if (!response.ok) {
      throw new Error('Failed to download data');
    }
    
    // Mock handling different formats
    switch (format) {
      case 'csv':
        toast.success("CSV Downloaded", {
          description: `CSV data for job #${jobId} downloaded successfully`,
        });
        break;
      case 'sql':
        toast.success("SQL Export Completed", {
          description: `Data exported to SQL database for job #${jobId}`,
        });
        break;
      case 'r':
        toast.success("R Data Export", {
          description: `Data exported for R analysis from job #${jobId}`,
        });
        break;
      case 'powerbi':
        toast.success("Power BI Export", {
          description: `Data prepared for Power BI from job #${jobId}`,
        });
        break;
    }
    
    return await response.json();
  } catch (error) {
    console.error("Download error:", error);
    throw error;
  }
};

export const viewJobData = (jobId: number): void => {
  // Mock implementation - would open a modal or navigate to a data view
  toast.info("View Data", {
    description: `Viewing data for job #${jobId}`,
  });
};

export const exportToPowerBI = (jobId: number): void => {
  // Mock implementation for Power BI export
  toast.success("Power BI Export", {
    description: "Mock data has been prepared for Power BI visualization",
  });
};
