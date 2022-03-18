# Maintainer Notes

These are some notes on common operations only important to package maintainers.

## Versioning

We use `bumpver` to increment all of our version strings. This removes the
common headaches around trying to write the version string once and
simultaneously avoid cyclical imports. It also automates versioning non-Python
sources.

To increment manually:

    bumpver update --set-version="1.1.0"

You can also test first:

    bumpver update --dry --set-version="1.1.0"

And you can even try to leave it to `bumpver` to decide your new version number,
but incrementing only one part of the version:

    bumpver update --patch
