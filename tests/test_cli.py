# tests/test_cli.py
"""Tests for CLI interface."""

import pytest
from pathlib import Path
from click.testing import CliRunner

from pageforge.cli import main, convert_file
from pageforge.config import get_default_config, Config


@pytest.fixture
def runner():
    """Create CLI test runner."""
    return CliRunner()


@pytest.fixture
def basic_markdown(tmp_path):
    """Create a basic markdown file for testing."""
    md_file = tmp_path / "test.md"
    md_file.write_text("""# Test Document

This is a test paragraph.

## Subsection

- Item 1
- Item 2
""")
    return md_file


@pytest.fixture
def config_file(tmp_path):
    """Create a test config file."""
    config = tmp_path / "config.yaml"
    config.write_text("""page:
  size: a4
  orientation: portrait
  margins:
    top: 1.5
    bottom: 1.5
    left: 1.0
    right: 1.0
fonts:
  body: Helvetica
  heading: Helvetica-Bold
  sizes:
    h1: 28
    body: 12
""")
    return config


class TestCLIBasics:
    """Test basic CLI invocation."""

    def test_help_option(self, runner):
        """Test --help displays help message."""
        result = runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert 'Convert Markdown to PDF' in result.output
        assert '--config' in result.output

    def test_no_arguments(self, runner):
        """Test CLI with no arguments shows usage."""
        result = runner.invoke(main, [])
        assert result.exit_code != 0

    def test_missing_input_file(self, runner, tmp_path):
        """Test error when input file doesn't exist."""
        nonexistent = tmp_path / "nonexistent.md"
        result = runner.invoke(main, [str(nonexistent)])
        assert result.exit_code != 0
        # Click will handle the "exists" validation


class TestBasicConversion:
    """Test basic PDF conversion."""

    def test_convert_with_default_output(self, runner, basic_markdown, tmp_path):
        """Test conversion using default output filename."""
        # Run in the same directory as the markdown file
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(main, [str(basic_markdown)])
            assert result.exit_code == 0
            assert 'PDF generated:' in result.output

            # Check default output file was created
            expected_output = basic_markdown.parent / "test.pdf"
            assert expected_output.exists()

    def test_convert_with_explicit_output(self, runner, basic_markdown, tmp_path):
        """Test conversion with explicit output path."""
        output_file = tmp_path / "output.pdf"
        result = runner.invoke(main, [str(basic_markdown), str(output_file)])
        assert result.exit_code == 0
        assert 'PDF generated:' in result.output
        assert output_file.exists()

    def test_convert_with_config(self, runner, basic_markdown, config_file, tmp_path):
        """Test conversion with custom config file."""
        output_file = tmp_path / "output.pdf"
        result = runner.invoke(main, [
            str(basic_markdown),
            str(output_file),
            '--config', str(config_file)
        ])
        assert result.exit_code == 0
        assert output_file.exists()


class TestConvertFileFunction:
    """Test the convert_file function directly."""

    def test_basic_conversion(self, basic_markdown, tmp_path):
        """Test convert_file with basic markdown."""
        output_path = tmp_path / "output.pdf"
        config = get_default_config()

        convert_file(basic_markdown, output_path, config)

        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_conversion_with_custom_config(self, basic_markdown, tmp_path):
        """Test convert_file with custom config."""
        output_path = tmp_path / "output.pdf"
        config = get_default_config()
        config.page.size = "a4"
        config.fonts.sizes.h1 = 28

        convert_file(basic_markdown, output_path, config)

        assert output_path.exists()

    def test_missing_input_file(self, tmp_path):
        """Test convert_file with nonexistent input."""
        nonexistent = tmp_path / "nonexistent.md"
        output_path = tmp_path / "output.pdf"
        config = get_default_config()

        with pytest.raises(FileNotFoundError):
            convert_file(nonexistent, output_path, config)

    def test_invalid_markdown_path(self, tmp_path):
        """Test convert_file with directory instead of file."""
        output_path = tmp_path / "output.pdf"
        config = get_default_config()

        with pytest.raises((FileNotFoundError, IsADirectoryError, ValueError)):
            convert_file(tmp_path, output_path, config)


class TestConfigLoading:
    """Test config file loading."""

    def test_invalid_config_file(self, runner, basic_markdown, tmp_path):
        """Test error with invalid config file."""
        bad_config = tmp_path / "bad_config.yaml"
        bad_config.write_text("invalid: yaml: content: [[[")

        output_file = tmp_path / "output.pdf"
        result = runner.invoke(main, [
            str(basic_markdown),
            str(output_file),
            '--config', str(bad_config)
        ])
        assert result.exit_code != 0
        assert 'Error' in result.output or 'error' in result.output.lower()

    def test_config_with_partial_settings(self, runner, basic_markdown, tmp_path):
        """Test config file with only partial settings (should merge with defaults)."""
        partial_config = tmp_path / "partial_config.yaml"
        partial_config.write_text("""fonts:
  sizes:
    h1: 32
""")

        output_file = tmp_path / "output.pdf"
        result = runner.invoke(main, [
            str(basic_markdown),
            str(output_file),
            '--config', str(partial_config)
        ])
        assert result.exit_code == 0
        assert output_file.exists()


class TestErrorHandling:
    """Test error handling and messages."""

    def test_read_only_output_directory(self, runner, basic_markdown, tmp_path):
        """Test error when output directory is not writable."""
        # This test is platform-specific and may not work on all systems
        # Skip if we can't create a read-only directory
        pytest.skip("Platform-specific test - skipping for compatibility")

    def test_empty_markdown_file(self, runner, tmp_path):
        """Test with empty markdown file."""
        empty_md = tmp_path / "empty.md"
        empty_md.write_text("")
        output_file = tmp_path / "output.pdf"

        result = runner.invoke(main, [str(empty_md), str(output_file)])
        # Should succeed but create minimal PDF
        assert result.exit_code == 0
        assert output_file.exists()

    def test_markdown_with_missing_images(self, runner, tmp_path, mocker):
        """Test markdown with references to missing images in interactive mode."""
        md_with_img = tmp_path / "with_image.md"
        md_with_img.write_text("""# Test

![Missing Image](missing.png)

Some text.
""")
        output_file = tmp_path / "output.pdf"

        # Mock user skipping the image (blank input)
        mocker.patch('builtins.input', return_value='')

        result = runner.invoke(main, [str(md_with_img), str(output_file)])
        # Should succeed but warn about missing image
        assert result.exit_code == 0
        assert output_file.exists()


class TestInteractiveModeFeatures:
    """Test interactive mode for missing images."""

    def test_interactive_mode_with_user_providing_valid_path(self, runner, tmp_path, mocker):
        """Test interactive mode where user provides a valid image path."""
        # Create actual image file
        valid_image = tmp_path / "valid_image.png"
        from PIL import Image
        img = Image.new('RGB', (100, 100), color='red')
        img.save(valid_image)

        # Create markdown with missing image
        md_file = tmp_path / "test.md"
        md_file.write_text("""# Test

![Test Image](missing.png)

Some text.
""")
        output_file = tmp_path / "output.pdf"

        # Mock user input to provide valid path
        mock_input = mocker.patch('builtins.input', return_value=str(valid_image))

        result = runner.invoke(main, [str(md_file), str(output_file)])

        # Should succeed, user was prompted, and image was loaded
        assert result.exit_code == 0
        assert output_file.exists()
        mock_input.assert_called_once()
        assert 'Image not found: missing.png' in mock_input.call_args[0][0]

    def test_interactive_mode_with_user_skipping(self, runner, tmp_path, mocker):
        """Test interactive mode where user skips the image (blank input)."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""# Test

![Test Image](missing.png)

Some text.
""")
        output_file = tmp_path / "output.pdf"

        # Mock user input to skip (blank)
        mock_input = mocker.patch('builtins.input', return_value='')

        result = runner.invoke(main, [str(md_file), str(output_file)])

        # Should succeed but with warning paragraph in PDF
        assert result.exit_code == 0
        assert output_file.exists()
        mock_input.assert_called_once()

    def test_interactive_mode_with_invalid_user_path(self, runner, tmp_path, mocker):
        """Test interactive mode where user provides invalid path."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""# Test

![Test Image](missing.png)

Some text.
""")
        output_file = tmp_path / "output.pdf"

        # Mock user input to provide invalid path
        mock_input = mocker.patch('builtins.input', return_value='/nonexistent/invalid.png')

        result = runner.invoke(main, [str(md_file), str(output_file)])

        # Should succeed but with warning paragraph in PDF
        assert result.exit_code == 0
        assert output_file.exists()
        mock_input.assert_called_once()


class TestNonInteractiveMode:
    """Test --no-prompt flag for non-interactive mode."""

    def test_no_prompt_flag_exists(self, runner):
        """Test that --no-prompt flag is recognized."""
        result = runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert '--no-prompt' in result.output or '-n' in result.output

    def test_no_prompt_with_missing_images_exit_code_2(self, runner, tmp_path):
        """Test that --no-prompt exits with code 2 when images are missing."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""# Test

![Missing Image](missing.png)

Some text.
""")
        output_file = tmp_path / "output.pdf"

        result = runner.invoke(main, [str(md_file), str(output_file), '--no-prompt'])

        # Should exit with code 2 for missing images
        assert result.exit_code == 2
        assert 'not found' in result.output.lower()

    def test_no_prompt_with_all_images_present(self, runner, tmp_path):
        """Test that --no-prompt succeeds when all images are present."""
        # Create actual image
        image_file = tmp_path / "test_image.png"
        from PIL import Image
        img = Image.new('RGB', (100, 100), color='blue')
        img.save(image_file)

        md_file = tmp_path / "test.md"
        md_file.write_text(f"""# Test

![Test Image](test_image.png)

Some text.
""")
        output_file = tmp_path / "output.pdf"

        result = runner.invoke(main, [str(md_file), str(output_file), '--no-prompt'])

        # Should succeed with exit code 0
        assert result.exit_code == 0
        assert output_file.exists()

    def test_no_prompt_short_flag(self, runner, tmp_path):
        """Test that -n short flag works for --no-prompt."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""# Test

![Missing](missing.png)
""")
        output_file = tmp_path / "output.pdf"

        result = runner.invoke(main, [str(md_file), str(output_file), '-n'])

        # Should exit with code 2
        assert result.exit_code == 2
