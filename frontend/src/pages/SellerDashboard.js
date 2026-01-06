import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import axios from 'axios';
import { Navbar } from '@/components/Navbar';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { PropertyCard } from '@/components/PropertyCard';
import { Plus } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function SellerDashboard() {
  const { user, token, loading } = useAuth();
  const navigate = useNavigate();
  const [properties, setProperties] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    price: '',
    location: '',
    bedrooms: '',
    bathrooms: '',
    area: '',
    property_type: 'villa',
    images: '',
  });

  useEffect(() => {
    if (!loading && (!user || user.role !== 'seller')) {
      navigate('/login');
    }
    if (user && token) {
      fetchProperties();
    }
  }, [user, token, loading]);

  const fetchProperties = async () => {
    try {
      const response = await axios.get(`${API}/properties/seller`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setProperties(response.data);
    } catch (error) {
      console.error('Failed to fetch properties:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const images = formData.images.split(',').map((url) => url.trim()).filter(Boolean);
      
      if (images.length === 0) {
        toast.error('Please provide at least one image URL');
        return;
      }

      await axios.post(
        `${API}/properties`,
        {
          ...formData,
          price: parseFloat(formData.price),
          bedrooms: parseInt(formData.bedrooms),
          bathrooms: parseInt(formData.bathrooms),
          area: parseFloat(formData.area),
          images,
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success('Property submitted for review!');
      setShowForm(false);
      setFormData({
        title: '',
        description: '',
        price: '',
        location: '',
        bedrooms: '',
        bathrooms: '',
        area: '',
        property_type: 'villa',
        images: '',
      });
      fetchProperties();
    } catch (error) {
      toast.error('Failed to submit property');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-text-muted">Loading...</div>
      </div>
    );
  }

  return (
    <div data-testid="seller-dashboard" className="min-h-screen">
      <Navbar />

      <div className="pt-32 pb-20 px-8">
        <div className="max-w-[1800px] mx-auto">
          <div className="flex items-center justify-between mb-12">
            <div>
              <h1 className="font-serif text-5xl mb-2 tracking-tight">Seller Dashboard</h1>
              <p className="text-text-muted">Manage your property listings</p>
            </div>
            <button
              onClick={() => setShowForm(!showForm)}
              data-testid="toggle-add-property-btn"
              className="flex items-center gap-2 bg-primary text-black hover:bg-[#F2C94C] transition-all duration-300 uppercase tracking-widest text-xs font-bold px-6 py-3"
            >
              <Plus className="w-4 h-4" />
              Add Property
            </button>
          </div>

          {showForm && (
            <div className="mb-12 glass p-8">
              <h2 className="font-serif text-3xl mb-8">Submit New Property</h2>
              <form onSubmit={handleSubmit} data-testid="add-property-form" className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="md:col-span-2">
                  <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">Title</label>
                  <Input
                    data-testid="property-title-input"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    required
                    className="bg-transparent border-b border-white/20 focus:border-primary outline-none py-4 text-white"
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">Description</label>
                  <Textarea
                    data-testid="property-description-input"
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    required
                    rows={4}
                    className="bg-transparent border border-white/20 focus:border-primary outline-none p-4 text-white resize-none"
                  />
                </div>
                <div>
                  <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">Price</label>
                  <Input
                    data-testid="property-price-input"
                    type="number"
                    value={formData.price}
                    onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                    required
                    className="bg-transparent border-b border-white/20 focus:border-primary outline-none py-4 text-white"
                  />
                </div>
                <div>
                  <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">Location</label>
                  <Input
                    data-testid="property-location-input"
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                    required
                    className="bg-transparent border-b border-white/20 focus:border-primary outline-none py-4 text-white"
                  />
                </div>
                <div>
                  <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">Bedrooms</label>
                  <Input
                    data-testid="property-bedrooms-input"
                    type="number"
                    value={formData.bedrooms}
                    onChange={(e) => setFormData({ ...formData, bedrooms: e.target.value })}
                    required
                    className="bg-transparent border-b border-white/20 focus:border-primary outline-none py-4 text-white"
                  />
                </div>
                <div>
                  <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">Bathrooms</label>
                  <Input
                    data-testid="property-bathrooms-input"
                    type="number"
                    value={formData.bathrooms}
                    onChange={(e) => setFormData({ ...formData, bathrooms: e.target.value })}
                    required
                    className="bg-transparent border-b border-white/20 focus:border-primary outline-none py-4 text-white"
                  />
                </div>
                <div>
                  <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">Area (sq ft)</label>
                  <Input
                    data-testid="property-area-input"
                    type="number"
                    value={formData.area}
                    onChange={(e) => setFormData({ ...formData, area: e.target.value })}
                    required
                    className="bg-transparent border-b border-white/20 focus:border-primary outline-none py-4 text-white"
                  />
                </div>
                <div>
                  <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">Property Type</label>
                  <Select value={formData.property_type} onValueChange={(value) => setFormData({ ...formData, property_type: value })}>
                    <SelectTrigger data-testid="property-type-select" className="bg-surface border-border text-text-main">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="villa">Villa</SelectItem>
                      <SelectItem value="penthouse">Penthouse</SelectItem>
                      <SelectItem value="mansion">Mansion</SelectItem>
                      <SelectItem value="estate">Estate</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="md:col-span-2">
                  <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">
                    Image URLs (comma-separated)
                  </label>
                  <Textarea
                    data-testid="property-images-input"
                    value={formData.images}
                    onChange={(e) => setFormData({ ...formData, images: e.target.value })}
                    required
                    rows={3}
                    placeholder="https://example.com/image1.jpg, https://example.com/image2.jpg"
                    className="bg-transparent border border-white/20 focus:border-primary outline-none p-4 text-white resize-none"
                  />
                </div>
                <div className="md:col-span-2">
                  <button
                    type="submit"
                    data-testid="submit-property-btn"
                    className="bg-primary text-black hover:bg-[#F2C94C] transition-all duration-300 uppercase tracking-widest text-xs font-bold px-8 py-4"
                  >
                    Submit Property
                  </button>
                </div>
              </form>
            </div>
          )}

          <div>
            <h2 className="font-serif text-3xl mb-8">Your Properties</h2>
            <div data-testid="seller-properties-list" className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {properties.map((property) => (
                <PropertyCard key={property.id} property={property} />
              ))}
            </div>
            {properties.length === 0 && (
              <div className="text-center text-text-muted py-20">
                <p>You haven't submitted any properties yet.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}