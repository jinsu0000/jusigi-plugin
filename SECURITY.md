# Security policy

## Reporting

Do not open a public issue containing a credential, account identifier, private portfolio, exploitable live-order path, or sensitive broker response. Use GitHub's private vulnerability reporting feature for this repository when available. If it is unavailable, open a minimal issue asking the maintainer for a private contact channel without including sensitive details.

## Supported version

The latest release on the default branch receives security fixes during the pre-1.0 period.

## Credential exposure

If a token or key was pasted into an editor, chat, issue, log, or commit:

1. Revoke or rotate it at the issuer immediately.
2. Remove it from the working tree and Git history where applicable.
3. Check audit logs and broker activity.
4. Replace it only through GitHub Secrets or an equivalent secret store.

Deleting the visible file alone does not make an exposed credential safe.
