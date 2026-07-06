from typing import Literal, Optional
from pydantic import BaseModel, Field


class InjectionDetection(BaseModel):
    is_prompt_injection: bool
    confidence: float = Field(ge=0.0, le=1.0)
    risk_level: Literal["low", "medium", "high", "critical"]
    attack_type: Literal[
        "none",
        "direct_override",
        "system_prompt_extraction",
        "data_exfiltration",
        "tool_misuse",
        "fake_authority",
        "roleplay_jailbreak",
        "obfuscated_instruction",
        "hidden_instruction",
        "multi_step_social_engineering",
        "other"
    ]
    suspicious_span: Optional[str]
    reasoning_summary: str
    recommended_action: Literal["allow", "sanitize", "block", "human_review"]


class VerificationResult(BaseModel):
    passed: bool
    confidence: float = Field(ge=0.0, le=1.0)
    failure_type: Literal[
        "none",
        "followed_untrusted_instruction",
        "revealed_secret",
        "unauthorized_tool_action",
        "ignored_user_task",
        "other"
    ]
    explanation: str


class AgentResponse(BaseModel):
    status: Literal["answered", "blocked", "blocked_after_generation", "error"]
    answer: str
    detection: InjectionDetection
    verification: Optional[VerificationResult] = None