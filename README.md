# WP2MD - Wordpress to markdown

A script to convert wordpress HTML to markdown. I use this to convert my posts and pages to markdown for cross-posting to other websites.

Customize it to your needs in order to process custom HTML from your specific wordpress installation (plugins, custom HTML and CSS).

DISCLAIMER: I am terrible at python programming.

## Python version and Dependencies
- Developed and tested with python 3.7
- pip packages:
  - pypandoc
- [Pandoc](https://pandoc.org/) must be installed and available in the path

## Usage

- python wp2md.py <file.html>
- will write out <file.md>
