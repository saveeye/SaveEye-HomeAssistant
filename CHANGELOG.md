# Changelog

All notable changes to this project are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.2] - 2026-08-20

### Fixed
- Clamp `total_increasing` cumulative energy sensors so meter-reported rounding jitter no longer registers as a decrease, which was causing `recorder` to log "state is not strictly increasing" and corrupting Energy dashboard long-term statistics.

## [1.0.1] - 2026-03-16

### Added
- Support for multiple devices per config entry.

## [1.0.0] - 2026-03-16

### Added
- Initial release: MQTT-based SaveEye sensor integration with branding and HACS support.
