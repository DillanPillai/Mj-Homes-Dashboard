
import React from "react";

interface MJHomeLogoProps {
  className?: string;
  showTagline?: boolean;
}

const MJHomeLogo: React.FC<MJHomeLogoProps> = ({ className = "", showTagline = true }) => {
  return (
    <div className={`flex flex-col items-center ${className}`}>
      <h1 className="text-4xl font-bold text-mjhome-orange">
        MJ <span className="relative">
          HOME
          <span className="absolute -top-1 left-1/2 -translate-x-1/2 w-8 h-8 border-2 border-mjhome-orange rounded-full opacity-60"></span>
        </span>
      </h1>
      {showTagline && (
        <p className="text-sm text-mjhome-deep-orange mt-1">Marketing Insights Dashboard</p>
      )}
    </div>
  );
};

export default MJHomeLogo;
