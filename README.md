# ansible-role-apt-over-https #

[![GitHub Build Status](https://github.com/cisagov/ansible-role-apt-over-https/workflows/build/badge.svg)](https://github.com/cisagov/ansible-role-apt-over-https/actions)
[![CodeQL](https://github.com/cisagov/ansible-role-apt-over-https/workflows/CodeQL/badge.svg)](https://github.com/cisagov/ansible-role-apt-over-https/actions/workflows/codeql-analysis.yml)

This is an Ansible role to convert any repository entries in [apt](https://wiki.debian.org/Apt)
[SourceList](https://wiki.debian.org/SourcesList) files that use HTTP to
instead use HTTPS.

**Note:** On Ubuntu systems the official repositories are not converted because
the official repositories do not support HTTPS. All official Debian repositories
support HTTPS.

## Requirements ##

None.

## Role Variables ##

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| apt_over_https_apt_source_files | A list of apt source files to modify.  Files that do not exist will be ignored. | `[/etc/apt/sources.list, /etc/apt/sources.list.d/debian.sources]` | No |

## Dependencies ##

None.

## Example Playbook ##

Here's how to use it in a playbook:

```yaml
- hosts: all
  become: true
  become_method: sudo
  tasks:
    - name: Modify any HTTP apt repos to use HTTPS
      ansible.builtin.include_role:
        name: apt_over_https
```

## Contributing ##

We welcome contributions!  Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) for
details.

## License ##

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain
dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.

## Author Information ##

Nicholas McDonnell - <nicholas.mcdonnell@gwe.cisa.dhs.gov>
