"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

sources_list = "/etc/apt/sources.list"
sources_list_d = "/etc/apt/sources.list.d"
testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize("pkg", ["apt-transport-https"])
def test_apt_https_support(host, pkg):
    """Ensure apt has support for repository URLs using HTTPS."""
    assert host.package(pkg).is_installed


def test_source_files_for_http(host):
    """Check if any source list file has any URLs still using HTTP."""
    source_files = []
    if host.file(sources_list).exists:
        source_files += [sources_list]

    source_files += [
        f"{sources_list_d}/{f}" for f in host.file(sources_list_d).listdir()
    ]

    for source_file in source_files:
        file_lines = host.file(source_file).content_string.split(os.linesep)
        sources = [line for line in file_lines if line.startswith("deb")]

        for source in sources:
            source_elements = source.split(" ")
            # The second element of a source entry can optionally be a set of options
            # in the form "[options]".
            repository_url = source_elements[
                1 if not source_elements[1].startswith("[") else 2
            ]
            if host.system_info.distribution == "ubuntu" and (
                "ubuntu.com" in repository_url or "canonical.com" in repository_url
            ):
                # We do not modify the standard repositories on Ubuntu systems
                continue
            assert repository_url.startswith("http://") is False
