import pytest
from unittest.mock import patch, MagicMock

def test_interactive_cli_generate_code_flow():
    inputs = {
        "checkbox": ["python"],
        "select": ["Choose file", "Generate code", "Quit"],
        "text": ["Generate this code"]
    }

    def checkbox_mock(*args, **kwargs):
        m = MagicMock()
        m.ask.return_value = inputs["checkbox"]
        return m

    def select_mock(*args, **kwargs):
        if inputs["select"]:
            val = inputs["select"].pop(0)
        else:
            val = "Quit"
        m = MagicMock()
        m.ask.return_value = val
        return m

    def text_mock(*args, **kwargs):
        val = inputs["text"].pop(0)
        m = MagicMock()
        m.ask.return_value = val
        return m

    with patch("ai_cli.commands.interactive.questionary.checkbox", side_effect=checkbox_mock), \
            patch("ai_cli.commands.interactive.questionary.select", side_effect=select_mock), \
            patch("ai_cli.commands.interactive.questionary.text", side_effect=text_mock), \
            patch("ai_cli.commands.interactive.create_new_file"), \
            patch("ai_cli.commands.interactive.choose_file") as mock_choose_file, \
            patch("ai_cli.commands.interactive.generate.generate") as mock_generate, \
            patch("builtins.print"), \
            patch("sys.exit", side_effect=SystemExit) as mock_exit:


        mock_choose_file.return_value = "/path/to/file.py"

        from ai_cli.commands.interactive import interactive_cli
        with pytest.raises(SystemExit):
            interactive_cli(max_iterations=10)
            print("choose_file call count:", mock_choose_file.call_count)
            print("generate call count:", mock_generate.call_count)
            print("generate call args:", mock_generate.call_args_list)
            print("exit call count:", mock_exit.call_count)

            mock_choose_file.assert_called_once()
            mock_generate.assert_called_once_with(
                file="/path/to/file.py",
                prompt="Generate this code",
                languages=["python"]
            )
            mock_exit.assert_called_once()

        mock_choose_file.assert_called_once()
        mock_generate.assert_called_once_with(file="/path/to/file.py", prompt="Generate this code",
                                              languages=["python"])
        mock_exit.assert_called_once()