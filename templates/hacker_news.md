# Hacker News Post Template

## Style Rules

- Title format: `{prefix}: {Project} {version} – {technical headline}` (prefix from project config, usually "Show HN")
- HN titles have a 80-character limit
- Body: concise, problem-driven, emphasize technical decisions and architecture
- Tone: understated, factual, engineering-focused. No marketing language.
- Do NOT use emojis
- Do NOT use markdown headers in the body (HN doesn't render them)
- Keep the body under 250 words
- End with links on separate lines: SaaS, Install, GitHub

## Structure

```
Title: {prefix}: {Project} {version} – {headline}

Body:

{Project} is {one sentence description}. {What's new in this version.}

{If SaaS: one paragraph about the hosted platform, factual.}

What's new in the SDK:

- {Feature 1} — {one sentence}
- {Feature 2} — {one sentence}
- {Feature 3} — {one sentence}

{One sentence on architecture or technical approach — what makes this interesting to HN.}

{saas_url}
Install: {install_command}
GitHub: {repo_url} ({stars} stars, {license})
```

## Example

See: dingo/docs/posts/v2.1.0_hacker_news.md
