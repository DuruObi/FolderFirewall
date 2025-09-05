# FolderFirewall 🔒📂

FolderFirewall is a cross-platform security application that disguises itself as a folder.  
When opened, it launches a **cloned, sandboxed system environment** where all activity stays encrypted, isolated, and secure.  

## ✨ Features
- 🗂️ Appears as a normal folder on the desktop
- 🔑 Asks for access before launching
- 🖥️ Creates a **cloned secure system** or opens a saved one
- 🔒 Encrypted overlay filesystem (AES-256)
- 🧹 Option to **save, discard, or snapshot** after each session
- 🌐 Configurable network rules (offline / VPN / Tor / full)
- 📝 Transparent logs for auditing

## 🚀 Roadmap
- [ ] Prototype (Linux) using LUKS + Podman sandbox
- [ ] Electron UI for launching clones
- [ ] Windows VHD + BitLocker integration
- [ ] macOS encrypted DMG + sandbox
- [ ] Export/import encrypted clones
- [ ] CI/CD with GitHub Actions

## 📂 Repository Structure
