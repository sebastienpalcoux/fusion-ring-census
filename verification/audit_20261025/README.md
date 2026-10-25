# Correctness audit — 25 October 2026

All **1,433,410 supplied rank‑3–11 tensors** passed exact fusion axioms and exhaustive based-isomorphism checks, with no duplicate classes; 43 software tests passed. The entire upstream enumeration was not regenerated. [Scope and counts](summary.json).

The companion classification retains **1,433,022 general exclusions, 378 realized rings and ten unresolved cases**. It incorporates exact replacement proofs for R6_2_143, R8_2_820 and R8_2_869, a direct exact identification of R8_3_721 without census completeness, and implementation/replay corrections. No tensor or classification status changes.

[Current proofs, correction details and exact commands](https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/main/evidence/correctness_20261025) · [Full original audit evidence](https://sebastienpalcoux.github.io/grothendieck-ring-classification/downloads/correctness-audit-2026-10-25.zip)

The audit pins the census at `a69cd7e10047a7d86f3f03a7c43cb52dbc73c2f0` and classification at `8014c749c17ddd2ad3d1b99a4359d49a8be921c5`. The new publication is a documented correction overlay; old receipts retain their original source identities and failures. Input validation, proof review, finite replay and external categorical existence are separate claims. Independent human verification and formalization remain pending.

The responsive census page uses the same address on phones and desktops. [Post-revision browser and software checks](mobile-replay-receipt.json) cover narrow-phone, phone, tablet and desktop widths; all 43 unit tests also pass after the mobile revision.
