# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| v0.1.x | ✅ |
| < v0.1 | ❌ |

## Reporting a Vulnerability

This is a static-client-side application. No data is sent to any server
(except fetching GeoJSON files from user-provided URLs).

**Known risks:**

1. **User-provided URLs**: The custom layer feature fetches GeoJSON from any
   public URL. Users should only load data from trusted sources.
2. **CORS restrictions**: GeoJSON files must be served with permissive CORS
   headers or from the same origin.
3. **No server-side validation**: All validation happens client-side. Do not
   use this tool to process sensitive data.

To report a vulnerability, open a GitHub issue with the "security" label.
