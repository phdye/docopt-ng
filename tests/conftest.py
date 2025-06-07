import json
import re
if not hasattr(json, "JSONDecodeError"):  # pragma: no cover - old Python
    json.JSONDecodeError = ValueError  # type: ignore
try:
    from pathlib import Path  # type: ignore
except Exception:  # pragma: no cover - old Python
    try:
        from pathlib2 import Path  # type: ignore
    except Exception:
        from docopt._vendor.pathlib import Path
try:
    from unittest import mock  # type: ignore
except Exception:  # pragma: no cover - old Python
    try:
        import mock  # type: ignore
    except Exception:
        from importlib import import_module
        mock = import_module("mock")  # type: ignore

import pytest

import docopt


def pytest_collect_file(file_path, parent):
    if file_path.suffix == ".docopt" and file_path.stem.startswith("test"):
        return DocoptTestFile.from_parent(path=file_path, parent=parent)


def parse_test(raw):
    raw = re.compile("#.*$", re.M).sub("", raw).strip()
    if raw.startswith('"""'):
        raw = raw[3:]

    for i, fixture in enumerate(raw.split('r"""')):
        if i == 0:
            if not fixture.strip() == "":
                raise DocoptTestException(
                    "Unexpected content before first testcase: {}".format(
                        fixture
                    )
                )
            continue

        try:
            doc, _, body = fixture.partition('"""')
            cases = []
            for case in body.split("$")[1:]:
                argv, _, expect = case.strip().partition("\n")
                try:
                    expect = json.loads(expect)
                except json.JSONDecodeError as e:
                    raise DocoptTestException(
                        "The test case JSON is invalid: {!r} - {}.".format(
                            expect,
                            e,
                        )
                    )
                prog, _, argv = argv.strip().partition(" ")
                cases.append((prog, argv, expect))
            if len(cases) == 0:
                raise DocoptTestException(
                    "No test cases follow the doc. Each example must have at "
                    "least one test case starting with '$'"
                )
        except Exception as e:
            raise DocoptTestException(
                "Failed to parse test case {}. {}\n".format(i, e),
                "The test's definition is:\nr\"\"\"{}".format(fixture)
            ) from None
        yield doc, cases


class DocoptTestFile(pytest.File):
    def collect(self):
        raw = self.path.open().read()
        for i, (doc, cases) in enumerate(parse_test(raw), 1):
            name = "{}({})".format(self.path.stem, i)
            for case in cases:
                yield DocoptTestItem.from_parent(
                    name=name, parent=self, doc=doc, case=case
                )


class DocoptTestItem(pytest.Item):
    def __init__(self, name, parent, doc, case):
        super(DocoptTestItem, self).__init__(name, parent)
        self.doc = doc
        self.prog, self.argv, self.expect = case

    def runtest(self):
        try:
            result = docopt.docopt(self.doc, argv=self.argv)
        except docopt.DocoptExit:
            result = "user-error"

        if self.expect != result:
            raise DocoptTestException(self, result)

    def repr_failure(self, excinfo):
        """Called when self.runtest() raises an exception."""
        if isinstance(excinfo.value, DocoptTestException):
            return "\n".join(
                (
                    "usecase execution failed:",
                    self.doc.rstrip(),
                    "$ {} {}".format(self.prog, self.argv),
                    "result> {}".format(json.dumps(excinfo.value.args[1])),
                    "expect> {}".format(json.dumps(self.expect)),
                )
            )
        return super().repr_failure(excinfo)

    def reportinfo(self):
        return self.path, 0, "usecase: {}".format(self.name)


class DocoptTestException(Exception):
    pass


@pytest.fixture(autouse=True)
def override_sys_argv(argv):
    """Patch `sys.argv` with a fixed value during tests.

    A lot of docopt tests call docopt() without specifying argv, which uses
    `sys.argv` by default, so a predictable value for it is necessary.
    """
    with mock.patch("sys.argv", new=argv):
        yield


@pytest.fixture
def argv():
    """The `sys.argv` value seen inside tests."""
    return ["exampleprogram"]
