# Manuscript theorems and Lean counterparts

Generated from `master.tex`. Matches below 100% are heuristic unless supplied through an override file. “Partial counterpart” does not certify the complete manuscript statement.

## Part A

### 1. The target

<table><tr><th width="50%">Manuscript</th><th width="50%">Lean counterpart</th></tr>
<tr><td valign="top"><b>Conjecture</b><br><code>conj:target</code><br><small>master.tex:39</small><pre>\begin{conjecture}[The target]\label{conj:target}
{{The conjecture, stated precisely, in the normal form the programme
attacks.}}
\end{conjecture}</pre><b>Remark:</b> Open conjecture; a Lean theorem should only encode a conditional implication.</td><td valign="top"><b>CONJ_target</b><br><small>`lean/conjectures.lean:26` · curated correspondence</small><br><b>Ledger status:</b> <code>statement only</code><br><pre>theorem CONJ_target : True := by
  sorry</pre><b>Remark:</b> Curated classification: statement only counterpart. Placeholder: the target conjecture is stated (not proved) in lean/conjectures.lean under the CONJ_ prefix. Only entries with status exactly &#x27;full&#x27; receive \leanok. This is at most a conditional encoding; it does not constitute a proof of the manuscript conjecture.</td></tr></table>

### 2. Example placeholder

<table><tr><th width="50%">Manuscript</th><th width="50%">Lean counterpart</th></tr>
<tr><td valign="top"><b>Theorem</b><br><code>thm:example</code><br><small>master.tex:44</small><pre>\begin{theorem}[Example placeholder]\label{thm:example}
{{Replace with the first real reduction. Delete this environment once the
manuscript has content.}}
\end{theorem}</pre><b>Remark:</b> No special manuscript-side remark.</td><td valign="top"><b>CONJ_target</b><br><small>`lean/conjectures.lean:26` · curated correspondence</small><br><b>Ledger status:</b> <code>statement only</code><br><pre>theorem CONJ_target : True := by
  sorry</pre><b>Remark:</b> Curated classification: statement only counterpart. Placeholder entry for the example theorem environment in master.tex; replace both together with real content. Every manuscript label must have exactly one entry in this ledger.</td></tr></table>
