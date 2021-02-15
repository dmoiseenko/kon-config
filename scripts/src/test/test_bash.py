from src.common.bash import execute_bash_script


def test_execute_bash_script(capfd):
    execute_bash_script(["echo test"])

    captured = capfd.readouterr()
    assert captured.out == "test\n"
