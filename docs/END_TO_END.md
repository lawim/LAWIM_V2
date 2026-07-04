# End-to-End Integration - LAWIM V2 Release Program U

## Complete End-to-End Flow Documentation

This document traces the complete flow of a typical user journey through all system layers.

## Example Journey: Real Estate Search to Purchase Lead

### Step 1: User Navigates to Search

```
Browser: User clicks "Search" in navigation
Route: /search
Component: SearchPage renders

UI Layer:
- Input field displayed
- Filter panel shown
- Empty search state
```

### Step 2: User Enters Search Query

```
Browser: User types "villa paris"
Event: onChange fired on input
State: query = "villa paris"
Component: Re-renders with new query

UI Layer:
- Search input displays "villa paris"
- Triggers API query
```

### Step 3: Brain Routes Intent

```
Brain Layer Decision:
- Intent: Search for properties
- Confidence: 99%
- Selected Path: "semantic_search_with_filters"
- Alternative Paths: 
  - keyword_search (confidence: 85%)
  - location_search (confidence: 75%)

Routing Logic:
- Detected: Multi-criteria search
- Classification: High-value search
- Path Selection: Use RAG for semantic matching
```

### Step 4: Conversation Context

```
Conversation Layer:
- Dialog Step: 1/3
- Message: "Searching for villas in Paris..."
- Clarification: "Would you like luxury properties?"
- Context History: Maintained

Dialog State:
- User Intent: Clear (property search)
- Confidence: High
- Next Action: Retrieve properties
```

### Step 5: Knowledge Retrieves Context

```
Knowledge Layer - RAG Pipeline:
1. Query Processing:
   - Input: "villa paris"
   - Tokenization: ["villa", "paris"]
   - Embedding: vec([villa=0.92, paris=0.88])

2. Semantic Search:
   - Query vector: [0.92, 0.88]
   - Search space: 5000+ properties
   - Top matches: 15 properties
   - Confidence: 0.87 average

3. Re-ranking:
   - Location filter: Paris (zone)
   - Type filter: Villa
   - Final results: 8 properties
   - Confidence: 0.91 average

4. Citation Building:
   - Property sources identified
   - Confidence scores calculated
```

### Step 6: Agents Execute Business Logic

```
Agents Layer:
1. Search Agent:
   - Receives: query + filters
   - Action: Execute database search
   - Returns: Property IDs [1, 2, 3, 4, 5, 6, 7, 8]

2. Filter Agent:
   - Receives: Results + User preferences
   - Action: Apply additional constraints
   - Returns: Filtered list [1, 3, 4, 5, 7]

3. Rank Agent:
   - Receives: Filtered properties
   - Action: Score by relevance
   - Returns: Ranked list [5, 3, 7, 1, 4]

4. Enrichment Agent:
   - Receives: Ranked properties
   - Action: Add market context
   - Returns: Enhanced property data

Execution Plan:
- Parallel: Agents 1-3 run simultaneously
- Sequential: Agent 4 runs after completion
- Total Time: ~400ms
```

### Step 7: API SDK Calls Backend

```
API SDK Layer:

Mock Mode (VITE_LAWIM_USE_MOCKS=true):
- Mock Delay: 0ms
- Returns: Hardcoded sample properties
- Data: 8 mock villas in Paris
- Response Time: < 1ms

Real Mode (VITE_LAWIM_USE_MOCKS=false):
- Endpoint: GET /v2/properties
- Parameters:
  {
    search: "villa paris",
    filters: { type: "villa", location: "paris" },
    page: 1,
    pageSize: 8
  }
- Response: 
  {
    data: [Property, Property, ...],
    message: "success"
  }
- Response Time: ~500-1000ms
- Error Handling: Retry on timeout
```

### Step 8: UI Updates with Results

```
UI Layer Update:
- Loading state cleared
- SearchPage re-renders
- Results grid populated
- Each card displays:
  - Property image
  - Title
  - Location
  - Price
  - Type badge
  - Rating/score

Rendering:
- React component lifecycle
- Tailwind styles applied
- Responsive layout
- Accessibility features enabled
```

### Step 9: User Clicks Property

```
User Action: Click on Villa property #5
Route Change: /property/5
Component: PropertyDetailPage renders

Browser History: Updated
Deep Link: Now shareable at /property/5
```

### Step 10: Property Details Load

```
Brain Layer:
- Decision: Load full property details
- Intent: Property consultation
- Path: Load related data

API Call:
- Endpoint: GET /v2/properties/5
- Response: Full property details
  {
    id: "5",
    title: "Luxury Villa Paris 16e",
    description: "...",
    location: "75016 Paris",
    type: "Villa",
    surface: "250 m²",
    bedrooms: 5,
    bathrooms: 3,
    price: 1500000,
    ...
  }

UI Display:
- Overview card: Basic info
- Valuation card: Price display
- Details section: Full specifications
- Actions: Add favorite, Request info, Create lead
```

### Step 11: User Clicks "Create Lead"

```
User Action: Click "Create CRM Lead" button
Brain Decision:
- Intent: Create CRM lead
- Path: Sales workflow
- Context: Property #5 auto-populated

Dialog:
- "Creating lead for this property..."
- Pre-fill: Property address, reference
- Confirmation: Lead ID returned

API Call:
- Endpoint: POST /v2/leads
- Payload:
  {
    propertyId: "5",
    source: "property_detail",
    createdAt: "2026-07-04T10:30:00Z"
  }

Response:
- Lead ID: "lead_12345"
- Status: "created"
- Reference: "REF-2026-07-00012345"

UI Feedback:
- Toast: "Lead created successfully"
- Reference number displayed
- Button state: Changed to "View in CRM"
```

### Step 12: Learning & Optimization

```
Learning Layer:
- Event Type: "lead_created_from_search"
- Data:
  {
    searchQuery: "villa paris",
    resultSelected: 5,
    timeToSelect: 45000,  // ms
    leadType: "property",
    confidence: 0.91
  }

System Update:
- User profile updated
- Search preference recorded
- Next searches: Slightly boosted for villas
- Analytics: Logged for reporting

Digital Twin Update:
- User model: Updated with lead history
- Property model: Interaction recorded
- System model: Conversion metric updated
```

### Step 13: Observability Logging

```
Observability Events (all timestamped):

1. workflow_execution:
   - ID: wf_1688484600123_1
   - Type: property_consultation
   - Duration: 2145ms
   - Status: success

2. brain_decision:
   - ID: brain_123
   - Intent: "property_consultation"
   - Confidence: 0.99
   - Path: "detailed_display"

3. knowledge_call:
   - ID: knowledge_456
   - Query: "villa paris"
   - Results: 8 items
   - Confidence: 0.91

4. agent_call:
   - ID: agent_789
   - Type: "search_agent"
   - Action: "retrieve_properties"
   - Status: "success"

5. conversation_event:
   - ID: conv_111
   - Message: "Displaying villas in Paris"
   - Sender: "system"

6. learning_event:
   - ID: learn_222
   - Event: "lead_created"
   - Data: {...}

7. digital_twin_update:
   - ID: twin_333
   - Entity: "user"
   - Change: {hasCreatedLead: true}

All events available in Observability Console (/observability)
```

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ USER JOURNEY: Real Estate Search to CRM Lead                │
└─────────────────────────────────────────────────────────────┘

START: User clicks "Search"
  ↓
[UI LAYER]
SearchPage component
Input: query field
  ↓
User types "villa paris"
  ↓
[BRAIN LAYER]
Intent: Search with criteria
Confidence: 99%
Path: Semantic search
  ↓
[CONVERSATION LAYER]
Dialog: Confirm search
State: User intent clear
  ↓
[KNOWLEDGE LAYER]
RAG: Semantic search
Results: 8 matching properties
Confidence: 0.91
  ↓
[AGENTS LAYER]
Search Agent: Execute query
Filter Agent: Apply constraints
Rank Agent: Score results
Enrichment Agent: Add context
  ↓
[API SDK]
Mode: Mock or Real (same response)
Response: Property list
  ↓
[UI UPDATE]
Display search results
Grid of property cards
  ↓
User clicks property #5
  ↓
[ROUTING]
Navigate to /property/5
  ↓
[API SDK]
Load property details
  ↓
[UI DISPLAY]
Property detail page
Sections: Overview, Valuation, Details
  ↓
User clicks "Create Lead"
  ↓
[AGENTS LAYER]
Create CRM lead
Assign reference
  ↓
[API SDK]
POST /v2/leads
  ↓
[LEARNING LAYER]
Log user behavior
Update recommendations
Update digital twin
  ↓
[OBSERVABILITY]
Log all events
Track metrics
  ↓
[UI FEEDBACK]
Show success toast
Display reference number
  ↓
END: Lead created and visible in CRM
```

## Multi-Layer Orchestration Summary

### Timeline (Total: ~2.5 seconds)

```
Time  | Layer          | Operation                    | Duration
------|---|---|---
0ms   | UI             | Component renders           | 10ms
10ms  | Input          | User types query            | 5000ms (user)
5010ms| Brain          | Intent routing              | 5ms
5015ms| Conversation   | Dialog confirmation         | 2ms
5017ms| Knowledge      | RAG semantic search         | 200ms
5217ms| Agents         | Parallel agent execution    | 150ms
5367ms| API SDK        | Mock/Real API call          | 50ms
5417ms| UI             | Results display             | 50ms
5467ms| User           | Reviews and clicks prop #5  | 3000ms (user)
8467ms| Brain          | Property consultation       | 3ms
8470ms| API SDK        | Load details                | 50ms
8520ms| UI             | Detail page display         | 50ms
8570ms| User           | Clicks create lead button   | 1000ms (user)
9570ms| Brain          | Lead creation intent        | 2ms
9572ms| Agents         | Create CRM lead             | 100ms
9672ms| API SDK        | POST lead                   | 50ms
9722ms| Learning       | Update systems              | 50ms
9772ms| Observability  | Log events                  | 20ms
9792ms| UI             | Show success + reference    | 30ms
9822ms| END            | User sees lead created      | -

Total System Time: ~4.8s (excluding user think time)
System Processing: ~500ms
Network Time: ~200ms
UI Rendering: ~200ms
```

## Error Scenarios

### Network Error During Search

```
Timeline:
1. User initiates search
2. API call made
3. Network timeout (5s)
4. Brain detects: Error state
5. Conversation: "Let me try again..."
6. Agents: Retry with exponential backoff
7. Retry 1: Failed (after 1s)
8. Retry 2: Failed (after 2s)
9. Retry 3: Success after 4s
10. UI: Display results with "Delayed" indicator
```

### Authentication Required

```
Timeline:
1. User tries to access /profile
2. Auth check: Not authenticated
3. Route: Redirect to /login
4. UI: Login page displayed
5. User enters credentials
6. Brain: Validate credentials
7. Auth: Login succeeds
8. Token: Stored in localStorage
9. Route: Redirect to /profile
10. UI: Profile page loads
```

### Permission Denied

```
Timeline:
1. User (viewer role) tries /admin/dashboard
2. Route: Check role-based access
3. Auth: Role is "viewer", not "admin"
4. UI: Display error state
5. Message: "You don't have access to this page"
6. UI: Show "Back to home" button
```

## State Transitions

### Workflow Status Transitions

```
idle
  ↓
loading (data fetch starts)
  ↓
running (processing in layers)
  ↓
├─→ success (completed normally)
├─→ error (exception occurred)
├─→ offline (no network)
├─→ timeout (took too long)
├─→ auth_error (auth failed)
└─→ permission_denied (access denied)
```

### Application State Transitions

```
empty (no data)
  ↓
loading
  ↓
├─→ success (display data)
├─→ error (show error state + retry)
├─→ offline (use mock/cache)
├─→ timeout (show timeout UI + retry)
├─→ auth_error (redirect to login)
└─→ permission_denied (show forbidden page)
```

## Integration Points

### Between Layers

1. **UI → Brain**: Intent extraction from user action
2. **Brain → Conversation**: Dialog state management
3. **Conversation → Knowledge**: Context building
4. **Knowledge → Agents**: Data for business logic
5. **Agents → API SDK**: Endpoint selection
6. **API SDK → Backend**: Network communication
7. **Backend → Response**: Data return
8. **Response → Learning**: Update system models
9. **Learning → Digital Twin**: Update entity state
10. **All → Observability**: Event logging

### Data Flow

```
User Action
    ↓
Browser Event
    ↓
React Component
    ↓
State Update
    ↓
Brain Decision
    ↓
Query Construction
    ↓
Knowledge Processing
    ↓
Agent Execution
    ↓
API Call
    ↓
Backend Processing
    ↓
Response Data
    ↓
State Update
    ↓
UI Rendering
    ↓
User Feedback
```

---

**Last Updated**: July 4, 2026  
**Version**: 1.0  
**Status**: Complete
