#coding: utf-8
 
import unittest
import jpsscraping
from jpsscraping import author

class TestAuthor(unittest.TestCase):
    def test_create_list(self):
        author_div_str = '湯川学, 田中 太郎<sup>A</sup>, <sup>◯</sup>山田花子<sup>A,B</sup>'
        author_list = author.create_list(author_div_str)
        self.assertEqual(author_list[0], '湯川学')
        self.assertEqual(author_list[1], '田中 太郎<sup>A</sup>')
        self.assertEqual(author_list[2], '<sup>◯</sup>山田花子<sup>A,B</sup>')

        affiliation_div = '帝大理工, Univ. of South Pole  <sup>A</sup>, 日大危機管理<sup>B</sup>'
        affi_list = author.create_list(affiliation_div)
        self.assertEqual(affi_list[0], '帝大理工')
        self.assertEqual(affi_list[1], 'Univ. of South Pole  <sup>A</sup>')
        self.assertEqual(affi_list[2], '日大危機管理<sup>B</sup>')

    def test_parse_author(self):
        author_div = '湯川学, 田中 太郎<sup>A</sup>, <sup> ◯</sup> 山田花子 <sup>A,  B</sup>'
        author_list = author.parse_author(author.create_list(author_div))
        self.assertEqual(author_list[0].name, '湯川学')
        self.assertEqual(author_list[0].affiliation_tag[0], '')
        self.assertFalse(author_list[0].is_presenter)
        self.assertEqual(author_list[1].name, '田中 太郎')
        self.assertEqual(author_list[1].affiliation_tag[0], 'A')
        self.assertFalse(author_list[1].is_presenter)
        self.assertEqual(author_list[2].name, '山田花子')
        self.assertEqual(author_list[2].affiliation_tag[0], 'A')
        self.assertEqual(author_list[2].affiliation_tag[1], 'B')
        self.assertTrue(author_list[2].is_presenter)

    def test_create_affi_dict(self):
        affiliation_div = '帝大理工, Univ. of South Pole  <sup>A</sup>, 日大危機管理<sup>B</sup>'
        affi_dict = author.create_affi_dict(author.create_list(affiliation_div))
        self.assertEqual(affi_dict[''], '帝大理工')
        self.assertEqual(affi_dict['A'], 'Univ. of South Pole')
        self.assertEqual(affi_dict['B'], '日大危機管理')
        affiliation_div = ' 東大理  '
        affi_dict = author.create_affi_dict(author.create_list(affiliation_div))
        self.assertEqual(affi_dict[''], '東大理')

if __name__ == '__main__':
    unittest.main()
