# DAG Plan: P2P API Distribution Campaign
Cycle Limit: 10 Minutes

## Phase 1: Parallel Execution (Leads & Packaging)
### Task 1A: Lead Generation
- **Assigned:** `frontend-engineer`
- **Goal:** Gather a list of 5-10 developer/indie hacker leads looking for Stripe/PayPal alternatives (using mock emails or GitHub usernames).
- **Output:** `workdir/leads.json`

### Task 1B: Stack Packaging
- **Assigned:** `backend-engineer`
- **Goal:** Package `p2p_invoice_generator`, `p2p_api_service`, and `p2p_distributor.py` into a single downloadable bundle.
- **Output:** `workdir/p2p_api_stack_v1.zip`

## Phase 2: Distribution Execution
**Dependencies:** Phase 1 (1A & 1B) complete.
### Task 2A: Campaign Dispatch
- **Assigned:** `devops-engineer`
- **Goal:** Connect `p2p_distributor.py` to target the leads from `leads.json` using the bundle `p2p_api_stack_v1.zip`. If SMTP is unavailable, use mock print outputs or GitHub comments.
- **Output:** `workdir/distribution_log.json`

## Phase 3: QA & Verification
**Dependencies:** Phase 2 complete.
### Task 3A: Campaign Verification
- **Assigned:** `qa-reviewer`
- **Goal:** Verify the bundle is valid and that outreach was logged correctly in `distribution_log.json`.

## State Management & Routing
- Update `workdir/task_state.json` after each phase to dictate the `next_agent`.
- If a phase fails repeatedly, assign `next_agent: system-planner` for DAG recomputation.
