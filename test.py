import contextlib
import os
import sys
import unittest

import connect as connect
import epiCalendar
import utils as utils


class testUtils(unittest.TestCase):
    def test_verifyCookieStrucutre(self):
        self.assertFalse(utils.verifyCookieStructure(""))
        self.assertFalse(utils.verifyCookieStructure("a"))
        self.assertFalse(utils.verifyCookieStructure("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))
        self.assertFalse(utils.verifyCookieStructure("00000dlJBa0_91pHyD9bDHAW5VO:118eurd6"))
        self.assertFalse(utils.verifyCookieStructure("00000dlJBa0_91pHyD9bDHAW5VO:1d18eurd6x"))
        self.assertFalse(utils.verifyCookieStructure("0000dlJBa0_91pHyD9bDHAW5VO:1d8eurd6"))
        self.assertFalse(utils.verifyCookieStructure("00010dlJBa0_91pHyD9bDHAW5VO:1d8eurd6"))
        self.assertFalse(utils.verifyCookieStructure("0000XXXXXXXXXXXXXXXXXXXXXXX:1dXXXXXXX"))
        self.assertTrue(utils.verifyCookieStructure("00000dlJBa0_91pHyD9bDHAW5VO:1d18eurd6"))

    def test_verifyCookieExpiration(self):
        self.assertFalse(utils.verifyCookieExpiration(""))
        self.assertFalse(utils.verifyCookieExpiration("xax"))
        self.assertFalse(utils.verifyCookieExpiration("00000dlJBa0_91pHyD9bDHAW5VO:1d18eurd6"))
        self.assertTrue(utils.verifyCookieExpiration(jsessionid))

class testConnect(unittest.TestCase):
    def test_firstRequest(self):
        r = connect.firstRequest(jsessionid)
        self.assertEqual(r.status_code, 200)
        self.assertIn('<div id="j_id', r.text)
        self.assertIn('javax.faces.ViewState', r.text)
        self.assertIn('action="/serviciosacademicos/web/expedientes/calendario.xhtml"', r.text)

    def test_postRequest(self):
        pass

class testCalendar(unittest.TestCase):

    def test_generate(self):
        options = (
            {'case': 'no flags', 'flags': ['-o', 'test'], 'filename': 'test'},
            {'case': 'disable location parsing', 'flags': ['--disable-location-parsing', '-o', 'testNoLocation'], 'filename': 'testNoLocation'},
            {'case': 'disable links', 'flags': ['--disable-links', '-o', 'testNoLinks'], 'filename': 'testNoLinks'},
            {'case': 'disable class type parsing', 'flags': ['--disable-class-type-parsing', '-o', 'testNoClassType'], 'filename': 'testNoClassType'},
            {'case': 'disable location parsing and links', 'flags': ['--disable-location-parsing', '--disable-links', '-o', 'testNoLocationNoLinks'], 'filename': 'testNoLocationNoLinks'},
            {'case': 'disable location parsing and disable class type parsing', 'flags': ['--disable-location-parsing', '--disable-class-type-parsing', '-o', 'testNoLocationNoClassType'], 'filename': 'testNoLocationNoClassType'},
            {'case': 'disable everything', 'flags': ['--disable-location-parsing', '--disable-links', '--disable-class-type-parsing', '-o', 'testAllFlags'], 'filename': 'testAllFlags'},
            {'case': 'enable stats', 'flags': ['--enable-stats', '-o', 'testStats'], 'filename': 'testStats'},
            {'case': 'dry run', 'flags': ['--dry-run', '-o', 'testDryRun'], 'filename': 'testDryRun'},
        )

        filetype = (
            {'case': 'ics', 'flags': [], 'extension': '.ics'},
            {'case': 'csv', 'flags': ['--csv'], 'extension': '.csv'},
        )

        for ext in filetype:
            with self.subTest(ext['case']):
                numberOfLines = -1
                for case in options:
                    with self.subTest(case=case['case']):
                        remove(case['filename'] + ext['extension'])
                        run(['epiCalendar.py', jsessionid, *case['flags'], *ext['flags']])
                        if case['case'] == 'dry run':
                            self.assertFalse(os.path.exists(case['filename'] + ext['extension']))
                            break
                        self.assertTrue(os.path.exists(case['filename'] + ext['extension']))
                        with open(case['filename'] + ext['extension'], 'r') as f:
                            linesRead = len(f.readlines())
                        if not numberOfLines == -1: self.assertEqual(linesRead, numberOfLines)
                        self.assertNotEqual(linesRead, 0)
                        numberOfLines = linesRead
                        remove(case['filename'] + ext['extension'])


def run(argv):
    with contextlib.redirect_stdout(None): epiCalendar.main(argv)

def remove(filename):
    if os.path.exists(filename): os.remove(filename)

if __name__ == '__main__':
    global jsessionid
    jsessionid = input("Enter valid JSESSIONID: ")
    if not utils.verifyCookieStructure(jsessionid):
        print("Invalid JSESSIONID.")
        sys.exit(1)
    unittest.main(verbosity=3)