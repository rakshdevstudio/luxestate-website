import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Building2 } from 'lucide-react';
import { toast } from 'sonner';

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    role: 'client',
  });
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const user = await register(formData.email, formData.password, formData.name, formData.role);
      toast.success('Account created successfully!');
      if (user.role === 'admin') {
        navigate('/admin');
      } else if (user.role === 'seller') {
        navigate('/seller');
      } else {
        navigate('/');
      }
    } catch (error) {
      toast.error('Registration failed. Email may already be in use.');
    }
  };

  return (
    <div data-testid="register-page" className="min-h-screen flex items-center justify-center px-8">
      <div className="w-full max-w-md">
        <div className="text-center mb-12">
          <Link to="/" className="inline-flex items-center gap-3 mb-8">
            <Building2 className="w-10 h-10 text-primary" />
            <span className="font-serif text-3xl tracking-tight text-primary">LUXESTATE</span>
          </Link>
          <h1 className="font-serif text-4xl mb-4 tracking-tight">Join LUXESTATE</h1>
          <p className="text-text-muted">Create your account to get started</p>
        </div>

        <form onSubmit={handleSubmit} data-testid="register-form" className="space-y-6">
          <div>
            <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">Name</label>
            <Input
              data-testid="register-name-input"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
              className="bg-transparent border-b border-white/20 focus:border-primary outline-none py-4 text-white placeholder:text-white/30 transition-all rounded-none"
            />
          </div>
          <div>
            <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">Email</label>
            <Input
              data-testid="register-email-input"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
              className="bg-transparent border-b border-white/20 focus:border-primary outline-none py-4 text-white placeholder:text-white/30 transition-all rounded-none"
            />
          </div>
          <div>
            <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">Password</label>
            <Input
              data-testid="register-password-input"
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              required
              className="bg-transparent border-b border-white/20 focus:border-primary outline-none py-4 text-white placeholder:text-white/30 transition-all rounded-none"
            />
          </div>
          <div>
            <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">Account Type</label>
            <Select value={formData.role} onValueChange={(value) => setFormData({ ...formData, role: value })}>
              <SelectTrigger data-testid="register-role-select" className="bg-surface border-border text-text-main">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="client">Client</SelectItem>
                <SelectItem value="seller">Seller</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <button
            type="submit"
            data-testid="register-submit-btn"
            className="w-full bg-primary text-black hover:bg-[#F2C94C] transition-all duration-300 uppercase tracking-widest text-xs font-bold px-8 py-4"
          >
            Create Account
          </button>
        </form>

        <div className="mt-8 text-center">
          <p className="text-text-muted">
            Already have an account?{' '}
            <Link to="/login" data-testid="goto-login-link" className="text-primary hover:underline">
              Sign in here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}