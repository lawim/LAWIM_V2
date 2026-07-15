# Matching Score Explanations

## How to Explain Scores to Users/Agents

### Philosophy
LAWIM is a ranking engine, not a filtering engine. Scores measure **estimated compatibility** between a Request and a Property, not absolute property quality.

### Score Components (Total 100)

| Component | Weight | What it measures |
|-----------|--------|-----------------|
| Geographic | 20% | Is property where client wants to live? |
| Mobility | 20% | Does travel distance match tolerance? |
| Property Type | 15% | Is property type compatible? |
| Budget | 10% | How far from budget? (preference, not constraint) |
| Standing | 10% | Quality level alignment |
| Services | 10% | Requested amenities present |
| Freshness | 15% | How recent/active is listing? |

### Bonuses/Maluses
- **Availability confirmed**: +10
- **Availability unconfirmed**: -20 (a great property that's taken has zero value)
- **Badges**: VERIFIED, RELIABLE, FAST_RESPONDER, TRUSTED_OWNER, TOP_AGENT all add bonus

### Speaking to Users
```
"This property scored [X]/100 because:
- It's in the neighborhood you requested ✓
- It's within your budget range ✓
- The property type matches ✓
- [Any missing items]"
```

### Speaking to Agents
```
"Match score: 85/100
- Geographic: 18/20 (exact neighborhood)
- Mobility: 17/20 (flexible mode)
- Type: 15/15 (apartment requested → apartment)
- Budget: 8/10 (5% above max)
- Freshness: 12/15 (listed 6 days ago)
- Availability: +10 (confirmed)"
```

### Exclusion Reasons
- Property is ARCHIVED, SOLD, RENTED, INACTIVE
- Property was explicitly rejected by this requester (blacklisted)
