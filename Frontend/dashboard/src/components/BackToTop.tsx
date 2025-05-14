
import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { ArrowUp } from "lucide-react";

interface BackToTopProps {
  threshold?: number;
}

const BackToTop = ({ threshold = 300 }: BackToTopProps) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const toggleVisibility = () => {
      if (window.scrollY > threshold) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };

    window.addEventListener("scroll", toggleVisibility);
    return () => window.removeEventListener("scroll", toggleVisibility);
  }, [threshold]);

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  return (
    <div className={`fixed bottom-6 right-6 transition-opacity duration-300 ${isVisible ? "opacity-100" : "opacity-0 pointer-events-none"}`}>
      <Button
        onClick={scrollToTop}
        variant="outline"
        size="icon"
        className="rounded-full shadow-md hover:shadow-lg"
      >
        <ArrowUp className="h-5 w-5" />
      </Button>
    </div>
  );
};

export default BackToTop;
