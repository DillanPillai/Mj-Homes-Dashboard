
export interface ScrapingJob {
  id: number;
  url: string;
  date: string;
  status: string;
  records: number;
  scriptType: string;
  location: string;
  price: number;
  interest: string;
}

export interface ScraperFilters {
  interest: string;
  location: string;
  minPrice: string;
  maxPrice: string;
  showOnlyCompleted: boolean;
}

export type ExportFormat = 'csv' | 'sql' | 'r' | 'powerbi';
