# Production build parts

The full OpenMesha single-file control plane (~535 KB) is stored as **gzip + base64** split into `b64_000.txt` … `b64_007.txt`.

`web/openmesha.html` fetches these parts at runtime, decompresses them in-browser (`DecompressionStream`), and boots the full app.

## Publish / refresh the full single file

```bash
gh auth login   # once
bash scripts/publish-web.sh /path/to/openmesha-production-3.html
```

That replaces `web/openmesha.html` with a true single-file artifact (no parts required).

## Assemble locally from parts

```bash
bash scripts/assemble-web.sh
```
