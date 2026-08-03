# Ansible SSH Host Key Verification Failure

## Problem

Running:

```bash
ansible -i inventory.ini servers -m ping
```

Error:

```
Failed to connect to the host via ssh:
Host key verification failed
```

---

# Cause

SSH does not trust the remote server yet.

SSH stores trusted hosts:

```
~/.ssh/known_hosts
```

The server fingerprint is missing.

---

# Diagnosis

Try:

```bash
ssh user@server_ip
```

Example:

```bash
ssh henry@192.168.181.130
```

First connection:

```
Are you sure you want to continue connecting?
```

Accept:

```
yes
```

---

# Solution

Add server fingerprint:

```bash
ssh henry@192.168.181.130
```

or:

```bash
ssh-keyscan 192.168.181.130 >> ~/.ssh/known_hosts
```

Test:

```bash
ansible -i inventory.ini servers -m ping
```

Expected:

```
ubuntu_vm | SUCCESS => {
    "ping": "pong"
}
```
