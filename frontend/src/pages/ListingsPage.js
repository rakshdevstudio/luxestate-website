import { useEffect, useState } from 'react';
import axios from 'axios';
import { Navbar } from '@/components/Navbar';
import { PropertyCard } from '@/components/PropertyCard';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Search } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function ListingsPage() {
  const [properties, setProperties] = useState([]);
  const [filters, setFilters] = useState({
    location: '',
    property_type: '',
    bedrooms: '',
    min_price: '',
    max_price: '',
  });

  useEffect(() => {
    fetchProperties();
  }, [filters]);

  const fetchProperties = async () => {
    try {
      const params = new URLSearchParams();
      params.append('status', 'approved');
      if (filters.location) params.append('location', filters.location);
      if (filters.property_type) params.append('property_type', filters.property_type);
      if (filters.bedrooms) params.append('bedrooms', filters.bedrooms);
      if (filters.min_price) params.append('min_price', filters.min_price);
      if (filters.max_price) params.append('max_price', filters.max_price);

      const response = await axios.get(`${API}/properties?${params.toString()}`);
      setProperties(response.data);
    } catch (error) {
      console.error('Failed to fetch properties:', error);
    }
  };

  return (
    <div data-testid="listings-page" className="min-h-screen">
      <Navbar />

      <div className="pt-32 pb-20 px-8">
        <div className="max-w-[1800px] mx-auto">
          <div className="mb-16">
            <h1 className="font-serif text-5xl md:text-6xl mb-4 tracking-tight">Property Collection</h1>
            <p className="text-text-muted text-lg">Explore our curated selection of luxury estates</p>
          </div>

          <div data-testid="filters-section" className="mb-12 grid grid-cols-1 md:grid-cols-5 gap-4">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
              <Input
                data-testid="location-filter"
                placeholder="Location"
                value={filters.location}
                onChange={(e) => setFilters({ ...filters, location: e.target.value })}
                className="pl-12 bg-surface border-border text-text-main placeholder:text-text-muted focus:border-primary"
              />
            </div>

            <Select value={filters.property_type} onValueChange={(value) => setFilters({ ...filters, property_type: value })}>
              <SelectTrigger data-testid="property-type-filter" className="bg-surface border-border text-text-main">
                <SelectValue placeholder="Property Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Types</SelectItem>
                <SelectItem value="villa">Villa</SelectItem>
                <SelectItem value="penthouse">Penthouse</SelectItem>
                <SelectItem value="mansion">Mansion</SelectItem>
                <SelectItem value="estate">Estate</SelectItem>
              </SelectContent>
            </Select>

            <Select value={filters.bedrooms} onValueChange={(value) => setFilters({ ...filters, bedrooms: value })}>
              <SelectTrigger data-testid="bedrooms-filter" className="bg-surface border-border text-text-main">
                <SelectValue placeholder="Bedrooms" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Any</SelectItem>
                <SelectItem value="2">2+</SelectItem>
                <SelectItem value="3">3+</SelectItem>
                <SelectItem value="4">4+</SelectItem>
                <SelectItem value="5">5+</SelectItem>
              </SelectContent>
            </Select>

            <Input
              data-testid="min-price-filter"
              type="number"
              placeholder="Min Price"
              value={filters.min_price}
              onChange={(e) => setFilters({ ...filters, min_price: e.target.value })}
              className="bg-surface border-border text-text-main placeholder:text-text-muted focus:border-primary"
            />

            <Input
              data-testid="max-price-filter"
              type="number"
              placeholder="Max Price"
              value={filters.max_price}
              onChange={(e) => setFilters({ ...filters, max_price: e.target.value })}
              className="bg-surface border-border text-text-main placeholder:text-text-muted focus:border-primary"
            />
          </div>

          <div data-testid="properties-grid" className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {properties.map((property) => (
              <PropertyCard key={property.id} property={property} />
            ))}
          </div>

          {properties.length === 0 && (
            <div className="text-center text-text-muted py-20">
              <p>No properties match your filters. Try adjusting your search.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}