
import React from "react";

const MJHomeLogo = ({ className = "", width = 150, height = 45 }) => {
  return (
    <div className={`flex items-center justify-center ${className}`}>
      <svg
        width={width}
        height={height}
        viewBox="0 0 200 60"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M38.3333 10.8333L48.3333 20.8333L38.3333 30.8333L28.3333 20.8333L38.3333 10.8333Z"
          fill="#FF9A62"
          stroke="#C25B26"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M20.8333 10.8333L30.8333 20.8333L20.8333 30.8333L10.8333 20.8333L20.8333 10.8333Z"
          fill="#FFB562"
          stroke="#C25B26"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M29.5833 28.3333L39.5833 38.3333L29.5833 48.3333L19.5833 38.3333L29.5833 28.3333Z"
          fill="#F87C32"
          stroke="#C25B26"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <text
          x="60"
          y="35"
          fontSize="26"
          fontWeight="bold"
          fill="#B75C26"
          fontFamily="Arial, sans-serif"
        >
          MJ-Homes
        </text>
      </svg>
    </div>
  );
};

export default MJHomeLogo;
