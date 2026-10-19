"""Generate 3 sample 5-page PDF resumes into this uploads folder."""
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
    PageBreak,
    HRFlowable,
)

OUT_DIR = Path(__file__).resolve().parent.parent / "uploads"


def styles():
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "Name",
            parent=base["Heading1"],
            fontSize=22,
            spaceAfter=4,
            textColor="#0f172a",
        ),
        "role": ParagraphStyle(
            "Role",
            parent=base["Normal"],
            fontSize=12,
            textColor="#334155",
            spaceAfter=6,
        ),
        "contact": ParagraphStyle(
            "Contact",
            parent=base["Normal"],
            fontSize=9,
            textColor="#475569",
            spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontSize=13,
            spaceBefore=10,
            spaceAfter=6,
            textColor="#1e293b",
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontSize=10,
            leading=14,
            spaceAfter=6,
        ),
        "job": ParagraphStyle(
            "Job",
            parent=base["Normal"],
            fontSize=11,
            leading=14,
            spaceBefore=8,
            spaceAfter=2,
            textColor="#0f172a",
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=base["Normal"],
            fontSize=9,
            textColor="#64748b",
            spaceAfter=4,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["Normal"],
            fontSize=10,
            leading=13,
        ),
    }


def bullets(items, s):
    return ListFlowable(
        [ListItem(Paragraph(i, s["bullet"]), leftIndent=8, bulletColor="#2563eb") for i in items],
        bulletType="bullet",
        start="•",
        leftIndent=15,
        spaceBefore=2,
        spaceAfter=6,
    )


def section(story, title, s):
    story.append(Paragraph(title, s["h2"]))
    story.append(HRFlowable(width="100%", thickness=0.6, color="#cbd5e1", spaceAfter=6))


def build_resume(path, person):
    s = styles()
    doc = SimpleDocTemplate(
        str(path),
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title=f"{person['name']} Resume",
    )
    story = []

    # --- Page 1: Intro + Contact + Summary + Education start ---
    story.append(Paragraph(person["name"], s["name"]))
    story.append(Paragraph(person["title"], s["role"]))
    story.append(
        Paragraph(
            f"{person['email']}  |  {person['phone']}  |  {person['location']}  |  {person['linkedin']}",
            s["contact"],
        )
    )
    story.append(HRFlowable(width="100%", thickness=1.2, color="#2563eb", spaceAfter=8))

    section(story, "1. Introduction / Professional Profile", s)
    for p in person["intro"]:
        story.append(Paragraph(p, s["body"]))

    section(story, "2. Professional Summary", s)
    for p in person["summary"]:
        story.append(Paragraph(p, s["body"]))

    section(story, "3. Contact Information", s)
    story.append(
        bullets(
            [
                f"<b>Full Name:</b> {person['name']}",
                f"<b>Email:</b> {person['email']}",
                f"<b>Phone:</b> {person['phone']}",
                f"<b>Location:</b> {person['location']}",
                f"<b>LinkedIn:</b> {person['linkedin']}",
                f"<b>Portfolio / Website:</b> {person.get('website', 'N/A')}",
                f"<b>Availability:</b> {person.get('availability', 'Open to full-time opportunities')}",
            ],
            s,
        )
    )

    section(story, "4. Education Details", s)
    for edu in person["education"]:
        story.append(Paragraph(f"<b>{edu['degree']}</b> — {edu['school']}", s["job"]))
        story.append(Paragraph(f"{edu['years']}  |  GPA: {edu['gpa']}  |  {edu['location']}", s["meta"]))
        story.append(bullets(edu["details"], s))

    story.append(PageBreak())

    # --- Page 2: Skills + more education/certifications ---
    section(story, "5. Core Skills", s)
    story.append(Paragraph("<b>Technical Skills</b>", s["job"]))
    story.append(bullets(person["skills_technical"], s))
    story.append(Paragraph("<b>Tools & Platforms</b>", s["job"]))
    story.append(bullets(person["skills_tools"], s))
    story.append(Paragraph("<b>Soft Skills</b>", s["job"]))
    story.append(bullets(person["skills_soft"], s))

    section(story, "6. Certifications & Training", s)
    story.append(bullets(person["certifications"], s))

    section(story, "7. Additional Qualifications", s)
    for p in person["additional"]:
        story.append(Paragraph(p, s["body"]))

    story.append(PageBreak())

    # --- Page 3: Projects ---
    section(story, "8. Projects", s)
    for proj in person["projects"]:
        story.append(Paragraph(f"<b>{proj['name']}</b>", s["job"]))
        story.append(Paragraph(f"{proj['role']}  |  {proj['period']}", s["meta"]))
        story.append(Paragraph(proj["desc"], s["body"]))
        story.append(bullets(proj["bullets"], s))

    story.append(PageBreak())

    # --- Page 4: Experience ---
    section(story, "9. Professional Experience (Detailed)", s)
    for job in person["experience"]:
        story.append(Paragraph(f"<b>{job['title']}</b> — {job['company']}", s["job"]))
        story.append(Paragraph(f"{job['period']}  |  {job['location']}", s["meta"]))
        story.append(Paragraph(job["overview"], s["body"]))
        story.append(bullets(job["bullets"], s))

    story.append(PageBreak())

    # --- Page 5: More experience + Hobbies ---
    section(story, "10. Extended Experience Highlights", s)
    for p in person["extended_experience"]:
        story.append(Paragraph(p, s["body"]))
    story.append(bullets(person["extended_bullets"], s))

    section(story, "11. Hobbies & Interests", s)
    story.append(Paragraph(person["hobbies_intro"], s["body"]))
    story.append(bullets(person["hobbies"], s))

    section(story, "12. Closing Note", s)
    story.append(Paragraph(person["closing"], s["body"]))

    doc.build(story)
    print(f"Created: {path.name}")


SOFTWARE = {
    "name": "Alex Rivera",
    "title": "Software Engineer — Full Stack & Cloud Systems",
    "email": "alex.rivera.dev@email.com",
    "phone": "+1 (415) 555-0142",
    "location": "San Francisco, CA, USA",
    "linkedin": "linkedin.com/in/alexrivera-swe",
    "website": "alexrivera.dev",
    "intro": [
        "I am a results-driven Software Engineer with over 7 years of experience designing, building, and shipping "
        "scalable web applications and distributed backend systems. My career has spanned early-stage startups and "
        "mid-size product companies, where I have owned features end-to-end — from requirements and architecture "
        "through implementation, testing, deployment, and production support.",
        "I specialize in modern TypeScript/JavaScript stacks, cloud-native services on AWS, and clean API design. "
        "I enjoy mentoring junior engineers, improving developer experience, and turning ambiguous product goals "
        "into reliable software that users trust.",
    ],
    "summary": [
        "Proven track record delivering customer-facing platforms serving 100K+ monthly active users with high "
        "availability targets (99.9%+). Strong background in React, Next.js, Node.js, .NET, PostgreSQL, Redis, "
        "and CI/CD automation. Comfortable leading technical design reviews, writing RFCs, and collaborating with "
        "product, design, and QA.",
        "Looking for a Software Engineer role focused on product impact, engineering excellence, and continuous learning.",
    ],
    "education": [
        {
            "degree": "B.S. in Computer Science",
            "school": "University of California, Berkeley",
            "years": "2013 – 2017",
            "gpa": "3.72 / 4.00",
            "location": "Berkeley, CA",
            "details": [
                "Coursework: Algorithms, Operating Systems, Databases, Distributed Systems, Machine Learning basics",
                "Senior Capstone: Real-time collaborative document editor (WebSockets + CRDTs)",
                "Teaching Assistant for Introduction to Data Structures (2 semesters)",
            ],
        },
        {
            "degree": "Online Specialization — Cloud Architecture",
            "school": "Coursera / Google Cloud",
            "years": "2021",
            "gpa": "Completed with distinction",
            "location": "Remote",
            "details": [
                "Covered GKE, Cloud Run, Pub/Sub, IAM, and cost-aware design patterns",
                "Capstone: Multi-service e-commerce demo with autoscaling and observability",
            ],
        },
    ],
    "skills_technical": [
        "Languages: TypeScript, JavaScript, C#, Python, SQL, HTML/CSS",
        "Frontend: React, Next.js, Redux, Tailwind CSS, accessibility (a11y) practices",
        "Backend: Node.js/Express, ASP.NET Core Web API, REST, GraphQL basics",
        "Data: PostgreSQL, MongoDB, Redis, Elasticsearch basics",
        "Cloud & DevOps: AWS (EC2, S3, Lambda, RDS), Docker, GitHub Actions, Terraform basics",
        "Testing: Jest, Playwright, xUnit, integration and contract testing mindset",
    ],
    "skills_tools": [
        "Git, GitHub, Jira, Linear, Figma (handoff), Postman, Swagger/OpenAPI",
        "Datadog, Sentry, CloudWatch for monitoring and incident triage",
        "VS Code, Visual Studio 2022, Cursor",
    ],
    "skills_soft": [
        "Clear written communication (RFCs, PR descriptions, runbooks)",
        "Cross-functional collaboration with Product and Design",
        "Mentorship, code review hygiene, and pragmatic prioritization",
    ],
    "certifications": [
        "AWS Certified Developer – Associate (2022)",
        "Scrum Foundation awareness (team delivery practices)",
        "Internal security training: OWASP Top 10 and secure coding checklist",
    ],
    "additional": [
        "I regularly contribute to internal engineering blogs covering incident retrospectives and performance "
        "tuning. I have also presented lunch-and-learns on Next.js App Router migration and API versioning strategies.",
        "Open to hybrid or remote roles with occasional on-site collaboration. Prefer environments that value "
        "automated testing, thoughtful code review, and measurable product outcomes.",
    ],
    "projects": [
        {
            "name": "ResumeMatch AI — Resume Ranking Web App",
            "role": "Full Stack Engineer (personal / portfolio)",
            "period": "2025 – 2026",
            "desc": "Built a simple Next.js + .NET Web API app that uploads resumes and uses Google Gemini to rank them against a job description.",
            "bullets": [
                "Implemented file upload (max 3 resumes), PDF text extraction, and Gemini prompt pipeline",
                "Designed a minimal 4-section UI: upload, list, job description, best-match result",
                "Focused on simple architecture: one controller, one Gemini service with small helper functions",
            ],
        },
        {
            "name": "PulseBoard — Real-time Ops Dashboard",
            "role": "Lead Frontend + API integration",
            "period": "2023 – 2024",
            "desc": "Internal dashboard for operations teams to monitor order pipelines and alert thresholds.",
            "bullets": [
                "React + WebSocket feed with optimistic UI updates and reconnect strategy",
                "Reduced mean time to notice (MTTN) for pipeline stalls by ~35%",
                "Added role-based views for managers vs on-call engineers",
            ],
        },
        {
            "name": "ShopLite Checkout Service",
            "role": "Backend Engineer",
            "period": "2022",
            "desc": "Stateless checkout microservice with idempotent payment intents and webhook reconciliation.",
            "bullets": [
                "Designed idempotency keys and outbox pattern for reliable event publishing",
                "Load-tested to 500 RPS with p95 latency under 120ms for read paths",
                "Wrote runbooks and chaos test checklist for payment provider outages",
            ],
        },
        {
            "name": "DocuSync Collaborative Notes",
            "role": "University Capstone / Maintainer",
            "period": "2017",
            "desc": "Browser-based collaborative notes with conflict-free replicated data types.",
            "bullets": [
                "Implemented CRDT merge logic and presence indicators",
                "Packaged demo with Docker Compose for local multi-user testing",
            ],
        },
    ],
    "experience": [
        {
            "title": "Senior Software Engineer",
            "company": "Northline Systems",
            "period": "Jan 2022 – Present",
            "location": "San Francisco, CA (Hybrid)",
            "overview": "Own customer account and billing surfaces for a B2B SaaS platform. Partner with product managers to ship quarterly roadmap items and keep production healthy.",
            "bullets": [
                "Led migration of legacy jQuery admin pages to Next.js + TypeScript, improving Lighthouse performance scores from ~55 to ~90",
                "Designed and shipped subscription upgrade/downgrade API with prorated billing edge cases covered by automated tests",
                "Introduced feature flags and canary releases; cut rollback time during incidents from hours to minutes",
                "Mentored 2 junior engineers; established PR checklist covering security, accessibility, and observability",
                "Participated in on-call rotation; authored postmortems with actionable follow-ups",
            ],
        },
        {
            "title": "Software Engineer",
            "company": "BrightCart Commerce",
            "period": "Aug 2018 – Dec 2021",
            "location": "Oakland, CA",
            "overview": "Built storefront and order APIs for a mid-market e-commerce platform used by independent retailers.",
            "bullets": [
                "Implemented cart and checkout flows with Node.js and PostgreSQL; reduced checkout abandonment by 8% after UX fixes",
                "Added Redis caching for catalog reads; lowered p95 catalog API latency by ~40%",
                "Collaborated with mobile team on shared OpenAPI contracts and contract tests",
                "Automated CI pipelines with lint, unit, and smoke tests on every pull request",
            ],
        },
        {
            "title": "Junior Software Engineer",
            "company": "HelioLabs Startup",
            "period": "Jun 2017 – Jul 2018",
            "location": "San Jose, CA",
            "overview": "Early-stage product engineer working across frontend and backend for an analytics MVP.",
            "bullets": [
                "Shipped MVP dashboard in React within first 3 months of joining",
                "Wrote ETL scripts in Python to ingest CSV exports from partner systems",
                "Set up basic monitoring and error reporting with Sentry",
            ],
        },
    ],
    "extended_experience": [
        "Across roles I have repeatedly owned ambiguous problems: unclear requirements, legacy code, and production "
        "pressure. My approach is to clarify success metrics early, ship iteratively behind flags, and invest in "
        "tests where failure is expensive (payments, auth, data integrity).",
        "I am comfortable pairing, running design reviews, and documenting decisions so teams can move faster later. "
        "Below are additional highlights not fully covered in the role bullets above.",
    ],
    "extended_bullets": [
        "Reduced AWS compute spend ~18% by right-sizing services and scheduling non-prod environments",
        "Championed structured logging and correlation IDs across services for faster incident debugging",
        "Helped hire 4 engineers by writing take-home briefs and conducting system design interviews",
        "Volunteered as internal open-source champion for shared UI component library",
        "Completed security review remediation for SSO/SAML enterprise login path",
    ],
    "hobbies_intro": "Outside of work I stay curious and balanced through a mix of technical and creative hobbies.",
    "hobbies": [
        "Building small open-source utilities and writing short engineering blog posts",
        "Weekend hiking in the Bay Area and amateur landscape photography",
        "Chess club meetups and solving algorithm puzzles for fun",
        "Cooking Mediterranean recipes and hosting friends for dinner",
        "Volunteering at local coding workshops for high school students",
    ],
    "closing": (
        "Thank you for reviewing my resume. I would welcome the chance to discuss how my software engineering "
        "background can help your team deliver reliable product outcomes. References available upon request."
    ),
}

MECHANICAL = {
    "name": "Jordan Blake",
    "title": "Mechanical Engineer — Design, Manufacturing & Product Development",
    "email": "jordan.blake.me@email.com",
    "phone": "+1 (312) 555-0198",
    "location": "Chicago, IL, USA",
    "linkedin": "linkedin.com/in/jordanblake-me",
    "website": "jordanblake-portfolio.com",
    "intro": [
        "I am a Mechanical Engineer with 6+ years of experience in product design, CAD modeling, DFM/DFA, and "
        "cross-functional manufacturing support. I have worked on consumer devices, industrial fixtures, and "
        "electromechanical assemblies from concept through pilot production.",
        "I combine strong fundamentals in solid mechanics and thermal/fluids with practical shop-floor awareness. "
        "I enjoy translating customer requirements into robust mechanical designs that can be built repeatedly "
        "with controlled cost and quality.",
    ],
    "summary": [
        "Hands-on experience with SolidWorks, Creo, FEA (static/modal), GD&T, CNC/DFM reviews, and supplier "
        "collaboration. Known for clear drawings, thorough design reviews, and closing the loop between design "
        "intent and manufacturing reality.",
        "Seeking a Mechanical Engineer role in product development or NPI where I can own mechanisms, enclosures, "
        "and continuous improvement of production processes.",
    ],
    "education": [
        {
            "degree": "B.S. in Mechanical Engineering",
            "school": "University of Illinois Urbana-Champaign",
            "years": "2014 – 2018",
            "gpa": "3.65 / 4.00",
            "location": "Urbana, IL",
            "details": [
                "Coursework: Machine Design, Heat Transfer, Fluid Mechanics, Controls, Manufacturing Processes",
                "Senior Design: Compact cooling fixture for battery pack prototype (team of 4)",
                "ASME student chapter project lead for Formula SAE chassis subsystem support",
            ],
        },
        {
            "degree": "Professional Development — GD&T Fundamentals",
            "school": "ASME Training",
            "years": "2020",
            "gpa": "Certificate earned",
            "location": "Online / Chicago",
            "details": [
                "Applied ASME Y14.5 concepts to improve drawing clarity and reduce supplier clarification loops",
                "Practice projects on positional tolerances and datum schemes for machined housings",
            ],
        },
    ],
    "skills_technical": [
        "CAD: SolidWorks (CSWP), Creo Parametric, AutoCAD basics",
        "Analysis: SolidWorks Simulation, ANSYS Mechanical basics, hand calculations for stress/deflection",
        "Manufacturing: CNC machining awareness, sheet metal, injection molding DFM, 3D printing (FDM/SLA)",
        "Documentation: Detailed drawings, BOMs, ECO/ECN processes, PLM basics",
        "Materials: Aluminum alloys, steels, engineering plastics, gasket/seal selection basics",
        "Testing: Prototype fixture design, dimensional inspection support, root-cause on field failures",
    ],
    "skills_tools": [
        "SolidWorks PDM, Windchill/PLM exposure, Jira for NPI tracking",
        "Minitab basics for capability awareness, Excel for tolerance stacks",
        "Calipers, micrometers, CMM report interpretation with quality team",
    ],
    "skills_soft": [
        "Cross-functional communication with electrical, manufacturing, and supply chain",
        "Structured problem solving (5-Why, fishbone) during build issues",
        "Clear design review presentations for stakeholders",
    ],
    "certifications": [
        "Certified SolidWorks Professional (CSWP)",
        "ASME GD&T Fundamentals Certificate",
        "OSHA 10-Hour General Industry awareness",
    ],
    "additional": [
        "I maintain a portfolio of CAD models and prototype photos (available under NDA). Comfortable traveling "
        "to suppliers for first-article reviews and pilot builds.",
        "Interested in roles involving mechatronics collaboration, thermal management, and design for high-volume "
        "or mid-volume manufacturing.",
    ],
    "projects": [
        {
            "name": "Precision Alignment Fixture for Assembly Line",
            "role": "Mechanical Design Lead",
            "period": "2024",
            "desc": "Designed an adjustable fixture to locate PCB-mounted optical modules during final assembly.",
            "bullets": [
                "Reduced average alignment time from 12 minutes to under 4 minutes per unit",
                "Incorporated quick-release clamps and hard stops for operator consistency",
                "Created full drawing package and work instruction sketches for manufacturing",
            ],
        },
        {
            "name": "Consumer Enclosure Redesign for Drop Reliability",
            "role": "Mechanical Engineer",
            "period": "2022 – 2023",
            "desc": "Redesigned plastic enclosure ribs and screw bosses after field drop failures.",
            "bullets": [
                "Ran FEA screening and correlated with physical drop tests",
                "Improved first-pass yield at ultrasonic weld by revising energy director geometry",
                "Coordinated tooling changes with overseas injection molding supplier",
            ],
        },
        {
            "name": "Battery Pack Cooling Channel Prototype",
            "role": "University Senior Design / Team Member",
            "period": "2018",
            "desc": "Compact air-cooled channel concept for a small battery module prototype.",
            "bullets": [
                "Performed thermal hand calculations and CFD screening with teammate support",
                "Built SLA prototypes and validated temperature rise under load",
            ],
        },
        {
            "name": "Sheet Metal Chassis Cost-Down Initiative",
            "role": "NPI Support Engineer",
            "period": "2021",
            "desc": "Simplified chassis bend sequence and fastener count for a mid-volume product.",
            "bullets": [
                "Cut piece-part cost ~11% without changing external envelope",
                "Updated drawings and ECO package; trained assembly on new torque map",
            ],
        },
    ],
    "experience": [
        {
            "title": "Mechanical Engineer II",
            "company": "Vertex Automation",
            "period": "Mar 2021 – Present",
            "location": "Chicago, IL",
            "overview": "Own mechanical design for industrial sensing products and factory fixtures. Partner with manufacturing engineering on DFM and pilot builds.",
            "bullets": [
                "Delivered 3 released products from concept to pilot, including enclosures, brackets, and seals",
                "Led weekly design reviews; maintained risk register for thermal, ingress, and assembly risks",
                "Reduced ECO cycle time by standardizing drawing templates and checklist",
                "Supported supplier FAIs and resolved dimensional stack-up issues on machined housings",
                "Mentored an engineering intern on SolidWorks best practices and drawing standards",
            ],
        },
        {
            "title": "Mechanical Design Engineer",
            "company": "Lakeview Consumer Devices",
            "period": "Jul 2018 – Feb 2021",
            "location": "Evanston, IL",
            "overview": "Designed plastic and sheet metal parts for portable consumer electronics accessories.",
            "bullets": [
                "Owned CAD for two accessory SKUs from EVT through DVT",
                "Collaborated with electrical engineers on connector keep-outs and grounding paths",
                "Built rapid prototypes (FDM/SLA) for UX and fit checks with industrial design",
                "Documented assembly steps and torque specs for contract manufacturer",
            ],
        },
        {
            "title": "Engineering Intern — Manufacturing Support",
            "company": "Midwest Precision Machining",
            "period": "Summer 2017",
            "location": "Rockford, IL",
            "overview": "Supported CNC shop with fixture ideas and drawing clarifications for customer jobs.",
            "bullets": [
                "Created simple soft-jaw concepts that improved setup repeatability",
                "Learned shop constraints that still influence my DFM decisions today",
            ],
        },
    ],
    "extended_experience": [
        "My strongest contributions come when design and manufacturing stay tightly coupled. I prioritize early "
        "supplier feedback, realistic tolerances, and prototypes that answer the riskiest questions first.",
        "Additional accomplishments and working style notes:",
    ],
    "extended_bullets": [
        "Introduced a lightweight tolerance stack spreadsheet used by two product teams",
        "Co-led a kaizen on packaging foam that reduced shipping damage claims by ~20%",
        "Presented mechanical risk reviews to executive stakeholders ahead of tooling kickoff",
        "Maintained spare-parts BOM accuracy for field service kits",
        "Supported ISO-oriented documentation habits with quality engineering partners",
    ],
    "hobbies_intro": "I stay sharp by combining hands-on making with outdoor and community activities.",
    "hobbies": [
        "Home workshop projects: custom shelves, small CNC machining hobby parts",
        "Cycling and weekend trail rides around the Chicago area",
        "3D printing community meetups and sharing print profiles",
        "Watching F1 and analyzing simple vehicle dynamics for fun",
        "Volunteering at local STEM days demonstrating basic mechanisms for students",
    ],
    "closing": (
        "I appreciate your time reviewing this resume. I am excited to bring practical mechanical design and "
        "manufacturing collaboration skills to your engineering team. References available upon request."
    ),
}

ELECTRICAL = {
    "name": "Samira Khan",
    "title": "Electrical Engineer — Power Electronics, Controls & Embedded Systems",
    "email": "samira.khan.ee@email.com",
    "phone": "+1 (512) 555-0174",
    "location": "Austin, TX, USA",
    "linkedin": "linkedin.com/in/samirakhan-ee",
    "website": "samirakhan-ee.com",
    "intro": [
        "I am an Electrical Engineer with 6 years of experience in power electronics, mixed-signal board design, "
        "and embedded firmware bring-up. I have taken designs from schematic and PCB layout through lab validation, "
        "EMI troubleshooting, and transfer to manufacturing.",
        "I enjoy solving the interface between hardware and firmware: clean schematics, thoughtful layout, "
        "instrumented test plans, and documentation that manufacturing and field teams can trust.",
    ],
    "summary": [
        "Experience with DC-DC converters, motor drive stages, sensor front-ends, STM32/ESP32 platforms, and "
        "lab tools (oscilloscope, logic analyzer, electronic load, spectrum analyzer basics). Strong collaborator "
        "with mechanical and software teams on system integration.",
        "Seeking an Electrical Engineer position focused on product hardware, power systems, or embedded controls "
        "in a hands-on engineering culture.",
    ],
    "education": [
        {
            "degree": "B.S. in Electrical Engineering",
            "school": "The University of Texas at Austin",
            "years": "2014 – 2018",
            "gpa": "3.70 / 4.00",
            "location": "Austin, TX",
            "details": [
                "Coursework: Power Electronics, Analog Circuits, Digital Logic, Control Systems, Embedded Systems",
                "Senior Design: Closed-loop BLDC motor controller with current sensing and GUI telemetry",
                "IEEE student branch volunteer for tutoring and lab safety workshops",
            ],
        },
        {
            "degree": "Continuing Education — PCB Design for EMC",
            "school": "Industry short course",
            "years": "2021",
            "gpa": "Completed",
            "location": "Austin / Online",
            "details": [
                "Covered return paths, stackups, filtering, and practical debug strategies for radiated emissions",
                "Applied learnings to reduce pre-compliance failures on a subsequent product spin",
            ],
        },
    ],
    "skills_technical": [
        "Circuit design: DC-DC (buck/boost), linear regulators, gate drivers, sensing (current/voltage/temperature)",
        "PCB: Altium Designer, KiCad; multilayer layout, controlled impedance awareness, DFM/DFT basics",
        "Embedded: C/C++ on STM32, ESP32; UART/SPI/I2C; FreeRTOS familiarity",
        "Controls: PID tuning basics, current/speed loops for small motor drives",
        "Validation: Bench bring-up, electronic load testing, thermal soak, EMI pre-compliance support",
        "Documentation: Schematics packages, BOMs, test procedures, ECO support",
    ],
    "skills_tools": [
        "Oscilloscope, multimeter, logic analyzer, soldering/rework station, programmable PSU",
        "Altium, KiCad, MATLAB/Simulink basics, Git for firmware",
        "Jira, Confluence, manufacturer portals for component lifecycle checks",
    ],
    "skills_soft": [
        "Clear lab notebooks and handoff notes for manufacturing test",
        "Cross-discipline integration with mechanical and firmware teammates",
        "Calm, structured debug under schedule pressure",
    ],
    "certifications": [
        "IPC-A-610 awareness training (electronics assembly quality)",
        "Internal ESD control and lab safety certification",
        "Vendor training: TI power design seminars (selected modules)",
    ],
    "additional": [
        "Comfortable owning schematic-to-layout reviews and first-power-on checklists. Interested in roles involving "
        "battery-powered systems, industrial sensors, or renewable-adjacent power electronics.",
        "Portfolio of non-confidential block diagrams and bring-up photos available on request.",
    ],
    "projects": [
        {
            "name": "48V-to-12V Isolated DC-DC Module",
            "role": "Electrical Design Owner",
            "period": "2023 – 2024",
            "desc": "Designed an isolated converter module for industrial sensing nodes with efficiency and thermal targets.",
            "bullets": [
                "Met >90% efficiency target at nominal load after two layout spins",
                "Defined protection features: OCP, OVP, and thermal shutdown coordination with firmware",
                "Wrote production test limits and partnered with manufacturing on ICT fixtures",
            ],
        },
        {
            "name": "BLDC Motor Drive Evaluation Board",
            "role": "Hardware + Firmware Bring-up",
            "period": "2022",
            "desc": "Three-phase inverter stage with current sensing and closed-loop speed control demo.",
            "bullets": [
                "Implemented FOC-lite control path with STM32 timers and ADC sampling",
                "Characterized torque ripple and improved PWM dead-time settings",
                "Created GUI telemetry for lab demos and customer evaluations",
            ],
        },
        {
            "name": "Low-Noise Sensor Front-End for Vibration Monitoring",
            "role": "Analog Design Engineer",
            "period": "2021",
            "desc": "Signal conditioning chain for piezoelectric sensors in predictive maintenance hardware.",
            "bullets": [
                "Improved SNR through careful grounding and filter stage redesign",
                "Collaborated with mechanical team on shield can and cable strain relief",
            ],
        },
        {
            "name": "University Senior Design — Smart Motor Controller",
            "role": "Team Electrical Lead",
            "period": "2018",
            "desc": "Capstone project delivering a complete motor control demo with safety interlocks.",
            "bullets": [
                "Owned power stage schematic and current sensing accuracy budget",
                "Presented final demo to faculty and industry judges",
            ],
        },
    ],
    "experience": [
        {
            "title": "Electrical Engineer",
            "company": "RedRiver Controls",
            "period": "Feb 2021 – Present",
            "location": "Austin, TX",
            "overview": "Design and validate electronics for industrial control products. Own schematics, layout reviews, and lab characterization for power and sensing boards.",
            "bullets": [
                "Released two board revisions to production with full test coverage documentation",
                "Reduced field return rate related to connector intermittent faults by redesigning strain and ESD path",
                "Led schematic reviews attended by firmware, mechanical, and quality stakeholders",
                "Built automated Python scripts to log electronic-load sweep data for regression comparisons",
                "Supported contract manufacturer with first-article electrical measurements and yield triage",
            ],
        },
        {
            "title": "Junior Electrical Engineer",
            "company": "OrbitSense IoT",
            "period": "Aug 2018 – Jan 2021",
            "location": "Austin, TX",
            "overview": "Worked on battery-powered IoT sensor nodes: power budget, charging path, and RF-adjacent layout constraints.",
            "bullets": [
                "Designed Li-ion charging and protection circuit for a wearable-adjacent form factor",
                "Improved sleep current by ~30% through rail sequencing and firmware coordination",
                "Performed bring-up of ESP32-based prototypes and wrote flash/test station checklist",
                "Assisted EMI pre-compliance; added filtering that passed subsequent lab visit",
            ],
        },
        {
            "title": "Electrical Engineering Intern",
            "company": "Texas Power Labs",
            "period": "Summer 2017",
            "location": "Round Rock, TX",
            "overview": "Supported lab characterization of power supply reference designs.",
            "bullets": [
                "Automated repetitive efficiency measurements and plotted results for senior engineers",
                "Learned disciplined lab safety and instrument care practices",
            ],
        },
    ],
    "extended_experience": [
        "I approach electrical design as a system problem: power integrity, signal integrity, thermal behavior, "
        "firmware timing, and manufacturability must be considered early. I document assumptions so future spins "
        "are cheaper and safer.",
        "Additional highlights:",
    ],
    "extended_bullets": [
        "Created a reusable first-power-on checklist adopted by the hardware team",
        "Partnered with procurement on second-source ICs during a supply shortage",
        "Presented lunch-and-learn on return current paths and common EMI mistakes",
        "Supported field FA by reproducing customer load profiles on the bench",
        "Mentored a new graduate engineer on Altium libraries and schematic hygiene",
    ],
    "hobbies_intro": "My hobbies keep me curious about both electronics and the wider world.",
    "hobbies": [
        "DIY audio amplifier and guitar pedal experiments (safe low-voltage projects)",
        "Amateur radio study / Morse practice sessions with local club friends",
        "Trail running and weekend camping in Texas Hill Country",
        "Reading popular science books on energy systems and semiconductors",
        "Mentoring university students at hardware hack nights",
    ],
    "closing": (
        "Thank you for considering my application. I would be glad to discuss how my electrical engineering "
        "experience in power, sensing, and embedded bring-up can support your product roadmap. References on request."
    ),
}


def main():
    # Use timestamp-style names so they look like normal uploads; UI strips leading digits-
    builds = [
        ("1000000001-Software_Engineer_Alex_Rivera.pdf", SOFTWARE),
        ("1000000002-Mechanical_Engineer_Jordan_Blake.pdf", MECHANICAL),
        ("1000000003-Electrical_Engineer_Samira_Khan.pdf", ELECTRICAL),
    ]
    for filename, person in builds:
        build_resume(OUT_DIR / filename, person)
    print("Done. Files are in:", OUT_DIR)


if __name__ == "__main__":
    main()
