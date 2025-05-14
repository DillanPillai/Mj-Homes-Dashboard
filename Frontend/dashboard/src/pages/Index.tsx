
import React from "react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import ScraperForm from "@/components/ScraperForm";
import ScraperHistory from "@/components/ScraperHistory";
import DataIntegration from "@/components/DataIntegration";
import BackToTop from "@/components/BackToTop";
import DashboardSidebar from "@/components/DashboardSidebar";
import { useAuth } from "@/contexts/AuthContext";

export default function Index() {
  const { user } = useAuth();

  return (
    <div className="flex h-screen overflow-hidden">
      <DashboardSidebar />
      
      <div className="flex-1 overflow-y-auto">
        <div className="container py-8 px-6">
          <header className="mb-8">
            <h1 className="text-3xl font-bold mb-2 text-mjhome-deep-orange">Welcome back, {user?.name || 'User'}</h1>
            <p className="text-muted-foreground">
              Manage your web scraping tasks and visualize data
            </p>
          </header>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Left column */}
            <div className="md:col-span-1">
              <Card className="border-mjhome-yellow/30 shadow-md h-full bg-white">
                <CardHeader className="pb-3">
                  <CardTitle className="text-mjhome-orange">Start New Job</CardTitle>
                  <CardDescription>Configure and launch a web scraping task</CardDescription>
                </CardHeader>
                <CardContent>
                  <ScraperForm />
                </CardContent>
                <CardFooter className="flex justify-between pt-0">
                  <div className="flex gap-2">
                    <Badge className="bg-mjhome-orange hover:bg-mjhome-deep-orange">Python</Badge>
                    <Badge variant="outline" className="text-mjhome-deep-orange border-mjhome-deep-orange/30">SQL</Badge>
                  </div>
                </CardFooter>
              </Card>
            </div>

            {/* Middle and right columns */}
            <div className="md:col-span-2">
              <div className="space-y-6">
                {/* Data Integration Card */}
                <Card className="border-mjhome-yellow/30 shadow-md bg-white">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-mjhome-orange">Data Integration</CardTitle>
                    <CardDescription>Connect with Python, R, SQL, and Power BI</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <DataIntegration />
                  </CardContent>
                </Card>

                {/* Scraping History Card */}
                <Card className="border-mjhome-yellow/30 shadow-md bg-white">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-mjhome-orange">Recent Scraping Jobs</CardTitle>
                    <CardDescription>View and manage your recent scraping jobs</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ScraperHistory />
                  </CardContent>
                  <CardFooter className="flex justify-end pt-0">
                    <Button variant="outline" size="sm" className="border-mjhome-orange text-mjhome-orange hover:bg-mjhome-orange/10">
                      View All Jobs
                    </Button>
                  </CardFooter>
                </Card>
              </div>
            </div>
          </div>
        </div>
      </div>
      <BackToTop threshold={300} />
    </div>
  );
}
