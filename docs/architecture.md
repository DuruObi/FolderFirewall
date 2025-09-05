# FolderFirewall Architecture

## Overview
FolderFirewall is a security application disguised as a folder. 
When opened, it asks for access: 
- Start a secure cloned environment (sandbox)
- Or manage files within the protected folder.

Everything done inside the cloned environment remains isolated and secure.

## Modules
- **UI:** Fake folder interface + prompts
- **Backend:** Security logic, sandbox environment
- **Scripts:** Install/setup scripts
- **Docs:** Documentation
- **Tests:** Automated tests


