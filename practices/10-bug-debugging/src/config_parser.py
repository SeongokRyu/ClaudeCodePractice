from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class FeatureFlags:
    enable_cache: bool
    enable_logging: bool
    enable_metrics: bool


@dataclass
class AppConfig:
    debug: bool
    verbose: bool
    max_retries: int
    timeout: int
    api_url: str
    features: FeatureFlags


RawConfig = Dict[str, str]


class ConfigParser:
    # BUG: parse_boolean uses truthy check, which means "false" string becomes True
    # because "false" is a non-empty string and thus truthy
    def _parse_boolean(self, value: str) -> bool:
        return bool(value)  # BUG: bool("false") == True

    def _parse_number(self, value: str) -> int:
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Invalid number: {value}")

    def parse(self, raw: RawConfig) -> AppConfig:
        return AppConfig(
            debug=self._parse_boolean(raw.get("debug", "false")),
            verbose=self._parse_boolean(raw.get("verbose", "false")),
            max_retries=self._parse_number(raw.get("maxRetries", "3")),
            timeout=self._parse_number(raw.get("timeout", "5000")),
            api_url=raw.get("apiUrl", "http://localhost:3000"),
            features=FeatureFlags(
                enable_cache=self._parse_boolean(raw.get("enableCache", "true")),
                enable_logging=self._parse_boolean(raw.get("enableLogging", "true")),
                enable_metrics=self._parse_boolean(raw.get("enableMetrics", "false")),
            ),
        )

    def parse_from_string(self, config_string: str) -> AppConfig:
        """Parse from environment-like key=value format."""
        raw: RawConfig = {}
        lines = config_string.split("\n")

        for line in lines:
            trimmed = line.strip()
            if trimmed == "" or trimmed.startswith("#"):
                continue
            eq_index = trimmed.find("=")
            if eq_index == -1:
                raise ValueError(f"Invalid config line: {trimmed}")
            key = trimmed[:eq_index].strip()
            value = trimmed[eq_index + 1:].strip()
            raw[key] = value

        return self.parse(raw)
