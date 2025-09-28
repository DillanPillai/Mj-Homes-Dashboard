// src/pages/Login.tsx

// Import React hooks for state and lifecycle control
import { useState, useEffect } from "react";

// Import Button component from your UI library
import { Button } from "@/components/ui/button";
// Import Input component from your UI library
import { Input } from "@/components/ui/input";
// Import Card and its subcomponents for styled container
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

// Import icons from lucide-react (Mail, Lock, Loader2 spinner)
import { Mail, Lock, Loader2 } from "lucide-react";

// Import authentication context (provides login and user state)
import { useAuth } from "@/contexts/AuthContext";
// Import custom toast hook (for showing notifications)
import { useToast } from "@/hooks/use-toast";
// Import navigation and location hooks from React Router
import { useNavigate, useLocation } from "react-router-dom";

// Define the Login component
const Login = () => {
  // State: tracks whether login request is in progress (loading spinner)
  const [isLoading, setIsLoading] = useState(false);

  // State: holds login form data (email and password)
  const [loginData, setLoginData] = useState({ email: "", password: "" });

  // Pull login function and current user from authentication context
  const { login, user } = useAuth();

  // Toast hook for displaying success/error messages
  const { toast } = useToast();

  // Router helpers: navigate lets us redirect, location gives current path
  const navigate = useNavigate();
  const location = useLocation();

  // Extract the "from" path (previous protected route), default to "/"
  const from = (location.state as any)?.from?.pathname || "/";

  // If user is already logged in, redirect them to the "from" page
  useEffect(() => {
    if (user) navigate(from, { replace: true });
  }, [user, from, navigate]); // Dependencies: runs when user, from, or navigate changes

  // Function: handles login form submission
  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); // Prevent default form submission (page reload)
    setIsLoading(true); // Show loading state

    try {
      // Attempt login with email and password
      const ok = await login(loginData.email, loginData.password);

      // Show toast notification depending on success or failure
      toast({
        title: ok ? "Login successful" : "Login failed", // Title message
        description: ok
          ? "Welcome to MJ Home Dashboard!" // Success message
          : "Please check your credentials and try again.", // Failure message
        variant: ok ? "default" : "destructive", // Style: normal vs error
        className: ok ? "bg-green-50 border-green-200 text-green-800" : "", // Extra styling for success
      });

      // If login worked, redirect to "from" path
      if (ok) navigate(from, { replace: true });
    } catch {
      // If an error occurred (server/network/etc.), show error toast
      toast({
        title: "Login error",
        description: "An error occurred during login.",
        variant: "destructive",
      });
    } finally {
      // Stop loading state after request is done
      setIsLoading(false);
    }
  };

  // JSX return: renders the login page
  return (
    // Full screen container: centered layout, light/dark backgrounds
    <div className="min-h-screen bg-white dark:bg-neutral-900 flex flex-col items-center justify-center px-4">
      
      {/* Logo section at top */}
      <div className="text-center mb-4">
        {/* AUT / MJ Home logo image */}
        <img
          src="/Logo.JPG" // Image source
          alt="MJ HOME" // Accessible description
          className="mx-auto h-16 md:h-20 w-auto object-contain" // Centered, responsive sizing
        />
      </div>

      {/* Wrapper: contains the login card and illustration */}
      <div className="relative w-full max-w-md mx-auto">
        
        {/* Background illustration image (positioned behind card) */}
        <img
  src="/MJHOMESIGNUP2.jpg"
  alt="Illustration"
  className="hidden md:block pointer-events-none select-none absolute right-full 
             top-1/2 -translate-y-[45%] translate-x-28
             w-[600px] lg:w-[680px] h-[424px] z-0"
  loading="eager"
/>


        {/* Login card container */}
        <Card className="relative z-10 bg-[#E9EBEE] dark:bg-neutral-800 rounded-md shadow-sm border-0">
          
          {/* Card header: title + description */}
          <CardHeader className="text-center">
            {/* Card title */}
            <CardTitle>Welcome</CardTitle>
            {/* Subtitle/description */}
            <CardDescription>
              Access your real estate analytics dashboard
            </CardDescription>
          </CardHeader>

          {/* Card content: holds the login form */}
          <CardContent>
            {/* Login form */}
            <form onSubmit={handleLogin} className="space-y-4">
              
              {/* Email field with Mail icon */}
              <div className="relative">
                {/* Mail icon positioned inside input */}
                <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-500" />
                {/* Input field for email */}
                <Input
                  type="email" // Input type = email
                  placeholder="Email Address" // Placeholder text
                  className="pl-10" // Padding left for icon space
                  value={loginData.email} // Bound to loginData.email
                  onChange={(e) =>
                    setLoginData({ ...loginData, email: e.target.value }) // Update state on change
                  }
                  required // Field is required
                  disabled={isLoading} // Disable while loading
                />
              </div>

              {/* Password field with Lock icon */}
              <div className="relative">
                {/* Lock icon positioned inside input */}
                <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-500" />
                {/* Input field for password */}
                <Input
                  type="password" // Input type = password
                  placeholder="Password" // Placeholder text
                  className="pl-10" // Padding left for icon space
                  value={loginData.password} // Bound to loginData.password
                  onChange={(e) =>
                    setLoginData({ ...loginData, password: e.target.value }) // Update state on change
                  }
                  required // Field is required
                  disabled={isLoading} // Disable while loading
                />
              </div>

              {/* Login button */}
              <Button
                type="submit" // Submit form on click
                className="w-full bg-[#F39200] hover:bg-[#dd7e00] text-white rounded-md" // Styled orange button
                disabled={isLoading} // Disable while loading
              >
                {/* Show spinner while loading, else show text */}
                {isLoading ? (
                  <>
                    {/* Spinner icon */}
                    <Loader2 className="w-4 h-4 animate-spin mr-2" />
                    {/* Loading text */}
                    Signing In...
                  </>
                ) : (
                  // Default button text
                  "Sign In"
                )}
              </Button>

              {/* Footer under form */}
              <div className="text-center mt-4 space-y-1">
                {/* Copyright text */}
                <p className="text-xs text-gray-600 dark:text-gray-300">
                  © 2025 – Developed by AUT students for academic R&amp;D
                  purposes. Internal use only.
                </p>
                {/* AUT logo */}
                <img
                  src="/AUT.jpg" // AUT logo file
                  alt="AUT University" // Accessible description
                  className="mx-auto h-12 w-auto object-contain" // Centered, responsive sizing
                />
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

// Export component so it can be used in routes
export default Login;
