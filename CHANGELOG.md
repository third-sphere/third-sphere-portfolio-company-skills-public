# Changelog

Versions refer to the `portco-skills` plugin as a whole. Bump the version in
**both** `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` — a
version set in one and not the other means installed copies never see the update.
`tests/test_plugin_manifest.py` enforces that they agree.

## 1.0.0

First release as an installable plugin. The seven skills below were already in
this repo; this version packages them for `claude plugin install` and adds
manifest/README consistency checks to CI.

- better-writing
- capstackcompass-public-portco-skill
- founder-update
- pitch-content-guide
- portco-brand-extract
- seed-pitch-kit
- tufte-viz
