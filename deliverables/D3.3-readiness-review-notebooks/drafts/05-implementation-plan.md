# Implementation Plan

This plan phases WP3 from its current state, two of the four pipeline pieces validated and the trigger
and distribution pieces not yet built, to a working, demonstrated platform. It is sequenced around WP3's
dependency chain rather than starting deliverables in parallel that are not yet actionable.

## Phase 1 — Resolve open questions and stand up a minimal skeleton (through September 2026)

1. **Answer the four architecture questions** (Section 4.1) in a short, written design decision.
   Provisional answers are enough to unblock building; they do not need to be permanent.
2. **Decide the baseline-computation strategy** jointly with D2.3's Section 5, item 1. This one
   decision simplifies both WP2's Use Case 1 delivery and this platform's data model.
3. **Confirm the authentication approach** (Section 4.2) with the owner of IFRC's identity platform,
   and design the trigger/orchestration piece's user/permission model around delegated authentication
   from day one rather than retrofitting it.
4. **Stand up a minimal, end-to-end version of the four pipeline pieces** (Section 2.1) that can run one
   existing WP2 notebook (the most stable of the three use cases; see D2.3): select parameters, run the
   notebook, compile it to a static site, publish it. This is deliberately narrow in scope, one
   notebook, one hazard, to prove the trigger and distribution pieces before generalising them, without
   committing yet to a specific job-queue or execution technology.

## Phase 2 — First official templates and training content in parallel (October–November 2026)

5. **Register the WP2 use-case notebooks as templates** in the platform as each reaches a stable,
   validated state per D2.3's timeline, starting with Use Case 1, then Use Case 2.
6. **Begin training material development (D3.1)** in parallel, per MapAction's own October start plan,
   once there is a real (if minimal) platform and at least one stable notebook to train against.
7. **Add object-storage publishing and the discovery/browse UI**, so generated analyses are findable by
   country, administrative area, and event: the second half of the use-case description in Section 2.1.

## Phase 3 — Authoring layer and documentation (November–December 2026)

8. **Build the light authoring UI** for select, authorised users: copy-from-template, a parameter form,
   submit-and-track-a-run, restricted by the delegated-authentication model from Phase 1.
9. **Implement the "published vs. scratchpad" distinction** decided in Section 4.1, item 3, as a
   first-class status on generated outputs.
10. **Draft technical documentation for ESA JupyterLab integration (D3.2)**, once the platform's
    notebook/environment contract is stable enough that the documentation will not need immediate
    rework.

## Phase 4 — Demonstration (early 2027, or as training and platform maturity allow)

11. **Run the IFRC user demonstration (D3.4)**, once training material (D3.1) and the platform (D3.3)
    are both far enough along to support a meaningful session with real National Society users, ideally
    incorporating the same National Societies interviewed during WP2's consultation round (D2.3, Section
    4.5) for continuity.

## Ongoing

12. **Assign an owner for notebook-catalogue governance** (Section 4.1, item 4) before the catalogue
    grows large enough for tidiness to become a real problem. This is cheap to do early and expensive
    to retrofit.

## Sequencing rationale

D3.1, D3.2, and D3.4 are deliberately not started in parallel with Phase 1, since each depends on
artefacts that do not yet exist; starting them early would mean redoing that work once the platform's
shape is known. This plan is scoped for the fastest realistic path to a working, demonstrated system.
