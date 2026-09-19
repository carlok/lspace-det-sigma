"""Build two paste-ready prompts, each with the LaTeX source of the note inline (no attachment needed).
Regenerate after any change to k33.tex or PROMPTS.md."""
from pathlib import Path

HERE = Path(__file__).parent
tex = (HERE / "k33.tex").read_text().rstrip()
both = (HERE / "PROMPTS.md").read_text()
A = both.split("## Prompt A — review the note", 1)[1].split("## Prompt B", 1)[0].strip().rstrip("-").rstrip()
B = both.split("## Prompt B — attempt the open case", 1)[1].split("## Prompt C", 1)[0].strip().rstrip("-").rstrip()
C = both.split("## Prompt C — fresh pass for a third model (o2)", 1)[1].split("## Prompt D", 1)[0].strip().rstrip("-").rstrip()
D = both.split("## Prompt D — one question: definiteness (single task)", 1)[1].split("## Prompt E", 1)[0].strip().rstrip("-").rstrip()
E = both.split("## Prompt E — next model, after four passes", 1)[1].strip()

fence = "`" * 3
note = (
    "\n\nThe note follows as LaTeX source; this is the whole document, there is no separate PDF content. "
    "Quote exact strings from it when you refer to a step.\n\n"
    + fence + "latex\n" + tex + "\n" + fence + "\n"
)

(HERE / "prompt_A_review.md").write_text("# Task: review the note below\n\n" + A + note)
(HERE / "prompt_B_open_case.md").write_text("# Task: settle the open case of the note below\n\n" + B + note)
(HERE / "prompt_C_o2.md").write_text("# Task: third pass on the note below\n\n" + C + note)
(HERE / "prompt_D_definiteness.md").write_text("# Task: one question, stated below\n\n" + D + note)
(HERE / "prompt_E_next.md").write_text("# Task: one question, stated below\n\n" + D + "\n\n## State after four passes\n\n" + E + note)
for f in ("prompt_A_review.md", "prompt_B_open_case.md", "prompt_C_o2.md", "prompt_D_definiteness.md", "prompt_E_next.md"):
    print(f, len((HERE / f).read_text()), "characters")
