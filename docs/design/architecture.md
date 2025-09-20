# 1) Make sure you're in the repo root
pwd
# optionally: cd ~/workspaces/FolderFirewall or where your repo is located

# 2) Create the docs/design folder
mkdir -p docs/design

# 3) Create the file with the content (use heredoc)
cat > docs/design/architecture.md << 'EOF'
# FolderFirewall – UI & Architecture Design

## Overview
**FolderFirewall** is a security application designed to disguise itself as a normal folder.  
When opened, it presents a secure interface where users can either:
- Start a **secure cloned environment (sandbox)**, or
- Manage **encrypted files** inside the protected folder.

This document outlines the **UI structure** and **navigation flow**, as defined in the Figma prototype.

---

## UI Structure

### 1. Fake Folder Icon (Landing Screen)
- **Appearance**: Standard folder shape with muted yellow (#FFD966) or gray color.
- **Label**: `"FolderFirewall"` in small text.
- **Behavior**: Clicking opens the **Access Prompt** screen.

---

### 2. Access Prompt Screen
- **Window Size**: ~800×600 px.
- **Header Text**: `"This folder is protected. Choose an option:"`
- **Buttons**:
  - `Start Secure Clone`
  - `Manage Files`
- **Exit Option**: Small button at the bottom → returns to the folder icon.

---

### 3. Secure Clone Environment
- **Layout**: Simulated desktop-style environment.
- **Elements**:
  - Fake file icons (e.g., `doc.txt`, `notes.pdf`).
  - Status bar: `"All actions are isolated here — safe & secure."`
- **Navigation**: Back button (top-left) → returns to Access Prompt.

---

### 4. Manage Files Screen
- **Layout**: Table-based file explorer.
- **Columns**: Filename | Size | Last Modified.
- **Example Rows**:
  - `secret.doc`
  - `image.png`
  - `notes.txt`
- **Navigation**: Back button → returns to Access Prompt.

---

## Navigation Flow
- **Folder Icon → Access Prompt**
- **Access Prompt → Secure Clone** (via "Start Secure Clone")
- **Access Prompt → Manage Files** (via "Manage Files")
- **Access Prompt → Exit → Folder Icon**
- **Back Buttons** → Always return to Access Prompt

---

## Style Guidelines
- **Theme**: Modern, minimal, futuristic security feel.
- **Typography**: Clean sans-serif (e.g., Inter, Roboto).
- **Colors**:
  - Folder: #FFD966 (or gray)
  - Backgrounds: #1E2A38 (dark blue)
  - Success accents: #28A745 (green)
- **Design Principles**:
  - Soft edges, rounded buttons
  - Subtle shadows
  - Consistent spacing

---

## Future Enhancements
- Add **encryption animations** when files are managed.
- Build **real sandboxing logic** (mapped to backend code).
- Optional **login/passphrase screen** before access.
EOF

# 4) Add, commit, and push
git add docs/design/architecture.md
git commit -m "Add UI & architecture design doc"
git push origin main

# 5) Verify locally
ls -la docs/design
cat docs/design/architecture.md
