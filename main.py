import re
import socket
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from disposable_domains import DISPOSABLE_DOMAINS, FREE_PROVIDERS

app = FastAPI(
    title="Disposable Email & Fraud Detector API",
    description="High-speed email validation API. Detects disposable emails, temporary domains, free providers, syntax errors, and DNS resolution to prevent fraud.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$"
)

class VerificationResult(BaseModel):
    email: str
    user: str
    domain: str
    is_valid_format: bool
    is_disposable: bool
    is_free_provider: bool
    domain_exists: bool
    risk_score: int = Field(..., description="Risk score from 0 (Safe) to 100 (High Risk)")
    status: str = Field(..., description="'safe', 'risky', or 'undeliverable'")
    reason: str

def check_domain_exists(domain: str) -> bool:
    try:
        socket.setdefaulttimeout(1.5)
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False

@app.get("/", tags=["General"])
def root():
    return {
        "status": "online",
        "service": "Disposable Email & Fraud Detector API",
        "version": "1.0.0",
        "endpoints": {
            "verify": "/v1/verify?email=test@example.com",
            "check_domain": "/v1/check-domain?domain=example.com",
            "docs": "/docs"
        }
    }

@app.get("/v1/verify", response_model=VerificationResult, tags=["Verification"])
def verify_email(
    email: str = Query(..., description="The email address to verify"),
    check_dns: bool = Query(True, description="Verify if the domain exists and resolves DNS")
):
    email_clean = email.strip().lower()
    
    if not EMAIL_REGEX.match(email_clean):
        return VerificationResult(
            email=email_clean,
            user="",
            domain="",
            is_valid_format=False,
            is_disposable=False,
            is_free_provider=False,
            domain_exists=False,
            risk_score=100,
            status="undeliverable",
            reason="Invalid email syntax format"
        )
    
    user, domain = email_clean.split("@", 1)
    is_disposable = domain in DISPOSABLE_DOMAINS
    is_free = domain in FREE_PROVIDERS
    
    domain_exists = True
    if check_dns:
        domain_exists = check_domain_exists(domain)
    
    # Cálculo de Risk Score (0 a 100)
    risk_score = 0
    reasons = []
    
    if is_disposable:
        risk_score = 95
        reasons.append("Disposable or temporary email service detected")
    elif not domain_exists:
        risk_score = 90
        reasons.append("Domain does not resolve or does not exist")
    elif is_free:
        risk_score = 15
        reasons.append("Free webmail provider (Gmail, Yahoo, Outlook, etc.)")
    else:
        risk_score = 0
        reasons.append("Valid business or custom domain")
        
    status = "safe"
    if risk_score >= 80:
        status = "risky" if is_disposable else "undeliverable"
    elif risk_score >= 40:
        status = "risky"
        
    return VerificationResult(
        email=email_clean,
        user=user,
        domain=domain,
        is_valid_format=True,
        is_disposable=is_disposable,
        is_free_provider=is_free,
        domain_exists=domain_exists,
        risk_score=risk_score,
        status=status,
        reason="; ".join(reasons)
    )

@app.get("/v1/check-domain", tags=["Verification"])
def check_domain_only(
    domain: str = Query(..., description="Domain to check")
):
    domain_clean = domain.strip().lower()
    is_disposable = domain_clean in DISPOSABLE_DOMAINS
    is_free = domain_clean in FREE_PROVIDERS
    domain_exists = check_domain_exists(domain_clean)
    
    return {
        "domain": domain_clean,
        "is_disposable": is_disposable,
        "is_free_provider": is_free,
        "domain_exists": domain_exists,
        "status": "disposable" if is_disposable else ("valid" if domain_exists else "invalid_domain")
    }
