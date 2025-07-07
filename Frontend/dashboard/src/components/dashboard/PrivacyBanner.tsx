
import { Shield, X } from 'lucide-react';
import { useState } from 'react';
import { Button } from '@/components/ui/button';

export const PrivacyBanner = () => {
  const [isVisible, setIsVisible] = useState(true);

  if (!isVisible) return null;

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
      <div className="flex items-start space-x-3">
        <Shield className="w-5 h-5 text-blue-600 mt-0.5" />
        <div className="flex-1">
          <h3 className="font-medium text-blue-900">Privacy & Data Compliance</h3>
          <p className="text-sm text-blue-700 mt-1">
            This dashboard only uses publicly available datasets. All data is sourced from public APIs and complies with data protection regulations.
          </p>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setIsVisible(false)}
          className="text-blue-600 hover:text-blue-800"
        >
          <X className="w-4 h-4" />
        </Button>
      </div>
    </div>
  );
};
