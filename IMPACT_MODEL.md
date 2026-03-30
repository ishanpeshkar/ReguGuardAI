# ReguGuard AI Impact Model

## Quantified Business Value

| Metric | Manual Process (Human) | ReguGuard AI System | Impact |
|---|---:|---:|---:|
| Analysis Time | 6-8 hours per circular | ~45-90 seconds per circular | ~99% time saved |
| Response Speed | 3-5 days | Real-time | Faster compliance decisions |
| Cost per Circular | ~$500 (legal/compliance counsel time) | ~$0.50-$1.00 (API token usage) | 99.8-99.9% cost reduction |
| Risk Mitigation | Inconsistent human-only review under load | Structured multi-agent checks + audit trail | Reduced missed-change and penalty risk |

## Assumptions Used

- Institution type: mid-sized bank or NBFC with centralized compliance team.
- Circular volume: ~150 relevant circulars/notices per year.
- Manual effort baseline: 6 hours average review effort per circular.
- Fully loaded reviewer cost: $80/hour.
- AI run includes all 5 agents plus orchestration overhead.
- AI token cost range shown as $0.50-$1.00 to account for model and prompt-size variance.

## Annual Cost Logic (Mid-Sized Bank)

Assumption: bank receives ~150 regulatory circulars per year.

### Manual Review Cost

- Hours per circular: 6
- Analyst/legal rate: $80/hour
- Circulars per year: 150

Manual annual cost = 150 x 6 x 80 = $72,000 per year

### AI Review Cost

- Approximate per-circular inference/token cost: $1 (conservative upper band)
- Circulars per year: 150

AI annual cost = 150 x 1 = $150 per year

## Financial Delta

- Annual savings = $72,000 - $150 = $71,850
- Reduction = ($71,850 / $72,000) x 100 = 99.79%

## Sensitivity Snapshot

- If manual review is 4 hours (instead of 6), annual manual spend is $48,000 and savings still exceed 99%.
- If AI cost doubles to $2/circular, annual AI spend is $300 and savings remain >99%.
- Economic result is robust because manual effort dominates total cost.

## Operational Value Beyond Cost

- Near-instant triage allows compliance teams to prioritize high-risk updates first.
- Structured output reduces dependence on individual reviewer quality and availability.
- Audit trail improves defensibility during internal and regulatory audits.
- Faster interpretation cycles shorten the time-to-policy-update across business units.

## Practical Notes

- Actual AI cost varies by model, prompt length, and traffic.
- If premium models are used for selected high-risk circulars, blended cost remains substantially below manual-only review.
- The strongest value is realized when AI outputs feed an approval workflow (human-in-the-loop) instead of replacing governance.
- Runtime depends on document size, API latency, and orchestrator cooldown intervals.
