# Ansible SSH Connection Timeout

## Problem

Command:

```bash
ansible -i inventory.ini servers -m ping
```

Error:

```
ssh: connect to host 192.168.x.x port 22:
Connection timed out
```

---

# Cause

Possible reasons:

## 1. Wrong IP

Check server:

```bash
ip addr
```

Update:

```
inventory.ini
```

---

## 2. SSH service stopped

On server:

```bash
systemctl status ssh
```

Start:

```bash
sudo systemctl start ssh
```

---

## 3. Firewall blocking SSH

Check:

```bash
sudo ufw status
```

Allow:

```bash
sudo ufw allow ssh
```

---

## 4. Network isolation

Test:

```bash
ping server_ip
```

Test SSH:

```bash
ssh user@server_ip
```

---

# Verification

After fixing:

```bash
ansible -i inventory.ini servers -m ping
```

Expected:

```
ubuntu_vm | SUCCESS => {
    "ping": "pong"
}
```
