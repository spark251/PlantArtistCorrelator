import unittest, search

class TestFormatSeconds(unittest.TestCase):

    def test_seconds(self):
        self.assertEqual(search.formatSeconds(2), "2 seconds")
        self.assertEqual(search.formatSeconds(1), "1 second")

    def test_minutes(self) :
        self.assertEqual(search.formatSeconds(60), "1 minute 0 seconds")
        self.assertEqual(search.formatSeconds(60+1), "1 minute 1 second")
        self.assertEqual(search.formatSeconds(60+2), "1 minute 2 seconds")

    def test_hours(self):
        self.assertEqual(search.formatSeconds(3600), "1 hour 0 minutes 0 seconds")
        self.assertEqual(search.formatSeconds(3600+60), "1 hour 1 minute 0 seconds")
        self.assertEqual(search.formatSeconds(3600+60*2), "1 hour 2 minutes 0 seconds")
        self.assertEqual(search.formatSeconds(3600*2), "2 hours 0 minutes 0 seconds")

class TestAddS(unittest.TestCase) :
    def test_addS(self) :
        self.assertEqual(search.addS("second", "seconds", 0), "seconds")
        self.assertEqual(search.addS("second", "seconds", 1), "second")
        self.assertEqual(search.addS("second", "seconds", 2), "seconds")
        self.assertEqual(search.addS("second", "seconds", 0.1), "seconds")
        self.assertEqual(search.addS("second", "seconds", 1.1), "second")
        self.assertEqual(search.addS("second", "seconds", 2.2), "seconds")

class TestGetPageText(unittest.TestCase) :
    def test_getPageText(self) :
        self.assertEqual(search.getPageText("https://api.twitter.com/1.1/search/tweets.json"),' ')
    def test_getVisibleText(self) :
        self.assertEqual(search.getVisibleText("<b>hello</b>more"),"hellomore")

if __name__ == '__main__':
    unittest.main()
