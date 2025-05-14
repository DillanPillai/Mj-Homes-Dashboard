
import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { useToast } from "@/hooks/use-toast";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Loader2 } from "lucide-react";

const ScraperForm = () => {
  const [url, setUrl] = useState("");
  const [scriptType, setScriptType] = useState("python");
  const [dataStorage, setDataStorage] = useState("sql");
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!url) {
      toast({
        title: "Error",
        description: "Please enter a URL to scrape",
        variant: "destructive",
      });
      return;
    }
    
    setIsLoading(true);
    
    try {
      // Send request to Python backend
      const response = await fetch('http://localhost:5000/api/scrape', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url,
          scriptType,
          dataStorage
        }),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        toast({
          title: "Success",
          description: `Scraping job #${data.job_id} started successfully`,
        });
      } else {
        throw new Error(data.error || "An error occurred while starting the scraper");
      }
    } catch (error) {
      console.error("Scraping error:", error);
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to start scraping job",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-2">
        <Label htmlFor="url">URL to Scrape</Label>
        <Input
          id="url"
          placeholder="https://example.com"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
        />
      </div>

      <div className="space-y-2">
        <Label>Script Type</Label>
        <RadioGroup
          value={scriptType}
          onValueChange={setScriptType}
          className="flex flex-col space-y-1"
        >
          <div className="flex items-center space-x-2">
            <RadioGroupItem value="python" id="python" />
            <Label htmlFor="python">Python</Label>
          </div>
          <div className="flex items-center space-x-2">
            <RadioGroupItem value="r" id="r" />
            <Label htmlFor="r">R</Label>
          </div>
        </RadioGroup>
      </div>

      <Separator />

      <div className="space-y-2">
        <Label htmlFor="dataStorage">Data Storage</Label>
        <RadioGroup 
          value={dataStorage}
          onValueChange={setDataStorage}
          className="flex flex-col space-y-1"
        >
          <div className="flex items-center space-x-2">
            <RadioGroupItem value="sql" id="sql" />
            <Label htmlFor="sql">SQL Database</Label>
          </div>
          <div className="flex items-center space-x-2">
            <RadioGroupItem value="csv" id="csv" />
            <Label htmlFor="csv">CSV File</Label>
          </div>
        </RadioGroup>
      </div>

      <Button type="submit" className="w-full" disabled={isLoading}>
        {isLoading ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            Starting Python Job...
          </>
        ) : (
          "Start Python Scraping Job"
        )}
      </Button>
    </form>
  );
};

export default ScraperForm;
