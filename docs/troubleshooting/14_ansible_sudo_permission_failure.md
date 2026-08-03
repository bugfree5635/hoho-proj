# Ansible Sudo Permission Failure

## Problem

Playbook:

```yaml
become: yes
```

Execution:

```bash
ansible-playbook docker-install.yml
```

Error:

```
sudo: interactive authentication is required
```

---

# Cause

Ansible connects successfully:

```
Ansible
   |
SSH
   |
Ubuntu Server
```

but sudo requires password.

Ansible cannot enter interactive passwords.

---

# Solution

Edit sudo configuration:

```bash
sudo visudo
```

Add:

```
henry ALL=(ALL) NOPASSWD:ALL
```

Test:

```bash
sudo whoami
```

Expected:

```
root
```

---

# Alternative

Run:

```bash
ansible-playbook \
-i inventory.ini \
docker-install.yml \
--ask-become-pass
```

---

# Prevention

For production:

Avoid:

```
ALL=(ALL) NOPASSWD:ALL
```

Use limited permissions:

Example:

```
henry ALL=(ALL) NOPASSWD:/usr/bin/systemctl restart docker
```

