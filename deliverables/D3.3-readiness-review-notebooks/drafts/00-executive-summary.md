# Executive Summary

This report is deliverable D3.3 of the ESA "Application Development concerning Disaster Data and
Analytics" activity: the readiness review for Work Package 3, "Interactive Analysis Tools and User
Demonstrations." Its title names the analytics-services notebooks specifically, but WP3 is made up of
four linked deliverables: this notebook-publishing platform (D3.3 itself), training material (D3.1),
technical documentation for integration into ESA JupyterLab environments (D3.2), and a demonstration
with IFRC users (D3.4). At the deliverable owner's direction, this report assesses readiness across all
four rather than the notebook-publishing piece in isolation, since the four are sequentially dependent
on one another. WP3's deliverables are due through December 2026, so this report weighs the soundness of
the design and its dependencies more heavily than whether every piece is built today.

## Where things stand

WP3 is the earliest-stage of the project's active work packages, which is expected given its position
downstream of WP1 and WP2. Its core piece, a Django application that lets select users author, run, and
publish analysis notebooks from templates with a light authentication layer, exists today as a detailed
architecture proposal, written up and discussed by the team. The pattern it proposes (parameterised
notebooks, run via papermill, published as static output) is not merely theoretical: WP2's Use Case 1
notebooks already work exactly this way in production, parameterised by country and published as a
working example, which is a strong, concrete validation of the approach ahead of building the Django
layer around it.

The three other WP3 deliverables are downstream of this platform and of the WP2 use-case notebooks
(D2.3), and none has started in earnest:

- **Notebook-publishing architecture (D3.3 core):** proposal complete and discussed with the team, with
  its core pattern already validated by WP2's notebooks; Django/Celery implementation not started.
- **Training material (D3.1):** not started; planned to begin in October, once user-facing notebooks
  and stakeholder consultations exist to train against.
- **Technical documentation for ESA JupyterLab integration (D3.2):** not started.
- **User demonstration with IFRC (D3.4):** not started; depends on the above three.

## Confidence

Confidence in the notebook-publishing architecture is medium-high: every component it proposes (Django,
Celery, Kubernetes, papermill, object storage) is already proven elsewhere in this project's stack, its
core parameterised-notebook pattern is already working in production for WP2's Use Case 1, and
authentication has a low-risk path by delegating to IFRC's existing identity provider rather than
building a new one. Confidence in the training, documentation, and demonstration deliverables landing in
finished form by their nominal dates is medium-low, because each depends on artefacts, stable use-case
notebooks, a working publishing platform, that do not yet exist. Given the December deadline, this is a
sequencing risk, not a design risk or a cause for concern in itself.

## What this report covers

Section 2 gives the state of work for each of the four WP3 deliverables. Section 3 assesses confidence
for each. Section 4 sets out the open questions: four specific, unresolved architecture decisions, the
authentication approach, and a scoping question on how much of WP3 can realistically land before the
Readiness Review meeting. Section 5 sets out a phased implementation plan. Section 6 concludes with
recommendations for the meeting.
