from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

# ── Color palette ──────────────────────────────────────────────────────────
SCE_NAVY   = colors.HexColor("#003087")
SCE_ORANGE = colors.HexColor("#E57200")
SCE_LIGHT  = colors.HexColor("#E8EEF8")
SCE_MID    = colors.HexColor("#CBD8ED")
BLACK      = colors.black
WHITE      = colors.white
GRAY       = colors.HexColor("#555555")
LIGHT_GRAY = colors.HexColor("#F5F5F5")
WARN_BG    = colors.HexColor("#FFF8F0")

# ── Document setup ─────────────────────────────────────────────────────────
OUTPUT = "/sessions/fervent-brave-babbage/mnt/outputs/SCE_Brand_Copy_Playbook_v1.1.pdf"
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    leftMargin=0.85*inch, rightMargin=0.85*inch,
    topMargin=0.85*inch,  bottomMargin=0.85*inch,
    title="SCE Brand Copy Playbook v1.1",
    author="SCE Internal",
)

styles = getSampleStyleSheet()

# ── Custom styles ──────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

cover_title   = S("CoverTitle",   fontName="Helvetica-Bold",   fontSize=28, textColor=SCE_NAVY,   spaceAfter=8,  leading=34)
cover_sub     = S("CoverSub",     fontName="Helvetica",        fontSize=13, textColor=GRAY,        spaceAfter=6,  leading=18)
cover_meta    = S("CoverMeta",    fontName="Helvetica",        fontSize=10, textColor=GRAY,        spaceAfter=4,  leading=14)
cover_tagline = S("CoverTagline", fontName="Helvetica-BoldOblique", fontSize=11, textColor=SCE_ORANGE, spaceAfter=4, leading=16)
h1            = S("H1",           fontName="Helvetica-Bold",   fontSize=15, textColor=SCE_NAVY,   spaceBefore=18, spaceAfter=6,  leading=20)
h2            = S("H2",           fontName="Helvetica-Bold",   fontSize=12, textColor=SCE_NAVY,   spaceBefore=12, spaceAfter=4,  leading=16)
h3            = S("H3",           fontName="Helvetica-Bold",   fontSize=10, textColor=BLACK,       spaceBefore=8,  spaceAfter=3,  leading=14)
body          = S("Body",         fontName="Helvetica",        fontSize=9.5, textColor=BLACK,      spaceAfter=4,  leading=14)
body_sm       = S("BodySm",       fontName="Helvetica",        fontSize=9,   textColor=BLACK,      spaceAfter=3,  leading=13)
bullet        = S("Bullet",       fontName="Helvetica",        fontSize=9.5, textColor=BLACK,      spaceAfter=3,  leading=14, leftIndent=14, firstLineIndent=-10)
bullet_bold   = S("BulletBold",   fontName="Helvetica-Bold",   fontSize=9.5, textColor=BLACK,      spaceAfter=3,  leading=14, leftIndent=14, firstLineIndent=-10)
note          = S("Note",         fontName="Helvetica-Oblique",fontSize=8.5, textColor=GRAY,       spaceAfter=4,  leading=13)
new_tag       = S("NewTag",       fontName="Helvetica-Bold",   fontSize=7.5, textColor=WHITE,      leading=11)
north_star    = S("NorthStar",    fontName="Helvetica-BoldOblique", fontSize=10, textColor=SCE_NAVY, leading=15, spaceAfter=4)

def b(text): return f"<b>{text}</b>"
def it(text): return f"<i>{text}</i>"
def bullet_item(text, bold_prefix=None):
    if bold_prefix:
        return Paragraph(f"<b>•  {bold_prefix}</b> {text}", bullet)
    return Paragraph(f"•  {text}", bullet)

def new_badge():
    """Small NEW badge to flag updated content."""
    data = [["  NEW  "]]
    t = Table(data, colWidths=[0.45*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), SCE_ORANGE),
        ("FONTNAME",   (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 7),
        ("TEXTCOLOR",  (0,0), (-1,-1), WHITE),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 1),
        ("BOTTOMPADDING",(0,0),(-1,-1),1),
        ("ROUNDEDCORNERS", [2,2,2,2]),
    ]))
    return t

def section_rule():
    return HRFlowable(width="100%", thickness=1.5, color=SCE_NAVY, spaceAfter=6, spaceBefore=2)

def light_rule():
    return HRFlowable(width="100%", thickness=0.5, color=SCE_MID, spaceAfter=4, spaceBefore=2)

def page_label(section, title):
    """Gray footer-style label printed as a paragraph at top of new section."""
    return Paragraph(f"<font color='#888888' size='8'>{section}</font>   <b><font size='8'>{title}</font></b>", body_sm)

def shaded_box(paragraphs, bg=SCE_LIGHT, pad=8):
    data = [[p] for p in paragraphs]
    t = Table(data, colWidths=[6.3*inch])
    style = [
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("TOPPADDING",    (0,0), (-1,-1), pad),
        ("BOTTOMPADDING", (0,0), (-1,-1), pad),
        ("LEFTPADDING",   (0,0), (-1,-1), pad+2),
        ("RIGHTPADDING",  (0,0), (-1,-1), pad+2),
        ("ROWBACKGROUNDS",(0,0), (-1,-1), [bg]),
        ("BOX",           (0,0), (-1,-1), 0.5, SCE_MID),
    ]
    t.setStyle(TableStyle(style))
    return t

def two_col_table(headers, rows, col_widths, alt=True):
    header_row = [Paragraph(b(h), body_sm) for h in headers]
    data = [header_row]
    for row in rows:
        data.append([Paragraph(str(cell), body_sm) for cell in row])
    t = Table(data, colWidths=col_widths)
    ts = [
        ("BACKGROUND",     (0,0), (-1,0),  SCE_NAVY),
        ("TEXTCOLOR",      (0,0), (-1,0),  WHITE),
        ("FONTNAME",       (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",       (0,0), (-1,-1), 8.5),
        ("TOPPADDING",     (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",  (0,0), (-1,-1), 5),
        ("LEFTPADDING",    (0,0), (-1,-1), 6),
        ("RIGHTPADDING",   (0,0), (-1,-1), 6),
        ("VALIGN",         (0,0), (-1,-1), "TOP"),
        ("GRID",           (0,0), (-1,-1), 0.4, SCE_MID),
    ]
    if alt:
        for i in range(1, len(data)):
            bg = LIGHT_GRAY if i % 2 == 0 else WHITE
            ts.append(("BACKGROUND", (0,i), (-1,i), bg))
    t.setStyle(TableStyle(ts))
    return t

# ══════════════════════════════════════════════════════════════════════════
# BUILD STORY
# ══════════════════════════════════════════════════════════════════════════
story = []

# ── COVER ─────────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.5*inch))

# Orange top bar
bar = Table([["  "]], colWidths=[6.3*inch], rowHeights=[6])
bar.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), SCE_ORANGE)]))
story.append(bar)
story.append(Spacer(1, 0.18*inch))

story.append(Paragraph("SCE Brand Copy Playbook", cover_title))
story.append(Paragraph(
    "A practical internal guide for writing web copy that feels cohesive with the "
    "public-facing voice on SCE.com", cover_sub))
story.append(Paragraph("Version 1.1  |  Updated April 24, 2026", cover_meta))
story.append(Spacer(1, 0.12*inch))
story.append(Paragraph('Official brand tagline: <font color="#E57200"><b>Energy for What\'s Ahead\u00ae</b></font>', cover_meta))
story.append(Spacer(1, 0.22*inch))
story.append(light_rule())
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("How to use this playbook", h2))
story.append(Paragraph(
    "Use this document to write, review, or prompt AI for SCE-style copy across "
    "webpages, landing pages, support content, banners, FAQs, email copy, and "
    "short-form digital experiences. It is designed to help teams produce copy that "
    "is <b>clear, helpful, trustworthy, and consistent</b>.", body))
story.append(Spacer(1, 0.06*inch))
story.append(shaded_box([
    Paragraph(
        "<i>This playbook is an unofficial synthesis based on a review of public-facing "
        "SCE.com pages, including the homepage, About SCE, Customer Service Center, "
        "Clean Energy &amp; Efficiency, Clean Energy and You, Help Paying Your Bill, "
        "CARE &amp; FERA, Wildfire Safety, and contact/help content. It should be used "
        "as a practical working guide, not a replacement for formal legal, regulatory, "
        "accessibility, or corporate brand review.</i>", note)
], bg=LIGHT_GRAY))
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("North star", h3))
story.append(shaded_box([
    Paragraph(
        "Lead with the customer need. Write in plain language. "
        "Make the next step obvious. Reinforce trust through clarity, "
        "responsibility, and practical value.", north_star)
], bg=SCE_LIGHT))

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Official mission statement <font color='#E57200'>[from SCE.com]</font>", h3))
story.append(shaded_box([
    Paragraph(
        "\"At Southern California Edison, our mission is to safely deliver reliable, "
        "clean and affordable electricity to the communities that make our region great.\"",
        north_star)
], bg=WARN_BG))

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("SCE corporate values <font color='#E57200'>[from SCE.com]</font>", h3))
story.append(Paragraph(
    "Safety &nbsp;&nbsp;|&nbsp;&nbsp; Integrity &nbsp;&nbsp;|&nbsp;&nbsp; "
    "Excellence &nbsp;&nbsp;|&nbsp;&nbsp; Respect &nbsp;&nbsp;|&nbsp;&nbsp; "
    "Continuous Improvement &nbsp;&nbsp;|&nbsp;&nbsp; Teamwork", body))

story.append(Spacer(1, 0.08*inch))
story.append(Paragraph(
    f"<font size='8' color='#888888'>SCE Brand Copy Playbook &nbsp;&nbsp;|&nbsp;&nbsp; Page 1</font>", body_sm))

# ── PAGE 2: QUICK REFERENCE ────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("1.  Quick Reference", h1))
story.append(section_rule())

story.append(Paragraph("The SCE voice in one sentence", h2))
story.append(shaded_box([
    Paragraph(
        "SCE copy sounds <b>clear, helpful, calm, trustworthy, action-oriented, and "
        "community-centered</b>—with optimism that is grounded in practical actions, "
        "real programs, and reliable service.", body)
], bg=SCE_LIGHT))
story.append(Spacer(1, 0.12*inch))

qr_rows = [
    ["Lead with the user task",      "Start with what the reader needs to do, solve, or understand."],
    ["Use plain language",           "Prefer familiar words, short sentences, and active voice."],
    ["Be specific",                  "Use concrete actions, named programs, timelines, and clear benefits."],
    ["Stay calm and responsible",    "Especially for billing, outages, wildfire, scams, and safety topics."],
    ["Make the next step obvious",   "Use straightforward CTAs: Learn More, View Options, Get Help, Apply Now."],
]
story.append(two_col_table(
    ["If you remember only this …", "Do this"],
    qr_rows,
    [2.1*inch, 4.2*inch]
))

story.append(Spacer(1, 0.16*inch))
story.append(Paragraph("Signature themes that often appear in SCE copy", h2))

themes = [
    ("<b>Safety</b>",                 "Protect customers and communities with clear, steady, useful guidance."),
    ("<b>Reliability</b>",            "Emphasize dependable service, grid stewardship, and operational responsibility."),
    ("<b>Affordability</b>",          "Help customers manage costs through support, options, and energy-saving tools."),
    ("<b>Clean energy progress</b>",  "Connect today's actions to a cleaner, more resilient future (California's 2045 net-zero goal)."),
    ("<b>Community support</b>",      "Frame SCE as a partner serving people, neighborhoods, and the region."),
    ("<b>Customer choice</b>",        "Show available tools, programs, and paths forward rather than a single \"pitch.\""),
    ("<b>Wildfire &amp; disaster recovery</b>  <font color='#E57200'>[updated]</font>",
     "One-quarter of SCE's service area is in a high fire risk area. Wildfire mitigation "
     "is a top priority. Use especially calm, factual, and empowering language. "
     "Acknowledge impact while directing customers to specific resources and programs."),
]
theme_data = [[Paragraph(t, body_sm), Paragraph(d, body_sm)] for t, d in themes]
theme_t = Table(theme_data, colWidths=[2.0*inch, 4.3*inch])
theme_t.setStyle(TableStyle([
    ("FONTSIZE",      (0,0), (-1,-1), 8.5),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ("RIGHTPADDING",  (0,0), (-1,-1), 6),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ("LINEBELOW",     (0,0), (-1,-2), 0.4, SCE_MID),
    ("BACKGROUND",    (0,0), (-1,0),  SCE_LIGHT),
    ("BACKGROUND",    (0,2), (-1,2),  SCE_LIGHT),
    ("BACKGROUND",    (0,4), (-1,4),  SCE_LIGHT),
    ("BACKGROUND",    (0,6), (-1,6),  WARN_BG),
    ("BOX",           (0,0), (-1,-1), 0.5, SCE_MID),
]))
story.append(theme_t)

story.append(Spacer(1, 0.08*inch))
story.append(Paragraph(
    "<font size='8' color='#888888'>SCE Brand Copy Playbook &nbsp;&nbsp;|&nbsp;&nbsp; Page 2</font>", body_sm))

# ── PAGE 3: VOICE ─────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("2.  Voice", h1))
story.append(section_rule())

story.append(Paragraph("Core voice attributes", h2))
voice_rows = [
    ["Clear",                "Easy to scan and easy to understand on first read.",            "Dense, technical, or abstract."],
    ["Helpful",              "Focused on solving the customer's need and guiding the next step.", "Overly promotional or self-congratulatory."],
    ["Trustworthy",          "Calm, factual, balanced, and responsible.",                     "Hyped, vague, defensive, or absolute."],
    ["Action-oriented",      "Built around useful verbs and tangible actions.",               "Passive, meandering, or generic."],
    ["Optimistic but grounded", "Positive about progress without sounding inflated.",         "Cheerleading, futurist jargon, or puffery."],
    ["Community-centered",   "Shows service to customers, communities, and California's future.", "Purely corporate or internally focused."],
]
story.append(two_col_table(
    ["Attribute", "What it means in practice", "What it does NOT sound like"],
    voice_rows,
    [1.35*inch, 2.85*inch, 2.1*inch]
))

story.append(Spacer(1, 0.16*inch))
story.append(Paragraph("Voice formula", h2))
story.append(Paragraph(
    "<b>Utility first.</b> SCE-style copy starts with usefulness, then reinforces trust, "
    "then ties back to mission or broader value when relevant.", body))
story.append(Spacer(1, 0.06*inch))

formula_steps = [
    ("1", "Lead with the reader's task, question, or concern."),
    ("2", "Follow with the action they can take now."),
    ("3", "Explain why it matters—safety, savings, reliability, or cleaner energy progress."),
    ("4", "Place the broader SCE mission behind the message instead of in front of it."),
]
fdata = [[Paragraph(f"<b>{n}</b>", body_sm), Paragraph(t, body_sm)] for n, t in formula_steps]
ft = Table(fdata, colWidths=[0.35*inch, 5.95*inch])
ft.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), SCE_LIGHT),
    ("FONTSIZE",      (0,0), (-1,-1), 9),
    ("TOPPADDING",    (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("RIGHTPADDING",  (0,0), (-1,-1), 6),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("LINEBELOW",     (0,0), (-1,-2), 0.4, SCE_MID),
    ("BOX",           (0,0), (-1,-1), 0.5, SCE_MID),
]))
story.append(ft)

story.append(Spacer(1, 0.08*inch))
story.append(Paragraph(
    "<font size='8' color='#888888'>SCE Brand Copy Playbook &nbsp;&nbsp;|&nbsp;&nbsp; Page 3</font>", body_sm))

# ── PAGE 4: TONE ──────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("3.  Tone", h1))
story.append(section_rule())

story.append(Paragraph("How tone shifts by situation", h2))
tone_rows = [
    ["Billing / payment assistance",
     "Reassuring, practical, respectful",
     "Available options, eligibility, next steps, nonjudgmental support"],
    ["Outages / PSPS / scams / safety",
     "Calm, precise, urgent when necessary",
     "Immediate actions, trusted resources, plain instructions"],
    ["Wildfire &amp; disaster recovery\n[updated — active topic]",
     "Calm, factual, empathetic, direct",
     "Acknowledge impact; specific programs (Wildfire Recovery Compensation Program); "
     "clear next steps; avoid fear-based language; reassure without overpromising"],
    ["Customer support / how-to content",
     "Straightforward, service-oriented",
     "Clarity, ease, completion of task"],
    ["Clean energy / efficiency",
     "Optimistic, empowering, concrete",
     "Benefits, practical actions, rebates, resilience, cleaner future (net-zero 2045)"],
    ["Corporate / about / strategy",
     "Confident, factual, mission-led",
     "Scale, responsibility, stewardship, long-term direction"],
    ["Careers / employer brand",
     "Purposeful, motivating, authentic",
     "Impact, teamwork, future-building, real contribution"],
]
tone_data = []
for i, (sit, tone, emp) in enumerate(tone_rows):
    bg = WARN_BG if "updated" in sit else (SCE_LIGHT if i % 2 == 0 else WHITE)
    tone_data.append([
        Paragraph(sit.replace("\n", "<br/>"), body_sm),
        Paragraph(tone, body_sm),
        Paragraph(emp, body_sm),
    ])
tone_t = Table(tone_data, colWidths=[1.75*inch, 1.55*inch, 3.0*inch])
tone_style = [
    ("FONTSIZE",      (0,0), (-1,-1), 8.5),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ("RIGHTPADDING",  (0,0), (-1,-1), 6),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ("GRID",          (0,0), (-1,-1), 0.4, SCE_MID),
]
for i, (sit, _, _) in enumerate(tone_rows):
    if "updated" in sit:
        tone_style.append(("BACKGROUND", (0,i), (-1,i), WARN_BG))
    elif i % 2 == 0:
        tone_style.append(("BACKGROUND", (0,i), (-1,i), SCE_LIGHT))
    else:
        tone_style.append(("BACKGROUND", (0,i), (-1,i), WHITE))
# header
header_row_t = Table(
    [[Paragraph(b("Situation"), body_sm), Paragraph(b("Recommended tone"), body_sm), Paragraph(b("What to emphasize"), body_sm)]],
    colWidths=[1.75*inch, 1.55*inch, 3.0*inch]
)
header_row_t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), SCE_NAVY),
    ("TEXTCOLOR",     (0,0), (-1,-1), WHITE),
    ("FONTNAME",      (0,0), (-1,-1), "Helvetica-Bold"),
    ("FONTSIZE",      (0,0), (-1,-1), 8.5),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ("RIGHTPADDING",  (0,0), (-1,-1), 6),
    ("GRID",          (0,0), (-1,-1), 0.4, SCE_MID),
]))
story.append(header_row_t)
tone_t.setStyle(TableStyle(tone_style))
story.append(tone_t)

story.append(Spacer(1, 0.08*inch))
story.append(Paragraph(
    "<font size='8' color='#888888'>SCE Brand Copy Playbook &nbsp;&nbsp;|&nbsp;&nbsp; Page 4</font>", body_sm))

# ── PAGE 5: DO / DON'T ────────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("4.  Do / Don't", h1))
story.append(section_rule())

do_items = [
    "Use task-led headlines: <i>Help Paying Your Bill, Explore Payment Options, Find Support for Your Move.</i>",
    "Write in plain language and keep one idea per sentence.",
    'Use <b>"you"</b> for customer actions and benefits; use <b>"we"</b> for SCE\'s role and responsibility.',
    "Use named programs, facts, and examples when they help the reader act or understand.",
    "Keep paragraphs short, use subheads, and make the CTA easy to spot.",
    "When relevant, tie copy back to safety, reliability, affordability, clean energy, or community impact.",
    "<b>Name specific programs when possible</b>: CARE (32.5% discount), FERA (18% discount), "
    "Energy Assistance Fund (EAF), Base Services Charge (BSC), PSPS, Wildfire Recovery Compensation Program. "
    "<font color='#E57200'>[updated]</font>",
]
dont_items = [
    "Don't open with a brand boast when the reader needs help completing a task.",
    "Don't sound like an ad if the page is service-oriented or support-oriented.",
    'Don\'t use hype words such as "game-changing," "revolutionary," "best-in-class," or "unlock."',
    "Don't overpromise outcomes, especially on sensitive topics such as safety, billing, or disaster response.",
    "Don't bury the action. Avoid making the reader hunt for what to do next.",
    "Don't rely on unexplained jargon, acronyms, or insider language.",
]

do_col = [Paragraph("<b>Do</b>", h3)] + [bullet_item(i) for i in do_items]
dont_col = [Paragraph("<b>Don't</b>", h3)] + [bullet_item(i) for i in dont_items]

# Pad shorter column
while len(dont_col) < len(do_col):
    dont_col.append(Spacer(1, 1))

dd_data = list(zip(do_col, dont_col))
dd_t = Table(dd_data, colWidths=[3.1*inch, 3.2*inch])
dd_t.setStyle(TableStyle([
    ("FONTSIZE",      (0,0), (-1,-1), 9),
    ("TOPPADDING",    (0,0), (-1,-1), 3),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ("LEFTPADDING",   (0,0), (-1,-1), 0),
    ("RIGHTPADDING",  (0,0), (-1,-1), 8),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ("LINEAFTER",     (0,0), (0,-1),  0.5, SCE_MID),
    ("LEFTPADDING",   (1,0), (1,-1),  10),
]))
story.append(dd_t)

story.append(Spacer(1, 0.16*inch))
story.append(Paragraph("Preferred word choices", h2))

word_rows = [
    ["help, support, explore, learn, manage, find, discover",        "unlock, supercharge, elevate, maximize"],
    ["reliable, affordable, clean, resilient, community, progress",  "revolutionary, game-changing, disruptive"],
    ["options, programs, resources, guidance, next steps",           "ecosystem, solutioning, future-proof"],
    ["apply, view, get help, learn more, compare, download",         "jump in, power up, let's do this"],
]
story.append(two_col_table(
    ["Use more often", "Use less often"],
    word_rows,
    [3.1*inch, 3.2*inch]
))

story.append(Spacer(1, 0.08*inch))
story.append(Paragraph(
    "<font size='8' color='#888888'>SCE Brand Copy Playbook &nbsp;&nbsp;|&nbsp;&nbsp; Page 5</font>", body_sm))

# ── PAGE 6: PAGE STRUCTURE ────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("5.  Page Structure Templates", h1))
story.append(section_rule())
story.append(Paragraph(
    "Use these formulas to keep copy cohesive across the site.", body))
story.append(Spacer(1, 0.08*inch))

templates = [
    ("A.  Support / service page", [
        "<b>Headline:</b> Lead with the task or problem to solve.",
        "<b>Subheadline:</b> Briefly explain the support available.",
        "<b>Body:</b> Present options, steps, or resources in clear buckets.",
        "<b>CTA:</b> Use a direct action such as View Options, Get Help, or Apply Now.",
        "<i>Template: [Task-based headline] \u2192 [Brief reassurance] \u2192 [Options / steps / eligibility] \u2192 [CTA]</i>",
    ]),
    ("B.  Clean energy / efficiency page", [
        "<b>Headline:</b> Frame the opportunity or benefit.",
        "<b>Subheadline:</b> Connect today's actions to savings, resilience, or cleaner energy progress.",
        "<b>Body:</b> Offer practical programs, rebates, tips, and next steps.",
        "<b>CTA:</b> Learn More, Explore Programs, See Rebates, or Get Started.",
        "<i>Template: [Future-oriented benefit] \u2192 [Why it matters] \u2192 [Programs / practical actions] \u2192 [CTA]</i>",
    ]),
    ("C.  About / strategy page", [
        "<b>Headline:</b> State mission, role, or contribution clearly.",
        "<b>Body intro:</b> Explain who SCE serves and what it provides.",
        "<b>Supporting sections:</b> Add proof points, values, reliability, clean energy, and community impact.",
        "<b>CTA:</b> Learn More, Explore Our Work, or Read More.",
        "<i>Template: [Mission statement] \u2192 [Who we serve] \u2192 [How we do it] \u2192 [Proof points / priority areas]</i>",
    ]),
    ("D.  Alert / issue response  \u2014  including wildfire &amp; disaster recovery", [
        "<b>Opening:</b> State the issue in plain language and acknowledge its importance.",
        "<b>Next steps:</b> Tell readers exactly what to do now.",
        "<b>Support:</b> Link to relevant programs, outage tools, safety information, or contact options.",
        "<b>Close:</b> Reinforce calm, credible support.",
        "<i>Template: [What happened / what to know] \u2192 [Immediate action] \u2192 [Resources / support] \u2192 [Trusted CTA]</i>",
        "<font color='#E57200'><i>[Updated: this template applies directly to Eaton Fire recovery "
        "and Wildfire Recovery Compensation Program messaging.]</i></font>",
    ]),
]

for title, items in templates:
    story.append(Paragraph(title, h3))
    story.append(shaded_box(
        [Paragraph(f"•  {i}", bullet) for i in items],
        bg=SCE_LIGHT if "Support" in title or "About" in title else (WARN_BG if "Alert" in title else WHITE)
    ))
    story.append(Spacer(1, 0.08*inch))

story.append(Paragraph(
    "<font size='8' color='#888888'>SCE Brand Copy Playbook &nbsp;&nbsp;|&nbsp;&nbsp; Page 6</font>", body_sm))

# ── PAGE 7: PROMPT LIBRARY ────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("6.  Prompt Library for AI", h1))
story.append(section_rule())

story.append(Paragraph("Master prompt (most flexible)", h2))
master_prompt = (
    "You are writing copy in an SCE website style.\n"
    "Write copy that feels consistent with Southern California Edison's public-facing website:\n"
    "- clear\n- helpful\n- calm\n- trustworthy\n- action-oriented\n- community-centered\n- optimistic but grounded\n\n"
    "Brand voice rules:\n"
    "1. Lead with the user's need, task, or question.\n"
    "2. Use plain language and active voice.\n"
    "3. Keep sentences concise and easy to scan.\n"
    "4. Make the next step obvious.\n"
    "5. When relevant, reinforce one or more of these themes:\n"
    "   - safety  |  reliability  |  affordability  |  clean energy progress\n"
    "   - community support  |  customer choice  |  wildfire & disaster recovery\n"
    "6. Sound practical and responsible, not salesy, flashy, or clever.\n"
    "7. Reassure without overpromising.\n"
    "8. Avoid jargon unless required; if you must use a technical term or program name, explain it simply.\n"
    "9. Use \"you\" for customer actions/benefits and \"we\" for SCE's role/responsibility.\n"
    "10. If information is missing, do not invent facts. Flag assumptions clearly.\n\n"
    "Please create:\n"
    "- Headline\n- Subheadline\n- Body copy\n- CTA\n- Optional alternate headline choices (3)\n\n"
    "Context:\n"
    "- Audience: [insert audience]\n"
    "- Purpose: [insert purpose]\n"
    "- Topic: [insert topic]\n"
    "- Desired action: [insert what the reader should do next]\n"
    "- Channel: [web page / landing page / email / article / banner / app / FAQ / support page]\n"
    "- Tone emphasis: [more helpful / more urgent / more reassuring / more inspirational]\n"
    "- Length: [short / medium / long]\n"
    "- Must include: [insert required facts, programs, links, dates, disclaimers]\n"
    "- Must avoid: [insert prohibited claims, phrases, or topics]\n\n"
    "Additional instructions:\n"
    "- Structure the copy for easy scanning with clear subheads if needed.\n"
    "- Prioritize clarity over persuasion.\n"
    "- Where appropriate, connect the content to practical benefits for customers and communities.\n"
    "- For support, billing, outage, wildfire, scam, or safety-related topics, use especially calm, precise, and empathetic language.\n"
    "- For clean energy or innovation topics, connect today's actions to a more reliable, resilient, and cleaner energy future (California's net-zero goal by 2045)."
)

# Long prompt — render as individual lines so it can flow across pages
for line in master_prompt.split("\n"):
    story.append(Paragraph(line if line.strip() else "&nbsp;", body_sm))


story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Quick prompt (fastest version)", h2))
quick_prompt = (
    "Write this in an SCE website voice: clear, helpful, calm, trustworthy, and action-oriented. "
    "Lead with the customer's need, use plain language, keep it easy to scan, and make the next step obvious. "
    "Avoid hype, jargon, and clever marketing language. Use a practical, community-centered tone and, "
    "where relevant, tie the message to safety, reliability, affordability, or clean energy progress.\n\n"
    "Create:\n1. headline\n2. subheadline\n3. body copy\n4. CTA\n\n"
    "Topic: [insert topic]\nAudience: [insert audience]\nPurpose: [insert purpose]\n"
    "Desired action: [insert CTA goal]\nLength: [insert length]\n"
    "Must include: [facts/programs]\nMust avoid: [claims/phrases]"
)
for line in quick_prompt.split("\n"):
    story.append(Paragraph(line if line.strip() else "&nbsp;", body_sm))


story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Channel-specific prompt starters", h2))
channels = [
    ("<b>Web hero:</b>",
     "\"Write a homepage hero in an SCE style with a task-led headline, one-line subheadline, and one CTA.\""),
    ("<b>FAQ / help article:</b>",
     "\"Write a support article in an SCE style with plain-language headings, concise answers, and clear next steps.\""),
    ("<b>Email:</b>",
     "\"Write a short customer email in an SCE style that is calm, clear, and practical. Include a helpful subject line and one primary CTA.\""),
    ("<b>Banner / promo tile:</b>",
     "\"Write a short banner in an SCE style with a benefit-led headline and a straightforward CTA.\""),
    ("<b>Program page:</b>",
     "\"Write a program overview in an SCE style that explains who it is for, why it matters, and how to get started.\""),
    ("<b>Wildfire / disaster recovery</b> <font color='#E57200'>[new]</font>:",
     "\"Write a wildfire safety or disaster recovery page in an SCE style. Acknowledge the situation calmly, "
     "state what SCE is doing, and provide specific resources and next steps. Avoid fear-based language. "
     "Use a tone that is calm, factual, and empathetic.\""),
]
for label, prompt in channels:
    story.append(bullet_item(f"{label}  {prompt}"))

story.append(Spacer(1, 0.08*inch))
story.append(Paragraph(
    "<font size='8' color='#888888'>SCE Brand Copy Playbook &nbsp;&nbsp;|&nbsp;&nbsp; Page 7</font>", body_sm))

# ── PAGE 8: EXAMPLES ──────────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("7.  Examples", h1))
story.append(section_rule())
story.append(Paragraph(
    "Use these examples to calibrate what \"on-brand\" feels like.", body))
story.append(Spacer(1, 0.06*inch))

def example_block(title, less_aligned, revision_items, why):
    elems = []
    elems.append(Paragraph(title, h3))
    elems.append(Paragraph(
        f"<b>Less aligned:</b> <i>{less_aligned}</i>", body_sm))
    elems.append(Paragraph("<b>SCE-style revision:</b>", body_sm))
    for item in revision_items:
        elems.append(Paragraph(f"•  {item}", bullet))
    elems.append(Paragraph(
        f"<font color='#003087'><b>Why it works:</b></font> {why}", body_sm))
    box = shaded_box(elems, bg=SCE_LIGHT)
    return [box, Spacer(1, 0.1*inch)]

ex1 = example_block(
    "Example 1: Bill assistance landing page  [updated]",
    "Summer costs are hitting hard, but don't worry—we've got game-changing solutions to maximize your savings fast.",
    [
        "<b>Headline:</b> Explore Bill Assistance and Payment Options",
        "<b>Subheadline:</b> Find programs and tools that can help you manage your energy costs.",
        "<b>Body:</b> If your bill is higher than expected, support may be available. SCE offers payment plans, "
        "income-qualified discounts—CARE (32.5% off) and FERA (18% off)—and one-time bill assistance through "
        "the Energy Assistance Fund (EAF) for eligible customers. Customers enrolled in CARE or FERA also qualify "
        "for a discounted Base Services Charge. Explore your options to find what best fits your household's needs.",
        "<b>CTA:</b> View Assistance Programs",
    ],
    "Starts with the need, removes hype, names real support options with accurate discount amounts, "
    "and ends with a clear next step."
)

ex2 = example_block(
    "Example 2: EV program tile",
    "Step into the mobility revolution with cutting-edge electrification solutions for tomorrow's driver.",
    [
        "<b>Headline:</b> Explore EV Charging and Rebate Options",
        "<b>Subheadline:</b> Learn how electric vehicle programs can help you charge at home and manage energy use.",
        "<b>Body:</b> Find resources for EV rebates, charging options, and ways to make your energy use more efficient. "
        "Learn what programs are available and how to get started.",
        "<b>CTA:</b> See EV Resources",
    ],
    "Feels helpful and practical. It focuses on what the customer can learn and do next."
)

ex3 = example_block(
    "Example 3: Safety / scam awareness message",
    "Criminals are everywhere, so act now before it's too late.",
    [
        "<b>Headline:</b> Stay Safe from Utility Scams",
        "<b>Subheadline:</b> Learn how to recognize common scam tactics and where to get trusted information.",
        "<b>Body:</b> Scammers may contact customers by phone, text, email, or in person. Review common warning signs, "
        "know what SCE will and will not ask for, and use official SCE channels if you need to verify a message "
        "or payment request.",
        "<b>CTA:</b> Learn How to Protect Yourself",
    ],
    "Calm, specific, and useful. It avoids fear-based language while still encouraging action."
)

ex4 = example_block(
    "Example 4: Clean energy feature intro  [updated]",
    "We're redefining the energy universe with transformational innovation and a category-leading clean-tech ecosystem.",
    [
        "<b>Headline:</b> Building a More Resilient Clean Energy Future",
        "<b>Subheadline:</b> See how today's programs, rebates, and grid improvements support progress for customers and communities.",
        "<b>Body:</b> SCE is working to safely deliver more reliable and accessible clean energy in support of "
        "California's net-zero goal by 2045. Explore practical ways to save energy, lower costs, "
        "and take part in California's clean energy future.",
        "<b>CTA:</b> Learn More",
    ],
    "Optimistic but grounded. Connects broader progress to practical benefits and customer action. "
    "Anchors the mission to California's specific 2045 net-zero target."
)

ex5 = example_block(
    "Example 5: Wildfire recovery response  [new]",
    "We regret the devastating losses and urge all affected customers to seek compensation immediately.",
    [
        "<b>Headline:</b> Impacted by a Wildfire? Find Recovery Resources",
        "<b>Subheadline:</b> SCE is committed to supporting communities affected by wildfires.",
        "<b>Body:</b> If you were affected by a wildfire in SCE's service area, resources and assistance programs "
        "may be available to you. The Wildfire Recovery Compensation Program provides support for eligible community "
        "members. Review the program details to understand your options and next steps.",
        "<b>CTA:</b> Learn About Recovery Resources",
    ],
    "Calm, empathetic, and specific. Acknowledges impact without overclaiming or using fear-based language. "
    "Directs customers to a named program with a clear next step."
)

for block in [ex1, ex2, ex3, ex4, ex5]:
    for elem in block:
        story.append(elem)

story.append(Paragraph(
    "<font size='8' color='#888888'>SCE Brand Copy Playbook &nbsp;&nbsp;|&nbsp;&nbsp; Page 8</font>", body_sm))

# ── PAGE 9: REVIEW CHECKLIST ──────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("8.  Review Checklist", h1))
story.append(section_rule())
story.append(Paragraph("Before publishing or sharing copy, ask:", body))
story.append(Spacer(1, 0.08*inch))

checklist = [
    "Does the headline reflect the user's task or need?",
    "Can the reader understand the page purpose in the first 5 seconds?",
    "Is the copy written in plain language with short, active sentences?",
    "Are the benefits and next steps concrete—not vague or promotional?",
    "Is the tone appropriate to the situation (especially for sensitive topics)?",
    "Are acronyms explained or obvious from context?",
    "Is the CTA direct, visible, and easy to act on?",
    "Does the copy reinforce trust through clarity and responsibility?",
    "For billing or assistance copy: are program names and discount amounts accurate "
    "(e.g., CARE = 32.5%, FERA = 18%)?  <font color='#E57200'>[updated]</font>",
    "For wildfire or disaster recovery copy: does the tone remain calm, factual, and empathetic? "
    "Are specific programs named?  <font color='#E57200'>[new]</font>",
    "Have required legal, accessibility, regulatory, and factual reviews been completed?",
]

cl_data = [[Paragraph(f"\u2610  {item}", body_sm)] for item in checklist]
cl_t = Table(cl_data, colWidths=[6.3*inch])
cl_style = [
    ("FONTSIZE",      (0,0), (-1,-1), 9),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ("RIGHTPADDING",  (0,0), (-1,-1), 8),
    ("LINEBELOW",     (0,0), (-1,-2), 0.4, SCE_MID),
    ("BOX",           (0,0), (-1,-1), 0.5, SCE_MID),
]
for i, item in enumerate(checklist):
    if "[updated]" in item or "[new]" in item:
        cl_style.append(("BACKGROUND", (0,i), (-1,i), WARN_BG))
    elif i % 2 == 0:
        cl_style.append(("BACKGROUND", (0,i), (-1,i), LIGHT_GRAY))
    else:
        cl_style.append(("BACKGROUND", (0,i), (-1,i), WHITE))
cl_t.setStyle(TableStyle(cl_style))
story.append(cl_t)

story.append(Spacer(1, 0.22*inch))
story.append(Paragraph("9.  Source Note", h1))
story.append(section_rule())
story.append(shaded_box([
    Paragraph(
        "This playbook was synthesized from a review of public-facing SCE.com content as of "
        "<b>April 24, 2026</b>. Reviewed pages included: Welcome to SCE (homepage), About SCE, "
        "CARE &amp; FERA, Bill Assistance Programs, Customer Service Center, Clean Energy &amp; Efficiency, "
        "Wildfire Safety, and customer support/contact content.", body_sm),
    Spacer(1, 6),
    Paragraph(
        "Observed themes included task-led headings, practical support language, clear calls to action, "
        "customer-service orientation, and a mission focused on safe, reliable, clean, and affordable electricity. "
        "The Eaton Fire and Wildfire Recovery Compensation Program are active and prominent topics on the site "
        "as of this revision.", body_sm),
    Spacer(1, 6),
    Paragraph(
        "<b>Key facts verified from SCE.com:</b> SCE serves 15 million people across 50,000 sq. miles; "
        "CARE discount = 32.5%, FERA discount = 18%; one-quarter of SCE's service area is in a high fire risk area; "
        "California's net-zero goal = 2045. Official tagline: <b>Energy for What's Ahead\u00ae</b>", body_sm),
    Spacer(1, 6),
    Paragraph(
        "<i>For production use, teams should continue to validate claims, dates, program details, URLs, "
        "accessibility requirements, and any legal or regulatory language against the most current approved source.</i>",
        note),
], bg=LIGHT_GRAY))

story.append(Spacer(1, 0.08*inch))
story.append(Paragraph(
    "<font size='8' color='#888888'>SCE Brand Copy Playbook &nbsp;&nbsp;|&nbsp;&nbsp; Page 9</font>", body_sm))

# ── Build ──────────────────────────────────────────────────────────────────
doc.build(story)
print("Done:", OUTPUT)
