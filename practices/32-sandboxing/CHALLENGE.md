# Challenge: 샌드박싱과 권한 제어

## Step 1: Enable Sandbox Mode

Learn about Claude Code's sandbox capabilities.

Tasks:
1. Understand what sandbox mode provides:
   - Filesystem isolation (restricted to project directory)
   - Network restrictions (limited outbound connections)
   - Process isolation (cannot spawn unrestricted processes)
2. Review the default sandbox configuration
3. Test basic operations in sandbox mode:
   - Can you read files in the project? (Yes)
   - Can you read files outside the project? (No)
   - Can you make network requests? (Restricted)

## Step 2: Configure Permissions

Create a `settings.json` with explicit allow/deny lists.

Permission system:
- `allow`: list of tool patterns that are permitted
- `deny`: list of tool patterns that are blocked (takes precedence over allow)
- Tool patterns: `ToolName(pattern)` for tools with arguments

Example:
```json
{
  "permissions": {
    "allow": [
      "Read",
      "Grep",
      "Glob",
      "Bash(git status)",
      "Bash(git diff*)",
      "Bash(npm test*)"
    ],
    "deny": [
      "Bash(rm *)",
      "Bash(curl *)",
      "Write",
      "Edit"
    ]
  }
}
```

Test by trying:
- Allowed operation: `git status` -- should work
- Denied operation: `rm file.txt` -- should be blocked
- Unspecified operation: behavior depends on configuration

## Step 3: Create Permission Profiles

Build four permission profiles for different use cases.

### Profile 1: Read-Only Review (`readonly-review.json`)
- Allow: Read, Grep, Glob, git diff, git log
- Deny: Edit, Write, Bash (most commands), any destructive operation
- Use case: reviewing code without any risk of modification

### Profile 2: Trusted Developer (`trusted-dev.json`)
- Allow: all standard tools, git operations, npm/node commands
- Deny: system-level commands, network access to non-localhost
- Use case: daily development work with reasonable safety

### Profile 3: CI/CD (`ci-cd.json`)
- Allow: Read, Bash(npm test), Bash(npm run build), Bash(git *)
- Deny: Edit, Write, interactive tools, network tools
- Use case: running in automated pipelines

### Profile 4: Zero Trust (`zero-trust.json`)
- Allow: Read (project files only), Grep, Glob
- Deny: everything else
- Use case: reviewing potentially malicious code

## Step 4: Test Sandbox Boundaries

For each profile, systematically test:

1. **File read access**
   - Can you read project files? (Should be: Yes for all profiles)
   - Can you read `/etc/passwd`? (Should be: No in sandbox)
   - Can you read `~/.ssh/id_rsa`? (Should be: No in sandbox)

2. **File write access**
   - Can you create new files? (Depends on profile)
   - Can you modify existing files? (Depends on profile)
   - Can you delete files? (Should be: No for most profiles)

3. **Command execution**
   - Can you run `git status`? (Depends on profile)
   - Can you run `curl`? (Should be: No for most profiles)
   - Can you run `node -e "..."`? (Depends on profile)

4. **Network access**
   - Can you access localhost APIs? (Depends on profile)
   - Can you access external URLs? (Should be: No for most profiles)

Document results in a table for each profile.

## Step 5: Docker-Based Isolation

Set up Docker for additional OS-level isolation.

Tasks:
1. Create a `Dockerfile` that:
   - Uses a minimal base image (node:alpine)
   - Installs Claude Code CLI
   - Creates a non-root user
   - Sets up a restricted workspace
   - Drops unnecessary capabilities

2. Create a `docker-compose.yml` that:
   - Mounts only the project directory (read-only for review, read-write for dev)
   - Limits memory and CPU
   - Restricts network access
   - Passes API keys via environment variables (not baked into image)

3. Test the Docker setup:
   - Run a code review inside the container
   - Verify filesystem isolation
   - Verify network restrictions

## Step 6: Zero-Trust Configuration

Design a comprehensive zero-trust setup for reviewing untrusted code.

Layers of protection:
1. **Docker container**: OS-level isolation
2. **Sandbox mode**: Claude Code's built-in restrictions
3. **Permission profile**: minimal tool access (read-only)
4. **Hooks**: log all actions, block any write attempts
5. **Network**: no outbound connections

Test scenario:
1. Clone an untrusted repository into the Docker container
2. Run Claude Code with the zero-trust profile
3. Ask Claude to review the code for security issues
4. Verify that Claude can read and analyze but cannot:
   - Modify any files
   - Execute any code from the repository
   - Make network requests
   - Access files outside the mounted directory

## Success Criteria

- [ ] Sandbox mode understood and tested
- [ ] Four permission profiles created with distinct trust levels
- [ ] Each profile tested for correct allow/deny behavior
- [ ] Docker setup working with filesystem and network isolation
- [ ] Zero-trust configuration verified with all protection layers
- [ ] Boundary tests documented with results
