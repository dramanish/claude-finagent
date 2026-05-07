#!/usr/bin/env python3
"""
QSR Digest — single managed agent runner.

Usage:
  python3 run-single.py          # run (reuse cached agent/env)
  python3 run-single.py --reset  # fresh agent + env
  python3 run-single.py --auth   # one-time Gmail OAuth setup
"""
import sys, json, pathlib, datetime, base64, email.message
import httpx, anthropic

COOKBOOK = pathlib.Path(__file__).parent
ENV_FILE = COOKBOOK.parent.parent / ".env"
ID_CACHE = COOKBOOK / ".single_ids.json"
OUT_DIR  = COOKBOOK / "out"
KB_DIR   = COOKBOOK / "knowledge-base"
BETA     = ["managed-agents-2026-04-01"]
MODEL    = "claude-opus-4-7"
TODAY    = datetime.date.today().strftime("%Y-%m-%d")

env_vars = dict(line.split("=", 1) for line in ENV_FILE.read_text().splitlines() if "=" in line)
API_KEY  = env_vars["ANTHROPIC_API_KEY"].strip()
client   = anthropic.Anthropic(api_key=API_KEY, timeout=httpx.Timeout(900.0, connect=10.0))


# ── Knowledge base ────────────────────────────────────────────────────────────

KB_FILES = [
    "Daniels Donuts.md",
    "LK Group.md",
    "GM vs Board Guide.md",
    "Research Priorities.md",
    "AU QSR Sector.md",
    "Krispy Kreme AU.md",
    "Donut King.md",
    "Brooklyn Donuts.md",
    "Collins Foods.md",
    "Queens Lane Capital.md",
]

def load_knowledge_base() -> str:
    sections = []
    for fname in KB_FILES:
        path = KB_DIR / fname
        if path.exists():
            text = path.read_text().strip()
            sections.append(f"### {fname.replace('.md', '')}\n{text}")
    return "\n\n".join(sections)

KB = load_knowledge_base()


# ── System prompt ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = f"""You are the LK Group QSR intelligence analyst for Daniels Donuts. You have three stages to complete in sequence. Emit the exact LOG lines shown — they drive the live display.

---

## STAGE 1 — SEARCH

Emit this line first:
LOG:STAGE:1:Searching — running 8 targeted AU QSR queries

Run ALL 8 searches. Do not skip any.

1. web_search("Krispy Kreme Australia 2026")
2. web_search("Donut King Retail Food Group Australia 2026")
3. web_search("Collins Foods ASX CKF Australia 2026")
4. web_search("Brooklyn Donuts Australia 2026")
5. web_search("Australia fast food QSR wage labour 2026")
6. web_search("Uber Eats DoorDash Australia fees 2026")
7. web_search("Australia donut doughnut new opening 2026")
8. web_search("Daniels Donuts LK Group Australia 2026")

After all searches complete, emit:
LOG:STAGE:1:DONE:N raw results collected

Only keep Australian items from the last 30 days with a real URL.

---

## STAGE 2 — CLASSIFY

Emit:
LOG:STAGE:2:Classifying — applying GM/Board/Both audience rules and priority flags

Use the knowledge base below to classify each item:
- **audience**: GM, Board, or Both (follow GM vs Board Guide exactly)
- **priority**: HIGH if it matches a Research Priority, NORMAL otherwise
- **why_it_matters**: one sentence, Daniels Donuts specific — name the implication, not the observation

Reject: items with no URL, US-only items, Tier 3 sources (anonymous blogs, social media).

After classifying emit:
LOG:STAGE:2:DONE:N items — H HIGH PRIORITY, M NORMAL

---

## STAGE 3 — WRITE DOCUMENT

Emit:
LOG:STAGE:3:Writing — building Word document with python-docx

Install python-docx if needed: pip install -q python-docx
Write and run a Python script via bash to build the Word doc.

Document structure:
- Header: LK Group — QSR Intelligence Digest | DATE | N items (H HIGH PRIORITY)
- Sort: HIGH first, then NORMAL. Within each tier: Both → Board → GM
- Each item: headline, [audience] label, ★ HIGH PRIORITY if applicable, summary (2-3 sentences), "Why it matters:" line, source name + URL, date
- Missing URL → bold [UNSOURCED]
- Item older than 30 days → [DATED — verify still current]

Save to: /out/qsr-digest-{TODAY}.docx
Create /out/ if it doesn't exist.

After saving emit:
LOG:STAGE:3:DONE:/out/qsr-digest-{TODAY}.docx

Then output a clean summary in this exact format for the Gmail draft:
DIGEST_SUMMARY_START
Subject: LK Group QSR Digest — {TODAY} — N items (H HIGH PRIORITY)

[For each HIGH PRIORITY item:]
★ [Both/GM/Board] HEADLINE
Why it matters: one sentence
Source: name — URL

[For each NORMAL item:]
• [Both/GM/Board] HEADLINE
Source: name — URL

DIGEST_SUMMARY_END

---

## KNOWLEDGE BASE

Use this intelligence — do not re-research these facts, they are authoritative.

{KB}
"""


# ── Logging ───────────────────────────────────────────────────────────────────

def ts():
    return datetime.datetime.now().strftime("%H:%M:%S")

def log(msg, icon="   "):
    print(f"[{ts()}] {icon}  {msg}", flush=True)

def banner(text, char="─"):
    width = 62
    print(f"\n{char*width}", flush=True)
    print(f"  {text}", flush=True)
    print(f"{char*width}", flush=True)

def stage_banner(n, title):
    icons = {1: "🔍", 2: "🧠", 3: "✍️"}
    print(f"\n{'═'*62}", flush=True)
    print(f"  {icons.get(n,'▶')}  STAGE {n} — {title.upper()}", flush=True)
    print(f"{'═'*62}", flush=True)


# ── Agent + environment ───────────────────────────────────────────────────────

def load_cache():
    return json.loads(ID_CACHE.read_text()) if ID_CACHE.exists() else {}

def save_cache(data):
    ID_CACHE.write_text(json.dumps(data, indent=2))

def create_agent():
    log("Creating managed agent...", "🤖")
    agent = client.beta.agents.create(
        name="qsr-digest-single",
        model=MODEL,
        system=SYSTEM_PROMPT,
        tools=[{
            "type": "agent_toolset_20260401",
            "default_config": {"enabled": False},
            "configs": [
                {"name": "web_search", "enabled": True},
                {"name": "bash",       "enabled": True},
                {"name": "write",      "enabled": True},
                {"name": "read",       "enabled": True},
            ],
        }],
        betas=BETA,
    )
    log(f"Agent:       {agent.id}", "✅")
    return agent.id

def create_environment():
    log("Creating cloud environment (installing python-docx)...", "📦")
    env = client.beta.environments.create(
        name=f"qsr-digest-{TODAY}-{datetime.datetime.now().strftime('%H%M%S')}",
        config={
            "type": "cloud",
            "packages": {"pip": ["python-docx"]},
            "networking": {"type": "unrestricted"},
        },
        betas=BETA,
    )
    log(f"Environment: {env.id}", "✅")
    return env.id


# ── Session runner ────────────────────────────────────────────────────────────

def run(agent_id, env_id):
    OUT_DIR.mkdir(exist_ok=True)
    banner(f"QSR Digest — {TODAY}  |  agent: {agent_id[:24]}…", "─")

    session = client.beta.sessions.create(
        agent={"id": agent_id, "type": "agent"},
        environment_id=env_id,
        title=f"QSR Digest {TODAY}",
        betas=BETA,
    )
    log(f"Session:     {session.id}", "🔑")

    client.beta.sessions.events.send(
        session.id,
        events=[{"type": "user.message", "content": [{"type": "text",
            "text": f"Today is {TODAY}. Run the full QSR digest pipeline."}]}],
        betas=BETA,
    )

    agent_replied = False
    summary_lines = []
    all_agent_text = []
    capturing_summary = False

    try:
        for event in client.beta.sessions.events.stream(session.id, betas=BETA, timeout=None):
            etype   = getattr(event, "type", "")
            name    = getattr(event, "name", "")
            inp     = getattr(event, "input", {}) or {}
            content = getattr(event, "content", None)
            text    = next(
                (getattr(b, "text", None) for b in (content or []) if getattr(b, "text", None)),
                None,
            )

            # Tool events
            if name == "web_search":
                log(inp.get("query", "")[:72], "🌐")
            elif name == "bash":
                cmd = inp.get("command", "")
                if "pip install" in cmd:
                    log("Installing python-docx in container", "📦")
                elif "python" in cmd:
                    log("Running document builder", "⚙️ ")
                else:
                    log(cmd[:70], "🐚")
            elif name == "write":
                log(f"Writing {inp.get('file_path','').split('/')[-1]}", "📝")

            # Agent messages — parse LOG lines and summary block
            elif etype == "agent.message" and text:
                agent_replied = True
                all_agent_text.append(text)
                for line in text.splitlines():
                    line = line.strip()

                    if line.startswith("LOG:STAGE:"):
                        parts = line.split(":", 3)
                        stage_num = int(parts[2]) if parts[2].isdigit() else 0
                        detail = parts[3] if len(parts) > 3 else ""
                        if "DONE" not in detail:
                            stage_banner(stage_num, detail)
                        else:
                            log(detail.replace("DONE:", "").strip(), "✅")

                    elif line == "DIGEST_SUMMARY_START":
                        capturing_summary = True
                    elif line == "DIGEST_SUMMARY_END":
                        capturing_summary = False
                    elif capturing_summary:
                        summary_lines.append(line)
                    elif line and not line.startswith("LOG:"):
                        log(line[:100], "💬")

            elif etype in ("session.status_idle", "session.status_complete"):
                if agent_replied:
                    log("Session complete", "✅")
                    break
            elif etype == "session.status_failed":
                log("Session FAILED", "❌")
                break

    except Exception:
        if agent_replied:
            log("Complete (stream closed)", "✅")
        else:
            s = client.beta.sessions.retrieve(session.id, betas=BETA)
            log(f"Stream dropped — session status: {getattr(s, 'status', 'unknown')}", "⚠️")

    # Retrieve docx from container
    banner("Output", "─")
    outfile = OUT_DIR / f"qsr-digest-{TODAY}.docx"
    try:
        file_bytes = client.beta.sessions.files.retrieve_content(
            session.id, f"out/qsr-digest-{TODAY}.docx", betas=BETA
        )
        outfile.write_bytes(file_bytes)
        log(f"Saved: {outfile}", "📄")
    except Exception:
        local = sorted(OUT_DIR.glob(f"qsr-digest-{TODAY}*.docx"))
        if local:
            log(f"Saved: {local[-1]}", "📄")
        else:
            log("Digest complete — docx in session container", "📄")

    # Use captured DIGEST_SUMMARY block, or fall back to all agent text
    if summary_lines:
        return "\n".join(summary_lines)
    return "\n\n".join(all_agent_text)


# ── Gmail draft ───────────────────────────────────────────────────────────────

def gmail_draft(summary_text: str):
    creds_path = COOKBOOK / "gmail-credentials.json"
    token_path = COOKBOOK / "gmail-token.json"

    if not creds_path.exists():
        log("Gmail not configured — run with --auth to set up (see GMAIL_SETUP.md)", "📧")
        return

    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
    except ImportError:
        log("Run: pip install google-auth-oauthlib google-api-python-client", "⚠️")
        return

    SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]
    creds = None

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            token_path.write_text(creds.to_json())
        else:
            log("Token missing or expired — run with --auth to re-authenticate", "⚠️")
            return

    service = build("gmail", "v1", credentials=creds)
    to_email = env_vars.get("DIGEST_TO_EMAIL", "").strip()
    if not to_email:
        log("DIGEST_TO_EMAIL not set in .env — skipping Gmail draft", "⚠️")
        return

    subject = f"LK Group QSR Digest — {TODAY}"
    body_lines = []
    for line in summary_text.splitlines():
        if line.startswith("Subject:"):
            subject = line.replace("Subject:", "").strip()
        else:
            body_lines.append(line)

    msg = email.message.EmailMessage()
    msg["To"]      = to_email
    msg["From"]    = to_email
    msg["Subject"] = subject
    msg.set_content("\n".join(body_lines))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().drafts().create(userId="me", body={"message": {"raw": raw}}).execute()
    log(f"Gmail draft created → {to_email}", "📧")


def gmail_auth():
    """One-time OAuth flow — saves gmail-token.json."""
    creds_path = COOKBOOK / "gmail-credentials.json"
    token_path = COOKBOOK / "gmail-token.json"
    if not creds_path.exists():
        print(f"\nMissing: {creds_path}")
        print("Follow GMAIL_SETUP.md to download credentials.json from Google Cloud.\n")
        sys.exit(1)
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print("Run: pip install google-auth-oauthlib google-api-python-client")
        sys.exit(1)
    SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]
    flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
    creds = flow.run_local_server(port=0)
    token_path.write_text(creds.to_json())
    print(f"✅  Token saved to {token_path}")
    print("You're set — run without --auth to produce the digest.")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--auth" in sys.argv:
        gmail_auth()
        sys.exit(0)

    reset = "--reset" in sys.argv
    if reset and ID_CACHE.exists():
        ID_CACHE.unlink()
        log("Cache cleared", "🗑️")

    cache    = load_cache()
    agent_id = cache.get("agent_id")
    env_id   = cache.get("env_id")

    if not agent_id:
        agent_id = create_agent()
        cache["agent_id"] = agent_id
        save_cache(cache)

    if not env_id:
        env_id = create_environment()
        cache["env_id"] = env_id
        save_cache(cache)

    log(f"Agent:       {agent_id}", "💾")
    log(f"Environment: {env_id}", "💾")

    summary = run(agent_id, env_id)

    if summary:
        gmail_draft(summary)
    else:
        log("No summary captured — skipping Gmail draft", "📧")
