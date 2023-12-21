import logging
import os

log = logging.getLogger(__name__)


def files_exist(self):
    """Checks a given pipeline directory for required files.

    Iterates through the pipeline's directory content and checks that specified
    files are either present or absent, as required.

    .. note::
        This test raises an ``AssertionError`` if neither ``nextflow.config`` or ``main.nf`` are found.
        If these files are not found then this cannot be a Nextflow pipeline and something has gone badly wrong.
        All lint tests are stopped immediately with a critical error message.

    Files that *must* be present:

    .. code-block:: bash

        .gitattributes
        .gitignore
        .nf-core.yml
        .editorconfig
        .prettierignore
        .prettierrc.yml
        .github/.dockstore.yml
        .github/CONTRIBUTING.md
        .github/ISSUE_TEMPLATE/bug_report.yml
        .github/ISSUE_TEMPLATE/config.yml
        .github/ISSUE_TEMPLATE/feature_request.yml
        .github/PULL_REQUEST_TEMPLATE.md
        .github/workflows/branch.yml
        .github/workflows/ci.yml
        .github/workflows/linting_comment.yml
        .github/workflows/linting.yml
        [LICENSE, LICENSE.md, LICENCE, LICENCE.md]  # NB: British / American spelling
        assets/email_template.html
        assets/email_template.txt
        assets/nf-core-PIPELINE_logo_light.png
        assets/sendmail_template.txt
        conf/modules.config
        conf/test.config
        conf/test_full.config
        CHANGELOG.md
        CITATIONS.md
        CODE_OF_CONDUCT.md
        docs/images/nf-core-PIPELINE_logo_light.png
        docs/images/nf-core-PIPELINE_logo_dark.png
        docs/output.md
        docs/README.md
        docs/usage.md
        lib/nfcore_external_java_deps.jar
        lib/NfcoreTemplate.groovy
        lib/Utils.groovy
        lib/WorkflowMain.groovy
        nextflow_schema.json
        nextflow.config
        README.md

    Files that *should* be present:

    .. code-block:: bash

        main.nf
        assets/multiqc_config.yml
        conf/base.config
        conf/igenomes.config
        .github/workflows/awstest.yml
        .github/workflows/awsfulltest.yml
        lib/WorkflowPIPELINE.groovy
        pyproject.toml

    Files that *must not* be present, due to being renamed or removed in the template:

    .. code-block:: bash

        Singularity
        parameters.settings.json
        pipeline_template.yml # saving information in .nf-core.yml
        .nf-core.yaml  # NB: Should be yml, not yaml
        bin/markdown_to_html.r
        conf/aws.config
        .github/workflows/push_dockerhub.yml
        .github/ISSUE_TEMPLATE/bug_report.md
        .github/ISSUE_TEMPLATE/feature_request.md
        docs/images/nf-core-PIPELINE_logo.png
        .markdownlint.yml
        .yamllint.yml
        lib/Checks.groovy
        lib/Completion.groovy
        lib/Workflow.groovy

    Files that *should not* be present:

    .. code-block:: bash

        .travis.yml

    .. tip:: You can configure the ``nf-core lint`` tests to ignore any of these checks by setting
            the ``files_exist`` key as follows in your ``.nf-core.yml`` config file. For example:

            .. code-block:: yaml

            lint:
                files_exist:
                    - assets/multiqc_config.yml
    """

    passed = []
    warned = []
    failed = []
    ignored = []

    # NB: Should all be files, not directories
    # List of lists. Passes if any of the files in the sublist are found.
    #: test autodoc
    try:
        _, short_name = self.nf_config["manifest.name"].strip("\"'").split("/")
    except ValueError:
        log.warning("Expected manifest.name to be in the format '<repo>/<pipeline>'. Will assume it is '<pipeline>'.")
        short_name = self.nf_config["manifest.name"].strip("\"'").split("/")

    files_fail = [
        [".gitattributes"],
        [".gitignore"],
        [".nf-core.yml"],
        [".editorconfig"],
        [".prettierignore"],
        [".prettierrc.yml"],
        ["CHANGELOG.md"],
        ["CITATIONS.md"],
        ["CODE_OF_CONDUCT.md"],
        ["CODE_OF_CONDUCT.md"],
        ["LICENSE", "LICENSE.md", "LICENCE", "LICENCE.md"],  # NB: British / American spelling
        ["nextflow_schema.json"],
        ["nextflow.config"],
        ["README.md"],
        [os.path.join(".github", ".dockstore.yml")],
        [os.path.join(".github", "CONTRIBUTING.md")],
        [os.path.join(".github", "ISSUE_TEMPLATE", "bug_report.yml")],
        [os.path.join(".github", "ISSUE_TEMPLATE", "config.yml")],
        [os.path.join(".github", "ISSUE_TEMPLATE", "feature_request.yml")],
        [os.path.join(".github", "PULL_REQUEST_TEMPLATE.md")],
        [os.path.join(".github", "workflows", "branch.yml")],
        [os.path.join(".github", "workflows", "ci.yml")],
        [os.path.join(".github", "workflows", "linting_comment.yml")],
        [os.path.join(".github", "workflows", "linting.yml")],
        [os.path.join("assets", "email_template.html")],
        [os.path.join("assets", "email_template.txt")],
        [os.path.join("assets", "sendmail_template.txt")],
        [os.path.join("assets", f"nf-core-{short_name}_logo_light.png")],
        [os.path.join("conf", "modules.config")],
        [os.path.join("conf", "test.config")],
        [os.path.join("conf", "test_full.config")],
        [os.path.join("docs", "images", f"nf-core-{short_name}_logo_light.png")],
        [os.path.join("docs", "images", f"nf-core-{short_name}_logo_dark.png")],
        [os.path.join("docs", "output.md")],
        [os.path.join("docs", "README.md")],
        [os.path.join("docs", "README.md")],
        [os.path.join("docs", "usage.md")],
        [os.path.join("lib", "nfcore_external_java_deps.jar")],
        [os.path.join("lib", "NfcoreTemplate.groovy")],
        [os.path.join("lib", "Utils.groovy")],
        [os.path.join("lib", "WorkflowMain.groovy")],
    ]

    files_warn = [
        ["main.nf"],
        [os.path.join("assets", "multiqc_config.yml")],
        [os.path.join("conf", "base.config")],
        [os.path.join("conf", "igenomes.config")],
        [os.path.join(".github", "workflows", "awstest.yml")],
        [os.path.join(".github", "workflows", "awsfulltest.yml")],
        [os.path.join("lib", f"Workflow{short_name[0].upper()}{short_name[1:]}.groovy")],
        ["modules.json"],
        ["pyproject.toml"],
    ]

    # List of strings. Fails / warns if any of the strings exist.
    files_fail_ifexists = [
        "Singularity",
        "parameters.settings.json",
        "pipeline_template.yml",  # saving information in .nf-core.yml
        ".nf-core.yaml",  # yml not yaml
        os.path.join("bin", "markdown_to_html.r"),
        os.path.join("conf", "aws.config"),
        os.path.join(".github", "workflows", "push_dockerhub.yml"),
        os.path.join(".github", "ISSUE_TEMPLATE", "bug_report.md"),
        os.path.join(".github", "ISSUE_TEMPLATE", "feature_request.md"),
        os.path.join("docs", "images", f"nf-core-{short_name}_logo.png"),
        ".markdownlint.yml",
        ".yamllint.yml",
        os.path.join("lib", "Checks.groovy"),
        os.path.join("lib", "Completion.groovy"),
        os.path.join("lib", "Workflow.groovy"),
    ]
    files_warn_ifexists = [".travis.yml"]

    # Remove files that should be ignored according to the linting config
    ignore_files = self.lint_config.get("files_exist", [])

    def pf(file_path):
        return os.path.join(self.wf_path, file_path)

    # First - critical files. Check that this is actually a Nextflow pipeline
    if not os.path.isfile(pf("nextflow.config")) and not os.path.isfile(pf("main.nf")):
        failed.append("File not found: nextflow.config or main.nf")
        raise AssertionError("Neither nextflow.config or main.nf found! Is this a Nextflow pipeline?")

    # Files that cause an error if they don't exist
    for files in files_fail:
        if any([f in ignore_files for f in files]):
            continue
        if any([os.path.isfile(pf(f)) for f in files]):
            passed.append(f"File found: {self._wrap_quotes(files)}")
        else:
            failed.append(f"File not found: {self._wrap_quotes(files)}")

    # Files that cause a warning if they don't exist
    for files in files_warn:
        if any([f in ignore_files for f in files]):
            continue
        if any([os.path.isfile(pf(f)) for f in files]):
            passed.append(f"File found: {self._wrap_quotes(files)}")
        else:
            warned.append(f"File not found: {self._wrap_quotes(files)}")

    # Files that cause an error if they exist
    for file in files_fail_ifexists:
        if file in ignore_files:
            continue
        if os.path.isfile(pf(file)):
            failed.append(f"File must be removed: {self._wrap_quotes(file)}")
        else:
            passed.append(f"File not found check: {self._wrap_quotes(file)}")

    # Files that cause a warning if they exist
    for file in files_warn_ifexists:
        if file in ignore_files:
            continue
        if os.path.isfile(pf(file)):
            warned.append(f"File should be removed: {self._wrap_quotes(file)}")
        else:
            passed.append(f"File not found check: {self._wrap_quotes(file)}")

    # Files that are ignoed
    for file in ignore_files:
        ignored.append(f"File is ignored: {self._wrap_quotes(file)}")

    return {"passed": passed, "warned": warned, "failed": failed, "ignored": ignored}
