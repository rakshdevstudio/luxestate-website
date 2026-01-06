import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import axios from 'axios';
import { Navbar } from '@/components/Navbar';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Building2, Users, Mail, TrendingUp, Check, X } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function AdminDashboard() {
  const { user, token, loading } = useAuth();
  const navigate = useNavigate();
  const [analytics, setAnalytics] = useState(null);
  const [properties, setProperties] = useState([]);
  const [leads, setLeads] = useState([]);
  const [users, setUsers] = useState([]);

  useEffect(() => {
    if (!loading && (!user || user.role !== 'admin')) {
      navigate('/login');
    }
    if (user && token) {
      fetchData();
    }
  }, [user, token, loading]);

  const fetchData = async () => {
    try {
      const headers = { Authorization: `Bearer ${token}` };
      const [analyticsRes, propertiesRes, leadsRes, usersRes] = await Promise.all([
        axios.get(`${API}/analytics`, { headers }),
        axios.get(`${API}/properties`, { headers }),
        axios.get(`${API}/leads`, { headers }),
        axios.get(`${API}/users`, { headers }),
      ]);
      setAnalytics(analyticsRes.data);
      setProperties(propertiesRes.data);
      setLeads(leadsRes.data);
      setUsers(usersRes.data);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    }
  };

  const handlePropertyAction = async (propertyId, status) => {
    try {
      await axios.patch(
        `${API}/properties/${propertyId}`,
        { status },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success(`Property ${status}!`);
      fetchData();
    } catch (error) {
      toast.error('Failed to update property');
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
    <div data-testid="admin-dashboard" className="min-h-screen">
      <Navbar />

      <div className="pt-32 pb-20 px-8">
        <div className="max-w-[1800px] mx-auto">
          <div className="mb-12">
            <h1 className="font-serif text-5xl mb-2 tracking-tight">Admin Dashboard</h1>
            <p className="text-text-muted">Manage properties, leads, and users</p>
          </div>

          {analytics && (
            <div data-testid="analytics-cards" className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
              <div className="bg-surface border border-white/5 p-6">
                <div className="flex items-center justify-between mb-4">
                  <Building2 className="w-8 h-8 text-primary" />
                  <div className="text-3xl font-bold">{analytics.total_properties}</div>
                </div>
                <div className="text-text-muted text-sm uppercase tracking-widest">Total Properties</div>
              </div>

              <div className="bg-surface border border-white/5 p-6">
                <div className="flex items-center justify-between mb-4">
                  <TrendingUp className="w-8 h-8 text-primary" />
                  <div className="text-3xl font-bold">{analytics.approved_properties}</div>
                </div>
                <div className="text-text-muted text-sm uppercase tracking-widest">Approved</div>
              </div>

              <div className="bg-surface border border-white/5 p-6">
                <div className="flex items-center justify-between mb-4">
                  <Users className="w-8 h-8 text-primary" />
                  <div className="text-3xl font-bold">{analytics.total_users}</div>
                </div>
                <div className="text-text-muted text-sm uppercase tracking-widest">Total Users</div>
              </div>

              <div className="bg-surface border border-white/5 p-6">
                <div className="flex items-center justify-between mb-4">
                  <Mail className="w-8 h-8 text-primary" />
                  <div className="text-3xl font-bold">{analytics.total_leads}</div>
                </div>
                <div className="text-text-muted text-sm uppercase tracking-widest">Leads</div>
              </div>
            </div>
          )}

          <Tabs defaultValue="properties" data-testid="admin-tabs" className="w-full">
            <TabsList className="bg-surface border border-white/10 mb-8">
              <TabsTrigger data-testid="properties-tab" value="properties" className="data-[state=active]:bg-primary data-[state=active]:text-black">
                Properties
              </TabsTrigger>
              <TabsTrigger data-testid="leads-tab" value="leads" className="data-[state=active]:bg-primary data-[state=active]:text-black">
                Leads
              </TabsTrigger>
              <TabsTrigger data-testid="users-tab" value="users" className="data-[state=active]:bg-primary data-[state=active]:text-black">
                Users
              </TabsTrigger>
            </TabsList>

            <TabsContent value="properties" data-testid="properties-tab-content">
              <div className="space-y-4">
                {properties.map((property) => (
                  <div
                    key={property.id}
                    data-testid={`property-item-${property.id}`}
                    className="bg-surface border border-white/5 p-6 flex items-center justify-between"
                  >
                    <div className="flex items-center gap-6">
                      <img src={property.images[0]} alt={property.title} className="w-32 h-24 object-cover" />
                      <div>
                        <h3 className="font-serif text-2xl mb-2">{property.title}</h3>
                        <p className="text-text-muted mb-2">{property.location}</p>
                        <div className="inline-block px-3 py-1 text-xs uppercase tracking-widest bg-primary/20 text-primary">
                          {property.status}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      {property.status === 'pending' && (
                        <>
                          <button
                            onClick={() => handlePropertyAction(property.id, 'approved')}
                            data-testid={`approve-btn-${property.id}`}
                            className="flex items-center gap-2 bg-success text-white hover:bg-success/80 transition-all duration-300 px-6 py-3 text-sm uppercase tracking-widest"
                          >
                            <Check className="w-4 h-4" />
                            Approve
                          </button>
                          <button
                            onClick={() => handlePropertyAction(property.id, 'rejected')}
                            data-testid={`reject-btn-${property.id}`}
                            className="flex items-center gap-2 bg-error text-white hover:bg-error/80 transition-all duration-300 px-6 py-3 text-sm uppercase tracking-widest"
                          >
                            <X className="w-4 h-4" />
                            Reject
                          </button>
                        </>
                      )}
                      {property.status !== 'pending' && (
                        <div className="text-text-muted text-sm">No actions available</div>
                      )}
                    </div>
                  </div>
                ))}
                {properties.length === 0 && (
                  <div className="text-center text-text-muted py-20">
                    <p>No properties yet.</p>
                  </div>
                )}
              </div>
            </TabsContent>

            <TabsContent value="leads" data-testid="leads-tab-content">
              <div className="space-y-4">
                {leads.map((lead) => (
                  <div
                    key={lead.id}
                    data-testid={`lead-item-${lead.id}`}
                    className="bg-surface border border-white/5 p-6"
                  >
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <div className="text-text-muted text-xs uppercase tracking-widest mb-1">Name</div>
                        <div className="text-lg">{lead.name}</div>
                      </div>
                      <div>
                        <div className="text-text-muted text-xs uppercase tracking-widest mb-1">Email</div>
                        <div className="text-lg">{lead.email}</div>
                      </div>
                      <div>
                        <div className="text-text-muted text-xs uppercase tracking-widest mb-1">Phone</div>
                        <div className="text-lg">{lead.phone}</div>
                      </div>
                      <div>
                        <div className="text-text-muted text-xs uppercase tracking-widest mb-1">Property ID</div>
                        <div className="text-lg">{lead.property_id}</div>
                      </div>
                      <div className="md:col-span-2">
                        <div className="text-text-muted text-xs uppercase tracking-widest mb-1">Message</div>
                        <div className="text-lg">{lead.message}</div>
                      </div>
                    </div>
                  </div>
                ))}
                {leads.length === 0 && (
                  <div className="text-center text-text-muted py-20">
                    <p>No leads yet.</p>
                  </div>
                )}
              </div>
            </TabsContent>

            <TabsContent value="users" data-testid="users-tab-content">
              <div className="space-y-4">
                {users.map((user) => (
                  <div
                    key={user.id}
                    data-testid={`user-item-${user.id}`}
                    className="bg-surface border border-white/5 p-6 flex items-center justify-between"
                  >
                    <div>
                      <h3 className="text-xl mb-2">{user.name}</h3>
                      <p className="text-text-muted mb-1">{user.email}</p>
                      <div className="inline-block px-3 py-1 text-xs uppercase tracking-widest bg-primary/20 text-primary">
                        {user.role}
                      </div>
                    </div>
                  </div>
                ))}
                {users.length === 0 && (
                  <div className="text-center text-text-muted py-20">
                    <p>No users yet.</p>
                  </div>
                )}
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}
