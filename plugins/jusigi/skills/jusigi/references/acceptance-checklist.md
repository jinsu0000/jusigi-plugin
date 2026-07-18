# Acceptance checklist

- [ ] User authorized the exact repository and mutations.
- [ ] Existing changes were preserved and reviewed.
- [ ] No secret value was requested, displayed, stored, or committed.
- [ ] Runtime policy is parsed from `config/investment-policy.yaml`.
- [ ] Core/satellite terminology is used; short selling defaults off.
- [ ] All tradeable symbols are on an explicit allowlist.
- [ ] Model output is structured and cannot bypass `RiskGate`.
- [ ] Paper mode is the default and live mode remains disabled.
- [ ] No live order adapter was generated, modified, or enabled.
- [ ] Tests cover cash, holdings, allowlist, confidence, freshness, session, order count, position size, and duplicate-order rejection.
- [ ] Workflow permissions are read-only unless a documented need exists.
- [ ] Scheduled jobs have timeouts and concurrency controls.
- [ ] Pull-request workflows cannot access trading secrets.
- [ ] Data source and freshness are stated in every report.
- [ ] Operations docs include pause, rollback, reconciliation, and incident steps.
- [ ] A secret-pattern scan reports no tracked credential material.
