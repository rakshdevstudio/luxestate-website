import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { Building2, LogOut, LayoutDashboard } from 'lucide-react';

export const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav data-testid="navbar" className="fixed top-0 left-0 right-0 z-50 glass-strong">
      <div className="max-w-[1800px] mx-auto px-8 py-6 flex items-center justify-between">
        <Link to="/" data-testid="nav-logo" className="flex items-center gap-3">
          <Building2 className="w-8 h-8 text-primary" />
          <span className="font-serif text-2xl tracking-tight text-primary">LUXESTATE</span>
        </Link>

        <div className="flex items-center gap-8">
          <Link
            to="/listings"
            data-testid="nav-listings"
            className="text-sm uppercase tracking-[0.2em] text-text-muted hover:text-primary transition-colors duration-300"
          >
            Properties
          </Link>

          {user ? (
            <>
              {user.role === 'seller' && (
                <Link
                  to="/seller"
                  data-testid="nav-seller-dashboard"
                  className="text-sm uppercase tracking-[0.2em] text-text-muted hover:text-primary transition-colors duration-300 flex items-center gap-2"
                >
                  <LayoutDashboard className="w-4 h-4" />
                  Dashboard
                </Link>
              )}
              {user.role === 'admin' && (
                <Link
                  to="/admin"
                  data-testid="nav-admin-dashboard"
                  className="text-sm uppercase tracking-[0.2em] text-text-muted hover:text-primary transition-colors duration-300 flex items-center gap-2"
                >
                  <LayoutDashboard className="w-4 h-4" />
                  Admin
                </Link>
              )}
              <button
                onClick={handleLogout}
                data-testid="nav-logout-btn"
                className="text-sm uppercase tracking-[0.2em] text-text-muted hover:text-primary transition-colors duration-300 flex items-center gap-2"
              >
                <LogOut className="w-4 h-4" />
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                data-testid="nav-login"
                className="text-sm uppercase tracking-[0.2em] text-text-muted hover:text-primary transition-colors duration-300"
              >
                Login
              </Link>
              <Link
                to="/register"
                data-testid="nav-register"
                className="bg-primary text-black hover:bg-[#F2C94C] transition-all duration-300 uppercase tracking-widest text-xs font-bold px-6 py-3"
              >
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};