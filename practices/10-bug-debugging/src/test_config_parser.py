import pytest
from config_parser import ConfigParser


class TestConfigParserParse:
    def setup_method(self):
        self.parser = ConfigParser()

    def test_should_parse_number_values_correctly(self):
        config = self.parser.parse({
            "maxRetries": "5",
            "timeout": "10000",
        })
        assert config.max_retries == 5
        assert config.timeout == 10000

    def test_should_parse_string_values_correctly(self):
        config = self.parser.parse({
            "apiUrl": "https://api.production.com",
        })
        assert config.api_url == "https://api.production.com"

    def test_should_use_defaults_for_missing_values(self):
        config = self.parser.parse({})
        assert config.max_retries == 3
        assert config.timeout == 5000
        assert config.api_url == "http://localhost:3000"

    # This test FAILS due to the bool("false") == True bug
    def test_should_parse_false_string_as_boolean_false(self):
        config = self.parser.parse({
            "debug": "false",
            "verbose": "false",
        })
        # BUG: bool("false") returns True because "false" is a non-empty string
        assert config.debug is False
        assert config.verbose is False

    def test_should_parse_true_string_as_boolean_true(self):
        config = self.parser.parse({
            "debug": "true",
            "verbose": "true",
        })
        assert config.debug is True
        assert config.verbose is True

    # This test FAILS due to the same bug in nested features
    def test_should_handle_feature_flags_correctly(self):
        config = self.parser.parse({
            "enableCache": "false",
            "enableLogging": "true",
            "enableMetrics": "false",
        })
        assert config.features.enable_cache is False
        assert config.features.enable_logging is True
        assert config.features.enable_metrics is False

    def test_should_throw_for_invalid_number_values(self):
        with pytest.raises(ValueError, match="Invalid number"):
            self.parser.parse({"maxRetries": "not-a-number"})


class TestConfigParserParseFromString:
    def setup_method(self):
        self.parser = ConfigParser()

    def test_should_parse_key_value_format(self):
        config_string = """
debug=true
maxRetries=5
apiUrl=https://api.example.com
        """
        config = self.parser.parse_from_string(config_string)
        assert config.debug is True
        assert config.max_retries == 5
        assert config.api_url == "https://api.example.com"

    def test_should_skip_comments_and_empty_lines(self):
        config_string = """
# This is a comment
debug=true

# Another comment
maxRetries=5
        """
        config = self.parser.parse_from_string(config_string)
        assert config.debug is True
        assert config.max_retries == 5

    def test_should_throw_for_invalid_format(self):
        with pytest.raises(ValueError, match="Invalid config line"):
            self.parser.parse_from_string("invalidline")
