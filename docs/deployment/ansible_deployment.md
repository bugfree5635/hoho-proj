# Ansible Server Automation Deployment

## Objective

Automate server configuration using Ansible instead of manually executing commands on each server.

The goal is to configure Ubuntu servers automatically:

- Update package repository
- Install Docker
- Enable Docker service
- Configure Docker user permission


---

# Architecture

```

Windows Host

|
|
v

WSL Ubuntu
(Ansible Controller)

|
| SSH key authentication
|
v

Ubuntu Server
(Managed Node)

|
|
v

Docker Environment

```


---

# Project Structure

```

ansible/

├── inventory.ini

└── docker-install.yml

```


---

# Install Ansible

On the Ansible controller:

```bash
sudo apt update

sudo apt install ansible-core
```

Verify:

```bash
ansible --version
```

Example:

```
ansible [core 2.x]
```

---

# Configure SSH Authentication

Generate SSH key:

```bash
ssh-keygen -t ed25519
```

Copy public key to server:

```bash
ssh-copy-id henry@192.168.181.130
```

Test:

```bash
ssh henry@192.168.181.130
```

The server should allow login without password.

---

# Inventory Configuration

File:

```
inventory.ini
```

Example:

```ini
[servers]

ubuntu_vm \
ansible_host=192.168.181.130 \
ansible_user=henry \
ansible_ssh_private_key_file=~/.ssh/id_ed25519
```

Explanation:

| Parameter        | Meaning                |
| ---------------- | ---------------------- |
| ansible_host     | Server IP              |
| ansible_user     | SSH user               |
| private_key_file | SSH authentication key |

---

# Enable Sudo Automation

The playbook requires:

```yaml
become: yes
```

The remote user needs sudo permission.

For lab environment:

```bash
sudo visudo
```

Add:

```
henry ALL=(ALL) NOPASSWD:ALL
```

---

# Docker Installation Playbook

File:

```
docker-install.yml
```

Example:

```yaml
- name: Install Docker

  hosts: servers

  become: yes


  tasks:

    - name: Update apt cache
      apt:
        update_cache: yes


    - name: Install docker packages
      apt:
        name:
          - docker.io
          - docker-compose-v2
        state: present


    - name: Enable docker service
      systemd:
        name: docker
        enabled: yes
        state: started


    - name: Add user to docker group
      user:
        name: "{{ ansible_user }}"
        groups: docker
        append: yes
```

---

# Execute Deployment

Run:

```bash
ansible-playbook \
-i inventory.ini \
docker-install.yml
```

Expected result:

```
PLAY RECAP

ubuntu_vm : 
ok=5
changed=2
failed=0
```

---

# Verify Server

SSH into server:

```bash
ssh henry@192.168.181.130
```

Check Docker:

```bash
docker version
```

Check service:

```bash
systemctl status docker
```

---

# Idempotency Test

Run the playbook again:

```bash
ansible-playbook \
-i inventory.ini \
docker-install.yml
```

Expected:

```
ok
changed=0
failed=0
```

This means the configuration already matches the desired state.

---

# Production Improvements

Future improvements:

* Use Ansible roles
* Store secrets with Ansible Vault
* Add multiple server groups
* Add CI/CD execution
* Add server hardening
* Add firewall configuration
