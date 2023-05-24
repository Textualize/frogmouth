# Frogmouth ChangeLog

## [0.6.0] - 2023-05-24

### Added

- Added Codeberg as a recognised forge for the "forge quick view".

### Changed

- Relaxed the required [Textual](https://github.com/Textualize/textual)
  dependency version requirement.

## [0.5.0] - 2023-05-08

### Changed

- Updated to work with [Textual](https://github.com/Textualize/textual) v0.24.0.

### Added

- Added a `changelog` command -- loads the Frogmouth ChangeLog from the
  repository for viewing.
- Added the ability to delete a single item of history from the history
  list. ([#34](https://github.com/Textualize/frogmouth/pull/34))
- Added the ability to clear down the whole of history.
  ([#34](https://github.com/Textualize/frogmouth/pull/34))
- Added toggling the navigation sidebar between left or right dock.
  ([#37](https://github.com/Textualize/frogmouth/pull/37))

### Changed

- Calling any navigation pane is now a toggle operation. If it isn't
  visible, it's made visible; if it's visible, the navigation sidebar is
  closed.

## [0.4.0] - 2023-05-03

### Added

- Added support for using <kbd>j</kbd> and <kbd>k</kbd> to scroll through
  the document.
- Added support for using <kbd>w</kbd> and <kbd>s</kbd> to scroll through the document.
- Added support for <kbd>space</kbd> to scroll through the document.
- Added <kbd>:</kbd> as a keypress for quickly getting to the input bar.
  ([#19](https://github.com/Textualize/frogmouth/pull/19))

### Changed

- Internal changes to the workings of the input dialogs, using the newer
  Textual screen result returning facility.
  ([#23](https://github.com/Textualize/frogmouth/pull/23))

## [0.3.2] - 2023-04-30

- Initial release
