# Landing Page Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current LandingPageA with a warm, community-centered landing page matching the approved design spec and HTML mockup.

**Architecture:** Single-page landing with 9 sections, each as a focused React component. A shared `useScrollAnimation` hook handles IntersectionObserver-based fade-up reveals. All design tokens live in `index.css` via Tailwind v4 `@theme`. The page replaces `LandingPageA` as the default at `/landing`; variants B and C remain accessible at their existing routes.

**Tech Stack:** React 19, TypeScript (strict), Tailwind CSS v4, Vite 8, lucide-react (icons), Outfit font (Google Fonts)

**Reference files:**
- Design spec: `docs/superpowers/specs/2026-04-07-landing-page-redesign-design.md`
- Approved mockup: `.superpowers/brainstorm/68622-1775542989/content/full-landing.html`

---

## File Structure

### New files

| File | Responsibility |
|------|---------------|
| `src/features/landing/LandingPage.tsx` | Page orchestrator — composes all 9 sections |
| `src/features/landing/sections/NavBar.tsx` | Fixed glass nav with anchor links and CTA |
| `src/features/landing/sections/HeroSection.tsx` | Dual-path hero with eyebrow, headline, trust strip, path cards |
| `src/features/landing/sections/VerticalsSection.tsx` | 5 service vertical cards in responsive grid |
| `src/features/landing/sections/HowItWorksSection.tsx` | Side-by-side Member/CHW 3-step flows |
| `src/features/landing/sections/ImpactStatsSection.tsx` | Dark green stats section with 4 metric cards |
| `src/features/landing/sections/TestimonialsSection.tsx` | 2x2 testimonial grid with mock author data |
| `src/features/landing/sections/WaitlistSection.tsx` | Email capture form with success state |
| `src/features/landing/sections/FinalCTASection.tsx` | Dual CTA buttons above footer |
| `src/features/landing/sections/FooterSection.tsx` | 4-column footer with brand, links, legal |
| `src/features/landing/hooks/useScrollAnimation.ts` | IntersectionObserver hook for scroll-triggered fade-up |

### Modified files

| File | Changes |
|------|---------|
| `src/index.css` | Replace design tokens with warm palette, add Outfit font, add animation keyframes |
| `index.html` | Swap Inter font link for Outfit |
| `src/App.tsx` | Update import from `LandingPageA` to `LandingPage` for `/landing` route |

### Unchanged files

- `LandingPageB.tsx`, `LandingPageC.tsx` — remain at `/landing/b` and `/landing/c` (they use inline styles, unaffected by token changes)
- All auth, CHW, member, and shared components — the existing app token variables (`--color-primary`, etc.) get updated but those pages will adopt the new palette naturally

---

## Task 1: Foundation — Design Tokens, Font, and Scroll Hook

**Files:**
- Modify: `web/index.html`
- Modify: `web/src/index.css`
- Create: `web/src/features/landing/hooks/useScrollAnimation.ts`

- [ ] **Step 1: Update `index.html` to load Outfit font**

Replace the Inter font link with Outfit. Keep Inter as a fallback loaded alongside Outfit since existing app pages still reference it.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CompassCHW</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&display=swap"
      rel="stylesheet"
    />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

- [ ] **Step 2: Replace design tokens in `index.css`**

Replace the entire `@theme` block and body styles with the new warm palette. Add keyframe animations for the landing page.

```css
@import "tailwindcss";

@theme {
  /* ─── Warm palette ─── */
  --color-primary: #2C3E2D;
  --color-primary-dark: #1E2E1F;
  --color-primary-hover: #3A5240;
  --color-accent: #6B8F71;
  --color-accent-light: rgba(107,143,113,0.1);
  --color-warm-bg: #FBF7F0;
  --color-warm-bg-dark: #F0EBE3;
  --color-warm-bg-darker: #EDE5D8;
  --color-card: #FFFFFF;
  --color-text-primary: #2C3E2D;
  --color-text-secondary: #7A7A6E;
  --color-text-muted: #BBBBAA;
  --color-chw-accent: #D4B896;
  --color-member-accent: #6B8F71;
  --color-border: rgba(44,62,45,0.06);
  --color-danger: #DC2626;
  --color-warning: #F59E0B;
  --color-success: #6B8F71;

  /* ─── Typography ─── */
  --font-sans: 'Outfit', 'Inter', system-ui, -apple-system, sans-serif;

  /* ─── Radii ─── */
  --radius-card: 20px;
  --radius-button: 12px;
  --radius-input: 12px;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

html,
body,
#root {
  height: 100%;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Outfit', 'Inter', system-ui, -apple-system, sans-serif;
  background-color: #FBF7F0;
  color: #2C3E2D;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#root {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* ─── Landing page animations ─── */
@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
```

- [ ] **Step 3: Create `useScrollAnimation` hook**

```typescript
// web/src/features/landing/hooks/useScrollAnimation.ts
import { useEffect, useRef, useState } from 'react';

/**
 * Returns a ref and visibility flag. When the element enters the viewport
 * (15% intersection), `isVisible` flips to true and stays true.
 */
export function useScrollAnimation<T extends HTMLElement = HTMLDivElement>() {
  const ref = useRef<T>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.unobserve(element);
        }
      },
      { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
    );

    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  return { ref, isVisible };
}
```

- [ ] **Step 4: Verify build compiles**

Run: `cd /Users/akrammahmoud/Compass/web && npm run build`
Expected: Build succeeds with no errors.

- [ ] **Step 5: Commit foundation changes**

```bash
cd /Users/akrammahmoud/Compass
git add web/index.html web/src/index.css web/src/features/landing/hooks/useScrollAnimation.ts
git commit -m "feat(landing): add warm palette tokens, Outfit font, and scroll animation hook"
```

---

## Task 2: NavBar Component

**Files:**
- Create: `web/src/features/landing/sections/NavBar.tsx`

- [ ] **Step 1: Create NavBar component**

```tsx
// web/src/features/landing/sections/NavBar.tsx
import { useState, useEffect } from 'react';

const REGISTER_URL = 'https://joincompasschw.com/register';

export function NavBar() {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav
      className="fixed top-0 left-0 right-0 z-100 flex items-center justify-between px-12 py-[18px] backdrop-blur-[16px]"
      style={{
        background: 'rgba(251,247,240,0.85)',
        borderBottom: isScrolled
          ? '1px solid rgba(44,62,45,0.1)'
          : '1px solid rgba(44,62,45,0.06)',
        WebkitBackdropFilter: 'blur(16px)',
      }}
    >
      <div className="text-[20px] font-bold tracking-[-0.03em] text-primary">
        Compass<span className="font-semibold text-accent">CHW</span>
      </div>
      <div className="flex items-center gap-8">
        <a
          href="#verticals"
          className="hidden text-[14px] font-medium text-text-secondary transition-colors hover:text-primary min-[901px]:inline"
        >
          Services
        </a>
        <a
          href="#how"
          className="hidden text-[14px] font-medium text-text-secondary transition-colors hover:text-primary min-[901px]:inline"
        >
          How It Works
        </a>
        <a
          href="#impact"
          className="hidden text-[14px] font-medium text-text-secondary transition-colors hover:text-primary min-[901px]:inline"
        >
          Impact
        </a>
        <a
          href={REGISTER_URL}
          className="rounded-[10px] bg-primary px-[22px] py-[10px] text-[13px] font-semibold text-[#F5EDE0] transition-all hover:-translate-y-px hover:bg-primary-hover"
        >
          Get Started
        </a>
      </div>
    </nav>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add web/src/features/landing/sections/NavBar.tsx
git commit -m "feat(landing): add glass-blur NavBar with anchor links"
```

---

## Task 3: Hero Section

**Files:**
- Create: `web/src/features/landing/sections/HeroSection.tsx`

- [ ] **Step 1: Create HeroSection component**

```tsx
// web/src/features/landing/sections/HeroSection.tsx
const REGISTER_URL = 'https://joincompasschw.com/register';

export function HeroSection() {
  return (
    <section
      className="relative flex min-h-[92vh] items-center overflow-hidden px-6 pt-[120px] pb-16 min-[901px]:px-12 min-[901px]:pt-[140px] min-[901px]:pb-[100px]"
      style={{
        background: 'linear-gradient(165deg, #FBF7F0 0%, #F3EDE4 60%, #EDE5D8 100%)',
      }}
    >
      {/* Decorative radial overlays */}
      <div
        className="pointer-events-none absolute -top-[200px] -right-[100px] h-[600px] w-[600px] rounded-full"
        style={{ background: 'radial-gradient(circle, rgba(107,143,113,0.06) 0%, transparent 65%)' }}
      />
      <div
        className="pointer-events-none absolute -bottom-[150px] -left-[50px] h-[400px] w-[400px] rounded-full"
        style={{ background: 'radial-gradient(circle, rgba(212,184,150,0.08) 0%, transparent 65%)' }}
      />

      <div className="relative z-1 mx-auto grid w-full max-w-[1200px] items-center gap-10 min-[901px]:grid-cols-2 min-[901px]:gap-16">
        {/* Left: Headline */}
        <div className="max-w-[480px]">
          <div className="mb-7 inline-flex items-center gap-2 rounded-full bg-accent-light px-4 py-[7px] text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
            <span className="h-[6px] w-[6px] rounded-full bg-accent" style={{ animation: 'pulse-dot 2s ease-in-out infinite' }} />
            Community Health Workers
          </div>
          <h1 className="mb-5 text-[36px] font-bold leading-[1.06] tracking-[-0.03em] text-primary min-[901px]:text-[52px]">
            Community health,<br />
            <span className="text-accent">connected.</span>
          </h1>
          <p className="mb-9 max-w-[420px] text-[17px] leading-[1.6] text-text-secondary">
            Whether you need help navigating housing, food, or healthcare — or you're a CHW
            ready to serve your neighborhood — Compass is your starting point.
          </p>
          <div className="flex flex-wrap gap-5">
            <TrustItem label="HIPAA Compliant" />
            <TrustItem label="Medi-Cal Certified" />
            <TrustItem label="No Cost to Members" />
          </div>
        </div>

        {/* Right: Path Cards */}
        <div className="flex flex-col gap-4">
          <PathCard
            variant="member"
            icon={'\u{1F64B}'}
            heading="I Need Help"
            description="Find a certified health worker from your neighborhood who speaks your language and knows your community."
            ctaLabel="Get Matched"
            hint="Free with your health plan"
          />
          <PathCard
            variant="chw"
            icon={'\u{1F4BC}'}
            heading="I'm a CHW"
            description="Accept work on your schedule. Bill through Medi-Cal. Grow your member panel at your own pace."
            ctaLabel="Start Earning"
            hint="$22/unit \u00B7 Flexible hours"
          />
        </div>
      </div>
    </section>
  );
}

function TrustItem({ label }: { label: string }) {
  return (
    <div className="flex items-center gap-2 text-[13px] font-medium text-[#999]">
      <div className="flex h-5 w-5 items-center justify-center rounded-full bg-accent-light text-[10px] font-bold text-accent">
        &#10003;
      </div>
      {label}
    </div>
  );
}

function PathCard({
  variant,
  icon,
  heading,
  description,
  ctaLabel,
  hint,
}: {
  variant: 'member' | 'chw';
  icon: string;
  heading: string;
  description: string;
  ctaLabel: string;
  hint: string;
}) {
  const isMember = variant === 'member';
  const accentBar = isMember
    ? 'linear-gradient(90deg, #6B8F71, #8FB896)'
    : 'linear-gradient(90deg, #D4B896, #C4A882)';
  const iconBg = isMember
    ? 'linear-gradient(135deg, #E8F0E9, #D8E8DA)'
    : 'linear-gradient(135deg, #F0EBE3, #E8E0D4)';

  return (
    <a
      href={REGISTER_URL}
      className="group relative block cursor-pointer overflow-hidden rounded-[20px] bg-card p-7 no-underline shadow-[0_4px_24px_rgba(44,62,45,0.05),0_1px_3px_rgba(44,62,45,0.04)] transition-all duration-300 hover:-translate-y-[3px] hover:shadow-[0_12px_40px_rgba(44,62,45,0.08)]"
      style={{ transitionTimingFunction: 'cubic-bezier(0.34, 1.56, 0.64, 1)' }}
    >
      {/* Top accent bar */}
      <div
        className="absolute top-0 right-0 left-0 h-[3px] rounded-t-[20px]"
        style={{ background: accentBar }}
      />

      <div className="mb-4 flex items-start gap-4">
        <div
          className="flex h-12 w-12 shrink-0 items-center justify-center rounded-[14px] text-[22px]"
          style={{ background: iconBg }}
        >
          {icon}
        </div>
        <div>
          <div className="mb-1 text-[22px] font-bold tracking-[-0.02em] text-primary">
            {heading}
          </div>
          <div className="text-[14px] leading-[1.5] text-text-secondary">{description}</div>
        </div>
      </div>
      <div className="flex items-center justify-between">
        {isMember ? (
          <span className="inline-flex items-center gap-2 rounded-[12px] bg-primary px-[26px] py-[13px] text-[14px] font-semibold text-[#F5EDE0] transition-all group-hover:-translate-y-px group-hover:bg-primary-hover">
            {ctaLabel} &rarr;
          </span>
        ) : (
          <span className="inline-flex items-center gap-2 rounded-[12px] border-[1.5px] border-[rgba(44,62,45,0.18)] bg-transparent px-[26px] py-[13px] text-[14px] font-semibold text-primary transition-all group-hover:-translate-y-px group-hover:border-[rgba(44,62,45,0.35)]">
            {ctaLabel} &rarr;
          </span>
        )}
        <span className="text-[12px] text-text-muted">{hint}</span>
      </div>
    </a>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add web/src/features/landing/sections/HeroSection.tsx
git commit -m "feat(landing): add dual-path HeroSection with trust strip"
```

---

## Task 4: Verticals Section

**Files:**
- Create: `web/src/features/landing/sections/VerticalsSection.tsx`

- [ ] **Step 1: Create VerticalsSection component**

```tsx
// web/src/features/landing/sections/VerticalsSection.tsx
import { useScrollAnimation } from '../hooks/useScrollAnimation';

interface Vertical {
  icon: string;
  title: string;
  description: string;
  iconBg: string;
}

const VERTICALS: Vertical[] = [
  {
    icon: '\u{1F3E0}',
    title: 'Housing',
    description: 'Shelter access, rental assistance, eviction prevention, transitional housing',
    iconBg: 'linear-gradient(135deg, #E8D8C4, #DBC8AE)',
  },
  {
    icon: '\u{1F49A}',
    title: 'Rehab & Recovery',
    description: 'Substance use treatment navigation, recovery support, program referrals',
    iconBg: 'linear-gradient(135deg, #D4E4D6, #C0D8C4)',
  },
  {
    icon: '\u{1F34E}',
    title: 'Food & Pantry',
    description: 'SNAP & WIC enrollment, food bank navigation, nutrition programs',
    iconBg: 'linear-gradient(135deg, #F0E4D0, #E8D8BC)',
  },
  {
    icon: '\u{1F9E0}',
    title: 'Mental Health',
    description: 'Therapy referrals, crisis support, counseling navigation, wellness resources',
    iconBg: 'linear-gradient(135deg, #D8E8F0, #C4DCE8)',
  },
  {
    icon: '\u{1F3E5}',
    title: 'Healthcare',
    description: 'Insurance enrollment, preventive care access, specialist referrals',
    iconBg: 'linear-gradient(135deg, #E0E8E0, #D0DCD0)',
  },
];

export function VerticalsSection() {
  const header = useScrollAnimation();

  return (
    <section id="verticals" className="bg-card px-6 py-16 min-[901px]:px-12 min-[901px]:py-[100px]">
      <div className="mx-auto max-w-[1200px]">
        <div
          ref={header.ref}
          className="transition-all duration-700"
          style={{
            opacity: header.isVisible ? 1 : 0,
            transform: header.isVisible ? 'translateY(0)' : 'translateY(24px)',
            transitionTimingFunction: 'cubic-bezier(0.22, 1, 0.36, 1)',
          }}
        >
          <div className="mb-5 inline-flex items-center gap-2 rounded-full bg-accent-light px-4 py-[6px] text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
            5 Service Verticals
          </div>
          <div className="mb-[14px] text-[32px] font-bold leading-[1.1] tracking-[-0.03em] text-primary min-[901px]:text-[40px]">
            Navigate what matters most
          </div>
          <div className="mb-12 max-w-[520px] text-[17px] leading-[1.6] text-text-secondary">
            Our CHWs specialize across the five core social determinants of health — matching
            you with someone who understands exactly what you're going through.
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 min-[901px]:grid-cols-5">
          {VERTICALS.map((v) => (
            <VerticalCard key={v.title} vertical={v} />
          ))}
        </div>
      </div>
    </section>
  );
}

function VerticalCard({ vertical }: { vertical: Vertical }) {
  const anim = useScrollAnimation();

  return (
    <div
      ref={anim.ref}
      className="cursor-default rounded-[20px] bg-warm-bg p-7 text-center transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_12px_32px_rgba(44,62,45,0.06)]"
      style={{
        opacity: anim.isVisible ? 1 : 0,
        transform: anim.isVisible ? 'translateY(0)' : 'translateY(24px)',
        transitionTimingFunction: 'cubic-bezier(0.22, 1, 0.36, 1)',
      }}
    >
      <div
        className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-[16px] text-[26px]"
        style={{ background: vertical.iconBg }}
      >
        {vertical.icon}
      </div>
      <div className="mb-[6px] text-[16px] font-bold tracking-[-0.01em] text-primary">
        {vertical.title}
      </div>
      <div className="text-[13px] leading-[1.5] text-text-secondary">{vertical.description}</div>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add web/src/features/landing/sections/VerticalsSection.tsx
git commit -m "feat(landing): add VerticalsSection with 5 service cards"
```

---

## Task 5: How It Works Section

**Files:**
- Create: `web/src/features/landing/sections/HowItWorksSection.tsx`

- [ ] **Step 1: Create HowItWorksSection component**

```tsx
// web/src/features/landing/sections/HowItWorksSection.tsx
import { useScrollAnimation } from '../hooks/useScrollAnimation';

interface Step {
  number: number;
  title: string;
  description: string;
}

const MEMBER_STEPS: Step[] = [
  {
    number: 1,
    title: 'Tell us what you need',
    description:
      'Select your area of need \u2014 housing, food, rehab, mental health, or healthcare. Share your ZIP and preferred language.',
  },
  {
    number: 2,
    title: 'Get matched with a CHW',
    description:
      "We'll find a certified health worker in your neighborhood who specializes in exactly what you need.",
  },
  {
    number: 3,
    title: 'Start your health journey',
    description:
      'Meet with your CHW, set goals together, and get connected to the right resources. No cost with your Medi-Cal plan.',
  },
];

const CHW_STEPS: Step[] = [
  {
    number: 1,
    title: 'Create your profile',
    description:
      'Upload your CHW certification, set your specializations, availability, service radius, and languages.',
  },
  {
    number: 2,
    title: 'Browse community requests',
    description:
      'See real-time demand in your area. Filter by vertical, urgency, and distance. Accept work that fits your schedule.',
  },
  {
    number: 3,
    title: 'Document & get paid',
    description:
      'Complete sessions, log notes with ICD-10 codes, and bill directly through Medi-Cal at $22 per unit.',
  },
];

export function HowItWorksSection() {
  const header = useScrollAnimation();
  const memberCol = useScrollAnimation();
  const chwCol = useScrollAnimation();

  return (
    <section
      id="how"
      className="px-6 py-16 min-[901px]:px-12 min-[901px]:py-[100px]"
      style={{ background: 'linear-gradient(180deg, #F5EDE0 0%, #FBF7F0 100%)' }}
    >
      <div className="mx-auto max-w-[1200px]">
        <FadeIn anim={header}>
          <div className="mb-5 inline-flex items-center gap-2 rounded-full bg-accent-light px-4 py-[6px] text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
            How It Works
          </div>
          <div className="mb-[14px] text-[32px] font-bold leading-[1.1] tracking-[-0.03em] text-primary min-[901px]:text-[40px]">
            Simple for everyone
          </div>
          <div className="mb-12 max-w-[520px] text-[17px] leading-[1.6] text-text-secondary">
            Two paths, one platform. Whether you need support or you provide it — getting
            started takes minutes.
          </div>
        </FadeIn>

        <div className="grid gap-12 min-[901px]:grid-cols-2 min-[901px]:gap-16">
          <FadeIn anim={memberCol}>
            <StepColumn
              variant="member"
              label="Member"
              heading="Need help?"
              steps={MEMBER_STEPS}
            />
          </FadeIn>
          <FadeIn anim={chwCol}>
            <StepColumn
              variant="chw"
              label="CHW"
              heading="Ready to serve?"
              steps={CHW_STEPS}
            />
          </FadeIn>
        </div>
      </div>
    </section>
  );
}

function FadeIn({
  anim,
  children,
}: {
  anim: { ref: React.RefObject<HTMLDivElement | null>; isVisible: boolean };
  children: React.ReactNode;
}) {
  return (
    <div
      ref={anim.ref}
      className="transition-all duration-700"
      style={{
        opacity: anim.isVisible ? 1 : 0,
        transform: anim.isVisible ? 'translateY(0)' : 'translateY(24px)',
        transitionTimingFunction: 'cubic-bezier(0.22, 1, 0.36, 1)',
      }}
    >
      {children}
    </div>
  );
}

function StepColumn({
  variant,
  label,
  heading,
  steps,
}: {
  variant: 'member' | 'chw';
  label: string;
  heading: string;
  steps: Step[];
}) {
  const isMember = variant === 'member';
  const pillClass = isMember
    ? 'bg-[rgba(107,143,113,0.12)] text-accent'
    : 'bg-[rgba(212,184,150,0.25)] text-[#A08060]';
  const numClass = isMember
    ? 'bg-[rgba(107,143,113,0.1)] text-accent'
    : 'bg-[rgba(212,184,150,0.2)] text-[#A08060]';
  const lineColor = isMember
    ? 'rgba(107,143,113,0.1)'
    : 'rgba(212,184,150,0.2)';

  return (
    <div>
      <h3 className="mb-8 text-[22px] font-bold tracking-[-0.02em] text-primary">
        <span
          className={`mr-[10px] inline-block rounded-[6px] px-3 py-1 align-middle text-[11px] font-semibold uppercase tracking-[0.06em] ${pillClass}`}
        >
          {label}
        </span>
        {heading}
      </h3>
      <div className="flex flex-col gap-7">
        {steps.map((step, i) => (
          <div key={step.number} className="relative flex gap-[18px]">
            {/* Connector line */}
            {i < steps.length - 1 && (
              <div
                className="absolute left-[19px] top-[44px] bottom-[-24px] w-[2px]"
                style={{ background: lineColor }}
              />
            )}
            <div
              className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-[12px] text-[16px] font-bold ${numClass}`}
            >
              {step.number}
            </div>
            <div>
              <div className="mb-1 text-[16px] font-semibold text-primary">{step.title}</div>
              <div className="text-[14px] leading-[1.5] text-text-secondary">
                {step.description}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add web/src/features/landing/sections/HowItWorksSection.tsx
git commit -m "feat(landing): add HowItWorksSection with Member/CHW step flows"
```

---

## Task 6: Impact Stats Section

**Files:**
- Create: `web/src/features/landing/sections/ImpactStatsSection.tsx`

- [ ] **Step 1: Create ImpactStatsSection component**

```tsx
// web/src/features/landing/sections/ImpactStatsSection.tsx
import { useScrollAnimation } from '../hooks/useScrollAnimation';

interface Stat {
  value: string;
  label: string;
}

const STATS: Stat[] = [
  { value: '81%', label: 'Member engagement rate with CHW-led navigation' },
  { value: '5', label: 'Social determinants of health covered' },
  { value: '$22', label: 'Per-unit Medi-Cal reimbursement for CHWs' },
  { value: '$0', label: 'Cost to members with qualifying health plans' },
];

export function ImpactStatsSection() {
  const header = useScrollAnimation();
  const grid = useScrollAnimation();

  return (
    <section id="impact" className="bg-primary px-6 py-16 min-[901px]:px-12 min-[901px]:py-20">
      <div className="mx-auto max-w-[1200px] text-center">
        <div
          ref={header.ref}
          className="transition-all duration-700"
          style={{
            opacity: header.isVisible ? 1 : 0,
            transform: header.isVisible ? 'translateY(0)' : 'translateY(24px)',
            transitionTimingFunction: 'cubic-bezier(0.22, 1, 0.36, 1)',
          }}
        >
          <div className="mb-5 inline-flex items-center gap-2 rounded-full bg-[rgba(255,255,255,0.08)] px-4 py-[6px] text-[11px] font-semibold uppercase tracking-[0.08em] text-[#8FB896]">
            Community Impact
          </div>
          <div className="mb-12 text-[32px] font-bold leading-[1.1] tracking-[-0.03em] text-[#F5EDE0] min-[901px]:text-[40px]">
            Built on real outcomes
          </div>
        </div>

        <div
          ref={grid.ref}
          className="grid grid-cols-2 gap-6 min-[901px]:grid-cols-4"
          style={{
            opacity: grid.isVisible ? 1 : 0,
            transform: grid.isVisible ? 'translateY(0)' : 'translateY(24px)',
            transition: 'opacity 0.7s cubic-bezier(0.22, 1, 0.36, 1), transform 0.7s cubic-bezier(0.22, 1, 0.36, 1)',
          }}
        >
          {STATS.map((stat) => (
            <div
              key={stat.value}
              className="rounded-[20px] border border-[rgba(255,255,255,0.08)] bg-[rgba(255,255,255,0.06)] px-5 py-8 transition-all duration-300 hover:-translate-y-[2px] hover:bg-[rgba(255,255,255,0.09)]"
            >
              <div className="mb-2 text-[42px] font-extrabold leading-none tracking-[-0.03em] text-white">
                {stat.value}
              </div>
              <div className="text-[14px] text-[rgba(255,255,255,0.5)]">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add web/src/features/landing/sections/ImpactStatsSection.tsx
git commit -m "feat(landing): add ImpactStatsSection with 4 metric cards"
```

---

## Task 7: Testimonials Section

**Files:**
- Create: `web/src/features/landing/sections/TestimonialsSection.tsx`

- [ ] **Step 1: Create TestimonialsSection component**

```tsx
// web/src/features/landing/sections/TestimonialsSection.tsx
import { useScrollAnimation } from '../hooks/useScrollAnimation';

interface Testimonial {
  quote: string;
  name: string;
  initials: string;
  location: string;
  role: 'member' | 'chw';
  avatarBg: string;
}

const TESTIMONIALS: Testimonial[] = [
  {
    quote:
      "When I was facing eviction, I didn't know where to turn. My CHW Maria helped me find emergency rental assistance in two days. She spoke my language, she knew my neighborhood \u2014 she felt like family.",
    name: 'Rosa Delgado',
    initials: 'RD',
    location: 'Boyle Heights, Los Angeles',
    role: 'member',
    avatarBg: 'linear-gradient(135deg, #D4B896, #C4A882)',
  },
  {
    quote:
      "I've been a community health worker for seven years, but I was always limited to one organization. Compass lets me serve more people across different needs \u2014 on my own time, and I actually earn more.",
    name: 'Darnell Washington',
    initials: 'DW',
    location: 'South LA, Los Angeles',
    role: 'chw',
    avatarBg: 'linear-gradient(135deg, #8BA5B5, #7090A0)',
  },
  {
    quote:
      "After my husband's accident, I needed help understanding our insurance options and finding a therapist who spoke Arabic. Fatima at Compass guided me through everything step by step.",
    name: 'Nadia Al-Rashid',
    initials: 'NA',
    location: 'Alhambra, Los Angeles',
    role: 'member',
    avatarBg: 'linear-gradient(135deg, #B8A0C8, #A090B8)',
  },
  {
    quote:
      'The billing is seamless \u2014 I document the session, add the ICD-10 codes, and Compass handles the Medi-Cal claim. I used to spend hours on paperwork. Now I spend that time with my members.',
    name: 'Linh Tran Nguyen',
    initials: 'LT',
    location: 'Alhambra, Los Angeles',
    role: 'chw',
    avatarBg: 'linear-gradient(135deg, #A0C4B0, #88B098)',
  },
];

export function TestimonialsSection() {
  const header = useScrollAnimation();
  const grid = useScrollAnimation();

  return (
    <section className="bg-card px-6 py-16 min-[901px]:px-12 min-[901px]:py-[100px]">
      <div className="mx-auto max-w-[1200px]">
        <div
          ref={header.ref}
          className="transition-all duration-700"
          style={{
            opacity: header.isVisible ? 1 : 0,
            transform: header.isVisible ? 'translateY(0)' : 'translateY(24px)',
            transitionTimingFunction: 'cubic-bezier(0.22, 1, 0.36, 1)',
          }}
        >
          <div className="mb-5 inline-flex items-center gap-2 rounded-full bg-accent-light px-4 py-[6px] text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
            Stories
          </div>
          <div className="mb-[14px] text-[32px] font-bold leading-[1.1] tracking-[-0.03em] text-primary min-[901px]:text-[40px]">
            From our community
          </div>
          <div className="mb-12 max-w-[520px] text-[17px] leading-[1.6] text-text-secondary">
            Real people navigating real challenges — with a little help from their neighbors.
          </div>
        </div>

        <div
          ref={grid.ref}
          className="grid gap-6 min-[901px]:grid-cols-2"
          style={{
            opacity: grid.isVisible ? 1 : 0,
            transform: grid.isVisible ? 'translateY(0)' : 'translateY(24px)',
            transition: 'opacity 0.7s cubic-bezier(0.22, 1, 0.36, 1), transform 0.7s cubic-bezier(0.22, 1, 0.36, 1)',
          }}
        >
          {TESTIMONIALS.map((t) => (
            <TestimonialCard key={t.name} testimonial={t} />
          ))}
        </div>
      </div>
    </section>
  );
}

function TestimonialCard({ testimonial }: { testimonial: Testimonial }) {
  const isMember = testimonial.role === 'member';
  const badgeClass = isMember
    ? 'bg-accent-light text-accent'
    : 'bg-[rgba(212,184,150,0.2)] text-[#A08060]';

  return (
    <div className="relative rounded-[20px] bg-warm-bg px-8 py-9">
      {/* Opening quote mark */}
      <div className="absolute top-6 left-7 text-[48px] font-extrabold leading-none text-[rgba(107,143,113,0.15)]">
        &ldquo;
      </div>
      <div className="mb-6 pt-5 text-[16px] leading-[1.65] text-primary">
        {testimonial.quote}
      </div>
      <div className="flex items-center gap-[14px]">
        <div
          className="flex h-11 w-11 shrink-0 items-center justify-center rounded-[14px] text-[15px] font-bold text-white"
          style={{ background: testimonial.avatarBg }}
        >
          {testimonial.initials}
        </div>
        <div>
          <div className="text-[14px] font-semibold text-primary">{testimonial.name}</div>
          <div className="text-[12px] text-[#999]">{testimonial.location}</div>
          <span
            className={`mt-1 inline-block rounded-[6px] px-[10px] py-[3px] text-[10px] font-semibold uppercase tracking-[0.05em] ${badgeClass}`}
          >
            {testimonial.role === 'member' ? 'Member' : 'CHW'}
          </span>
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add web/src/features/landing/sections/TestimonialsSection.tsx
git commit -m "feat(landing): add TestimonialsSection with 4 community stories"
```

---

## Task 8: Final CTA Section

**Files:**
- Create: `web/src/features/landing/sections/FinalCTASection.tsx`

- [ ] **Step 1: Create FinalCTASection component**

```tsx
// web/src/features/landing/sections/FinalCTASection.tsx
import { useScrollAnimation } from '../hooks/useScrollAnimation';

const REGISTER_URL = 'https://joincompasschw.com/register';

export function FinalCTASection() {
  const anim = useScrollAnimation();

  return (
    <section
      className="px-6 py-16 text-center min-[901px]:px-12 min-[901px]:py-[100px]"
      style={{ background: 'linear-gradient(165deg, #F5EDE0 0%, #EDE5D8 100%)' }}
    >
      <div
        ref={anim.ref}
        className="mx-auto max-w-[640px] transition-all duration-700"
        style={{
          opacity: anim.isVisible ? 1 : 0,
          transform: anim.isVisible ? 'translateY(0)' : 'translateY(24px)',
          transitionTimingFunction: 'cubic-bezier(0.22, 1, 0.36, 1)',
        }}
      >
        <div className="mb-5 inline-flex items-center gap-2 rounded-full bg-accent-light px-4 py-[6px] text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
          Get Started
        </div>
        <div className="mb-4 text-[32px] font-bold leading-[1.1] tracking-[-0.03em] text-primary min-[901px]:text-[40px]">
          Your community is waiting
        </div>
        <div className="mx-auto mb-10 max-w-[520px] text-[17px] leading-[1.6] text-text-secondary">
          Whether you need a health navigator or you are one — Compass connects you to the
          people and resources that matter.
        </div>
        <div className="flex justify-center gap-[14px]">
          <a
            href={REGISTER_URL}
            className="inline-flex items-center gap-2 rounded-[14px] bg-primary px-9 py-4 text-[16px] font-semibold text-[#F5EDE0] no-underline transition-all hover:-translate-y-px hover:bg-primary-hover active:translate-y-px"
          >
            I Need Help &rarr;
          </a>
          <a
            href={REGISTER_URL}
            className="inline-flex items-center gap-2 rounded-[14px] border-[1.5px] border-[rgba(44,62,45,0.18)] bg-transparent px-9 py-4 text-[16px] font-semibold text-primary no-underline transition-all hover:-translate-y-px hover:border-[rgba(44,62,45,0.35)] active:translate-y-px"
          >
            I'm a CHW &rarr;
          </a>
        </div>
      </div>
    </section>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add web/src/features/landing/sections/FinalCTASection.tsx
git commit -m "feat(landing): add FinalCTASection with dual CTA buttons"
```

---

## Task 9: Waitlist Section

**Files:**
- Create: `web/src/features/landing/sections/WaitlistSection.tsx`

- [ ] **Step 1: Create WaitlistSection component with form logic**

```tsx
// web/src/features/landing/sections/WaitlistSection.tsx
import { useState, type FormEvent } from 'react';
import { useScrollAnimation } from '../hooks/useScrollAnimation';

export function WaitlistSection() {
  const anim = useScrollAnimation();
  const [submitted, setSubmitted] = useState(false);

  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setSubmitted(true);
  }

  return (
    <section id="waitlist" className="bg-card px-6 py-16 min-[901px]:px-12 min-[901px]:py-[100px]">
      <div
        ref={anim.ref}
        className="mx-auto max-w-[560px] text-center transition-all duration-700"
        style={{
          opacity: anim.isVisible ? 1 : 0,
          transform: anim.isVisible ? 'translateY(0)' : 'translateY(24px)',
          transitionTimingFunction: 'cubic-bezier(0.22, 1, 0.36, 1)',
        }}
      >
        <div className="mb-5 inline-flex items-center gap-2 rounded-full bg-accent-light px-4 py-[6px] text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
          Join the Waitlist
        </div>
        <div className="mb-3 text-[32px] font-bold leading-[1.1] tracking-[-0.03em] text-primary min-[901px]:text-[40px]">
          Be the first to know
        </div>
        <div className="mx-auto mb-10 max-w-[520px] text-[17px] leading-[1.6] text-text-secondary">
          We're launching in Los Angeles soon. Drop your name and email to get early access —
          whether you need help or you're a CHW ready to serve.
        </div>

        {!submitted ? (
          <WaitlistForm onSubmit={handleSubmit} />
        ) : (
          <div className="py-8 text-center">
            <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-accent-light text-[24px] text-accent">
              &#10003;
            </div>
            <h3 className="mb-2 text-[20px] font-bold text-primary">You're on the list</h3>
            <p className="text-[14px] leading-[1.5] text-text-secondary">
              Thanks for joining the Compass community. We'll be in touch when we launch in
              Los Angeles.
            </p>
          </div>
        )}
      </div>
    </section>
  );
}

function WaitlistForm({ onSubmit }: { onSubmit: (e: FormEvent<HTMLFormElement>) => void }) {
  const [roleSelected, setRoleSelected] = useState(false);

  return (
    <form onSubmit={onSubmit} className="flex flex-col gap-[14px]">
      <div className="grid grid-cols-1 gap-[14px] min-[901px]:grid-cols-2">
        <FormField label="First Name" id="firstName" type="text" placeholder="Maria" required />
        <FormField label="Last Name" id="lastName" type="text" placeholder="Reyes" required />
      </div>
      <FormField
        label="Email Address"
        id="email"
        type="email"
        placeholder="maria@example.com"
        required
      />
      <div className="text-left">
        <label htmlFor="role" className="mb-[6px] block text-[13px] font-semibold text-primary">
          I am a...
        </label>
        <select
          id="role"
          required
          onChange={(e) => setRoleSelected(e.target.value !== '')}
          defaultValue=""
          className="w-full cursor-pointer appearance-none rounded-[12px] border-[1.5px] border-[rgba(44,62,45,0.12)] bg-warm-bg px-[18px] py-[14px] text-[15px] outline-none transition-all focus:border-accent focus:shadow-[0_0_0_3px_rgba(107,143,113,0.1)]"
          style={{
            fontFamily: "'Outfit', sans-serif",
            color: roleSelected ? '#2C3E2D' : '#7A7A6E',
            backgroundImage:
              "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1.5L6 6.5L11 1.5' stroke='%237A7A6E' stroke-width='1.5' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E\")",
            backgroundRepeat: 'no-repeat',
            backgroundPosition: 'right 16px center',
            paddingRight: '40px',
          }}
        >
          <option value="" disabled>
            Select one
          </option>
          <option value="member">Community member looking for help</option>
          <option value="chw">Certified Community Health Worker</option>
          <option value="organization">Healthcare organization / partner</option>
          <option value="other">Other / just curious</option>
        </select>
      </div>
      <button
        type="submit"
        className="mt-1 flex w-full items-center justify-center gap-2 rounded-[14px] bg-primary px-8 py-4 text-[16px] font-semibold text-[#F5EDE0] transition-all hover:-translate-y-px hover:bg-primary-hover active:translate-y-px"
        style={{ fontFamily: "'Outfit', sans-serif" }}
      >
        Join the Waitlist &rarr;
      </button>
      <p className="mt-2 text-[12px] leading-[1.5] text-text-muted">
        No spam, ever. We'll only reach out when we're ready to launch in your area.
      </p>
    </form>
  );
}

function FormField({
  label,
  id,
  type,
  placeholder,
  required,
}: {
  label: string;
  id: string;
  type: string;
  placeholder: string;
  required?: boolean;
}) {
  return (
    <div className="text-left">
      <label htmlFor={id} className="mb-[6px] block text-[13px] font-semibold text-primary">
        {label}
      </label>
      <input
        type={type}
        id={id}
        name={id}
        placeholder={placeholder}
        required={required}
        className="w-full rounded-[12px] border-[1.5px] border-[rgba(44,62,45,0.12)] bg-warm-bg px-[18px] py-[14px] text-[15px] text-primary placeholder-text-muted outline-none transition-all focus:border-accent focus:shadow-[0_0_0_3px_rgba(107,143,113,0.1)]"
        style={{ fontFamily: "'Outfit', sans-serif" }}
      />
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add web/src/features/landing/sections/WaitlistSection.tsx
git commit -m "feat(landing): add WaitlistSection with email capture form and success state"
```

---

## Task 10: Footer Section

**Files:**
- Create: `web/src/features/landing/sections/FooterSection.tsx`

- [ ] **Step 1: Create FooterSection component**

```tsx
// web/src/features/landing/sections/FooterSection.tsx
const REGISTER_URL = 'https://joincompasschw.com/register';

interface FooterColumn {
  title: string;
  links: { label: string; href: string }[];
}

const COLUMNS: FooterColumn[] = [
  {
    title: 'Platform',
    links: [
      { label: 'For Members', href: REGISTER_URL },
      { label: 'For CHWs', href: REGISTER_URL },
      { label: 'How It Works', href: '#how' },
      { label: 'Service Areas', href: '#verticals' },
    ],
  },
  {
    title: 'Company',
    links: [
      { label: 'About', href: '#' },
      { label: 'Careers', href: '#' },
      { label: 'Blog', href: '#' },
      { label: 'Contact', href: '#' },
    ],
  },
  {
    title: 'Legal',
    links: [
      { label: 'Privacy Policy', href: '#' },
      { label: 'Terms of Service', href: '#' },
      { label: 'HIPAA Notice', href: '#' },
      { label: 'Accessibility', href: '#' },
    ],
  },
];

export function FooterSection() {
  return (
    <footer className="bg-primary px-6 pt-16 pb-10 min-[901px]:px-12">
      <div className="mx-auto grid max-w-[1200px] grid-cols-1 gap-8 min-[901px]:grid-cols-[2fr_1fr_1fr_1fr] min-[901px]:gap-12">
        {/* Brand column */}
        <div>
          <div className="mb-3 text-[22px] font-bold text-[#F5EDE0]">
            Compass<span className="font-semibold text-[#8FB896]">CHW</span>
          </div>
          <p className="max-w-[280px] text-[14px] leading-[1.6] text-[rgba(255,255,255,0.4)]">
            The first gig-economy marketplace for community health workers. Connecting
            neighborhoods to the care they deserve.
          </p>
        </div>

        {/* Link columns */}
        {COLUMNS.map((col) => (
          <div key={col.title}>
            <h4 className="mb-4 text-[12px] font-semibold uppercase tracking-[0.08em] text-[rgba(255,255,255,0.35)]">
              {col.title}
            </h4>
            {col.links.map((link) => (
              <a
                key={link.label}
                href={link.href}
                className="mb-[10px] block text-[14px] text-[rgba(255,255,255,0.6)] no-underline transition-colors hover:text-[#F5EDE0]"
              >
                {link.label}
              </a>
            ))}
          </div>
        ))}
      </div>

      {/* Bottom bar */}
      <div className="mx-auto mt-10 flex max-w-[1200px] items-center justify-between border-t border-[rgba(255,255,255,0.08)] pt-6 text-[13px] text-[rgba(255,255,255,0.3)]">
        <span>&copy; 2026 CompassCHW. All rights reserved.</span>
        <span>Los Angeles, California</span>
      </div>
    </footer>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add web/src/features/landing/sections/FooterSection.tsx
git commit -m "feat(landing): add FooterSection with links and brand"
```

---

## Task 11: Page Orchestrator and Routing

**Files:**
- Create: `web/src/features/landing/LandingPage.tsx`
- Modify: `web/src/App.tsx`

- [ ] **Step 1: Create LandingPage orchestrator**

```tsx
// web/src/features/landing/LandingPage.tsx
import { NavBar } from './sections/NavBar';
import { HeroSection } from './sections/HeroSection';
import { VerticalsSection } from './sections/VerticalsSection';
import { HowItWorksSection } from './sections/HowItWorksSection';
import { ImpactStatsSection } from './sections/ImpactStatsSection';
import { TestimonialsSection } from './sections/TestimonialsSection';
import { FinalCTASection } from './sections/FinalCTASection';
import { WaitlistSection } from './sections/WaitlistSection';
import { FooterSection } from './sections/FooterSection';

export function LandingPage() {
  return (
    <div className="min-h-[100dvh]">
      <NavBar />
      <HeroSection />
      <VerticalsSection />
      <HowItWorksSection />
      <ImpactStatsSection />
      <TestimonialsSection />
      <FinalCTASection />
      <WaitlistSection />
      <FooterSection />
    </div>
  );
}
```

- [ ] **Step 2: Update App.tsx routing**

In `web/src/App.tsx`, replace the `LandingPageA` import and routes:

**Replace:**
```typescript
import { LandingPageA } from './features/landing/LandingPageA';
```
**With:**
```typescript
import { LandingPage } from './features/landing/LandingPage';
import { LandingPageA } from './features/landing/LandingPageA';
```

**Replace:**
```tsx
{/* Public marketing page */}
<Route path="/landing" element={<LandingPageA />} />
<Route path="/landing/a" element={<LandingPageA />} />
```
**With:**
```tsx
{/* Public marketing page */}
<Route path="/landing" element={<LandingPage />} />
<Route path="/landing/a" element={<LandingPageA />} />
```

This keeps the old LandingPageA accessible at `/landing/a` while the new design becomes the default.

- [ ] **Step 3: Verify build compiles**

Run: `cd /Users/akrammahmoud/Compass/web && npm run build`
Expected: Build succeeds with no TypeScript or bundling errors.

- [ ] **Step 4: Commit**

```bash
git add web/src/features/landing/LandingPage.tsx web/src/App.tsx
git commit -m "feat(landing): wire up new LandingPage as default route"
```

---

## Task 12: Visual Verification and Responsive Polish

**Files:**
- Potentially modify any section component for visual fixes

- [ ] **Step 1: Start dev server and visually verify**

Run: `cd /Users/akrammahmoud/Compass/web && npm run dev`

Open `http://localhost:5173/landing` in the browser. Walk through each section and compare against the approved mockup at `.superpowers/brainstorm/68622-1775542989/content/full-landing.html`.

Checklist:
- [ ] Nav: fixed, blurred glass, logo renders "Compass**CHW**", links hidden on mobile
- [ ] Hero: asymmetric 2-col on desktop, stacked on mobile, eyebrow pulse dot animates
- [ ] Path cards: green accent bar on Member, tan on CHW, hover lift works
- [ ] All CTAs link to `https://joincompasschw.com/register`
- [ ] Verticals: 5-col on desktop, 2-col on mobile, hover lift
- [ ] How It Works: 2-col on desktop, stacked on mobile, connector lines visible
- [ ] Impact: dark green bg, 4-col on desktop, 2-col on mobile
- [ ] Testimonials: 2x2 on desktop, 1-col on mobile, quote marks, role badges
- [ ] Final CTA: dual buttons centered
- [ ] Waitlist: form submits, shows success state
- [ ] Footer: 4-col on desktop, 2-col on mobile, bottom bar
- [ ] Scroll animations: sections fade up on scroll
- [ ] Existing routes work: `/landing/a`, `/landing/b`, `/landing/c`, `/login`, `/register`

- [ ] **Step 2: Fix any visual discrepancies found**

Apply targeted fixes to the relevant section components. Document what was changed.

- [ ] **Step 3: Commit fixes (if any)**

```bash
git add -A
git commit -m "fix(landing): polish responsive layout and visual consistency"
```

---

## Task 13: Production Build and Final Commit

- [ ] **Step 1: Run production build**

Run: `cd /Users/akrammahmoud/Compass/web && npm run build`
Expected: Clean build with no warnings or errors.

- [ ] **Step 2: Run lint**

Run: `cd /Users/akrammahmoud/Compass/web && npm run lint`
Expected: No lint errors.

- [ ] **Step 3: Test production preview**

Run: `cd /Users/akrammahmoud/Compass/web && npm run preview`
Open `http://localhost:4173/landing` — verify the production build renders correctly.

- [ ] **Step 4: Push to main for Vercel auto-deploy**

```bash
cd /Users/akrammahmoud/Compass
git push origin main
```

Vercel auto-deploys on push to `main`. After push, verify deployment at `https://joincompasschw.com`.
