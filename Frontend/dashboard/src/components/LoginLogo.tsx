
import React from "react";
import MJHomeLogo from "./MJHomeLogo";
import { Button } from "./ui/button";
import { Link } from "react-router-dom";

const LoginLogo = () => {
  return (
    <div className="flex flex-col items-center gap-6 p-8">
      <MJHomeLogo className="scale-150 mb-6" showTagline={true} />
      
      <div className="flex flex-col gap-2 w-full max-w-[200px]">
        <Link to="/login">
          <Button className="w-full bg-mjhome-orange hover:bg-mjhome-deep-orange text-white">
            Login
          </Button>
        </Link>
        
        <Link to="/signup">
          <Button variant="outline" className="w-full border-mjhome-orange text-mjhome-orange hover:bg-mjhome-orange/10">
            Sign Up
          </Button>
        </Link>
      </div>
    </div>
  );
};

export default LoginLogo;
