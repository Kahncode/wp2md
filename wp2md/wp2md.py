
from html.parser import HTMLParser
import pypandoc
from pypandoc.pandoc_download import download_pandoc
import sys
import os.path
import re
import html

#This html parser would be a better way to extract the relevant block but for now we are using simple string logic
#class WordpressHTMLParser(HTMLParser):
#	def __init__(self):
#		self.article_str = ""
#		self.inside_article = False
#		super().__init__()

#	def get_attr(self, attrs, name):
#		for attr in attrs:
#			if attr[0] == name:
#				return attr[1]
#		return None

#	def handle_starttag(self, tag, attrs):
#		if tag == "article":
#			self.article_str = self.rawdata
#			return

#	def handle_endtag(self, tag):
#		if tag == "article":
#			self.inside_article = False
#			return


def isolate_article(html_str):
	#parser = WordpressHTMLParser()
	#parser.feed(html_str)
	
	start_index = html_str.find('<article')
	end_index = html_str.find('/article>')
	article_str = html_str[start_index:end_index+9]
	end_index = article_str.rfind('<footer')
	return article_str[0:end_index]
	

def process_md(md_str):

	# process code blocks and add correct syntax highlight
	md_str = re.sub(r'``` {.EnlighterJSRAW enlighter-language="(.+)"}', r'``` \1', md_str);
	
	#null language defaults to cpp
	md_str = md_str.replace('``` null', '``` cpp')

	#remove the more tag
	md_str = re.sub(r'^\[\]\{#more\-[0-9]+\}\n', '', md_str, 0, re.MULTILINE)
	
	#remove remaining artifacts
	md_str = re.sub(r'\{.*\}', '', md_str)
	md_str = re.sub(r':::.*', '', md_str)

	#remove specific bug for kahncode
	md_str = re.sub(r'\[\[\[(!\[\])', r'\1', md_str)

	#No more than one line break between paragraphs
	md_str = re.sub(r'^\s*\n\s*\n', '\n', md_str, 0, re.MULTILINE)

	return md_str

#main
if __name__ == '__main__':

	print("Wordpress To Markdown")
	print("Arguments", sys.argv)
	if len(sys.argv) < 2:
		exit

	pandoc_version = pypandoc.get_pandoc_version()
	if pandoc_version:
		print("Using pandoc version ", pandoc_version)
	else:
		print("Downloading pandoc at latest version")
		download_pandoc()

	html_file = sys.argv[1]
	md_file = os.path.splitext(html_file)[0] + '.' + "md"
	print("Processing file ", html_file, " to ", md_file)

	with open(html_file) as f:
		html_str = f.read()

		#isolate relevant html block
		article_str = isolate_article(html_str)

		#Test line: pandoc -f html -t markdown article.html --wrap=preserve > article.md
		md_str = pypandoc.convert_text(article_str, 'markdown', format='html', extra_args=['--wrap=preserve'])

		#avoid the double line break bugs with \r\n
		md_str = md_str.replace('\r\n', '\n')
		#Post-process
		md_str = process_md(md_str)

		
		print(md_str)

		with open(md_file, 'w') as w:
			w.write(md_str)