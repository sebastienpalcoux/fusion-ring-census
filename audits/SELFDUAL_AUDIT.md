> Supplied package report, retained unchanged below. Its timings refer to the
> producer of that package. Fresh integration checks are recorded separately in
> `verification/optimization_20261021/`.

# Independent checks of the self-dual pruning

The added tests check necessary conditions independently of the optimized enumeration. They do not infer completeness merely from matching class counts.

## Mathematical checks

Write `u` for the fixed mixed-coefficient row, `Q` for the symmetric tail of the first multiplication matrix, `q = Q e_0`, and `t_j = T_{00j}`. All integer entries lie in `[0,M]`; the mixed entries of `t` lie in `[b,M]`. The weight `C` is 1 ordinarily and 2 in the existing folded subproblem.

* The canonical row filter is valid because changing the distinguished nonunit generator and sorting the other generators gives the first parameter block `sort(Q_ii, T_iik : k != i)`. A canonical parameter vector has this block lexicographically at least `u`. Permuting positions with equal `u_k` preserves both the weighted contraction and the sorted block; the mask constructor's symmetry reduction therefore preserves every attainable value. Increasing `Q_ii` cannot decrease the sorted tuple, which justifies its binary search.
* The first two witness equations are exact consequences of associativity. Set `B = T_0 u - Q^2 e_0 - u u_0 + C e_0 + a Q e_0` and `K = [Q,T_0] - q u^t + u q^t`. Their scalar residuals are respectively `(Q B - K u)_0` and `(Q^2 B - Q K u - K Q u)_0`. The random-identity check constructs these associativity blocks directly and compares them with the optimized moment formulas.
* Prefix intervals and gcd conditions are necessary conditions on an integer linear sum. The last two edge values are tested against both the exact linear equation and the exact quadratic moment equation. They are never selected by numerical approximation.
* Witness residuals are advanced only for the current supported indices and restored after recursion. Descendants write higher-index support lists, leaving the parent's restoration list unchanged. Witnesses are rebuilt only before any witness-dependent descendant state is active.
* When `sum(u)=0`, every witness moment is independent of `t`; the choice `t=0` represents all witnesses for this filter. The complete tail enumeration still runs normally.
* Reaching either witness resource cap disables witness pruning for the entire current first-row subtree, with the original allowed mask retained. Partial witness lists are discarded. Thus the caps weaken pruning and cannot remove solutions.

For `N <= 6`, `M <= 15`, and `C <= 2`, a conservative absolute bound for a first-moment residual is 202,530; adding a suffix interval endpoint stays below 304,000. These fit signed 32-bit arithmetic. The second moment and its polynomial coefficients use signed 64-bit arithmetic; direct moment sums have absolute triangle bounds below 33 million in this range. Mask shifts use indices at most 15.

## Executable evidence

`audit_selfdual_local.cpp` includes the package's actual enumeration source, with only `main` renamed. It compares:

* 429,341 canonical row masks with exhaustive bounded assignments and independent square-sum sets;
* 61,080 completed lower blocks of `Q` with exhaustive bounded witnesses;
* 60,840 direct last-edge masks and 60,120 two-edge masks with independently computed matrix moments;
* 101,320 witness residual restorations with their saved pre-recursion values.

These checks cover ranks 4–8, bounds 1–3, both weights, and a fixed reproducible random seed. `audit_identity.cpp` separately checks both moment identities on 100,000 random symmetric tensor slices across ranks 4–8, bounds 1–15, and both weights under undefined-behavior sanitization.

The final candidate also completes rank 6, bound 2 and rank 7, bound 1 under AddressSanitizer and UndefinedBehaviorSanitizer with one and two OpenMP threads. Output sets agree exactly between thread modes and with the earlier checked candidate. Two-thread sanitizer tests are pinned to one CPU. LeakSanitizer is disabled because the execution environment uses ptrace; address and undefined-behavior checking remain enabled.

Forcing the stored-witness cap to 1 and, separately, the recursive-visit cap to 1 reproduces the same complete output sets for both cases. This exercises the conservative fallback rather than merely inspecting its code.

## Reproduce local algebra checks

From the package root:

```bash
g++ -O2 -std=c++17 -fopenmp audits/audit_selfdual_local.cpp -o /tmp/audit_selfdual_local
/tmp/audit_selfdual_local systems
g++ -O2 -std=c++17 -fsanitize=undefined -fno-sanitize-recover=all audits/audit_identity.cpp -o /tmp/audit_identity
/tmp/audit_identity
python3 audits/audit_selfdual_fallback.py
```

These tests support the algebraic coverage argument; they are not a formal proof in a proof assistant.

The recorded final source hash is `c78c177ff03f472cbdd86d65ffb114abb77788c2a4ef7c8fd8c778856f6d5a57`; the evidence JSON also records the exact completion-solver header hash.
