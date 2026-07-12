"""
LEXER - Tahap pertama bikin bahasa pemrograman.
Tugasnya: ubah teks mentah jadi list token yang punya makna.

Contoh:
    input  : buat x = 5
    output : [KEYWORD(buat), IDENTIFIER(x), OPERATOR(=), NUMBER(5)]
"""

# Semua kata yang punya arti khusus dalam bahasa kita (bukan nama variabel bebas)
KEYWORDS = {
    "buat",      # deklarasi variabel -> buat x = 5
    "tulis",     # print -> tulis "halo"
    "kalo",      # if -> kalo x > 5 maka
    "kalo_tidak",# else
    "maka",      # then (penutup kondisi kalo)
    "ulang",     # loop -> ulang 5 kali
    "kali",      # penutup loop -> ulang 5 kali
    "fungsi",
    "kembalikan",    # function -> fungsi tambah(a, b)
    "selesai",   # penutup blok (if/loop/fungsi)
}


class Token:
    """Representasi satu token. Tiap token punya TIPE dan NILAI."""

    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})"


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0  # posisi karakter yang lagi dibaca
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        """Maju satu karakter ke depan."""
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None  # udah habis teksnya

    def skip_whitespace(self):
        """Lewatin spasi, tab, newline -- gak punya makna buat token."""
        while self.current_char is not None and self.current_char in " \t\n":
            self.advance()

    def read_number(self):
        """Baca angka, misal '123' atau '3.14'."""
        result = ""
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == "."):
            result += self.current_char
            self.advance()
        if "." in result:
            return Token("NUMBER", float(result))
        return Token("NUMBER", int(result))

    def read_string(self):
        """Baca teks di dalam tanda kutip, misal '"halo dunia"'."""
        self.advance()  # skip kutip pembuka
        result = ""
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()  # skip kutip penutup
        return Token("STRING", result)

    def read_identifier(self):
        """Baca nama variabel/keyword, misal 'buat' atau 'nama_saya'."""
        result = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):
            result += self.current_char
            self.advance()

        if result in KEYWORDS:
            return Token("KEYWORD", result)
        return Token("IDENTIFIER", result)

    def get_next_token(self):
        """Fungsi utama: ambil satu token berikutnya dari teks."""
        while self.current_char is not None:

            if self.current_char in " \t\n":
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.read_number()

            if self.current_char == '"':
                return self.read_string()

            if self.current_char.isalpha() or self.current_char == "_":
                return self.read_identifier()

            # Operator dan simbol satu-dua karakter
            two_char = self.text[self.pos:self.pos + 2]
            if two_char in (">=", "<=", "==", "!="):
                self.advance()
                self.advance()
                return Token("OPERATOR", two_char)

            single_char_tokens = {
                "+": "OPERATOR",
                "-": "OPERATOR",
                "*": "OPERATOR",
                "/": "OPERATOR",
                "=": "OPERATOR",
                ">": "OPERATOR",
                "<": "OPERATOR",
                "(": "LPAREN",
                ")": "RPAREN",
                ",": "COMMA",
            }
            if self.current_char in single_char_tokens:
                char = self.current_char
                self.advance()
                return Token(single_char_tokens[char], char)

            raise Exception(f"Karakter gak dikenal: '{self.current_char}' di posisi {self.pos}")

        return Token("EOF", None)  

    def tokenize(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == "EOF":
                break
        return tokens


if __name__ == "__main__":
    kode = '''
    buat x = 5
    buat nama = "Raymond"
    tulis "Halo, " + nama
    kalo x > 3 maka
        tulis "x lebih besar dari 3"
    selesai
    '''

    lexer = Lexer(kode)
    tokens = lexer.tokenize()

    print("=== HASIL TOKENISASI ===")
    for t in tokens:
        print(t)