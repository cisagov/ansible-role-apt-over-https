"""Module containing the tests for the prerequisites_only scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize("pkg", ["apt-transport-https"])
def test_apt_https_support(host, pkg):
    """Ensure apt has support for repository URLs using HTTPS."""
    if host.system_info.distribution in ["debian", "kali", "ubuntu"]:
        assert host.package(pkg).is_installed


def test_source_list_for_http(host):
    """Ensure the source list file has all URLs using HTTP."""
    if host.system_info.distribution in ["debian", "kali", "ubuntu"]:
        source_file = "/etc/apt/sources.list"
        # As of Debian Bookworm the /etc/apt/sources.list file has
        # moved to /etc/apt/sources.list.d/debian.sources
        if (
            host.system_info.distribution == "debian"
            and host.system_info.codename == "bookworm"
        ):
            source_file = "/etc/apt/sources.list.d/debian.sources"

        file_lines = host.file(source_file).content_string.split(os.linesep)
        sources = [line for line in file_lines if line.startswith("deb")]

        for source in sources:
            source_elements = source.split(" ")
            # The second element of a source entry can optionally be a
            # set of options in the form "[options]".
            repository_url = source_elements[
                1 if not source_elements[1].startswith("[") else 2
            ]
            assert repository_url.startswith("http://")
