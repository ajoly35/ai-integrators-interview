"""AI Integrators study page, Streamlit version of index.html (same text, same routing, same agents).

Deploy on Streamlit Community Cloud from the public repo ajoly35/ai-integrators-interview, main file streamlit_app.py.
Links work exactly as on the GitHub Pages version:
  ?src=<tester tag>           tag passed to the agent as dynamic variable `source` (and as the widget user-id)
  ?arm=info | control         force the information-experiment arm; otherwise randomised 50/50 per browser session
  ?m=us                       US agent and voice; also chosen when the src tag starts with "us"
The ElevenLabs widget is embedded with streamlit.components.v1.html, the mechanism the Horizons and RF interview
apps already use in the field, so microphone access inside the component iframe is known to work.
"""
import html
import json
import random
import re

import streamlit as st
import streamlit.components.v1 as components

AGENTS = {
    "uk": "agent_4101m54ss1atepdtagan9nyza7dj",  # v3 UK (Daniel), ajolybzh35@gmail.com account
    "us": "agent_3701m54ss398er28w6yhkp9x9k8e",  # v3 US (Eric)
}
WIDGET_SRC = "https://unpkg.com/@elevenlabs/convai-widget-embed"
WIDGET_HEIGHT = 480  # room for the expanded widget with its transcript (voice only, no text box)

st.set_page_config(page_title="AI Integrators Study", page_icon="🎙️", layout="centered",
                   initial_sidebar_state="collapsed")

# --- routing from the query string -----------------------------------------------------------------------------
q = st.query_params
source = re.sub(r"[^a-z0-9_-]", "", q.get("src") or "direct", flags=re.I)[:32] or "direct"
market = (q.get("m") or ("us" if source.lower().startswith("us") else "uk")).lower()
if market not in AGENTS:
    market = "uk"
arm = q.get("arm")
if arm not in ("info", "control"):
    if st.session_state.get("arm") not in ("info", "control"):
        st.session_state["arm"] = random.choice(["info", "control"])
    arm = st.session_state["arm"]

# --- page ------------------------------------------------------------------------------------------------------
st.markdown(
    """
<style>
  #MainMenu, footer, header {visibility: hidden;}
  .block-container {max-width: 680px; padding-top: 3rem; font-family: Georgia, "Times New Roman", serif;}
  .aii-tag {font: 600 12px/1 system-ui, sans-serif; letter-spacing: .08em; text-transform: uppercase; color: #1f4e79;}
  .aii-h1 {font-size: 30px; line-height: 1.2; margin: 12px 0 20px; font-weight: 700;}
  .aii-body p, .aii-body li {font-size: 17px; line-height: 1.55;}
  .aii-box {border-top: 1px solid #e2e2dc; border-bottom: 1px solid #e2e2dc; padding: 16px 0; margin: 24px 0;}
  .aii-quiet {color: #5c5c58; font-size: 15px;}
</style>
<div class="aii-tag">London School of Economics · Pilot</div>
<div class="aii-h1">How is AI really being put to work?</div>
<div class="aii-body">
<p>We are interviewing people who build and deploy AI systems for other organisations: founders, engineers,
forward-deployed engineers and consultants at AI startups and agencies. You see how adoption actually happens;
we want to learn from that.</p>
<div class="aii-box">
<ul>
<li>An AI interviewer asks about one client firm you worked with, how each level of that firm was affected, and
a similar firm that did not go ahead.</li>
<li>It takes about 30 minutes and is done by voice, so you need a microphone and a quiet place.</li>
<li>Please do not name clients, prospective clients or individuals. Answers are used for research only and
reported in aggregate.</li>
<li>You can stop at any time. Say "stop" or press the end-call button to finish.</li>
</ul>
<p class="aii-quiet">This is a pilot of the interview. Conversations are recorded and transcribed by ElevenLabs on
behalf of the research team. Questions: Adrien Joly, LSE.</p>
</div>
</div>
""",
    unsafe_allow_html=True,
)

consent = st.checkbox("I have read the above and agree to take part in this pilot interview.", key="consent")

if not consent:
    st.caption("Tick the box to show the interviewer. Allow microphone access when asked.")
else:
    st.caption("The interviewer is below. Press the call button to start.")
    dyn = html.escape(json.dumps({"source": source, "arm": arm}), quote=True)
    markup = f"""
    <style>html,body{{margin:0;padding:0;background:transparent;}}</style>
    <elevenlabs-convai agent-id="{html.escape(AGENTS[market], quote=True)}" user-id="{html.escape(source, quote=True)}"
      dynamic-variables="{dyn}"></elevenlabs-convai>
    <script src="{WIDGET_SRC}" async type="text/javascript"></script>
    """
    components.html(markup, height=WIDGET_HEIGHT)
