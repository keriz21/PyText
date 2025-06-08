# PyText

A simple Python tool to convert custom `.pytex` formatted text files into PDF documents with basic styling. This project leverages the `fpdf2` library to generate PDFs, supporting custom fonts, headings, and justified text.

basicly is my latex compiler version with easy install

## Features

- **Custom Markup to PDF**: Converts `.pytex` files, which use a simple markdown-like syntax, into well-formatted PDF documents.
- **Heading Support**: Recognizes `/h1` tags for prominent headings.
- **Add image support**: Recoognizes `/img` tags for add image
- **Text Formatting**: Supports basic paragraph formatting, including justified text if the `multi_cell_justify` method is available in your `fpdf2` setup.
- **Custom Font Integration**: Allows the use of custom TrueType Fonts (`.ttf`) for both regular and bold text, ensuring consistent document aesthetics.
- **Easy to Use**: A straightforward script for generating PDFs from your structured text content.

## Installation

Before running `PyText`, you need to install the `fpdf2` library.

```bash
pip install fpdf2
```
