import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';
import { Navbar } from '@/components/Navbar';
import { PropertyCard } from '@/components/PropertyCard';
import { ArrowRight, Award, Shield, TrendingUp } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function HomePage() {
  const [featuredProperties, setFeaturedProperties] = useState([]);

  useEffect(() => {
    fetchFeaturedProperties();
  }, []);

  const fetchFeaturedProperties = async () => {
    try {
      const response = await axios.get(`${API}/properties?status=approved`);
      setFeaturedProperties(response.data.slice(0, 3));
    } catch (error) {
      console.error('Failed to fetch properties:', error);
    }
  };

  return (
    <div data-testid="home-page" className="min-h-screen">
      <Navbar />

      <section className="relative h-screen flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0">
          <img
            src="https://images.pexels.com/photos/3195642/pexels-photo-3195642.jpeg"
            alt="Luxury Estate"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-black/50 to-black"></div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          className="relative z-10 text-center px-8 max-w-5xl"
        >
          <h1 data-testid="hero-title" className="font-serif text-6xl md:text-8xl mb-6 tracking-tight leading-none">
            Where Architecture
            <br />
            <span className="text-gradient-gold">Meets Artistry</span>
          </h1>
          <p data-testid="hero-subtitle" className="text-text-muted text-lg md:text-xl mb-12 max-w-2xl mx-auto leading-relaxed">
            Discover the world's most extraordinary properties. Each estate, a masterpiece.
          </p>
          <Link
            to="/listings"
            data-testid="explore-properties-btn"
            className="inline-flex items-center gap-3 bg-primary text-black hover:bg-[#F2C94C] transition-all duration-300 uppercase tracking-widest text-xs font-bold px-8 py-4"
          >
            Explore Properties
            <ArrowRight className="w-4 h-4" />
          </Link>
        </motion.div>
      </section>

      <section className="py-32 px-8">
        <div className="max-w-[1800px] mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
            <div className="text-primary text-xs uppercase tracking-[0.2em] mb-4">Featured Collection</div>
            <h2 className="font-serif text-5xl md:text-6xl mb-6 tracking-tight">Signature Properties</h2>
          </motion.div>

          <div data-testid="featured-properties" className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {featuredProperties.map((property, index) => (
              <motion.div
                key={property.id}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                viewport={{ once: true }}
              >
                <PropertyCard property={property} />
              </motion.div>
            ))}
          </div>

          {featuredProperties.length === 0 && (
            <div className="text-center text-text-muted py-20">
              <p>No approved properties yet. Check back soon.</p>
            </div>
          )}
        </div>
      </section>

      <section className="py-32 px-8 bg-surface">
        <div className="max-w-[1800px] mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="text-center"
            >
              <div className="w-16 h-16 mx-auto mb-6 flex items-center justify-center border border-primary/30">
                <Award className="w-8 h-8 text-primary" />
              </div>
              <h3 className="font-serif text-2xl mb-4">Curated Excellence</h3>
              <p className="text-text-muted leading-relaxed">
                Every property is hand-selected for its architectural significance and investment potential.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              viewport={{ once: true }}
              className="text-center"
            >
              <div className="w-16 h-16 mx-auto mb-6 flex items-center justify-center border border-primary/30">
                <Shield className="w-8 h-8 text-primary" />
              </div>
              <h3 className="font-serif text-2xl mb-4">Trusted Process</h3>
              <p className="text-text-muted leading-relaxed">
                Rigorous verification and transparent dealings ensure your investment is secure.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              viewport={{ once: true }}
              className="text-center"
            >
              <div className="w-16 h-16 mx-auto mb-6 flex items-center justify-center border border-primary/30">
                <TrendingUp className="w-8 h-8 text-primary" />
              </div>
              <h3 className="font-serif text-2xl mb-4">Market Intelligence</h3>
              <p className="text-text-muted leading-relaxed">
                Access real-time insights and analytics to make informed acquisition decisions.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      <footer className="py-12 px-8 border-t border-white/5">
        <div className="max-w-[1800px] mx-auto text-center text-text-muted text-sm">
          <p>&copy; 2025 LUXESTATE. Where real estate becomes art.</p>
        </div>
      </footer>
    </div>
  );
}