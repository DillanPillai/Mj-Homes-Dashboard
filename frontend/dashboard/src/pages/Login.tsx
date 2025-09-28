// src/pages/Login.tsx

// Import React hooks for state management and side effects
import { useState, useEffect } from "react";

// Import Button component from the UI library (shadcn/ui)
import { Button } from "@/components/ui/button";
// Import Input component from the UI library
import { Input } from "@/components/ui/input";
// Import Card and its subcomponents for a styled container
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

// Import icons from lucide-react (Mail icon, Lock icon, Loader2 spinner)
import { Mail, Lock, Loader2 } from "lucide-react";

// Import authentication context (provides login method and user state)
import { useAuth } from "@/contexts/AuthContext";
// Import custom toast hook (used for notifications)
import { useToast } from "@/hooks/use-toast";
// Import React Router hooks for navigation and location
import { useNavigate, useLocation } from "react-router-dom";

// Define the Login component
const Login = () => {
  // State: track whether login request is in progress (loading state)
  const [isLoading, setIsLoading] = useState(false);

  // State: store login form data (email + password)
  const [loginData, setLoginData] = useState({ email: "", password: "" });

  // Extract login function and current user from authentication context
  const { login, user } = useAuth();

  // Toast hook for showing notifications (success or error messages)
  const { toast } = useToast();

  // Router helpers: navigation and current route info
  const navigate = useNavigate();
  const location = useLocation();

  // Extract "from" path (redirect destination after login), fallback to "/"
  const from = (location.state as any)?.from?.pathname || "/";

  // If user is already logged in, redirect them automatically
  useEffect(() => {
    if (user) navigate(from, { replace: true });
  }, [user, from, navigate]); // Run effect if user, from, or navigate changes

  // Function: handle login form submission
  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); // Prevent default form behavior (page reload)
    setIsLoading(true); // Show loading spinner

    try {
      // Attempt login using the AuthContext's login function
      const ok = await login(loginData.email, loginData.password);

      // Show notification depending on login result
      toast({
        title: ok ? "Login successful" : "Login failed", // Success or failure message
        description: ok
          ? "Welcome to MJ Home Dashboard!" // Success text
          : "Please check your credentials and try again.", // Failure text
        variant: ok ? "default" : "destructive", // Styling for notification
        className: ok ? "bg-green-50 border-green-200 text-green-800" : "", // Styling for success case
      });

      // If login succeeded, redirect to the "from" route
      if (ok) navigate(from, { replace: true });
    } catch {
      // Handle error (network/server/etc.) with toast
      toast({
        title: "Login error",
        description: "An error occurred during login.",
        variant: "destructive",
      });
    } finally {
      // Reset loading state regardless of outcome
      setIsLoading(false);
    }
  };

  // Render JSX
  return (
    // Full-screen container, centered vertically and horizontally
    <div className="min-h-screen bg-white dark:bg-neutral-900 flex flex-col items-center justify-center px-4">
      
      {/* Logo section at the top */}
      <div className="text-center mb-4">
        {/* MJ Home logo image */}
        <img
          src="/Logo.JPG" // Logo image source
          alt="MJ HOME" // Accessible description
          className="mx-auto h-16 md:h-20 w-auto object-contain" // Responsive sizing
        />
      </div>

      {/* Wrapper that contains the login card and background illustration */}
      <div className="relative w-full max-w-md mx-auto">
        
        {/* Background illustration image, positioned behind the login card */}
        <img
          src="/MJHOMESIGNUP2.jpg" // Illustration file
          alt="Illustration" // Alt text for accessibility
          className="hidden md:block pointer-events-none select-none absolute right-full 
                     top-1/2 -translate-y-[45%] translate-x-28
                     w-[600px] lg:w-[680px] h-[422px] z-0" // Styling + positioning
          loading="eager" // Hint browser to load eagerly
        />

        {/* Login card */}
        <Card className="relative z-10 bg-[#E9EBEE] dark:bg-neutral-800 rounded-md shadow-sm border-0">
          
          {/* Card header with title + description */}
          <CardHeader className="text-center">
            <CardTitle>Welcome</CardTitle> {/* Card title */}
            <CardDescription> {/* Subtitle */}
              Access your real estate analytics dashboard
            </CardDescription>
          </CardHeader>

          {/* Card content: holds the login form */}
          <CardContent>
            {/* Form for login */}
            <form onSubmit={handleLogin} className="space-y-4">
              
              {/* Email input with icon */}
              <div className="relative">
                {/* Mail icon inside input */}
                <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-500" />
                <Input
                  type="email" // Email input type
                  placeholder="Email Address" // Placeholder text
                  className="pl-10" // Padding for icon
                  value={loginData.email} // Controlled value
                  onChange={(e) =>
                    setLoginData({ ...loginData, email: e.target.value }) // Update state
                  }
                  required // Must be filled
                  disabled={isLoading} // Disabled while loading
                />
              </div>

              {/* Password input with icon */}
              <div className="relative">
                {/* Lock icon inside input */}
                <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-500" />
                <Input
                  type="password" // Password input type
                  placeholder="Password" // Placeholder text
                  className="pl-10" // Padding for icon
                  value={loginData.password} // Controlled value
                  onChange={(e) =>
                    setLoginData({ ...loginData, password: e.target.value }) // Update state
                  }
                  required // Must be filled
                  disabled={isLoading} // Disabled while loading
                />
              </div>

              {/* Submit button */}
              <Button
                type="submit" // Submits form
                className="w-full bg-[#F39200] hover:bg-[#dd7e00] text-white rounded-md" // Orange button styling
                disabled={isLoading} // Disabled while loading
              >
                {/* Show spinner if loading, else show text */}
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin mr-2" /> {/* Spinner */}
                    Signing In... {/* Loading text */}
                  </>
                ) : (
                  "Sign In" // Default text
                )}
              </Button>

              {/* Footer under login form */}
              <div className="text-center mt-4 space-y-1">
                {/* Copyright notice */}
                <p className="text-xs text-gray-600 dark:text-gray-300">
                  © 2025 – Developed by AUT students for academic R&amp;D
                  purposes. Internal use only.
                </p>
                {/* AUT logo */}
                <img
                  src="/AUT.jpg" // AUT logo file
                  alt="AUT University" // Accessible description
                  className="mx-auto h-12 w-auto object-contain" // Responsive, centered
                />
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

// Export the Login component so it can be used in routing
export default Login;
