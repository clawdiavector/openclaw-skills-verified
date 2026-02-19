# OpenClaw Skills - Verified

Curated, reviewed skills safe to install into OpenClaw.

## Install a skill

```bash
bash skill-install/scripts/install.sh <skill-name> <workspace-path>
```

Or list all available skills:

```bash
bash skill-install/scripts/list.sh
```

## Versioning

Each skill has a `manifest.json` with a semver version. Git tags in the format `<skill-name>@<version>` allow installing specific versions.

## Contributing

Submit skills via the [submissions repo](https://github.com/clawdiavector/openclaw-skills-submissions). Skills are reviewed before being added here.
