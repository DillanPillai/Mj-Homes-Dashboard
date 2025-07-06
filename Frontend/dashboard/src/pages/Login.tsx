import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Mail, Lock, Loader2 } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { useToast } from '@/hooks/use-toast';

const Login = () => {
  const [loginData, setLoginData] = useState({ email: '', password: '' });
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const { toast } = useToast();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const success = await login(loginData.email, loginData.password);
      toast({
        title: success ? 'Login successful' : 'Login failed',
        description: success
          ? 'Welcome to MJ Home Dashboard!'
          : 'Please check your credentials and try again.',
        variant: success ? 'default' : 'destructive',
        className: success
          ? 'bg-green-50 border-green-200 text-green-800'
          : '',
      });
    } catch {
      toast({
        title: 'Login error',
        description: 'An error occurred during login.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex items-center justify-center px-4 relative">
      {/* AUT Logo - top-left */}
      <div className="absolute top-6 left-6">
        <img
          src="/AUT.jpg"
          alt="AUT University"
          className="h-16 w-auto object-contain"
        />
      </div>

      <div className="w-full max-w-md space-y-6">
        {/* MJ HOME Image Logo */}
        <div className="text-center">
          <img
            src="/Logo.JPG"
            alt="MJ HOME"
            className="mx-auto h-20 w-auto object-contain"
          />
        </div>

        {/* Login Card */}
        <Card className="bg-[#E9EBEE] rounded-md shadow-sm border-0">
          <CardHeader className="text-center">
            <CardTitle>Welcome</CardTitle>
            <CardDescription>
              Access your real estate analytics dashboard
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="relative">
                <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-500" />
                <Input
                  type="email"
                  placeholder="Email Address"
                  className="pl-10"
                  value={loginData.email}
                  onChange={(e) =>
                    setLoginData({ ...loginData, email: e.target.value })
                  }
                  required
                  disabled={isLoading}
                />
              </div>
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
              <Button
                type="submit"
                className="w-full bg-[#F39200] hover:bg-[#dd7e00] text-white rounded-md"
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin mr-2" />
                    Signing In...
                  </>
                ) : (
                  'Sign In'
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Credit Line */}
        <p className="text-xs text-muted-foreground text-center mt-2">
          © 2025 – Developed by AUT students for academic R&D purposes. Internal use only.
        </p>
      </div>
    </div>
  );
};

export default Login;
