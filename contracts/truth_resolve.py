# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json
import typing


class TruthResolve(gl.Contract):
    claim: str
    source_a: str
    source_b: str
    result: str

    def __init__(self):
        self.claim = ""
        self.source_a = ""
        self.source_b = ""
        self.result = ""

    @gl.public.write
    def verify_claim(
        self,
        claim: str,
        source_a: str,
        source_b: str,
    ) -> typing.Any:
        if not claim.strip():
            raise gl.vm.UserError("Claim cannot be empty")
        if not source_a.startswith(("http://", "https://")):
            raise gl.vm.UserError("Source A must be an HTTP(S) URL")
        if not source_b.startswith(("http://", "https://")):
            raise gl.vm.UserError("Source B must be an HTTP(S) URL")

        self.claim = claim
        self.source_a = source_a
        self.source_b = source_b

        def evaluate_sources() -> str:
            page_a = gl.nondet.web.get(source_a).body.decode("utf-8")
            page_b = gl.nondet.web.get(source_b).body.decode("utf-8")

            prompt = f"""
You are the evidence analyst for TruthResolve.

Claim:
{claim}

Source A URL:
{source_a}

Source A content:
{page_a[:12000]}

Source B URL:
{source_b}

Source B content:
{page_b[:12000]}

Compare the two sources and determine whether the claim is:
SUPPORTED, CONTRADICTED, or UNRESOLVED.

Use only information present in the supplied sources.
Do not invent facts.

Return ONLY valid JSON with exactly these keys:
{{
  "verdict": "SUPPORTED|CONTRADICTED|UNRESOLVED",
  "confidence": "LOW|MEDIUM|HIGH",
  "evidence": "brief evidence summary",
  "conflict": "brief description of any disagreement"
}}
"""
            response = gl.nondet.exec_prompt(prompt)
            cleaned = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(cleaned)

            verdict = data.get("verdict", "UNRESOLVED")
            confidence = data.get("confidence", "LOW")

            if verdict not in ("SUPPORTED", "CONTRADICTED", "UNRESOLVED"):
                verdict = "UNRESOLVED"
            if confidence not in ("LOW", "MEDIUM", "HIGH"):
                confidence = "LOW"

            return json.dumps(
                {
                    "verdict": verdict,
                    "confidence": confidence,
                    "evidence": str(data.get("evidence", ""))[:1500],
                    "conflict": str(data.get("conflict", ""))[:1000],
                },
                sort_keys=True,
            )

        consensus_result = gl.eq_principle.prompt_comparative(
            evaluate_sources,
            principle="""
The verdict field must be exactly the same.
The confidence level should be compatible.
The evidence and conflict fields may use different wording but must describe
the same source-grounded conclusion.
Do not accept a result that introduces facts not present in the supplied sources.
""",
        )

        parsed = json.loads(consensus_result)
        self.result = json.dumps(parsed, sort_keys=True)
        return self.result

    @gl.public.view
    def get_result(self) -> str:
        return self.result

    @gl.public.view
    def get_claim(self) -> str:
        return self.claim

    @gl.public.view
    def get_sources(self) -> str:
        return json.dumps(
            {"source_a": self.source_a, "source_b": self.source_b},
            sort_keys=True,
        )
