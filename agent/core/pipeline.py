import json
import re
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from prompts.research import SYSTEM_PROMPT
from core.config import MAX_ROUNDS
from core.agent import create_agent, TOOLS


def _build_tool_map() -> dict:
    return {t.name: t for t in TOOLS}


def _execute_tool(tool_call: dict, tool_map: dict) -> str:
    name = tool_call["name"]
    args = tool_call["args"]
    fn = tool_map.get(name)
    if fn is None:
        return f"Unknown tool: {name!r}"
    try:
        return str(fn.invoke(args))
    except Exception as e:
        return f"Tool '{name}' raised: {e}"


def _extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in model output: {text!r}")
    return json.loads(match.group())


def run_pipeline(claim: str) -> dict:
    agent = create_agent()
    tool_map = _build_tool_map()

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=claim),
    ]

    evidence: list[dict] = []

    for round_num in range(MAX_ROUNDS):
        ai_response = agent.invoke(messages)

        if ai_response.tool_calls:
            messages.append(ai_response)

            for tc in ai_response.tool_calls:
                result = _execute_tool(tc, tool_map)

                evidence.append({
                    "round": round_num + 1,
                    "tool": tc["name"],
                    "input": tc["args"],
                    "output": result,
                })

                messages.append(
                    ToolMessage(content=result, tool_call_id=tc["id"])
                )

            continue

        final_text = ai_response.content.strip()
        try:
            verdict = _extract_json(final_text)
        except (ValueError, json.JSONDecodeError) as e:
            return {
                "status": "failed",
                "verdict": None,
                "response": f"Agent returned non-JSON output: {e}",
                "confidence": None,
                "sources": [],
                "question": None,
                "evidence": evidence,
            }

        verdict.setdefault("evidence", evidence)
        return verdict

    return {
        "status": "failed",
        "verdict": None,
        "response": f"Research loop hit the {MAX_ROUNDS}-round cap without producing a final answer.",
        "confidence": None,
        "sources": [],
        "question": None,
        "evidence": evidence,
    }
