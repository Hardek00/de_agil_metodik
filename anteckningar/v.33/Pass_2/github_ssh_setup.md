# Setting up SSH Keys for GitHub

Follow these steps to generate, add, and use SSH keys for GitHub access.

---

## 1. Check if an SSH key already exists
```bash
ls -l ~/.ssh
```
Look for files like:
- `id_ed25519` and `id_ed25519.pub`
- or another `*.pub` pair

If you already have a key and it’s connected to GitHub, you can skip to **Step 4**.

---

## 2. Generate a new SSH key
```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -C "your_email@example.com"
```
- Replace `"your_email@example.com"` with the email you use for GitHub.
- Press **Enter** to accept the default location and optionally set a passphrase.

This will create:
- `~/.ssh/id_ed25519` (private key)
- `~/.ssh/id_ed25519.pub` (public key)

---

## 3. Add the public key to GitHub
Display the public key:
```bash
cat ~/.ssh/id_ed25519.pub
```
Copy the output, then:
1. Go to **GitHub** → **Settings** → **SSH and GPG keys**
2. Click **New SSH key**
3. Paste the key and save.

---

## 4. Start the SSH agent and add your key
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

---

## 5. (Optional) Configure SSH for GitHub
Create or edit the SSH config file:
```bash
nano ~/.ssh/config
```
Add:
```
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
  AddKeysToAgent yes
```

---

**Test the connection:**
```bash
ssh -T git@github.com
```
You should see:
```
Hi <username>! You've successfully authenticated, but GitHub does not provide shell access.
```
