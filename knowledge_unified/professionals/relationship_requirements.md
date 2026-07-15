# Relationship Requirements for Professionals

## Source: LAWIM KNOWLEDGE/roles-matrix.md + KNOWLEDGE/runtime-gap-remediation-plan.md

## Agent ↔ Client Relationship

### Assignment Rules
- Max 3 agents shown to a client per lead
- Client chooses which agent(s) to contact
- Exclusive mandates: 1 agent receives the lead exclusively
- Agents are matched by: zone, specialty, reactivity, trust_score, history

### Agent Responsibilities
| Responsibility | Description |
|----------------|-------------|
| Acknowledge lead | Within 15 minutes of assignment |
| Contact client | Within 24 hours |
| Property visit | Within 48 hours of client agreement |
| Availability update | Daily (property still available or not) |
| Client feedback | After every interaction |
| Transaction follow-up | Until deal is closed or abandoned |

### Client Rights
- View agent profile, ratings, and history
- Accept/reject agent assignment
- Request different agent if unsatisfied
- Direct contact with property owner if introduced

## Agent ↔ LAWIM Platform Relationship

### SLA Requirements

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| Lead response time | < 2 hours | > 24 hours → lead reassigned |
| Lead completion rate | > 80% | < 50% → account suspended |
| Trust score | > 3.0/5.0 | < 2.0 → account review |
| Accuracy of listings | 100% | Any verified inaccuracy → warning |
| Client satisfaction | > 4.0/5.0 | < 3.0 → account review |

### Commission Model
| Transaction Type | Standard Commission | Notes |
|-----------------|-------------------|-------|
| Sale (agent) | 5-10% | Negotiable per mandate |
| Rent (agent) | 1 month rent | One-time from owner |
| Direct owner | 0% | No commission |
| Promoter | Per agreement | Project-based |

### Suspension Grounds
1. Repeated failure to respond to leads within SLA
2. Verified false or misleading property listings
3. Client complaints (3+ unresolved)
4. Fraud or attempted fraud
5. Trust score below 2.0
6. Harassment of clients or operators

## Operator ↔ Agent Relationship

### Operator Duties
- Triage incoming requests within 5 minutes
- Assign leads to best-matching agents
- Review agent performance weekly
- Handle escalated client issues
- Quality-check published properties

### Escalation Path
```
Client Issue → Operator → Manager → Admin
Agent Issue → Manager → Admin
Technical Issue → Operator → Admin
Fraud Signal → Operator → Legal → Admin
```

## Partner Professional Relationships

### Notary ↔ LAWIM
- LAWIM recommends notaries for title verification
- Notaries verify land titles at regulated fees
- Notaries provide authentication for sale acts

### Land Expert ↔ LAWIM
- Land experts provide feasibility studies
- Experts perform land surveys
- Experts verify boundaries and title status

### Architect ↔ LAWIM
- Architects provide design plans for construction projects
- Architects assist with building permits
- Architects supervise construction for investors

## Multi-Agent Relationships

### Co-agency Rules
- Multiple agents can be associated with one property (co-listing)
- Commission split: must be pre-agreed between agents
- Lead attribution: first agent to introduce the client gets priority
- Dispute resolution: handled by LAWIM operations team

### Agent Queue Management
- Agents are presented in round-robin order by default
- Premium/subscribed agents get priority placement
- Performance-based boosting: higher trust score → higher queue position
- Clients can request specific agents by name
