import { useEffect, useState } from 'react';
import { NavLink, Route, Routes } from 'react-router-dom';
import type { PropertySummary } from '@api-sdk';
import { apiSdk } from '@api-sdk';
import { Badge, Button, Card, Checkbox, Input, PageShell, Select, Textarea } from '@ui';

const navItems = [
  { to: '/', label: 'Home' },
  { to: '/search', label: 'Search' },
  { to: '/map', label: 'Map' },
  { to: '/estimation', label: 'Estimation' },
  { to: '/assistant', label: 'Assistant' },
  { to: '/marketplace', label: 'Marketplace' },
  { to: '/contact', label: 'Contact' },
  { to: '/login', label: 'Login' },
  { to: '/profile', label: 'Profile' },
  { to: '/dashboard', label: 'Dashboard' }
];

function HomePage() {
  return (
    <PageShell
      eyebrow="LAWIM Intelligence Platform"
      title="Operational intelligence for modern teams"
      description="A polished frontend shell for monitoring, coordination, and mission control workflows."
      actions={
        <>
          <Button>Launch workspace</Button>
          <Button variant="secondary">Explore capabilities</Button>
        </>
      }
    >
      <div className="grid gap-6 md:grid-cols-3">
        <Card title="Realtime visibility" description="Track operations from a single intelligent surface." />
        <Card title="Automation" description="Coordinate workflows across teams and systems." />
        <Card title="Governance" description="Keep oversight simple with clear auditing and controls." />
      </div>
    </PageShell>
  );
}

function SearchPage() {
  const [properties, setProperties] = useState<PropertySummary[]>([]);

  useEffect(() => {
    void apiSdk.getProperties().then((response) => setProperties(response.data));
  }, []);

  return (
    <PageShell eyebrow="Discovery" title="Search opportunities" description="Browse the latest listings and refine your next move.">
      <div className="grid gap-6 lg:grid-cols-[1.4fr_0.8fr]">
        <div className="grid gap-4">
          {properties.map((property) => (
            <Card key={property.id} title={property.title} description={`${property.location} • ${property.type}`}>
              <div className="flex items-center justify-between text-sm text-slate-300">
                <span>{property.location}</span>
                <span className="font-semibold text-white">€{property.price.toLocaleString()}</span>
              </div>
            </Card>
          ))}
        </div>
        <Card title="Refine search" description="Filter by region, type, and priority.">
          <div className="flex flex-col gap-3">
            <Input label="Keyword" placeholder="Luxury villa" />
            <Select label="Category">
              <option>Residential</option>
              <option>Commercial</option>
            </Select>
            <Checkbox label="Ready to review" />
          </div>
        </Card>
      </div>
    </PageShell>
  );
}

function MapPage() {
  return (
    <PageShell eyebrow="Location intelligence" title="Map overview" description="Visualize properties and operations across the territory.">
      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-10 text-center text-slate-300">
          Interactive map ready for Leaflet integration.
        </div>
        <Card title="Live signals" description="Monitor hotspots and recent actions.">
          <div className="flex flex-col gap-2 text-sm text-slate-300">
            <div className="flex items-center justify-between">
              <span>North district</span>
              <Badge variant="success">Healthy</Badge>
            </div>
            <div className="flex items-center justify-between">
              <span>Harbor market</span>
              <Badge variant="warning">Needs review</Badge>
            </div>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}

function EstimationPage() {
  return (
    <PageShell eyebrow="Valuation" title="Estimate a property" description="Capture the essentials and generate a quick assessment.">
      <div className="grid gap-6 lg:grid-cols-[1fr_0.7fr]">
        <Card title="Property details" description="Share the information needed to build a first estimate.">
          <div className="grid gap-4 md:grid-cols-2">
            <Input label="Address" placeholder="12 Rue de la Paix" />
            <Input label="Surface" placeholder="120 m²" />
            <Select label="Property type">
              <option>House</option>
              <option>Apartment</option>
              <option>Office</option>
            </Select>
            <Input label="Expected price" placeholder="€500k" />
            <Textarea label="Notes" placeholder="Recent renovations, view quality, parking, etc." className="md:col-span-2" />
          </div>
        </Card>
        <Card title="Suggested outcome" description="A guided result for the current workflow.">
          <div className="space-y-3 text-sm text-slate-300">
            <p>Estimated range: €470k – €530k</p>
            <p>Confidence: High</p>
            <Button className="w-full">Generate estimate</Button>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}

function AssistantPage() {
  return (
    <PageShell eyebrow="AI assistant" title="Ask your intelligent copilot" description="Use the assistant to surface the right next action.">
      <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <Card title="Suggested prompts" description="Get started faster with prepared workflows.">
          <div className="flex flex-col gap-2 text-sm text-slate-300">
            <span>• Summarize the latest pipeline</span>
            <span>• Highlight high-value opportunities</span>
            <span>• Draft a follow-up message</span>
          </div>
        </Card>
        <Card title="Conversation" description="The assistant is ready to support your team.">
          <Textarea label="Message" placeholder="What do you want to understand today?" />
          <div className="mt-4 flex gap-3">
            <Button>Send</Button>
            <Button variant="secondary">Save draft</Button>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}

function MarketplacePage() {
  const [listings, setListings] = useState<{ title: string; status: string }[]>([]);

  useEffect(() => {
    void apiSdk.getMarketListings().then((response) => setListings(response.data.map((item) => ({ title: item.title, status: item.status }))));
  }, []);

  return (
    <PageShell eyebrow="Marketplace" title="Marketplace flows" description="Coordinate offers, deals, and service requests from one place.">
      <div className="grid gap-6 md:grid-cols-2">
        {listings.map((listing) => (
          <Card key={listing.title} title={listing.title} description="Available for review">
            <Badge variant="info">{listing.status}</Badge>
          </Card>
        ))}
      </div>
    </PageShell>
  );
}

function ContactPage() {
  return (
    <PageShell eyebrow="Contact" title="Stay in touch" description="Reach the team for onboarding, collaboration, or support.">
      <Card title="Contact the LAWIM team" description="We reply within one business day.">
        <div className="grid gap-4 md:grid-cols-2">
          <Input label="Name" placeholder="Your name" />
          <Input label="Email" placeholder="you@company.com" />
          <Textarea label="Message" placeholder="How can we help?" className="md:col-span-2" />
          <Button className="md:col-span-2">Send message</Button>
        </div>
      </Card>
    </PageShell>
  );
}

function LoginPage() {
  return (
    <PageShell eyebrow="Auth" title="Sign in to LAWIM" description="Use your workspace credentials to continue.">
      <Card title="Credentials" description="Secure access for clients and operators.">
        <div className="grid gap-4">
          <Input label="Email" placeholder="name@lawim.com" />
          <Input label="Password" placeholder="••••••••" type="password" />
          <Button>Continue</Button>
        </div>
      </Card>
    </PageShell>
  );
}

function ProfilePage() {
  return (
    <PageShell eyebrow="Profile" title="Your workspace profile" description="Manage your preferences, identity, and coverage.">
      <Card title="Preferences" description="Personalize your experience.">
        <div className="space-y-3 text-sm text-slate-300">
          <p>Role: Director</p>
          <p>Notifications: Enabled</p>
          <p>Theme: Dark</p>
        </div>
      </Card>
    </PageShell>
  );
}

function DashboardPage() {
  return (
    <PageShell eyebrow="Client workspace" title="Dashboard" description="Follow the latest opportunities and actions in one place.">
      <div className="grid gap-6 md:grid-cols-3">
        <Card title="Pipeline" description="4 new opportunities" />
        <Card title="Meetings" description="2 scheduled today" />
        <Card title="Documents" description="12 shared this week" />
      </div>
    </PageShell>
  );
}

export function WebApp() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <nav className="border-b border-slate-800 bg-slate-950/80 px-4 py-4 text-slate-300 sm:px-6">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4">
          <div className="font-semibold text-white">LAWIM</div>
          <div className="flex flex-wrap gap-3 text-sm">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) => (isActive ? 'text-white' : 'text-slate-400 hover:text-white')}
              >
                {item.label}
              </NavLink>
            ))}
          </div>
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/map" element={<MapPage />} />
        <Route path="/estimation" element={<EstimationPage />} />
        <Route path="/assistant" element={<AssistantPage />} />
        <Route path="/marketplace" element={<MarketplacePage />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="*" element={<HomePage />} />
      </Routes>
    </div>
  );
}
