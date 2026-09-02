# Executive Summary

This report is deliverable D3.3 of the ESA "Application Development concerning Disaster Data and
Analytics" activity: the readiness review for Work Package 3, "Interactive Analysis Tools and User
Demonstrations." Its title names the analytics-services notebooks specifically, but WP3 is made up of
four linked deliverables: this notebook-publishing platform (D3.3 itself), training material (D3.1),
technical documentation for integration into ESA JupyterLab environments (D3.2), and a demonstration
with IFRC users (D3.4). At the deliverable owner's direction, this report assesses readiness across all
four rather than the notebook-publishing piece in isolation, since the four are sequentially dependent
on one another.

## Where things stand

WP3 is the earliest-stage of the project's active work packages. Its core piece, a Django application
that lets select users author, run, and publish analysis notebooks from templates with a light
authentication layer, exists today as a detailed architecture proposal, written up and discussed by the
team but not yet built. The three other WP3 deliverables are downstream of it and of the WP2 use-case
notebooks (D2.3), and none has started in earnest:

- **Notebook-publishing architecture (D3.3 core):** proposal complete and discussed with the team; no
  implementation started.
- **Training material (D3.1):** not started; planned to begin in October, once user-facing notebooks
  and stakeholder consultations exist to train against.
- **Technical documentation for ESA JupyterLab integration (D3.2):** not started.
- **User demonstration with IFRC (D3.4):** not started; depends on the above three.

This sequencing was expected: WP3 begins after WP1 and WP2 lay the foundation it builds on.

## Confidence

Confidence in the notebook-publishing architecture is medium: every component it proposes (Django,
Celery, Kubernetes, papermill, object storage) is already proven elsewhere in this project's stack, and
authentication has a low-risk path by delegating to IFRC's existing identity provider rather than
building a new one. Confidence in the training, documentation, and demonstration deliverables landing in
finished form by their nominal dates is low-medium, because each depends on artefacts, stable use-case
notebooks, a working publishing platform, that do not yet exist. This is a sequencing risk, not a
design risk.

## What this report covers

Section 2 gives the state of work for each of the four WP3 deliverables. Section 3 assesses confidence
for each. Section 4 sets out the open questions: four specific, unresolved architecture decisions, the
authentication approach, and a scoping question on how much of WP3 can realistically land before the
Readiness Review meeting. Section 5 sets out a phased implementation plan. Section 6 concludes with
recommendations for the meeting.
