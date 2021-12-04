import unittest
import requests

class TestApp(unittest.TestCase):

    def test_app_run(self):
        try:
            r = requests.get("http://127.0.0.1:5000")
        except:
            self.fail("App not running. Test Failed.")

    def test_about(self):
        try:
            r = requests.get("http://127.0.0.1:5000/about")
        except:
            self.fail("About Route does not exist.")

    def test_index(self):
        try:
            r = requests.get("http://127.0.0.1:5000/index")
        except:
            self.fail("Index Route does not exist.")

    def test_about_title(self):
        r = requests.get("http://127.0.0.1:5000/about")
        page_src = r.text
 
        if page_src.find("Welcome to the CSCI 5030 - Software Development Spellchecker") < 0:
            self.fail("Can't find About Page title or Language is not recognised.")

    def test_index_btn(self):
        r = requests.get("http://127.0.0.1:5000/index")
        page_src = r.text
 
        if page_src.find('<button type="submit" style="margin:0; position:absolute; left:47.5%;">Spell Check</button>') < 0:
            self.fail("Can't find Spell Check Button.")

    def test_index_input(self):
        r = requests.get("http://127.0.0.1:5000/index")
        page_src = r.text
 
        if page_src.find('''<div contenteditable="true" id="InputOutputDiv" class="divStyleLeft" style="float: left">
                    
                </div>''') < 0:
            self.fail("Can't find Input text area.")

    def test_index_recomm(self):
        r = requests.get("http://127.0.0.1:5000/index")
        page_src = r.text
 
        if page_src.find('''<div contenteditable="false" id="RecommendationsDiv" class="divStyleRight" style="float:left">
                    
                </div>''') < 0:
            self.fail("Can't find Recommendations area.")

    def test_lang_dropdown(self):
        r = requests.get("http://127.0.0.1:5000/index")
        page_src = r.text
 
        if page_src.find('''<select onchange="myFunction(this)">
          <option value="en">English</option>
          <option value="es">Spanish</option>
          <option value="ir">Irish</option>
        </select>''') < 0:
            self.fail("Can't find multi language selector.")

    def test_index_lang_indicator(self):
        r = requests.get("http://127.0.0.1:5000/index")
        page_src = r.text
 
        if page_src.find('<p style="display:inline-block">Current language:</p>') < 0:
            self.fail("Can't find current language indicator.")

if __name__ == "__main__":
    unittest.main(warnings="ignore", failfast = True)