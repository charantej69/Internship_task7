# Extension Audit Checklist

1. Open your browser's extensions/add-ons manager:
   - Chrome: chrome://extensions
   - Firefox: about:addons
2. Review each installed extension:
   - Name, publisher, version.
   - Install date (if available).
   - Enabled/disabled status.
   - Permissions requested (access to site data, read/write on all sites, nativeMessaging, etc.)
   - Number and tone of user reviews; recent negative reviews mentioning malicious behavior.
3. Identify suspicious indicators:
   - Unknown publisher or publisher name mismatch.
   - Permission scope is broader than extension's purpose.
   - Recent surge of pop-ups, redirects or CPU/network usage after installation.
   - Extensions installed without your knowledge.
   - Reviews or security reports mentioning data exfiltration, ads injection, or credential theft.
4. Actions:
   - Disable the extension first (non-destructive).
   - Test browser behavior (restart, check performance).
   - If confirmed suspicious, remove/uninstall.
   - Reboot the browser and re-check.
5. Document:
   - Record name, publisher, permissions, why flagged, action taken (disabled/removed), date/time, screenshots if needed.
6. Optional:
   - Reset browser settings or create a fresh profile if multiple extensions were malicious.
   - Change passwords if you suspect credentials were exposed.
