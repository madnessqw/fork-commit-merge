# BoTTube Accessibility Audit Report
**For Bounty:** #1618 - Report any accessibility issue in BoTTube UI (1 RTC)
**Status:** READY TO SUBMIT (pending GitHub token permissions)

## Issues Found

### 1. 🔴 CRITICAL: Password Field Not Masked (Login Page)
- **Location:** `/login`
- **Issue:** The password input field uses `type="text"` instead of `type="password"`
- **Impact:** Passwords are visible in plain text as users type, exposing sensitive information
- **WCAG Violation:** Security best practice
- **Fix:** Change `<input type="text">` to `<input type="password">` for the password field

### 2. 🟡 MEDIUM: Missing Form Labels Association (Upload Page)
- **Location:** `/upload`
- **Issue:** File upload buttons "Choose File" lack associated labels for screen readers
- **Impact:** Screen reader users cannot determine which file input is for video vs thumbnail
- **WCAG Violation:** 1.3.1 Info and Relationships
- **Fix:** Add `aria-label` or visible labels: "Video File" and "Thumbnail File"

### 3. 🟡 MEDIUM: API Key Field Lacks Proper Labeling
- **Location:** `/upload`
- **Issue:** The API key textbox has placeholder text but no persistent visible label
- **Impact:** Users may not understand what the field is for once they start typing
- **WCAG Violation:** 3.3.2 Labels or Instructions
- **Fix:** Add a visible `<label>` element associated with the input via `for` attribute

### 4. 🟢 LOW: Menu Button Lacks Descriptive Text
- **Location:** All pages (header)
- **Issue:** The hamburger menu button shows only "☰" with no text label
- **Impact:** Screen readers may not announce the button's purpose clearly
- **WCAG Violation:** 2.4.4 Link Purpose (In Context)
- **Fix:** Add `aria-label="Open navigation menu"` to the button

### 5. 🟢 LOW: Recovery Banner May Disrupt Screen Reader Flow
- **Location:** All pages (top banner)
- **Issue:** The recovery update banner is announced on every page load
- **Impact:** Repetitive announcements for screen reader users
- **WCAG Violation:** 2.2.2 Pause, Stop, Hide
- **Fix:** Add `aria-live="polite"` or allow users to dismiss the banner

## How to Submit This Bounty

When GitHub token permissions are resolved, run:
```bash
gh issue comment 1618 --repo scottcjn/rustchain-bounties --body-file work/bounty-submissions/accessibility-comment.md
```

## Evidence
- Screenshots: Available in browser session logs
- DOM analysis: Completed via accessibility tree inspection
- Pages tested: /, /login, /upload
