import React, { useRef, useState } from 'react';
import { Upload, FileText, AlertCircle, CheckCircle, Trash2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { DatasetStatus } from '../DatasetStatus';
import { PrivacyBanner } from '../PrivacyBanner';
import * as XLSX from 'xlsx';

export const DataUploadSection = () => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [excelData, setExcelData] = useState<any[][]>([]);
  const [kpis, setKpis] = useState<{
    total: number;
    avgRent: number;
    avgBedrooms: number;
    topSuburb: string;
  } | null>(null);
  const [recentUploads, setRecentUploads] = useState<any[]>([]);

  const handleChooseFileClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const uploadEntry = {
      name: file.name,
      date: new Date().toISOString().split('T')[0],
      size: `${(file.size / 1024 / 1024).toFixed(1)} MB`,
      status: 'processing',
    };

    setRecentUploads((prev) => [uploadEntry, ...prev]);

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = new Uint8Array(e.target?.result as ArrayBuffer);
        const workbook = XLSX.read(data, { type: 'array' });
        const worksheet = workbook.Sheets[workbook.SheetNames[0]];
        const parsed = XLSX.utils.sheet_to_json(worksheet, { header: 1 }) as any[][];

        setExcelData(parsed);

        const rows = parsed.slice(1);
        const headers = parsed[0];

        const rentColIndex = headers.indexOf('Weekly Rent ($NZD)');
        const bedroomsColIndex = headers.indexOf('Bedrooms');
        const suburbColIndex = headers.indexOf('Suburb');

        if (rentColIndex === -1 || bedroomsColIndex === -1 || suburbColIndex === -1) {
          throw new Error('Required columns not found');
        }

        const total = rows.length;
        const avgRent = Math.round(
          rows.reduce((sum, row) => sum + Number(row[rentColIndex] || 0), 0) / total
        );
        const avgBedrooms = parseFloat(
          (
            rows.reduce((sum, row) => sum + Number(row[bedroomsColIndex] || 0), 0) / total
          ).toFixed(1)
        );

        const suburbCounts: Record<string, number> = {};
        rows.forEach((row) => {
          const suburb = row[suburbColIndex];
          if (suburb) {
            suburbCounts[suburb] = (suburbCounts[suburb] || 0) + 1;
          }
        });
        const topSuburb =
          Object.entries(suburbCounts).sort((a, b) => b[1] - a[1])[0]?.[0] || 'N/A';

        setKpis({ total, avgRent, avgBedrooms, topSuburb });

        setRecentUploads((prev) => [
          { ...uploadEntry, status: 'processed' },
          ...prev.slice(1),
        ]);
      } catch (err) {
        setRecentUploads((prev) => [
          { ...uploadEntry, status: 'not compatible' },
          ...prev.slice(1),
        ]);
      }
    };
    reader.readAsArrayBuffer(file);
  };

  const handleClearAll = () => {
    setKpis(null);
    setExcelData([]);
    setRecentUploads([]);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Data Upload & Management</h1>
        <p className="text-gray-500 mt-1">Upload and manage your data sources for analytics</p>
      </div>

      <PrivacyBanner />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Upload className="w-5 h-5 mr-2" /> Upload New Dataset
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div
              className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:bg-gray-50 transition"
              onClick={handleChooseFileClick}
            >
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                className="hidden"
              />
              <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">Drop files here</h3>
              <p className="text-gray-500 mb-4">or click to browse</p>
              <Button type="button" className="bg-blue-600 hover:bg-blue-700">
                Choose Files
              </Button>
            </div>

            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <div className="flex items-start space-x-2">
                <AlertCircle className="w-5 h-5 text-yellow-600 mt-0.5" />
                <div>
                  <h4 className="font-medium text-yellow-800">Supported Formats</h4>
                  <p className="text-sm text-yellow-700 mt-1">
                    CSV, Excel (.xlsx), JSON files from public data sources only
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <DatasetStatus />
      </div>

      {kpis && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardContent className="py-4">
              <h4 className="text-sm text-gray-500 mb-1">Total Listings</h4>
              <p className="text-xl font-semibold">{kpis.total}</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="py-4">
              <h4 className="text-sm text-gray-500 mb-1">Avg Weekly Rent</h4>
              <p className="text-xl font-semibold">${kpis.avgRent}</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="py-4">
              <h4 className="text-sm text-gray-500 mb-1">Avg Bedrooms</h4>
              <p className="text-xl font-semibold">{kpis.avgBedrooms}</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="py-4">
              <h4 className="text-sm text-gray-500 mb-1">Top Suburb</h4>
              <p className="text-xl font-semibold">{kpis.topSuburb}</p>
            </CardContent>
          </Card>
        </div>
      )}

      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>Recent Uploads</CardTitle>
          {recentUploads.length > 0 && (
            <Button variant="outline" onClick={handleClearAll} className="flex items-center gap-2">
              <Trash2 className="w-4 h-4" />
              Clear All
            </Button>
          )}
        </CardHeader>
        <CardContent>
          {recentUploads.length === 0 ? (
            <p className="text-gray-500 text-sm italic">
              No files uploaded yet. Your uploaded datasets will appear here.
            </p>
          ) : (
            <div className="space-y-3">
              {recentUploads.map((file, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <FileText className="w-5 h-5 text-gray-400" />
                    <div>
                      <p className="font-medium">{file.name}</p>
                      <p className="text-sm text-gray-500">
                        {file.date} • {file.size}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    {file.status === 'processed' ? (
                      <CheckCircle className="w-5 h-5 text-green-600" />
                    ) : file.status === 'processing' ? (
                      <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
                    ) : (
                      <AlertCircle className="w-5 h-5 text-red-600" />
                    )}
                    <span
                      className={`text-sm capitalize ${
                        file.status === 'processed'
                          ? 'text-green-600'
                          : file.status === 'processing'
                          ? 'text-blue-600'
                          : 'text-red-600'
                      }`}
                    >
                      {file.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};
