# Executive Summary

This report is deliverable D3.3 of the ESA "Application Development concerning Disaster Data and
Analytics" activity: the readiness review for Work Package 3, "Interactive Analysis Tools and User
Demonstrations." Its title names the analytics-services notebooks specifically, but WP3 is made up of
four linked deliverables: this notebook-publishing platform (D3.3 itself), training material (D3.1),
technical documentation for integration into ESA JupyterLab environments (D3.2), and a demonstration
with IFRC users (D3.4). This report assesses readiness across the full proposed notebook publishing pipeline. WP3's deliverables are due in December 2026, so this report weighs the soundness of
the design and its dependencies more heavily than whether every piece is built today.

## Current state

WP3 is the earliest-stage of the project's active work packages, which is expected given its position
downstream of WP1 and WP2. Its core piece is a notebook-publishing pipeline with four functional pieces:

1. Triggering a run;
2. Generating the notebook output;
3. Compiling it to a static site, and;
4. Distributing the result.

Two of the
four, notebook generation and static-site compilation, have been tested to work with WP2's Use Case 1 notebook, parameterised by country and published as a
working example. This is a concrete validation of the platform's central mechanism. The other two,
triggering beyond WP2's existing automated events, and distribution, are not yet built. Rather than
committing to a specific orchestration technology now, this report identifies the four pieces and
assesses confidence in each individually.

The three other WP3 deliverables are downstream of this platform and of the WP2 use-case notebooks
(D2.3), and none has started in earnest:

- **Notebook-publishing pipeline (D3.3 core):** four core pieces identified; notebook generation and
  static-site compilation already validated in production by WP2; triggering and distribution not yet
  built.
- **Training material (D3.1):** not started; planned to begin in October, once user-facing notebooks
  and stakeholder consultations exist to train against.
- **Technical documentation for ESA JupyterLab integration (D3.2):** not started.
- **User demonstration with IFRC (D3.4):** not started; depends on the above three.

## Confidence

Confidence in the notebook-publishing pipeline is high overall, and uneven across its four pieces:
high for notebook generation and static-site compilation, already working in production for WP2's Use
Case 1, and lower for triggering and distribution, which are undesigned. Authentication is proposed for this piece to allow authenticated users to "self-service" their own notebook runs, but is not essential.
Confidence in the training, documentation, and demonstration deliverables landing in
finished form by their nominal dates is medium, because each depends on artifacts, stable use-case
notebooks, a working publishing platform, that do not yet exist. Given the December deadline, this is a
sequencing risk, not a design risk or a cause for concern.

## What this report covers

Section 2 gives the state of work for each of the four WP3 deliverables. Section 3 assesses confidence
for each. Section 4 sets out the open questions: four specific, unresolved architecture decisions, the
authentication approach, and a scoping question on how much of WP3 can realistically land before the
Readiness Review meeting. Section 5 sets out a phased implementation plan. Section 6 concludes with
recommendations for the meeting.
