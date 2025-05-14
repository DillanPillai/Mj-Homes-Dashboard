
import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { useToast } from "@/hooks/use-toast";
import { useAuth } from "@/contexts/AuthContext";
import { useNavigate, Link } from "react-router-dom";
import MJHomeLogo from "@/components/MJHomeLogo";

const SignUp = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [termsAccepted, setTermsAccepted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();
  const { signup } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      toast({
        variant: "destructive",
        title: "Passwords don't match",
        description: "Please make sure your passwords match.",
      });
      return;
    }
    
    if (!termsAccepted) {
      toast({
        variant: "destructive",
        title: "Terms not accepted",
        description: "Please accept the terms and conditions to continue.",
      });
      return;
    }
    
    setIsLoading(true);

    try {
      await signup(email, password, name);
      toast({
        title: "Account created",
        description: "Your account has been created successfully!",
      });
      navigate("/");
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Registration failed",
        description: error.message || "Please check your details and try again.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-mjhome-cream flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-white p-8 rounded-xl shadow-lg border border-mjhome-yellow/20">
          <div className="flex flex-col items-center mb-8">
            <MJHomeLogo className="mb-6" />
            <h2 className="text-2xl font-semibold text-center text-mjhome-deep-orange">Create Account</h2>
            <p className="text-muted-foreground text-center mt-2">
              Join us to start exploring properties
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="name" className="text-sm font-medium">
                Full Name
              </label>
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="John Doe"
                required
                className="border-mjhome-orange/30 focus:border-mjhome-orange"
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium">
                Email
              </label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                required
                className="border-mjhome-orange/30 focus:border-mjhome-orange"
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium">
                Password
              </label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="border-mjhome-orange/30 focus:border-mjhome-orange"
              />
            </div>
            
            <div className="space-y-2">
              <label htmlFor="confirm-password" className="text-sm font-medium">
                Confirm Password
              </label>
              <Input
                id="confirm-password"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="border-mjhome-orange/30 focus:border-mjhome-orange"
              />
            </div>

            <div className="flex items-start space-x-2 pt-2">
              <Checkbox 
                id="terms"
                checked={termsAccepted} 
                onCheckedChange={setTermsAccepted}
                className="mt-1"
              />
              <label htmlFor="terms" className="text-sm text-muted-foreground">
                I agree to the <a href="#" className="text-mjhome-orange hover:underline">Terms of Service</a> and <a href="#" className="text-mjhome-orange hover:underline">Privacy Policy</a>
              </label>
            </div>

            <Button
              type="submit"
              disabled={isLoading}
              className="w-full bg-mjhome-orange hover:bg-mjhome-deep-orange text-white"
            >
              {isLoading ? "Creating Account..." : "Create Account"}
            </Button>
          </form>

          <div className="mt-6 text-center text-sm">
            <p>
              Already have an account?{" "}
              <Link to="/login" className="text-mjhome-orange hover:underline font-medium">
                Sign in
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignUp;
