# Jarvis-Lang

A simple interpreted programming language with Indonesian-language syntax, built from scratch in Python — lexer, parser, and interpreter included.

## Why

Built as a learning project to understand how programming languages actually work under the hood: tokenizing raw text, parsing it into an abstract syntax tree (AST), and interpreting that tree to produce results.

## Features

- Variables (`buat`)
- Print statements (`tulis`)
- Conditionals (`kalo ... maka ... selesai`)
- Loops (`ulang ... kali ... selesai`)
- Functions with parameters and return values (`fungsi ... kembalikan ... selesai`)
- Local variable scope per function call
- Arithmetic and comparison operators: `+ - * / > < >= <= == !=`
- Strings and numbers (int/float)
- Custom `.jarvis` file extension, runnable standalone via a compiled `.exe`

## Example

```
buat x = 5
buat nama = "Tony"
tulis "Halo, " + nama

kalo x > 3 maka
    tulis "x lebih besar dari 3"
selesai

fungsi tambah(a, b)
    kembalikan a + b
selesai

buat hasil = tambah(3, 4)
tulis hasil
```

## Architecture

```
Source code (.jarvis)
      ↓
   Lexer      → breaks raw text into tokens (KEYWORD, IDENTIFIER, NUMBER, STRING, OPERATOR...)
      ↓
   Parser     → builds an Abstract Syntax Tree (AST) from the tokens
      ↓
 Interpreter  → walks the AST and executes it
```

## Project Structure

```
Jarvis-Lang/
├── lexer.py          # Tokenizer
├── parser.py          # Builds the AST from tokens
├── interpreter.py       # Executes the AST
├── main.py                # Entry point — run a .jarvis file
└── *.jarvis                 # Example / test programs
```

## Usage

### Run a script directly with Python

```bash
python main.py program.jarvis
```

### Build a standalone executable

```bash
pip install pyinstaller
python -m PyInstaller --onefile --name jarvis main.py
```

The resulting `dist/jarvis.exe` can run `.jarvis` files without Python installed.

### Make `.jarvis` files double-clickable (Windows)

Run in an **Administrator** Command Prompt:

```cmd
assoc .jarvis=JarvisFile
ftype JarvisFile="path\to\dist\jarvis.exe" "%1" %*
```

After this, double-clicking any `.jarvis` file runs it directly.

## Roadmap

- [ ] `kalo_tidak` (else branch)
- [ ] Comments
- [ ] Better error messages (line numbers instead of character position)
- [ ] Lists / arrays
- [ ] Nested function scope improvements

## Notes

This is an educational project — not optimized for performance or production use. Built step by step: lexer → parser → interpreter → functions.
