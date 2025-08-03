
import { HelpCircle } from 'lucide-react';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';

interface MetricTooltipProps {
  metric: string;
  description: string;
}

export const MetricTooltip = ({ metric, description }: MetricTooltipProps) => {
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <button className="inline-flex items-center">
          <HelpCircle className="w-4 h-4 text-gray-400 hover:text-gray-600 ml-1" />
        </button>
      </TooltipTrigger>
      <TooltipContent className="max-w-xs">
        <div>
          <p className="font-medium">{metric}</p>
          <p className="text-sm text-gray-600 mt-1">{description}</p>
        </div>
      </TooltipContent>
    </Tooltip>
  );
};
