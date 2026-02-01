"""Tests for folder_paths.format_output_filename and get_timestamp functions."""

import re
import sys
import os

# Add the ComfyUI root to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import folder_paths


class TestGetTimestamp:
    """Tests for get_timestamp function."""

    def test_returns_string(self):
        """Should return a string."""
        result = folder_paths.get_timestamp()
        assert isinstance(result, str)

    def test_format_matches_expected_pattern(self):
        """Should return format YYYYMMDD-HHMMSS-ffffff."""
        result = folder_paths.get_timestamp()
        # Pattern: 8 digits, hyphen, 6 digits, hyphen, 6 digits
        pattern = r"^\d{8}-\d{6}-\d{6}$"
        assert re.match(pattern, result), f"Timestamp '{result}' does not match expected pattern"

    def test_is_filesystem_safe(self):
        """Should not contain characters that are unsafe for filenames."""
        result = folder_paths.get_timestamp()
        unsafe_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', ' ']
        for char in unsafe_chars:
            assert char not in result, f"Timestamp contains unsafe character: {char}"


class TestFormatOutputFilename:
    """Tests for format_output_filename function."""

    def test_basic_format(self):
        """Should format filename with counter and timestamp."""
        result = folder_paths.format_output_filename("test", 1, "png")
        # Pattern: test_00001_YYYYMMDD-HHMMSS-ffffff_.png
        pattern = r"^test_00001_\d{8}-\d{6}-\d{6}_\.png$"
        assert re.match(pattern, result), f"Filename '{result}' does not match expected pattern"

    def test_counter_padding(self):
        """Should pad counter to 5 digits."""
        result = folder_paths.format_output_filename("test", 42, "png")
        assert "_00042_" in result

    def test_extension_with_leading_dot(self):
        """Should handle extension with leading dot."""
        result = folder_paths.format_output_filename("test", 1, ".png")
        assert result.endswith("_.png")
        assert "..png" not in result

    def test_extension_without_leading_dot(self):
        """Should handle extension without leading dot."""
        result = folder_paths.format_output_filename("test", 1, "webm")
        assert result.endswith("_.webm")

    def test_batch_num_replacement(self):
        """Should replace %batch_num% placeholder."""
        result = folder_paths.format_output_filename("test_%batch_num%", 1, "png", batch_num="3")
        assert "test_3_" in result
        assert "%batch_num%" not in result

    def test_custom_timestamp(self):
        """Should use provided timestamp instead of generating one."""
        custom_ts = "20260101-120000-000000"
        result = folder_paths.format_output_filename("test", 1, "png", timestamp=custom_ts)
        assert custom_ts in result

    def test_different_extensions(self):
        """Should work with various extensions."""
        extensions = ["png", "webp", "webm", "svg", "glb", "safetensors", "latent"]
        for ext in extensions:
            result = folder_paths.format_output_filename("test", 1, ext)
            assert result.endswith(f"_.{ext}")


if __name__ == "__main__":
    # Simple test runner
    import traceback

    test_classes = [TestGetTimestamp, TestFormatOutputFilename]
    passed = 0
    failed = 0

    for test_class in test_classes:
        instance = test_class()
        for method_name in dir(instance):
            if method_name.startswith("test_"):
                try:
                    getattr(instance, method_name)()
                    print(f"✓ {test_class.__name__}.{method_name}")
                    passed += 1
                except AssertionError as e:
                    print(f"✗ {test_class.__name__}.{method_name}: {e}")
                    failed += 1
                except Exception as e:
                    print(f"✗ {test_class.__name__}.{method_name}: {traceback.format_exc()}")
                    failed += 1

    print(f"\n{passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
