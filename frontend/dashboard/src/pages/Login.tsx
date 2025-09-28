// src/pages/Login.tsx

// Import React hooks for local state and side effects
import { useState, useEffect } from "react";

// Import Button component from shadcn/ui library
import { Button } from "@/components/ui/button";
// Import Input component from shadcn/ui library
import { Input } from "@/components/ui/input";
// Import Card and its subcomponents for styled containers
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

// Import icons from lucide-react
import { Mail, Lock, Loader2 } from "lucide-react";

// Import authentication context (contains login method & current user state)
import { useAuth } from "@/contexts/AuthContext";
// Import toast hook for showing notifications
import { useToast } from "@/hooks/use-toast";
// Import navigation and location hooks from React Router
import { useNavigate, useLocation } from "react-router-dom";

// Define the Login component
const Login = () => {
  // Track whether login is in progress (for spinner and disabling inputs)
  const [isLoading, setIsLoading] = useState(false);

  // State for login form data: email and password
  const [loginData, setLoginData] = useState({ email: "", password: "" });

  // Get login function and current user from AuthContext
  const { login, user } = useAuth();

  // Toast function for notifications
  const { toast } = useToast();

  // Router helpers
  const navigate = useNavigate();
  const location = useLocation();

  // Destination after login: either previous route ("from") or "/"
  const from = (location.state as any)?.from?.pathname || "/";

  // Redirect if user is already logged in
  useEffect(() => {
    if (user) navigate(from, { replace: true });
  }, [user, from, navigate]);

  // Handle login form submission
  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); // prevent default form submit (page reload)
    setIsLoading(true); // start loading state

    try {
      // Try to log in with given email and password
      const ok = await login(loginData.email, loginData.password);

      // Show toast message based on login result
      toast({
        title: ok ? "Login successful" : "Login failed",
        description: ok
          ? "Welcome to MJ Home Dashboard!"
          : "Please check your credentials and try again.",
        variant: ok ? "default" : "destructive",
        className: ok ? "bg-green-50 border-green-200 text-green-800" : "",
      });

      // Navigate to previous route if login was successful
      if (ok) navigate(from, { replace: true });
    } catch {
      // Show toast if an error occurred
      toast({
        title: "Login error",
        description: "An error occurred during login.",
        variant: "destructive",
      });
    } finally {
      // Reset loading state
      setIsLoading(false);
    }
  };

  // JSX render
  return (
    // Full-page container with light/dark background, centered contents
    <div className="min-h-screen bg-white dark:bg-neutral-900 flex flex-col items-center justify-center px-4">
      
      {/* Logo above the card */}
      <div className="text-center mb-4">
        <img
          src="/Logo.JPG" // MJ Home logo
          alt="MJ HOME" // Accessible description
          className="mx-auto h-16 md:h-20 w-auto object-contain" // Responsive sizing
        />
      </div>

      {/* Wrapper for card + illustration */}
      <div className="relative w-full max-w-md mx-auto">
        
        {/* Illustration image positioned behind the login card */}
        <img
          src="/MJHOMESIGNUP2.jpg" // Background illustration
          alt="Illustration"
          className="hidden md:block pointer-events-none select-none absolute right-full 
                     top-1/2 -translate-y-[35%] translate-x-28
                     w-[620px] h-[345px] z-0"
          // - hidden on mobile, shown on md and up
          // - pointer-events-none/select-none: can't interact or select
          // - absolute right-full: placed to the left of the card
          // - top-1/2 -translate-y-[35%]: vertically shifted downward
          // - translate-x-28: shifted horizontally into the viewport
          // - fixed width/height: 620px by 345px
          // - z-0: placed behind the card
          loading="eager" // loads immediately
        />

        {/* Login card container */}
        <Card className="relative z-10 bg-[#E9EBEE] dark:bg-neutral-800 rounded-md shadow-sm border-0">
          
          {/* Card header with welcome text */}
          <CardHeader className="text-center">
            <CardTitle>Welcome</CardTitle>
            <CardDescription>
              Access your real estate analytics dashboard
            </CardDescription>
          </CardHeader>

          {/* Card content contains the login form */}
          <CardContent>
            <form onSubmit={handleLogin} className="space-y-4">
              
              {/* Email input with mail icon */}
              <div className="relative">
                <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-500" />
                <Input
                  type="email"
                  placeholder="Email Address"
                  className="pl-10" // padding so text doesn't overlap icon
                  value={loginData.email}
                  onChange={(e) =>
                    setLoginData({ ...loginData, email: e.target.value })
                  }
                  required
                  disabled={isLoading}
                />
              </div>

              {/* Password input with lock icon */}
              <div className="relative">
                <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-500" />
                <Input
                  type="password"
                  placeholder="Password"
                  className="pl-10"
                  value={loginData.password}
                  onChange={(e) =>
                    setLoginData({ ...loginData, password: e.target.value })
                  }
                  required
                  disabled={isLoading}
                />
              </div>

              {/* Submit button */}
              <Button
                type="submit"
                className="w-full bg-[#F39200] hover:bg-[#dd7e00] text-white rounded-md"
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin mr-2" /> {/* Spinner */}
                    Signing In...
                  </>
                ) : (
                  "Sign In"
                )}
              </Button>

              {/* Footer below form */}
              <div className="text-center mt-4 space-y-1">
                <p className="text-xs text-gray-600 dark:text-gray-300">
                  © 2025 – Developed by AUT students for academic R&amp;D
                  purposes. Internal use only.
                </p>
                <img
                  src="/AUT.jpg" // AUT logo
                  alt="AUT University"
                  className="mx-auto h-12 w-auto object-contain"
                />
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

// Export Login component for routing use
export default Login;
