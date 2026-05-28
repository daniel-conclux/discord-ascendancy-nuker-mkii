# ASCENDANCY NUKER MKII – TRANSCENDENCE EDITION
Developed by Daniel Conclux of Hyperion Ascendancy

By utilizing this program, you agree to the regulations of the Hyperion Ascendancy. Any violations may result in punishment and disciplinary actions.

------------------------------------------------------------

## OVERVIEW
This document provides structured instructions for the configuration and operation of the Ascendancy Nuker (MKII version). Users are required to input the Guild ID and User ID to initiate execution.
Run interface.py to operate the nuker using an User Interface, run asc_mkii.py to operate the nuker using the terminal, run asc_mkii_command.py to trigger the nuke using a prefix command.

------------------------------------------------------------

## I. VERSION INFORMATION
### 01. MKI - ASCENDING
    - Lower execution speed
    - Supports multiple commands
    - Operates via prefix and slash commands

### 02. MKII - TRANSCENDENCE
    - Execution speed dependent on hardware performance and network bandwidth
    - Operates via a terminal-based commands

### 03. MKIII - ASCENDENCE
    - Execution speed dependent on hardware performance and network bandwidth
    - Supports multiple command interfaces:
        • Prefix commands
        • Slash commands
        • Terminal-based commands

------------------------------------------------------------

## II. CONFIGURATION (config.json)
The configuration file allows customization of operational parameters:

### 01. Webhook_name
    Defines the assigned name for generated webhooks

### 02. Message_spam
    Specifies the message content used during automated messaging

### 03. Token
    Authentication token for the bot

### 04. Channel_name
    Defines names for automated channel creation

### 05. Role_name
    Defines names for automated role creation

### 06. Server_name
    Specifies the target server’s renamed identity

### 07. Ban_kick_reason
    Text used in moderation action logs

### 08. Enable_logo (True / False)
    Enables or disables ASCII logo and enhanced terminal output
    (Recommended to disable on mobile devices)

------------------------------------------------------------

## III. REQUIREMENTS
### Recommended Python Version:
    Python 3.11.9 or lower (due to pygame compatibility constraints)
    Remove any pygame-related line if you wish to utilize newer Python versions

### Required Libraries:
    - discord
    - random
    - time
    - asyncio
    - os
    - json
    - aiohttp
    - pillow
    - pygame
    - io
    - base64
    - threading
    - sys

------------------------------------------------------------

## IV. OPERATING INSTRUCTIONS
### A. Android (Mobile)
    01. Install “Pydroid 3” from the Google Play Store
    02. Open the application and access the Pip package manager
    03. Install required libraries individually
    04. Return to the editor
    05. Open the project directory
    06. Execute the file: asc_mkii.py
    07. Proceed to Section IV.F

### B. iOS (Mobile)
    01. Install “Pythonista” from the App Store
    02. Follow equivalent steps
    03. Proceed to Section IV.F

### C. Windows (Desktop)
    01. Install Python
    02. Open Command Prompt or PowerShell
    03. Install required libraries using: "py -m pip install <library_name>"
    04. Navigate to the nuker directory
    05. Open a terminal in the directory
    06. Execute: "py asc_mkii.py"
    07. Proceed to Section IV.F
    XX. Use Ctrl + C to terminate execution

### D. Linux (Desktop)
    01. Follow equivalent procedures to Windows
    02. Proceed to Section IV.F

### E. Bot Setup
    01. Access Discord Developer Portal
    02. Create a new application
    03. Generate and copy the bot token
    04. Insert token into configuration file
    05. Enable required intents:
        • Presence Intent
        • Server Members Intent
        • Message Content Intent
    06. Generate OAuth2 URL
    07. Assign administrative permissions
    08. Invite bot to server

### F. Execution Procedure
    01. Ensure administrative privileges are available
    02. Verify absence or hierarchy dominance over protection systems (anti-nuke bots)
    03. Add bot to the server
    04. Adjust role hierarchy accordingly (bot's role must be as high as possible)
    05. Disable notifications if necessary
    06. Execute script
    07. Input required identifiers

------------------------------------------------------------

## V. PROCESS STRUCTURE
### Phase 1: Fetching
    - Channel
    - Role
    - Emoji
    - Sticker
    - Member

### Phase 2: Erasure
    - Channel deletion
    - Role deletion
    - Emoji removal
    - Sticker removal
    - Member massban

### Phase 3: Defamation
    - Server identity updates:
        • Change server name
        • Change server icon
        • Change server banner (if available)
        • [REMOVED] Change server traits - Bots cannot use this endpoint
        • Change server descriptions (Require community enabled)
    - [REMOVED] Vanity URL adjustments - Bots cannot use this endpoint

### Phase 4: Reconstruction
    - Administrator role creation (will be assigned to the specified user ID)
        • Custom name
    - Channel generation (100)
        • Custom name & topic
    - Emoji creation (50)
        • Custom image & name

### Phase 5: Saturation
    - Webhook generation
        • Custom avatar & name
    - Server saturation

------------------------------------------------------------
