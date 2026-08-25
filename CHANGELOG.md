# Changelog

Versions refer to the `portco-skills` plugin as a whole. Bump the version in
**both** `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` — a
version set in one and not the other means installed copies never see the update.
`tests/test_plugin_manifest.py` enforces that they agree.

## 1.1.0

Licensing. The repo shipped with no LICENSE, which meant that despite being
public, nobody had a granted right to use it.

- LICENSE: Mozilla Public License 2.0, verbatim from mozilla.org
- NOTICE: copyright line, and an explicit statement that the Third Sphere and
  CapStack Compass marks are not licensed (MPL section 2.3)
- `license: MPL-2.0` declared in both manifests, with a CI check that the
  declaration matches the LICENSE file actually present
- README: a plain-language summary of what the license does and does not allow

Why MPL-2.0 rather than MIT or Apache-2.0: modified skills that get distributed
have to stay open, so improvements remain available to the next founder. The
copyleft is file-level, so a portfolio company can combine these skills with
proprietary work and only the files they change carry the obligation. Internal
use and private forks carry no obligation at all.

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
