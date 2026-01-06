import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Navbar } from '@/components/Navbar';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { MapPin, Bed, Bath, Maximize, ArrowLeft } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function PropertyDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [property, setProperty] = useState(null);
  const [selectedImage, setSelectedImage] = useState(0);
  const [leadData, setLeadData] = useState({
    name: '',
    email: '',
    phone: '',
    message: '',
  });

  useEffect(() => {
    fetchProperty();
  }, [id]);

  const fetchProperty = async () => {
    try {
      const response = await axios.get(`${API}/properties/${id}`);
      setProperty(response.data);
    } catch (error) {
      console.error('Failed to fetch property:', error);
      toast.error('Property not found');
      navigate('/listings');
    }
  };

  const handleSubmitLead = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/leads`, {
        ...leadData,
        property_id: id,
      });
      toast.success('Your inquiry has been submitted!');
      setLeadData({ name: '', email: '', phone: '', message: '' });
    } catch (error) {
      toast.error('Failed to submit inquiry');
    }
  };

  if (!property) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-text-muted">Loading...</div>
      </div>
    );
  }

  return (
    <div data-testid="property-detail-page" className="min-h-screen">
      <Navbar />

      <div className="pt-32 pb-20 px-8">
        <div className="max-w-[1800px] mx-auto">
          <button
            onClick={() => navigate('/listings')}
            data-testid="back-to-listings-btn"
            className="flex items-center gap-2 text-text-muted hover:text-primary transition-colors mb-8 text-sm uppercase tracking-widest"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Listings
          </button>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
            <div className="lg:col-span-2">
              <div className="mb-6">
                <img
                  src={property.images[selectedImage]}
                  alt={property.title}
                  data-testid="main-property-image"
                  className="w-full h-[600px] object-cover"
                />
              </div>

              <div data-testid="image-thumbnails" className="grid grid-cols-4 gap-4 mb-12">
                {property.images.map((image, index) => (
                  <button
                    key={index}
                    onClick={() => setSelectedImage(index)}
                    data-testid={`thumbnail-${index}`}
                    className={`h-32 overflow-hidden border-2 transition-all duration-300 ${
                      selectedImage === index ? 'border-primary' : 'border-white/10 hover:border-white/30'
                    }`}
                  >
                    <img src={image} alt={`View ${index + 1}`} className="w-full h-full object-cover" />
                  </button>
                ))}
              </div>

              <div className="mb-12">
                <h1 data-testid="property-title" className="font-serif text-5xl mb-4 tracking-tight">
                  {property.title}
                </h1>
                <div className="flex items-center gap-2 text-text-muted mb-8">
                  <MapPin className="w-5 h-5" />
                  <span data-testid="property-location" className="text-lg">{property.location}</span>
                </div>

                <div className="flex items-center gap-8 mb-12 pb-8 border-b border-white/10">
                  <div className="flex items-center gap-3">
                    <Bed className="w-5 h-5 text-primary" />
                    <div>
                      <div className="text-2xl font-bold">{property.bedrooms}</div>
                      <div className="text-text-muted text-sm">Bedrooms</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <Bath className="w-5 h-5 text-primary" />
                    <div>
                      <div className="text-2xl font-bold">{property.bathrooms}</div>
                      <div className="text-text-muted text-sm">Bathrooms</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <Maximize className="w-5 h-5 text-primary" />
                    <div>
                      <div className="text-2xl font-bold">{property.area.toLocaleString()}</div>
                      <div className="text-text-muted text-sm">sq ft</div>
                    </div>
                  </div>
                </div>

                <div>
                  <h2 className="font-serif text-3xl mb-6">About This Property</h2>
                  <p data-testid="property-description" className="text-text-muted leading-relaxed text-lg whitespace-pre-line">
                    {property.description}
                  </p>
                </div>
              </div>
            </div>

            <div className="lg:col-span-1">
              <div className="glass p-8 sticky top-32">
                <div className="mb-8">
                  <div className="text-text-muted text-sm uppercase tracking-widest mb-2">Price</div>
                  <div data-testid="property-price" className="text-primary font-bold text-4xl">
                    ${property.price.toLocaleString()}
                  </div>
                </div>

                <div className="mb-8">
                  <div className="text-text-muted text-sm uppercase tracking-widest mb-2">Type</div>
                  <div className="text-xl capitalize">{property.property_type}</div>
                </div>

                <form onSubmit={handleSubmitLead} data-testid="inquiry-form" className="space-y-4">
                  <div>
                    <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">Name</label>
                    <Input
                      data-testid="inquiry-name-input"
                      value={leadData.name}
                      onChange={(e) => setLeadData({ ...leadData, name: e.target.value })}
                      required
                      className="bg-transparent border-b border-white/20 focus:border-primary outline-none py-4 text-white placeholder:text-white/30 transition-all rounded-none"
                    />
                  </div>
                  <div>
                    <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">Email</label>
                    <Input
                      data-testid="inquiry-email-input"
                      type="email"
                      value={leadData.email}
                      onChange={(e) => setLeadData({ ...leadData, email: e.target.value })}
                      required
                      className="bg-transparent border-b border-white/20 focus:border-primary outline-none py-4 text-white placeholder:text-white/30 transition-all rounded-none"
                    />
                  </div>
                  <div>
                    <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">Phone</label>
                    <Input
                      data-testid="inquiry-phone-input"
                      value={leadData.phone}
                      onChange={(e) => setLeadData({ ...leadData, phone: e.target.value })}
                      required
                      className="bg-transparent border-b border-white/20 focus:border-primary outline-none py-4 text-white placeholder:text-white/30 transition-all rounded-none"
                    />
                  </div>
                  <div>
                    <label className="text-text-muted text-sm uppercase tracking-widest mb-2 block">Message</label>
                    <Textarea
                      data-testid="inquiry-message-input"
                      value={leadData.message}
                      onChange={(e) => setLeadData({ ...leadData, message: e.target.value })}
                      required
                      rows={4}
                      className="bg-transparent border border-white/20 focus:border-primary outline-none p-4 text-white placeholder:text-white/30 transition-all rounded-none resize-none"
                    />
                  </div>
                  <button
                    type="submit"
                    data-testid="submit-inquiry-btn"
                    className="w-full bg-primary text-black hover:bg-[#F2C94C] transition-all duration-300 uppercase tracking-widest text-xs font-bold px-8 py-4"
                  >
                    Submit Inquiry
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}