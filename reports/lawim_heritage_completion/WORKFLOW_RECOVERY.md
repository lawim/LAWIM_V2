# WORKFLOW RECOVERY REPORT — LAWIM H0.4

**Date:** 15 July 2026
**Source:** 05-WORKFLOW-REFERENCE.md (4,749 lignes, backup branch)

---

## Workflows Recovered

| # | Workflow | States | Source | Confidence |
|---|----------|--------|--------|------------|
| 1 | Property Lifecycle | Creation→Qualification→Validation→Published→Available→Matching→Visits→Negotiation→Reserved→Transaction→Unavailable→Archived | 05-WORKFLOW Ch34-51 | HIGH |
| 2 | Dossier Lifecycle | Creation→Qualification→Matching→Proposal→Follow-up→Resolution→Archived | 05-WORKFLOW Ch52-73 | HIGH |
| 3 | Matching Lifecycle | Need→Criteria→Search→Match→Proposal→Decision→Learning→Rematching→Closed | 05-WORKFLOW Ch5 + 04-MATCHING | HIGH |
| 4 | Contact Lifecycle | Interest→Introduction→Consent→Exchange→Visit Proposal→Visit→Negotiation→Transaction→End | 05-WORKFLOW Ch74-89 | HIGH |
| 5 | Visit Lifecycle | Request→Scheduling→Confirmation→Preparation→Visit→Feedback→Follow-up→Closed | 05-WORKFLOW Ch90-108 | HIGH |
| 6 | Negotiation Lifecycle | Opening→Discussion→Offers→Counter-offers→Agreement→Formalization | 05-WORKFLOW Ch109-127 | HIGH |
| 7 | Transaction Lifecycle | Agreement→Documents→Financing→Signing→Payment→Transfer→Completion | 05-WORKFLOW Ch128-145 | HIGH |
| 8 | Payment Lifecycle | Service Selection→Quote→Validation→Payment→Confirmation→Delivery | 05-WORKFLOW Ch147-163 | HIGH |
| 9 | Disputes Lifecycle | Reception→Analysis→Mediation→Resolution→Closure→Appeal | 05-WORKFLOW Ch164-181 | HIGH |
| 10 | Archiving Lifecycle | Inactivity Detection→Warning→Archiving→Retention→Permanent Deletion | 05-WORKFLOW Ch182-194 | HIGH |
| 11 | Mediation Workflow | Complaint→Analysis→Mediator→Proposal→Accept/Reject→Resolution | 05-WORKFLOW Ch195 | HIGH |
| 12 | User Identity Lifecycle | Registration→Validation→Verification→Active→Suspended→Archived | 08-ROLE Ch16-30 | HIGH |
| 13 | Organization Lifecycle | Creation→Configuration→Validation→Active→Suspended→Closed | 08-ROLE Ch75-89 | HIGH |
| 14 | Agent Invitation | Invitation→Acceptance→Training→Validation→Active | 08-ROLE Ch24, Ch82 | HIGH |
| 15 | Publication (SIE) | Creation→Qualification→Validation→Publication→Distribution | 05-WORKFLOW Ch212 | HIGH |
| 16 | Redirection (SIE) | Detection→Analysis→Redirection→Follow-up | 05-WORKFLOW Ch213 | HIGH |
| 17 | Conversion & Attribution | Contact→Interest→Qualification→Conversion→Attribution | 05-WORKFLOW Ch214 | HIGH |
| 18 | CRM Pipeline (8 stages) | Prospection→Qualification→Presentation→Proposal→Follow-up→Closing→Activation→Retention | CRM_MODEL.md | HIGH |
| 19 | Agent Opt-In | Detection→Request→Log→Sharing | CRM_MODEL.md | HIGH |
| 20 | Identity Resolution | Detection→Comparison→Scoring→Merge/Keep→Notification | CRM_MODEL.md | HIGH |
| 21 | Main Cross-cutting | Spans all workflows, coordinates transitions | 05-WORKFLOW Ch203 | HIGH |

## SLA Definitions

| Property Type | First Match | First Rematch | First Follow-up |
|--------------|------------|--------------|-----------------|
| Chambre | immédiat | 24h | 48h |
| Studio | immédiat | 48h | 72h |
| Appartement | immédiat | 72h | 5 jours |
| Maison | immédiat | 5 jours | 7 jours |
| Villa | immédiat | 7 jours | 10 jours |
| Duplex | immédiat | 7 jours | 10 jours |
| Terrain résidentiel | immédiat | 10 jours | 15 jours |
| Terrain agricole | immédiat | 15 jours | 20 jours |
| Terrain industriel | immédiat | 20 jours | 30 jours |
| Commerce | immédiat | 7 jours | 10 jours |
| Bureau | immédiat | 10 jours | 15 jours |
| Entrepôt | immédiat | 15 jours | 20 jours |
| Hôtel | immédiat | 30 jours | 45 jours |
| Immeuble | immédiat | 30 jours | 45 jours |

## Next Best Action (NBA) Rules

12 official NBA actions:
1. Ask a question
2. Launch matching
3. Launch rematching
4. Present one property
5. Present multiple properties
6. Contact holder
7. Organize visit
8. Schedule follow-up
9. Notify
10. Open negotiation
11. Request document
12. Close dossier

**Source:** docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md §20
