from __future__ import annotations

from datetime import datetime, timezone

import pytest


def pytest_terminal_summary(
    terminalreporter: pytest.TerminalReporter,
    exitstatus: int,
    config: pytest.Config,
) -> None:
    stats = terminalreporter.stats
    total = sum(len(stats.get(key, [])) for key in ("passed", "failed", "error", "skipped", "xfailed", "xpassed"))
    passed = len(stats.get("passed", []))
    failed = len(stats.get("failed", []))
    errors = len(stats.get("error", []))
    skipped = len(stats.get("skipped", []))
    xfailed = len(stats.get("xfailed", []))
    xpassed = len(stats.get("xpassed", []))

    tr = terminalreporter
    tr.section("Test Summary")
    tr.write_line(f"Total: {total}")
    tr.write_line(f"Passed: {passed}")
    tr.write_line(f"Failed: {failed}")
    tr.write_line(f"Errors: {errors}")
    tr.write_line(f"Skipped: {skipped}")
    tr.write_line(f"XFailed: {xfailed}")
    tr.write_line(f"XPassed: {xpassed}")
    tr.write_line(f"Exit status: {exitstatus}")
    tr.write_line(f"Finished at (UTC): {datetime.now(timezone.utc).isoformat(timespec='seconds')}")

    if failed or errors:
        tr.section("Failed/Error Tests")
        for report in [*stats.get("failed", []), *stats.get("error", [])]:
            tr.write_line(f"- {report.nodeid}")

