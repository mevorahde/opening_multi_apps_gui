# Security Policy

## Reporting a vulnerability

Please use GitHub's private security-advisory reporting feature for this repository when it is
available. Include a concise description, affected version or commit, reproduction steps, and the
potential impact. Do not include real credentials, private executable paths, configuration files,
or other personal data.

If private reporting is unavailable, open a minimal issue requesting a private contact channel.
Do not publish exploit details or sensitive machine information in a public issue. Maintainers may
need time to reproduce and assess a report; this project does not promise a specific response or
remediation timeline.

## Local configuration

Saved executable paths are local user configuration. The versioned JSON file, legacy `save.txt`,
logs, and any copied path lists must not be committed, attached to issues, or included in release
artifacts. Redact paths before sharing screenshots or diagnostics.

## Operational-log privacy

Application-managed operational logs contain only predefined event classifications and integer
counts. They do not include complete application paths or configuration contents. Logging failures
are nonfatal. This guarantee applies only to logs written by Morning App Launcher; Windows,
security software, launched applications, and CI runners may maintain their own independent logs.

## Remaining operating-system boundary

Morning App Launcher validates that a selected path is an existing file before asking Windows to
open it. The concrete Windows adapter is the only production code that calls `os.startfile`.
Launching still occurs with the current user's permissions and normal Windows file associations.
The project does not sandbox child processes, inspect executable behavior, perform malware
scanning, verify publisher signatures, or bypass Windows security prompts. Users remain
responsible for trusting the files they select.

## Supported versions

Security fixes are applied to the latest code on the maintained branch. Older snapshots and
downloaded workflow artifacts may not receive updates.
