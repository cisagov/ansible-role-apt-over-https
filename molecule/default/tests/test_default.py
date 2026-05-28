"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize(
    "sourcelist_file",
    ["/etc/apt/sources.list", "/etc/apt/sources.list.d/debian.sources"],
)
def test_source_list_for_http(host, sourcelist_file):
    """Check if the source list file has any URLs still using HTTP."""
    if host.system_info.distribution in ["debian", "kali", "ubuntu"]:
        target_file = host.file(sourcelist_file)
        if target_file.exists:
            file_lines = target_file.content_string.split(os.linesep)
            sources = [line for line in file_lines if line.startswith("deb")]

            for source in sources:
                source_elements = source.split(" ")
                # The second element of a source entry can optionally be a
                # set of options in the form "[options]".
                repository_url = source_elements[
                    1 if not source_elements[1].startswith("[") else 2
                ]
                if host.system_info.distribution == "ubuntu" and (
                    "ubuntu.com" in repository_url or "canonical.com" in repository_url
                ):
                    # We do not modify the standard repositories on Ubuntu systems
                    continue
                assert repository_url.startswith("http://") is False


def test_apt_update(host):
    """Check if the output of apt update indicates any unexpected HTTP URLs."""
    if host.system_info.distribution in ["debian", "kali", "ubuntu"]:
        cmd = host.run("apt update")
        assert cmd.succeeded
        # Typical output looks like:
        # $ apt update
        # Get:1 http://security.ubuntu.com/ubuntu jammy-security InRelease [110 kB]
        # Get:2 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB]
        # Get:3 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [928 kB]  # noqa: B950
        # Get:4 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [119 kB]
        # <snip>
        # Get:18 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 Packages [49.4 kB]  # noqa: B950
        # Fetched 24.9 MB in 3s (9622 kB/s)
        # Reading packlists... Done
        # Building dependency tree... Done
        # Reading state information... Done
        # 7 packages can be upgraded. Run 'apt list --upgradable' to see them.
        output = cmd.stdout
        sources = [line for line in output if line.startswith("Get:")]
        for source in sources:
            repository_url = source.split(" ")[1]
            if host.system_info.distribution == "ubuntu" and (
                "ubuntu.com" in repository_url or "canonical.com" in repository_url
            ):
                # The standard repositories on Ubuntu systems are
                # HTTP-only
                continue
            assert repository_url.startswith("http://") is False
