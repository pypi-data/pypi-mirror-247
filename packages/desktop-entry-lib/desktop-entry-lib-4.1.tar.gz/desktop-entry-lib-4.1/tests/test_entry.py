import desktop_entry_lib
import pytest_subtests
import pyfakefs
import pathlib
import pytest
import os


def _generate_test_entry() -> desktop_entry_lib.DesktopEntry:
    entry = desktop_entry_lib.DesktopEntry()
    entry.Type = "Application"
    entry.Version = "1.5"
    entry.Name.default_text = "Test"
    entry.Comment.default_text = "Hello"
    entry.Comment.translations["de"] = "Hallo"
    return entry


def test_should_show(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("XDG_CURRENT_DESKTOP", False)

    entry = desktop_entry_lib.DesktopEntry()

    assert entry.should_show() is True

    entry.Hidden = True
    assert entry.should_show() is False

    entry.Hidden = False
    assert entry.should_show() is True

    entry.NotShowIn.append("TestDesktop")
    assert entry.should_show() is True

    monkeypatch.setenv("XDG_CURRENT_DESKTOP", "TestDesktop")
    assert entry.should_show() is False

    entry.NotShowIn.clear()

    entry.OnlyShowIn.append("HelloWorld")
    assert entry.should_show() is False

    monkeypatch.setenv("XDG_CURRENT_DESKTOP", "HelloWorld")
    assert entry.should_show() is True

    entry.Hidden = True
    assert entry.should_show() is False


def test_should_show_in_menu() -> None:
    entry = desktop_entry_lib.DesktopEntry()

    assert entry.should_show_in_menu() is True

    entry.NoDisplay = True
    assert entry.should_show_in_menu() is False

    entry.NoDisplay = False
    assert entry.should_show_in_menu() is True


def test_is_empty() -> None:
    entry = desktop_entry_lib.DesktopEntry()
    assert entry.is_empty() is True
    entry.Name.default_text = "Test"
    assert entry.is_empty() is False


def test_from_string() -> None:
    entry = desktop_entry_lib.DesktopEntry.from_string("[Desktop Entry]\nType=Application\nName=Test\nExec=prog")
    assert entry.Name.default_text == "Test"
    assert entry.Exec == "prog"


def test_invalid_desktop_entry_exception() -> None:
    with pytest.raises(desktop_entry_lib.InvalidDesktopEntry):
        desktop_entry_lib.DesktopEntry.from_string("Hello")


def test_from_file(tmp_path: pathlib.Path) -> None:
    entry = _generate_test_entry()
    entry.write_file(os.path.join(tmp_path, "com.example.App.desktop"))
    assert entry == desktop_entry_lib.DesktopEntry.from_file(os.path.join(tmp_path, "com.example.App.desktop"))


def test_from_id(tmp_path: pathlib.Path) -> None:
    entry = _generate_test_entry()
    os.environ["XDG_DATA_DIRS"] = str(tmp_path)
    entry.write_file(os.path.join(tmp_path, "applications", "com.example.App.desktop"))
    assert entry == desktop_entry_lib.DesktopEntry.from_id("com.example.App")


def test_equals() -> None:
    entry = _generate_test_entry()
    assert entry == entry
    assert not entry == desktop_entry_lib.DesktopEntry()
    assert not entry == 42


def test_get_keywords() -> None:
    entry = _generate_test_entry()
    assert isinstance(entry.get_keywords(), list)
    assert isinstance(desktop_entry_lib.DesktopEntry.get_keywords(), list)


def test_get_working_directory(subtests: pytest_subtests.SubTests) -> None:
    with subtests.test("Path key set"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Path = "/test"
        assert entry.get_working_directory() == "/test"

    with subtests.test("Path key not set"):
        assert desktop_entry_lib.DesktopEntry().get_working_directory() == os.path.expanduser("~")


def test_get_command(subtests: pytest_subtests.SubTests, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    fs.os = pyfakefs.fake_filesystem.OSType.LINUX

    with subtests.test("Exec key not set"):
        assert desktop_entry_lib.DesktopEntry().get_command([], []) == []

    with subtests.test("Single file path"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%f"
        assert entry.get_command(["/hello.txt", "/world.txt"], []) == ["/hello.txt"]

    with subtests.test("Single file url"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%f"
        assert entry.get_command([], ["https://example.com", "file:///hello.txt", "file:///world.txt"]) == ["/hello.txt"]

    with subtests.test("Multiple files path"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%F"
        assert entry.get_command(["/hello.txt", "/world.txt"], []) == ["/hello.txt", "/world.txt"]

    with subtests.test("Multiple files url"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%F"
        assert entry.get_command([], ["https://example.com", "file:///hello.txt", "file:///world.txt"]) == ["/hello.txt", "/world.txt"]

    with subtests.test("Single url path"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%u"
        assert entry.get_command(["/hello.txt", "/world.txt"], []) == ["file:///hello.txt"]

    with subtests.test("Single url url"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%u"
        assert entry.get_command([], ["https://example.com", "file:///hello.txt", "file:///world.txt"]) == ["https://example.com"]

    with subtests.test("Multiple urls path"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%U"
        assert entry.get_command(["/hello.txt", "/world.txt"], []) == ["file:///hello.txt", "file:///world.txt"]

    with subtests.test("Multiple urls url"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%U"
        assert entry.get_command([], ["https://example.com", "file:///hello.txt", "file:///world.txt"]) == ["https://example.com", "file:///hello.txt", "file:///world.txt"]

    with subtests.test("With icon"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Icon = "Testicon"
        entry.Exec = "%i"
        assert entry.get_command([], []) == ["--icon", "Testicon"]

    with subtests.test("Without icon"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%i"
        assert entry.get_command([], []) == []

    with subtests.test("Name"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Name.default_text = "Testname"
        entry.Exec = "%c"
        assert entry.get_command([], []) == ["Testname"]

    with subtests.test("With path"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.file_path = "Testpath"
        entry.Exec = "%k"
        assert entry.get_command([], []) == ["Testpath"]

    with subtests.test("Without path"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%k"
        assert entry.get_command([], []) == [""]
