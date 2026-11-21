import sys, unittest
sys.path.insert(0, ".")
from waformat.core import md_to_wa, wa_to_md

class MdToWaTests(unittest.TestCase):
    def test_bold(self):
        self.assertEqual(md_to_wa("Ini **penting** ya"), "Ini *penting* ya")
    def test_italic_star(self):
        self.assertEqual(md_to_wa("kata *miring* ini"), "kata _miring_ ini")
    def test_bold_italic(self):
        self.assertEqual(md_to_wa("***tegas***"), "*_tegas_*")
    def test_heading(self):
        self.assertEqual(md_to_wa("## Judul Besar"), "*Judul Besar*")
    def test_strike(self):
        self.assertEqual(md_to_wa("~~salah~~ benar"), "~salah~ benar")
    def test_link(self):
        self.assertEqual(md_to_wa("lihat [situs ini](https://contoh.id)"),
                         "lihat situs ini (https://contoh.id)")
    def test_bare_link_text_same(self):
        self.assertEqual(md_to_wa("[https://contoh.id](https://contoh.id)"),
                         "https://contoh.id")
    def test_inline_code(self):
        self.assertEqual(md_to_wa("jalankan `npm test` sekarang"),
                         "jalankan ```npm test``` sekarang")
    def test_bullet(self):
        self.assertEqual(md_to_wa("- satu\n- dua"), "• satu\n• dua")
    def test_table(self):
        md = "| Nama | Harga |\n| --- | --- |\n| Kopi | 15000 |"
        self.assertEqual(md_to_wa(md), "Nama • Harga\nKopi • 15000")
    def test_fence_untouched(self):
        md = "```\n**bukan tebal**\n```"
        self.assertEqual(md_to_wa(md), md)

class WaToMdTests(unittest.TestCase):
    def test_bold(self):
        self.assertEqual(wa_to_md("Ini *penting* ya"), "Ini **penting** ya")
    def test_italic(self):
        self.assertEqual(wa_to_md("kata _miring_ ini"), "kata *miring* ini")
    def test_strike(self):
        self.assertEqual(wa_to_md("~salah~ benar"), "~~salah~~ benar")
    def test_bullet(self):
        self.assertEqual(wa_to_md("• satu"), "- satu")
    def test_roundtrip_bold(self):
        self.assertEqual(wa_to_md(md_to_wa("**tebal** dan *miring*")),
                         "**tebal** dan *miring*")

if __name__ == "__main__":
    unittest.main()
