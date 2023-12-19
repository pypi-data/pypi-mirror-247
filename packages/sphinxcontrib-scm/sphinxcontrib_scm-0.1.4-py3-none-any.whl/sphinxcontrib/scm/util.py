from __future__ import annotations

from pathlib import Path
from typing import Any

from docutils.parsers.rst import directives
from git.cmd import Git
from sphinx.config import Config
from sphinx.util import logging

logger = logging.getLogger(f"sphinxcontrib-scm.{__name__}")


class Helper:
    options: dict

    def get_source_info(self, lineno: int | None = None) -> tuple[str, int]:
        raise NotImplementedError

    @property
    def config(self) -> Config:
        raise NotImplementedError

    def get_contributors(self) -> list[str]:
        """Return list of Git contributors for given path using `git shortlog`

        :path: Path of which to get contributors
        :flags: Additional flags passed to `git shortlog`
        """
        docfile_path = Path(self.get_source_info()[0]).resolve()
        docfile_name = docfile_path.name
        docdir_path = docfile_path.parent
        min_commits = self.option_over_conf("min_commits", "scm_contribs_min_commits")

        limit_authors = self.option_over_conf(
            "limit_authors", "scm_contribs_limit_authors"
        )
        if limit_authors is not None and limit_authors < 1:
            logger.warning(
                "List of contributors limited to less than one entry. "
                "Check '(scm_contribs_)limit_authors' option/config value"
            )

        flags: list[str] = []

        contribs_email = directives.choice(
            self.option_over_conf("email", "scm_contribs_email"),
            ("true", "false"),
        )
        flags += ["--email"] if contribs_email == "true" else ["--no-email"]

        contribs_sort = directives.choice(
            self.option_over_conf("sort", "scm_contribs_sort"),
            ("name", "num"),
        )
        flags += ["--numbered"] if contribs_sort == "num" else ["--no-numbered"]

        contribs_type = directives.choice(
            self.option_over_conf("type", "scm_contribs_type"),
            ("author", "committer"),
        )
        flags += ["--committer"] if contribs_type == "committer" else ["--no-committer"]

        git_shortlog_options = [
            "--summary",
            *flags,
            "HEAD",
            "--",
            docfile_name,
        ]

        contributors = []
        git_shortlog = Git(docdir_path).shortlog(*git_shortlog_options)
        git_shortlog_items = git_shortlog.split("\n")
        for item in git_shortlog_items:
            if not item:
                continue
            num, contributor = item.split("\t")
            if int(num) < min_commits:
                continue
            contributors += [contributor]

        return contributors[:limit_authors]

    def option_over_conf(self, option_name: str, config_value: str) -> Any:
        """Return option if option is set, else return config value"""
        # logger.debug("Option '%s': '%s'", option_name, self.options.get(option_name))
        # logger.debug("Config '%s': '%s'", config_value, self.config[config_value])
        if self.options.get(option_name) is not None:
            # logger.debug("-[Option]-> '%s'", self.options.get(option_name))
            return self.options.get(option_name)
        # logger.debug("-[Config]-> '%s'", self.config[config_value])
        return self.config[config_value]
