
import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Search } from "lucide-react";
import { toast } from "sonner";

const ScraperForm = () => {
  const [url, setUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsLoading(true);

    // Validate URL
    if (!url || !url.trim()) {
      toast.error("Please enter a URL");
      setIsLoading(false);
      return;
    }

    // Simulate API call
    setTimeout(() => {
      toast.success("Scraping job started", {
        description: `Started scraping ${url}`,
      });
      setUrl("");
      setIsLoading(false);
    }, 1500);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="url">Website URL</Label>
        <Input
          id="url"
          placeholder="Enter website URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="border-mjhome-orange/20 focus:border-mjhome-orange"
        />
        <p className="text-xs text-muted-foreground">
          Enter the website you want to scrape data from
        </p>
      </div>

      <div className="space-y-2">
        <Label htmlFor="script-type">Script Type</Label>
        <select
          id="script-type"
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 border-mjhome-orange/20"
        >
          <option value="basic">Basic Scraper</option>
          <option value="advanced">Advanced (JavaScript)</option>
          <option value="api">API Extraction</option>
        </select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="data-type">Data Type</Label>
        <select
          id="data-type"
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 border-mjhome-orange/20"
        >
          <option value="property">Property Listings</option>
          <option value="pricing">Pricing Data</option>
          <option value="reviews">Customer Reviews</option>
          <option value="custom">Custom Data</option>
        </select>
      </div>

      <Button
        type="submit"
        disabled={isLoading}
        className="w-full bg-mjhome-orange hover:bg-mjhome-deep-orange text-white"
      >
        {isLoading ? (
          "Starting..."
        ) : (
          <>
            <Search className="mr-2 h-4 w-4" /> Start Scraping
          </>
        )}
      </Button>
    </form>
  );
};

export default ScraperForm;
