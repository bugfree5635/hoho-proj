# VS Code Git Credential Socket Failure

## Problem

When pushing code to GitHub from a VS Code terminal, Git fails with an authentication error:

```text
Missing or invalid credentials.

Error: connect ECONNREFUSED /run/user/1000/vscode-git-xxxxxxxx.sock

remote: No anonymous write access.
fatal: Authentication failed for 'https://github.com/USERNAME/REPOSITORY.git/'
```

The important part is:

```text
ECONNREFUSED /run/user/1000/vscode-git-xxxxxxxx.sock
```

## Cause

Git is trying to use the VS Code Git credential helper:

```text
VS Code
   ↓
Git credential helper
   ↓
vscode-git-xxxx.sock
   ↓
GitHub credentials
```

but the VS Code credential socket is no longer available.

This can happen when:

* VS Code's Git credential process stopped
* the terminal is connected to a remote VM
* VS Code was restarted
* an old credential-helper socket remains in Git configuration
* Git is configured to use VS Code's credential helper while the helper is unavailable

The problem is therefore not necessarily your GitHub account or repository permissions.

## Debug

Check the Git remote:

```bash
git remote -v
```

If it shows:

```text
origin  https://github.com/USERNAME/REPOSITORY.git
```

you are using HTTPS.

Check the configured credential helpers:

```bash
git config --show-origin --get-all credential.helper
```

You may see something similar to:

```text
file:/home/henry/.gitconfig
!f() { ... vscode-git-...sock ... }; f
```

Check your Git configuration:

```bash
git config --list --show-origin | grep credential
```

If you see a VS Code socket path such as:

```text
/run/user/1000/vscode-git-xxxxxxxx.sock
```

Git is attempting to use VS Code's credential service.

## Recommended Solution: Use SSH

For development, SSH is a good way to avoid depending on the VS Code credential socket.

Check whether you already have an SSH key:

```bash
ls -la ~/.ssh
```

If you already have a key such as:

```text
id_ed25519
id_ed25519.pub
```

test GitHub authentication:

```bash
ssh -T git@github.com
```

A successful result looks like:

```text
Hi USERNAME! You've successfully authenticated,
but GitHub does not provide shell access.
```

This confirms that your SSH key is working.

Change the Git remote from HTTPS to SSH:

```bash
git remote set-url origin git@github.com:USERNAME/REPOSITORY.git
```

Verify:

```bash
git remote -v
```

You should now see:

```text
origin  git@github.com:USERNAME/REPOSITORY.git
```

Then push:

```bash
git push origin feature/auth
```

## If You Do Not Have an SSH Key

Generate an ED25519 key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Press Enter to accept the default location:

```text
/home/henry/.ssh/id_ed25519
```

Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

Add the key:

```bash
ssh-add ~/.ssh/id_ed25519
```

Display the public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the entire output and add it to your GitHub account's SSH keys.

Then test:

```bash
ssh -T git@github.com
```

## Verify the Repository Remote

After SSH authentication works:

```bash
git remote -v
```

Expected:

```text
origin  git@github.com:USERNAME/REPOSITORY.git (fetch)
origin  git@github.com:USERNAME/REPOSITORY.git (push)
```

Then:

```bash
git push origin feature/auth
```

## Alternative: Keep Using HTTPS

If you specifically want HTTPS, you can remove the broken VS Code credential helper and configure another Git credential manager.

First inspect the current configuration:

```bash
git config --show-origin --get-all credential.helper
```

Be careful when changing credential configuration because credentials may be stored differently depending on the credential manager.

After fixing it, test:

```bash
git push origin feature/auth
```

Git should ask for credentials or use the configured credential manager rather than trying to connect to:

```text
/run/user/1000/vscode-git-*.sock
```

## Important: GitHub Password Is Not Your HTTPS Credential

GitHub does not accept your normal GitHub account password for Git operations over HTTPS.

HTTPS authentication normally uses a Personal Access Token (PAT) or a credential manager.

SSH avoids this workflow entirely:

```text
HTTPS:

Git
 ↓
Credential Manager
 ↓
GitHub token
 ↓
GitHub


SSH:

Git
 ↓
SSH private key
 ↓
GitHub
```

## Verify SSH Directly

Before debugging Git itself, test the SSH connection:

```bash
ssh -T git@github.com
```

If this succeeds:

```text
Hi USERNAME! You've successfully authenticated,
but GitHub does not provide shell access.
```

then GitHub authentication through SSH is working.

If:

```bash
git push
```

still fails, check the remote:

```bash
git remote -v
```

If it still starts with:

```text
https://github.com/
```

Git is still using HTTPS.

Change it:

```bash
git remote set-url origin git@github.com:USERNAME/REPOSITORY.git
```

## Lesson

The error:

```text
ECONNREFUSED /run/user/1000/vscode-git-*.sock
```

does not mean:

> GitHub rejected your SSH key.

It means Git attempted to communicate with a local VS Code credential service and that service was unavailable.

The troubleshooting chain is:

```text
git push
   ↓
Authentication failure?
   ↓
Check remote
   ↓
HTTPS or SSH?
   ↓
HTTPS
   ↓
Check credential helper

OR

SSH
   ↓
ssh -T git@github.com
   ↓
Check SSH key / GitHub authentication
```

The key lesson is:

> **Separate Git transport from authentication. First determine whether your remote uses HTTPS or SSH, then debug the authentication mechanism for that transport.**
