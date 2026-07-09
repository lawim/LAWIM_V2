# Workflows - LAWIM V2 Release Program U

## Complete Workflow Specifications

This document provides detailed specifications for all 13 business workflows implemented in LAWIM V2 Release Program U.

## Workflow Template

Each workflow follows this orchestration pattern:

```
User Action
    ↓
UI Component Renders
    ↓
Brain Layer - Intent Recognition
    ↓
Conversation Layer - Dialog Management
    ↓
Knowledge Layer - Context Retrieval (RAG)
    ↓
Agents Layer - Business Logic Execution
    ↓
API SDK - Backend Integration
    ↓
Mock/Real API Response
    ↓
State Update
    ↓
UI Re-render
```

## Workflow 1: Real Estate Search

### Description
Users search for properties using filters and keywords.

### Entry Points
- Navigation: `/search`
- Home page: "Search opportunities" button
- Deep link: `/search?query=villa&type=residential`

### User Steps
1. User navigates to search page
2. Enters search query and/or selects filters
3. System displays matching properties
4. User clicks property for details

### Technical Flow

**Layer: UI**
- Component: `SearchPage`
- State: query, filters, results, loading, error
- Events: search input, filter change

**Layer: Brain**
- Decision: Parse search intent
- Classification: Search type (keyword, filter-based, location-based)
- Path: Route to appropriate knowledge source

**Layer: Conversation**
- Dialog: Confirm search filters
- Clarification: Ask for specifics if needed
- Feedback: Provide result summary

**Layer: Knowledge**
- Query Type: Semantic search + filter application
- RAG: Retrieve property embeddings
- Ranking: Sort by relevance + user preferences

**Layer: Agents**
- Search Agent: Execute property search
- Filter Agent: Apply constraints
- Rank Agent: Sort results

**Layer: API SDK**
- Endpoint: `GET /v2/properties`
- Parameters: `search`, `filters`, `page`, `pageSize`
- Mock Data: 10 sample properties

### States Handled
- Loading: "Loading properties..."
- Empty: "No properties matched"
- Error: "Unable to load properties" + Retry
- Offline: Mock fallback data
- Success: Display results

### Testing
```bash
# Mock mode
VITE_LAWIM_USE_MOCKS=true npm run test

# API mode
VITE_LAWIM_USE_MOCKS=false npm run test
```

---

## Workflow 2: Property Consultation

### Description
Users view detailed information about a specific property.

### Entry Points
- From search results: Click property card
- Direct link: `/property/:id`
- Map: Click property marker

### User Steps
1. User selects a property
2. System loads full details
3. User reviews information
4. User can add to favorites or request more info

### Technical Flow

**Layer: UI**
- Component: `PropertyDetailPage`
- Params: `id` from URL
- Sections: Overview, Valuation, Details, Actions

**Layer: Brain**
- Decision: Property display format selection
- Classification: Property type (residential, commercial, etc.)
- Path: Determine detail depth

**Layer: Conversation**
- Dialog: Offer related properties
- Dialog: Refine the need when more precision is useful
- Upsell: Suggest similar properties
- CTA: "Would you like to see similar properties?"

**Layer: Knowledge**
- Query: Property details retrieval
- Context: Related properties and market data
- Enrichment: Comparable properties

**Layer: Agents**
- Property Agent: Load property details
- Comparison Agent: Find similar properties
- Recommendation Agent: Suggest next actions

**Layer: API SDK**
- Endpoint: `GET /v2/properties/:id`
- Response: Full property details
- Mock Data: Single property with all fields

### Related Workflows
- Add to Favorites (from this page)
- Create CRM Lead (from this page)
- Property Estimation (from this page)

---

## Workflow 3: Add to Favorites

### Description
Authenticated users save properties to their favorites list.

### Entry Points
- Property detail: "Add to favorites" button
- Search results: Star icon
- Favorites page: Remove from favorites

### User Steps
1. User clicks favorite button
2. System saves to user's favorites
3. Visual confirmation shown
4. Favorites count updated

### Technical Flow

**Layer: UI**
- Component: Star/heart icon toggle
- Animation: Smooth transition
- Feedback: Toast notification

**Layer: Brain**
- Decision: Permission check
- Classification: User favorite preference
- Path: Save or remove

**Layer: Conversation**
- Dialog: "Added to favorites" confirmation
- Suggestion: "Check your favorites anytime"

**Layer: Knowledge**
- Update: User preference store
- Context: User favorites list

**Layer: Agents**
- Preference Agent: Save favorite
- Notification Agent: Alert user

**Layer: API SDK**
- Endpoint: `POST /v2/favorites` (add), `DELETE /v2/favorites/:id` (remove)
- Auth: Required (Protected route)

### Protection
- ✅ Requires authentication
- ✅ User data isolation
- ✅ CSRF token validation

---

## Workflow 4: Account Creation

### Description
New users create an account.

### Entry Points
- Login page: "Create account" link
- Direct link: `/register` (planned)

### User Steps
1. User fills the registration form
2. System validates required fields and uniqueness
3. Account created
4. User redirected to dashboard

### Technical Flow

**Layer: UI**
- Component: Registration form
- Fields: Full name, Email, Username, WhatsApp number, Password, Confirmation, Preferred language, Conditions checkbox
- Validation: Real-time feedback

The registration flow requires a unique email, a unique username and a WhatsApp number. The phone number is mandatory.

**Layer: Brain**
- Decision: Account creation approval
- Classification: Public user account by default
- Path: Welcome flow

**Layer: Conversation**
- Dialog: Welcome message
- Onboarding: Introduction to platform

**Layer: API SDK**
- Endpoint: `POST /api/auth/register`
- Payload: `{ full_name, email, username, phone_e164, password, password_confirmation, preferred_language, accept_terms }`
- Mock: Returns success with sample user

### States
- Validation errors
- Email exists
- Username exists
- WhatsApp number exists
- Success creation

---

## Workflow 5: Authentication

### Description
Users log in to access protected features.

### Entry Points
- Login page: `/login`
- Protected route redirect

### User Steps
1. User enters identifier and password
2. System validates credentials
3. Token stored
4. Redirect to dashboard

### Mock Credentials
| Usage | Email | Username | Phone | Password |
| --- | --- | --- | --- | --- |
| Admin | `admin@lawim.app` | `admin` | `+237686822667` | `LAWIM@Demo2026µ` |
| Manager | `manager@lawim.app` | `manager` | `+237686822668` | `LAWIM@Demo2026µ` |
| Agent LAWIM | `agent@lawim.app` | `agent` | `+237686822669` | `LAWIM@Demo2026µ` |
| Utilisateur propriétaire | `owner@lawim.app` | `owner` | `+237686822670` | `LAWIM@Demo2026µ` |
| Investisseur / Banque | `investor@lawim.app` | `investor` | `+237686822671` | `LAWIM@Demo2026µ` |

The runtime keeps these five standard accounts synchronized at startup so they remain usable across environments.

### Login Rule
- Identifier accepted as email, phone number or username
- Endpoint: `POST /api/auth/login`
- Payload: `{ identifier, password }`

The access page stays minimal: one central card, a discreet language selector, and a compact contact band in the footer.

### Technical Flow

**Layer: Auth Store**
- Zustand store with login/logout
- localStorage persistence
- Auto-hydration on load

**Layer: API SDK**
- Endpoint: `POST /api/auth/login`
- Response: `{ user, token, roles }`

### Protected Routes
All routes with `<ProtectedRoute>` wrapper:
- `/profile`
- `/dashboard`
- `/favorites`
- `/notifications`
- `/requests`
- `/documents`

---

## Workflow 6: Create CRM Lead

### Description
System creates CRM records from property interactions.

### Entry Points
- Property detail: "Create lead" button
- Admin dashboard: Manual entry

### User Steps
1. User initiates lead creation
2. System populates from property context
3. Lead created in system
4. Confirmation shown

### Technical Flow

**Layer: UI**
- Trigger: Button or automatic
- Form: Property-pre-filled

**Layer: Brain**
- Decision: Lead type classification
- Path: CRM integration

**Layer: Agents**
- CRM Agent: Create record
- Notification Agent: Alert sales

**Layer: API SDK**
- Endpoint: `POST /v2/leads` (planned)

---

## Workflow 7: Create Service Request

### Description
Users submit service requests (inspections, valuations, etc.).

### Entry Points
- Requests page: `/requests`
- Property detail: "Request service"

### User Steps
1. User selects service type
2. User provides details
3. Request submitted
4. Confirmation with reference number

### Technical Flow

**Layer: UI**
- Component: Service request form
- Types: Inspection, Valuation, etc.

**Layer: Brain**
- Decision: Request routing
- Path: Appropriate handler

**Layer: Agents**
- Request Agent: Process submission
- Workflow Agent: Assign handler

**Layer: API SDK**
- Endpoint: `POST /v2/requests`
- Response: Request record with ID

---

## Workflow 8: Marketplace

### Description
Users browse the marketplace for services and deals.

### Entry Points
- Navigation: `/marketplace`
- Home page: Marketplace widget

### User Steps
1. User browses listings
2. User filters by category
3. User views item details
4. User contacts seller

### Technical Flow

**Layer: UI**
- Component: `MarketplacePage`
- Grid: Item cards

**Layer: API SDK**
- Endpoint: `GET /v2/marketplace`
- Mock: Sample listings

---

## Workflow 9: Property Estimation

### Description
System estimates property value based on input.

### Entry Points
- Navigation: `/estimation`
- Home page: Quick estimation widget

### User Steps
1. User enters property details
2. User clicks "Generate estimate"
3. System returns valuation
4. User can save result

### Technical Flow

**Layer: UI**
- Component: `EstimationPage`
- Form: Address, size, type, expected price
- Result: Estimated value + confidence

**Layer: Brain**
- Decision: Valuation model selection
- Path: Appropriate estimation engine

**Layer: Agents**
- Valuation Agent: Calculate estimate
- Confidence Agent: Assess reliability

**Layer: API SDK**
- Endpoint: `POST /v2/estimations`
- Response: `{ estimate, confidence }`
- Mock: Fixed estimate with confidence

---

## Workflow 10: AI Assistant

### Description
Users interact with AI assistant for guidance.

### Entry Points
- Navigation: `/assistant`
- Floating chat (planned)
- Contextual help

### User Steps
1. User opens assistant
2. User states an intent in natural language
3. Assistant asks the useful clarifying questions
4. Answers are reused to enrich the search and matching context
5. Assistant responds with next actions or compatible results

### Technical Flow

**Layer: UI**
- Component: `AssistantPage`
- Chat: Message input + history

**Layer: Brain**
- Decision: Intent recognition
- Path: Appropriate assistant module

**Layer: Conversation**
- Dialog: Multi-turn conversation with progressive qualification
- Context: Maintain state

**Layer: Knowledge**
- Query: Retrieve relevant information
- Context: Build response

**Layer: Agents**
- Assistant Agent: Generate response
- Learning: Learn from interactions

**Layer: API SDK**
- Endpoint: `POST /v2/assistant`
- Method: `askAssistant({ message })`
- Mock: Canned responses

---

## Workflow 11: Document Search

### Description
Users search documents and knowledge base.

### Entry Points
- Navigation: `/documents`
- Assistant (as reference)

### User Steps
1. User enters search query
2. System searches documents
3. Results displayed
4. User clicks to view document

### Technical Flow

**Layer: Knowledge**
- RAG: Semantic document search
- Ranking: Relevance scoring

**Layer: API SDK**
- Endpoint: `GET /v2/documents/search`
- Method: `searchDocuments(query)`

---

## Workflow 12: User Dashboard

### Description
Authenticated users view their dashboard.

### Entry Points
- Navigation: `/dashboard`
- Home page: "Open dashboard" button
- After login: Auto-redirect

### User Steps
1. User authenticates
2. Dashboard loads as a short cockpit
3. User sees the essentials first: greeting, activity, priorities, quick stats and module cards
4. User opens a dedicated module when needed and can always return to the dashboard

### Technical Flow

**Layer: UI**
- Component: `DashboardPage`
- Widgets: Statistics, actions, notifications

**Layer: API SDK**
- Endpoint: `GET /v2/dashboard/summary`
- Response: `{ properties, opportunities, communications, pendingTasks }`

---

## Workflow 13: Admin Dashboard

### Description
Admin users access administrative dashboard.

### Entry Points
- Navigation: `/admin/dashboard` (role-protected)
- Requires admin role

### User Steps
1. User with admin role logs in
2. Navigation shows admin menu
3. User accesses admin dashboard
4. Admin sees system-wide metrics

### Technical Flow

**Layer: Auth**
- Role Check: Admin only
- Protected Route: Requires `admin` role

**Layer: API SDK**
- Endpoint: `GET /v2/admin/dashboard` (planned)
- Response: System-wide metrics

---

## Shared Infrastructure

### Error Handling
All workflows implement:
- Loading states
- Error boundaries
- Retry logic
- Fallback UI

### State Management
- Zustand stores for complex state
- React Query for server state
- Local component state for UI

### Testing Strategy
- Unit: Component rendering
- Integration: Workflow completion
- E2E: Full user journey
- Mock vs. Real mode verification

---

## Performance Targets

- Page load: < 2s
- Workflow execution: < 1s average
- Search results: < 500ms
- API response: < 1s

## Accessibility

All workflows are:
- WCAG 2.1 Level AA compliant
- Keyboard navigable
- Screen reader friendly
- Color blind friendly

---

**Last Updated**: July 4, 2026  
**Version**: 1.0  
**Status**: Complete
