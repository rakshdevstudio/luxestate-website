import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { Input } from '@/components/ui/input';
import { Building2 } from 'lucide-react';
import { toast } from 'sonner';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const user = await login(email, password);
      toast.success('Welcome back!');
      if (user.role === 'admin') {
        navigate('/admin');
      } else if (user.role === 'seller') {
        navigate('/seller');
      } else {
        navigate('/');
      }
    } catch (error) {
      toast.error('Invalid credentials');
    }
  };

  return (
    <div data-testid="login-page" className="min-h-screen flex items-center justify-center px-8">
      <div className="w-full max-w-md">
        <div className="text-center mb-12">
          <Link to="/" className="inline-flex items-center gap-3 mb-8">
            <Building2 className="w-10 h-10 text-primary" />
            <span className="font-serif text-3xl tracking-tight text-primary">LUXESTATE</span>
          </Link>
          <h1 className="font-serif text-4xl mb-4 tracking-tight">Welcome Back</h1>
          <p className="text-text-muted">Sign in to access your account</p>
        </div>

        <form onSubmit={handleSubmit} data-testid="login-form" className="space-y-6">
          <div>
            <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">Email</label>
            <Input
              data-testid="login-email-input"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="bg-transparent border-b border-white/20 focus:border-primary outline-none py-4 text-white placeholder:text-white/30 transition-all rounded-none"
            />
          </div>
          <div>
            <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">Password</label>
            <Input
              data-testid="login-password-input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="bg-transparent border-b border-white/20 focus:border-primary outline-none py-4 text-white placeholder:text-white/30 transition-all rounded-none"
            />
          </div>
          <button
            type="submit"
            data-testid="login-submit-btn"
            className="w-full bg-primary text-black hover:bg-[#F2C94C] transition-all duration-300 uppercase tracking-widest text-xs font-bold px-8 py-4"
          >
            Sign In
          </button>
        </form>

        <div className="mt-8 text-center">
          <p className="text-text-muted">
            Don't have an account?{' '}
            <Link to="/register" data-testid="goto-register-link" className="text-primary hover:underline">
              Register here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}