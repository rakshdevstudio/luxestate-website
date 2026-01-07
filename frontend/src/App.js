import { useEffect } from 'react';
import '@/App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Lenis from 'lenis';
import { Toaster } from '@/components/ui/sonner';
import HomePage from '@/pages/HomePage';
import ListingsPage from '@/pages/ListingsPage';
import PropertyDetailPage from '@/pages/PropertyDetailPage';
import LoginPage from '@/pages/LoginPage';
import RegisterPage from '@/pages/RegisterPage';
import SellerDashboard from '@/pages/SellerDashboard';
import AdminDashboard from '@/pages/AdminDashboard';
import { AuthProvider } from '@/context/AuthContext';

function App() {
  useEffect(() => {
    // Remove any Emergent badge that might exist
    const removeEmergentBadge = () => {
      const badge = document.getElementById('emergent-badge');
      if (badge) {
        badge.remove();
      }
      // Also check for any links to emergent.sh
      const emergentLinks = document.querySelectorAll('a[href*="emergent.sh"]');
      emergentLinks.forEach(link => {
        if (link.id === 'emergent-badge' || link.textContent.includes('Emergent')) {
          link.remove();
        }
      });
    };

    // Remove badge immediately and also check periodically
    removeEmergentBadge();
    const interval = setInterval(removeEmergentBadge, 1000);

    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smooth: true,
    });

    function raf(time) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }

    requestAnimationFrame(raf);

    return () => {
      clearInterval(interval);
      lenis.destroy();
    };
  }, []);

  return (
    <AuthProvider>
      <div className="App">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/listings" element={<ListingsPage />} />
            <Route path="/property/:id" element={<PropertyDetailPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/seller" element={<SellerDashboard />} />
            <Route path="/admin" element={<AdminDashboard />} />
          </Routes>
        </BrowserRouter>
        <Toaster position="top-right" />
      </div>
    </AuthProvider>
  );
}

export default App;