# OenEye - Catalog (auto)


## iso_root

---
format: xima-interactive-v1
target: README.md
status: ACTIVE [o∞o]
last_sync: 2026-10-01
metrics:
  device: "0:0"
  free_clusters: 103
  eof_chains: 102
  active_links: 819
---
# [o∞o] oeneyeOS Ecosystem

Modular, secure, and kernel-aligned OS environment mapping core assets to Sector 3 (`0x8000`).

## Channels & Status
* **Canary Channel**: Stable (`0x8000`)
* **Dev Channel**: Active (FS Mapped / Device 0:0)
* **Core Brand**: Online `[o∞o]`

## Interactive .xima Capabilities & Metrics
* **FAT77 Cluster Validation**: 103 Free, 102 EOF, 819 Active Links verified via Device 0 simulation.
* **Documentation Pipeline**: Dynamic runtime metadata linking and automated schema validation.

## Roadmap: Socket Tables
* **Socket Mapping**: Inter-process and loopback socket state registry.
* **sslOENEYE Framing**: Length-prefixed TLS framing with SHA256 integrity validation tables.
# test Tue Oct  6 09:34:35 CEST 2026


---

## oeneyeCURL

# oeneyeCURL

A curl wrapper that knows OENEYE OS Project assets by name, so you don't
have to remember Zenodo record IDs or exact filenames.

## Usage

```bash
chmod +x oeneyeCURL.sh

./oeneyeCURL.sh list                 # see what it knows about
./oeneyeCURL.sh logo                 # -> ./oeneye-logo.png
./oeneyeCURL.sh logo /tmp/logo.png   # custom output path
./oeneyeCURL.sh wg-server            # -> ./oeneye-wg-server.zip
./oeneyeCURL.sh distro-logo          # -> ./oeneye-distro-logo.zip
./oeneyeCURL.sh about                # project blurb + citation
./oeneyeCURL.sh cite                 # BibTeX stub
```

## Known assets

| name          | source                                              |
|---------------|------------------------------------------------------|
| `logo`        | canonical oeneye logo PNG (Zenodo record 22973195)   |
| `wg-server`   | `oeneye-wg-server.zip` (Zenodo record 22973347)      |
| `distro-logo` | `oeneye-distro-logo.zip` (Zenodo record 22973347)    |

New assets are added by adding one line to the `ASSETS` associative array
at the top of `oeneyeCURL.sh`:

```bash
[some-name]="https://zenodo.org/records/.../files/....?download=1|default-filename"
```

## Integration

`oeneye-set-distro-logo.sh` auto-detects `oeneyeCURL.sh` if it's sitting in
the same directory and uses it to fetch the default logo; otherwise it
falls back to a plain `curl` call to the same URL. Keep the two scripts
together for that to kick in.

## Citation

```bibtex
@misc{oeneyecurl2026,
  author    = {Ketelhut, Kai Olaf},
  title     = {DIY distro logo (oeneyeCURL asset registry)},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.22973347},
  url       = {https://doi.org/10.5281/zenodo.22973347},
  note      = {Curatorium / OENEYE OS Project. org-curatorium community. CC-BY-4.0}
}
```

# test post commit hook update


---
