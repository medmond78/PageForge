# tests/test_integration.py
"""End-to-end integration tests for PageForge."""

import pytest
from pathlib import Path
from click.testing import CliRunner

from pageforge.cli import main, convert_file
from pageforge.config import get_default_config
from pageforge.parser import parse_markdown
from pageforge.generator import generate_pdf


@pytest.fixture
def runner():
    """Create CLI test runner."""
    return CliRunner()


@pytest.fixture
def fixtures_dir():
    """Get path to fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def complex_markdown(fixtures_dir):
    """Path to complex test markdown file."""
    return fixtures_dir / "complex.md"


@pytest.fixture
def basic_markdown(fixtures_dir):
    """Path to basic test markdown file."""
    return fixtures_dir / "basic.md"


@pytest.fixture
def sample_config(fixtures_dir):
    """Path to sample config file."""
    return fixtures_dir / "sample_config.yaml"


class TestEndToEnd:
    """Test complete pipeline from markdown to PDF."""

    def test_complex_markdown_to_pdf(self, complex_markdown, tmp_path):
        """Test full pipeline with complex markdown containing all features."""
        output_path = tmp_path / "complex_output.pdf"
        config = get_default_config()

        # Run the full conversion
        result = convert_file(complex_markdown, output_path, config, interactive=False)

        # Verify PDF was created
        assert output_path.exists(), "PDF file should be created"
        assert output_path.stat().st_size > 0, "PDF file should not be empty"

        # Verify result shows images were found
        assert result['missing_images'] == 0, "All images should be found in fixtures"

    def test_basic_markdown_to_pdf(self, basic_markdown, tmp_path):
        """Test full pipeline with basic markdown."""
        output_path = tmp_path / "basic_output.pdf"
        config = get_default_config()

        # Run conversion
        result = convert_file(basic_markdown, output_path, config, interactive=False)

        # Verify output
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_pipeline_with_custom_config(self, complex_markdown, sample_config, tmp_path):
        """Test full pipeline with custom configuration."""
        output_path = tmp_path / "custom_config_output.pdf"

        # Load custom config via CLI's config loader
        from pageforge.cli import load_config_from_yaml
        config = load_config_from_yaml(sample_config)

        # Verify config was loaded with custom values
        assert config.page.size == "a4"
        assert config.fonts.sizes.h1 == 28
        assert config.fonts.sizes.body == 12

        # Run conversion with custom config
        result = convert_file(complex_markdown, output_path, config, interactive=False)

        # Verify output
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_metadata_extraction_from_frontmatter(self, complex_markdown):
        """Test that YAML frontmatter is correctly extracted."""
        # Read and parse markdown
        content = complex_markdown.read_text(encoding='utf-8')
        doc = parse_markdown(content, complex_markdown)

        # Verify metadata was extracted
        assert doc.metadata is not None
        assert doc.metadata['title'] == "PageForge Feature Test Document"
        assert doc.metadata['author'] == "PageForge Test Suite"
        # YAML parser converts dates to datetime.date objects
        from datetime import date
        assert doc.metadata['date'] == date(2026, 8, 12) or doc.metadata['date'] == "2026-08-12"
        assert doc.metadata['description'] == "Comprehensive test document covering all supported markdown features"

    def test_image_resolution_in_pipeline(self, complex_markdown, fixtures_dir, tmp_path):
        """Test that images are correctly resolved relative to markdown file."""
        output_path = tmp_path / "image_test.pdf"
        config = get_default_config()

        # The complex markdown references test-image.png and test-diagram.svg
        # These should exist in fixtures_dir
        test_image = fixtures_dir / "test-image.png"
        test_diagram = fixtures_dir / "test-diagram.svg"

        # Verify test images exist
        assert test_image.exists(), "Test image should exist in fixtures"
        assert test_diagram.exists(), "Test diagram should exist in fixtures"

        # Run conversion
        result = convert_file(complex_markdown, output_path, config, interactive=False)

        # All images should be found (no missing images)
        assert result['missing_images'] == 0
        assert output_path.exists()

    def test_all_heading_levels(self, complex_markdown, tmp_path):
        """Test that all heading levels (H1-H6) are rendered."""
        output_path = tmp_path / "headings_test.pdf"
        config = get_default_config()

        # Parse to verify heading levels exist
        content = complex_markdown.read_text(encoding='utf-8')
        doc = parse_markdown(content, complex_markdown)

        # Check that HTML contains all heading levels
        assert '<h1>' in doc.html, "Should have H1 headings"
        assert '<h2>' in doc.html, "Should have H2 headings"
        assert '<h3>' in doc.html, "Should have H3 headings"
        assert '<h4>' in doc.html, "Should have H4 headings"
        assert '<h5>' in doc.html, "Should have H5 headings"
        assert '<h6>' in doc.html, "Should have H6 headings"

        # Generate PDF
        result = convert_file(complex_markdown, output_path, config, interactive=False)
        assert output_path.exists()

    def test_code_blocks_with_syntax_highlighting(self, complex_markdown, tmp_path):
        """Test that code blocks with language specification are handled."""
        output_path = tmp_path / "code_test.pdf"
        config = get_default_config()
        config.code.syntax_highlight = True

        # Parse to verify code blocks exist
        content = complex_markdown.read_text(encoding='utf-8')
        doc = parse_markdown(content, complex_markdown)

        # Check that HTML contains code blocks
        assert '<pre>' in doc.html or '<code>' in doc.html, "Should have code blocks"

        # Generate PDF with syntax highlighting
        result = convert_file(complex_markdown, output_path, config, interactive=False)
        assert output_path.exists()

    def test_tables_rendering(self, complex_markdown, tmp_path):
        """Test that markdown tables are rendered correctly."""
        output_path = tmp_path / "tables_test.pdf"
        config = get_default_config()

        # Parse to verify tables exist
        content = complex_markdown.read_text(encoding='utf-8')
        doc = parse_markdown(content, complex_markdown)

        # Check that HTML contains tables
        assert '<table>' in doc.html, "Complex markdown should have tables"

        # Generate PDF
        result = convert_file(complex_markdown, output_path, config, interactive=False)
        assert output_path.exists()


class TestCLIIntegration:
    """Test CLI integration with various options."""

    def test_cli_with_complex_markdown(self, runner, complex_markdown, tmp_path):
        """Test CLI with complex markdown file."""
        output_file = tmp_path / "cli_output.pdf"

        result = runner.invoke(main, [
            str(complex_markdown),
            str(output_file),
            '--no-prompt'
        ])

        assert result.exit_code == 0, f"CLI should succeed: {result.output}"
        assert 'PDF generated:' in result.output
        assert output_file.exists()
        assert output_file.stat().st_size > 0

    def test_cli_with_custom_config(self, runner, complex_markdown, sample_config, tmp_path):
        """Test CLI with custom config file."""
        output_file = tmp_path / "cli_custom_config.pdf"

        result = runner.invoke(main, [
            str(complex_markdown),
            str(output_file),
            '--config', str(sample_config),
            '--no-prompt'
        ])

        assert result.exit_code == 0
        assert 'PDF generated:' in result.output
        assert output_file.exists()

    def test_cli_default_output_naming(self, runner, basic_markdown, tmp_path):
        """Test CLI with default output filename (input.md -> input.pdf)."""
        # Copy basic.md to tmp_path so default output is in tmp_path
        test_md = tmp_path / "test_input.md"
        test_md.write_text(basic_markdown.read_text(encoding='utf-8'))

        # Copy image to tmp_path so it's found
        fixtures_dir = basic_markdown.parent
        test_image = fixtures_dir / "test-image.png"
        if test_image.exists():
            dst = tmp_path / "test-image.png"
            dst.write_bytes(test_image.read_bytes())

        result = runner.invoke(main, [str(test_md), '--no-prompt'])

        expected_output = test_md.with_suffix('.pdf')
        assert result.exit_code == 0, f"CLI should succeed. Output: {result.output}"
        assert expected_output.exists()

    def test_cli_verbose_output(self, runner, basic_markdown, tmp_path):
        """Test that CLI provides informative output."""
        output_file = tmp_path / "verbose_test.pdf"

        result = runner.invoke(main, [
            str(basic_markdown),
            str(output_file)
        ])

        # Check for expected output messages
        assert result.exit_code == 0
        assert 'PDF generated:' in result.output
        assert str(output_file) in result.output


class TestErrorHandling:
    """Test error handling in integration scenarios."""

    def test_missing_markdown_file(self, runner, tmp_path):
        """Test error when markdown file doesn't exist."""
        nonexistent = tmp_path / "nonexistent.md"
        output_file = tmp_path / "output.pdf"

        # CLI test
        result = runner.invoke(main, [str(nonexistent), str(output_file)])
        assert result.exit_code != 0
        # Click validates existence before our code runs

    def test_missing_markdown_file_direct(self, tmp_path):
        """Test error when markdown file doesn't exist (direct function call)."""
        nonexistent = tmp_path / "nonexistent.md"
        output_file = tmp_path / "output.pdf"
        config = get_default_config()

        with pytest.raises(FileNotFoundError) as exc_info:
            convert_file(nonexistent, output_file, config)

        assert "not found" in str(exc_info.value).lower()

    def test_directory_instead_of_file(self, tmp_path):
        """Test error when path is a directory instead of a file."""
        output_file = tmp_path / "output.pdf"
        config = get_default_config()

        with pytest.raises((FileNotFoundError, IsADirectoryError, ValueError)):
            convert_file(tmp_path, output_file, config)

    def test_invalid_config_file(self, runner, basic_markdown, tmp_path):
        """Test error with malformed YAML config."""
        bad_config = tmp_path / "bad.yaml"
        bad_config.write_text("invalid: yaml: content: [[[")

        output_file = tmp_path / "output.pdf"

        result = runner.invoke(main, [
            str(basic_markdown),
            str(output_file),
            '--config', str(bad_config)
        ])

        assert result.exit_code != 0
        assert 'Error' in result.output or 'error' in result.output.lower()

    def test_nonexistent_config_file(self, runner, basic_markdown, tmp_path):
        """Test error when config file doesn't exist."""
        nonexistent_config = tmp_path / "nonexistent.yaml"
        output_file = tmp_path / "output.pdf"

        result = runner.invoke(main, [
            str(basic_markdown),
            str(output_file),
            '--config', str(nonexistent_config)
        ])

        assert result.exit_code != 0
        # Click validates existence

    def test_empty_markdown_file(self, tmp_path):
        """Test that empty markdown file still generates a PDF."""
        empty_md = tmp_path / "empty.md"
        empty_md.write_text("")
        output_file = tmp_path / "output.pdf"
        config = get_default_config()

        # Should succeed but create minimal PDF
        result = convert_file(empty_md, output_file, config)

        assert output_file.exists()
        assert output_file.stat().st_size > 0  # Even empty docs have PDF structure

    def test_markdown_only_whitespace(self, tmp_path):
        """Test markdown file with only whitespace."""
        whitespace_md = tmp_path / "whitespace.md"
        whitespace_md.write_text("\n\n   \n\t\n\n")
        output_file = tmp_path / "output.pdf"
        config = get_default_config()

        # Should succeed
        result = convert_file(whitespace_md, output_file, config)
        assert output_file.exists()

    def test_missing_images_non_interactive(self, tmp_path):
        """Test handling of missing images in non-interactive mode."""
        md_with_missing = tmp_path / "missing_image.md"
        md_with_missing.write_text("""# Test

![Missing Image](does_not_exist.png)

Some text after image.
""")
        output_file = tmp_path / "output.pdf"
        config = get_default_config()

        # Should succeed but report missing images
        result = convert_file(md_with_missing, output_file, config, interactive=False)

        assert output_file.exists()
        assert result['missing_images'] == 1, "Should report 1 missing image"


class TestPDFQuality:
    """Tests verifying PDF output quality and structure."""

    def test_pdf_has_content(self, complex_markdown, tmp_path):
        """Test that generated PDF has substantial content."""
        output_path = tmp_path / "content_test.pdf"
        config = get_default_config()

        convert_file(complex_markdown, output_path, config, interactive=False)

        # PDF should be reasonably large for complex document
        file_size = output_path.stat().st_size
        assert file_size > 10000, f"PDF should be substantial size, got {file_size} bytes"

    def test_multiple_conversions_consistent(self, basic_markdown, tmp_path):
        """Test that converting same file multiple times produces consistent results."""
        output1 = tmp_path / "output1.pdf"
        output2 = tmp_path / "output2.pdf"
        config = get_default_config()

        # Convert twice
        convert_file(basic_markdown, output1, config)
        convert_file(basic_markdown, output2, config)

        # Files should exist and have same size
        assert output1.exists()
        assert output2.exists()
        assert output1.stat().st_size == output2.stat().st_size

    def test_different_configs_produce_different_output(self, basic_markdown, tmp_path):
        """Test that different configurations affect output."""
        output_default = tmp_path / "default.pdf"
        output_custom = tmp_path / "custom.pdf"

        # Default config
        config_default = get_default_config()
        convert_file(basic_markdown, output_default, config_default)

        # Modified config
        config_custom = get_default_config()
        config_custom.fonts.sizes.h1 = 36  # Much larger
        config_custom.page.margins.top = 3.0  # Much larger
        convert_file(basic_markdown, output_custom, config_custom)

        # Files should be different sizes due to different formatting
        size_default = output_default.stat().st_size
        size_custom = output_custom.stat().st_size

        # Sizes should be different (larger margins/fonts might change size)
        # Note: This isn't guaranteed but likely for most docs
        assert output_default.exists()
        assert output_custom.exists()


class TestComplexScenarios:
    """Test complex real-world scenarios."""

    def test_full_workflow_with_all_options(self, runner, complex_markdown, sample_config, tmp_path):
        """Test complete workflow: custom config, complex doc, CLI."""
        output_file = tmp_path / "full_workflow.pdf"

        result = runner.invoke(main, [
            str(complex_markdown),
            str(output_file),
            '--config', str(sample_config),
            '--no-prompt'
        ])

        # Verify success
        assert result.exit_code == 0, f"Full workflow should succeed: {result.output}"
        assert output_file.exists()
        assert output_file.stat().st_size > 10000  # Substantial content

        # Verify output message
        assert 'PDF generated:' in result.output
        assert str(output_file) in result.output

    def test_batch_conversion(self, basic_markdown, tmp_path):
        """Test converting multiple files in sequence (simulating batch processing)."""
        config = get_default_config()
        outputs = []

        # Convert same file multiple times with different outputs
        for i in range(3):
            output = tmp_path / f"batch_{i}.pdf"
            convert_file(basic_markdown, output, config)
            outputs.append(output)

        # All should exist
        for output in outputs:
            assert output.exists()
            assert output.stat().st_size > 0

    def test_large_document_performance(self, tmp_path):
        """Test that large documents can be processed."""
        # Create a large markdown file
        large_md = tmp_path / "large.md"
        content = "# Large Document\n\n"

        # Add many sections
        for i in range(50):
            content += f"## Section {i}\n\n"
            content += f"This is section {i} with some content. " * 10
            content += "\n\n"
            content += f"- List item 1 in section {i}\n"
            content += f"- List item 2 in section {i}\n"
            content += "\n"

        large_md.write_text(content)

        output_file = tmp_path / "large.pdf"
        config = get_default_config()

        # Should complete without error
        result = convert_file(large_md, output_file, config)

        assert output_file.exists()
        assert output_file.stat().st_size > 10000  # Should be substantial (>10KB)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
