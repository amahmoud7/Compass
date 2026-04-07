# Compass CHW — Landing Page Redesign Design Spec

**Date:** 2026-04-07
**Status:** Approved
**Authors:** Akram Mahmoud (CTO), Claude (design assistant)

---

## Overview

Redesign the Compass CHW landing page at `joincompasschw.com` to replace the current generic healthcare aesthetic with a premium, warm, community-centered design using taste-skill principles. The landing page is the primary entry point for both community members seeking help and CHWs looking for work.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Tone** | Warm & Human | CHWs are neighbors helping neighbors — not a clinical SaaS product |
| **Audience** | Dual Hero (split entry) | Neither audience (Members or CHWs) is secondary |
| **Page Depth** | Story-Driven (full narrative) | Full Compass story on one scrollable page for credibility and conversion |
| **Typography** | Outfit | Geometric, friendly, approachable without being playful |

## Taste-Skill Configuration

```
DESIGN_VARIANCE = 6   (moderate asymmetry — offset, not chaotic)
MOTION_INTENSITY = 4  (scroll-triggered fades, hover lifts — no heavy animation)
VISUAL_DENSITY = 4    (airy, spacious — marketing page, not a dashboard)
```

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--color-primary` | `#2C3E2D` | Headlines, primary buttons, footer background |
| `--color-accent` | `#6B8F71` | Accent text, eyebrow badges, trust checkmarks, links |
| `--color-accent-light` | `rgba(107,143,113,0.1)` | Badge backgrounds, icon containers |
| `--color-warm-bg` | `#FBF7F0` | Page background |
| `--color-warm-bg-dark` | `#F0EBE3` | Gradient endpoints, section alternation |
| `--color-warm-bg-darker` | `#EDE5D8` | Deeper gradient endpoints |
| `--color-card` | `#FFFFFF` | Card surfaces |
| `--color-text-primary` | `#2C3E2D` | Headings, body text |
| `--color-text-secondary` | `#7A7A6E` | Subtitles, descriptions |
| `--color-text-muted` | `#BBBBAA` | Hints, fine print |
| `--color-chw-accent` | `#D4B896` | CHW path card accent, CHW testimonial badges |
| `--color-member-accent` | `#6B8F71` | Member path card accent, member badges |

### Anti-Patterns (from taste-skill)

- NO `Inter` font — replaced with `Outfit`
- NO pure `#000000` — using `#2C3E2D` (deep forest green)
- NO neon/purple/blue gradients
- NO 3-column equal card layouts
- NO generic placeholder names — using real Compass mock data
- NO `h-screen` — using `min-h-[100dvh]`

## Typography

| Level | Font | Weight | Size | Tracking | Line Height |
|-------|------|--------|------|----------|-------------|
| Display (H1) | Outfit | 700 | 52px | -0.03em | 1.06 |
| Section Title (H2) | Outfit | 700 | 40px | -0.03em | 1.1 |
| Card Heading (H3) | Outfit | 700 | 22px | -0.02em | 1.2 |
| Body | Outfit | 400 | 17px | normal | 1.6 |
| Body Small | Outfit | 400 | 14px | normal | 1.5 |
| Eyebrow | Outfit | 600 | 11px | 0.08em | 1.0 |
| UI Label | Outfit | 600 | 13px | normal | 1.0 |

## Page Sections (9 Total)

### Section 1: Navigation

- Fixed top, blurred glass background (`backdrop-filter: blur(16px)`)
- Logo: "Compass**CHW**" — primary color, accent on "CHW"
- Links: Services, How It Works, Impact, Get Started (CTA button)
- Responsive: links collapse, only CTA button on mobile

### Section 2: Hero (Dual Path)

- **Layout:** Asymmetric 2-column grid — headline left, path cards right
- **Left column:**
  - Eyebrow badge with animated pulse dot: "Community Health Workers"
  - Headline: "Community health, **connected.**"
  - Subtitle: One sentence addressing both audiences
  - Trust strip: HIPAA Compliant, Medi-Cal Certified, No Cost to Members
- **Right column:** Two stacked path cards
  - "I Need Help" — green top accent bar, primary CTA ("Get Matched"), hint: "Free with your health plan"
  - "I'm a CHW" — warm tan accent bar, secondary outlined CTA ("Start Earning"), hint: "$22/unit - Flexible hours"
- Both cards link to `https://joincompasschw.com/register`
- Background: warm bone gradient with subtle radial light effects
- Cards have hover lift with spring-like cubic-bezier transition

### Section 3: Verticals

- Background: White
- 5-card grid (responsive: 2-column on mobile)
- Each card: icon in gradient-tinted container, title, short description
- Cards: Housing, Rehab & Recovery, Food & Pantry, Mental Health, Healthcare
- Hover: `translateY(-4px)` lift with soft shadow

### Section 4: How It Works

- Background: Warm gradient (`#F5EDE0` to `#FBF7F0`)
- Side-by-side 2-column layout — Member flow left, CHW flow right
- Each column: 3 numbered steps with connector lines
- Member steps: Tell us what you need, Get matched, Start your health journey
- CHW steps: Create your profile, Browse community requests, Document & get paid
- Color-coded step numbers (green for Member, warm tan for CHW)

### Section 5: Impact Stats

- Background: Dark forest green (`#2C3E2D`)
- 4-card grid with semi-transparent card backgrounds
- Stats: 81% engagement, 5 verticals, $22/unit, $0 cost to members
- Large display numbers (42px, weight 800), muted labels below
- Hover: subtle lift and background opacity shift

### Section 6: Testimonials

- Background: White
- 2x2 grid (responsive: single column on mobile)
- 4 testimonial cards: 2 members, 2 CHWs
- Each card: large opening quote mark, quote text, author with avatar + name + location + role badge
- Testimonial authors from mock data: Rosa Delgado, Darnell Washington, Nadia Al-Rashid, Linh Tran Nguyen
- Warm bone card backgrounds (`#FBF7F0`)

### Section 7: Waitlist / Email Capture

- Background: White
- Centered form (max-width: 560px)
- Fields: First Name + Last Name (side by side), Email, Role dropdown (Member, CHW, Organization, Other)
- Submit button: full-width, primary style
- Anti-spam note below
- Success state: green checkmark circle, confirmation message
- Form fields: warm bone background, accent-colored focus ring

### Section 8: Final CTA (above footer)

- Background: Warm gradient
- Centered headline: "Your community is waiting"
- Dual buttons repeating the Member/CHW split
- Both link to `https://joincompasschw.com/register`

### Section 9: Footer

- Background: Dark forest green (`#2C3E2D`)
- 4-column grid: Brand/tagline, Platform links, Company links, Legal links
- Bottom bar: copyright, location
- Footer links: For Members and For CHWs link to `/register`; How It Works and Service Areas anchor to page sections

## Animations

- **Scroll-triggered fade-up:** `translateY(24px)` + `opacity: 0` to visible, `0.7s` with `cubic-bezier(0.22, 1, 0.36, 1)`, triggered at 15% intersection
- **Eyebrow pulse:** Infinite 2s ease-in-out opacity cycle on the green dot
- **Card hover:** `translateY(-3px)` with `cubic-bezier(0.34, 1.56, 0.64, 1)` (spring feel) + shadow expansion
- **Button hover:** `translateY(-1px)` + background darken
- **Button active:** `translateY(1px)` (press-down feel)
- All animations on `transform` and `opacity` only (GPU-accelerated)

## Responsive Breakpoints

| Breakpoint | Changes |
|------------|---------|
| `> 900px` | Full layout — 2-column hero, 5-column verticals, 2-column how-it-works, 4-column stats, 2x2 testimonials |
| `<= 900px` | Single column throughout, hero title 36px, section padding 64px 24px, nav links hidden except CTA, form fields stack |

## Links & Routing

All CTA buttons (hero path cards, section 8 buttons, nav "Get Started", footer platform links) route to:

```
https://joincompasschw.com/register
```

Internal anchor links:
- "Services" nav link → `#verticals`
- "How It Works" nav link → `#how`
- "Impact" nav link → `#impact`

## Future Enhancements (Not In Scope)

- Higgsfield-generated images/videos for hero, verticals, testimonial portraits, and stats background
- A/B testing between landing page variants
- Analytics integration (Vercel Analytics, Plausible, or PostHog)
- Contact form backend (currently frontend-only)

## Deployment

- **Platform:** Vercel (free tier)
- **Domain:** `joincompasschw.com` (GoDaddy registration, DNS pointed to Vercel)
- **Framework:** React 19 + Vite + Tailwind CSS v4
- **Root Directory:** `web/`
- **Auto-deploy:** Every push to `main` on `github.com/Compasschw/Compass`

## Reference Mockup

The approved full-page mockup is available at:
```
/Users/akrammahmoud/Compass/.superpowers/brainstorm/68622-1775542989/content/full-landing.html
```
