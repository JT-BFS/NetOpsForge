# Augment Control Contract

## Read / Observe Operations
Allowed without ticket:
- show commands
- GET APIs
- health checks
- diagnostics
Engineer awareness still required.

## Write / Change Operations
Allowed ONLY when:
1) Valid ServiceNow ticket
2) Engineer types YES
3) Target tagged allow_execute

If missing → deny and propose instead.
