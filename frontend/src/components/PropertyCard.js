import { Link } from 'react-router-dom';
import { MapPin, Bed, Bath, Maximize } from 'lucide-react';

export const PropertyCard = ({ property }) => {
  return (
    <Link
      to={`/property/${property.id}`}
      data-testid={`property-card-${property.id}`}
      className="group block bg-surface border border-white/5 hover:border-primary/30 transition-all duration-500 overflow-hidden"
    >
      <div className="relative h-80 overflow-hidden">
        <img
          src={property.images[0]}
          alt={property.title}
          className="w-full h-full object-cover property-image-hover"
        />
        <div className="absolute top-4 right-4 bg-primary text-black px-4 py-2 text-xs uppercase tracking-widest font-bold">
          {property.status}
        </div>
      </div>

      <div className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="font-serif text-2xl mb-2 text-text-main group-hover:text-primary transition-colors duration-300">
              {property.title}
            </h3>
            <div className="flex items-center gap-2 text-text-muted text-sm">
              <MapPin className="w-4 h-4" />
              <span>{property.location}</span>
            </div>
          </div>
          <div className="text-right">
            <div className="text-primary font-bold text-2xl">
              ${property.price.toLocaleString()}
            </div>
          </div>
        </div>

        <div className="flex items-center gap-6 text-text-muted text-sm pt-4 border-t border-white/5">
          <div className="flex items-center gap-2">
            <Bed className="w-4 h-4" />
            <span>{property.bedrooms} Beds</span>
          </div>
          <div className="flex items-center gap-2">
            <Bath className="w-4 h-4" />
            <span>{property.bathrooms} Baths</span>
          </div>
          <div className="flex items-center gap-2">
            <Maximize className="w-4 h-4" />
            <span>{property.area} sq ft</span>
          </div>
        </div>
      </div>
    </Link>
  );
};