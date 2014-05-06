# -*- encoding: UTF-8 -*-
import markdown2
import os
import sys
import re
import json
import urllib2


settings = {
    "browser": "default",
    "parser": "default",
    "enable_mathjax": False,
    "enable_highlight": True,
    "github_mode": "markdown",
    "css": "http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap-combined.min.css",
    "allow_css_overrides": False,
    "markdown_filetypes": [".md", ".markdown", ".mdown"],
    "strip_yaml_front_matter": False,
    "host": '/static/',
}


def error_message(msg):
    print msg


def status_message():
    print msg


def get_cwd():
    return os.path.dirname(__file__)


class MarkdownPreviewCommand():

    ''' preview file contents with python-markdown and your web browser '''

    def __init__(self, filename):
        self.filename = filename

    def get_contents(self, contents):
        ''' Get contents or selection from view and optionally strip the YAML front matter '''
        if settings.get('strip_yaml_front_matter') and contents.startswith('---'):
            title = ''
            title_match = re.search(
                '(?:title:)(.+)', contents, flags=re.IGNORECASE)
            if title_match:
                stripped_title = title_match.group(1).strip()
                title = '%s\n%s\n\n' % (
                    stripped_title, '=' * len(stripped_title))
            contents_without_front_matter = re.sub(
                r'(?s)^---.*---\n', '', contents)
            contents = '%s%s' % (title, contents_without_front_matter)
        return contents

    def getCSS(self):
        ''' return the correct CSS file based on parser and settings '''
        config_parser = settings.get('parser')
        config_css = settings.get('css')

        styles = ''
        if config_css and config_css != 'default':
            styles += u"<link href='%s' rel='stylesheet' type='text/css'>" % config_css
        else:
            css_filename = 'markdown.css'
            if config_parser and config_parser == 'github':
                css_filename = 'github.css'
            # path via package manager
            css_path = os.path.join(
                get_cwd(), css_filename)
            if not os.path.isfile(css_path):
                # path via git repo
                css_path = os.path.join(
                    os.path.dirname(get_cwd()), 'sublimetext-markdown-preview', css_filename)
                if not os.path.isfile(css_path):
                    error_message('markdown.css file not found!')
                    raise Exception("markdown.css file not found!")
            styles += u"<style>%s</style>" % open(
                css_path, 'r').read().decode('utf-8')

        return styles

    def getMathJax(self):
        ''' return the MathJax script if enabled '''

        if settings.get('enable_mathjax') is True:
            mathjax_path = os.path.join(
                get_cwd(), "mathjax.html")

            if not os.path.isfile(mathjax_path):
                error_message('mathjax.html file not found!')
                raise Exception("mathjax.html file not found!")

            return open(mathjax_path, 'r').read().decode('utf-8')
        return ''

    def getHighlight(self):
        ''' return the Highlight.js and css if enabled '''

        highlight = ''
        if settings.get('enable_highlight') is True and settings.get('parser') == 'default':
            highlight_path = os.path.join(
                get_cwd(), "../static/highlight.js")
            highlight_css_path = os.path.join(
                get_cwd(), "../static/highlight.css")

            if not os.path.isfile(highlight_path):
                error_message('highlight.js file not found!')
                raise Exception("highligh.js file not found!")

            if not os.path.isfile(highlight_css_path):
                error_message('highlight.css file not found!')
                raise Exception("highlight.css file not found!")

            highlight += u"<style>%s</style>" % open(
                highlight_css_path, 'r').read().decode('utf-8')
            highlight += u"<script>%s</script>" % open(
                highlight_path, 'r').read().decode('utf-8')
            highlight += "<script>hljs.initHighlightingOnLoad();</script>"
        return highlight

    def postprocessor(self, html):
        ''' fix relative paths in images, scripts, and links for the internal parser '''
        def tag_fix(match):
            tag, src = match.groups()
            filename = self.filename
            if not src.startswith(('file://', 'https://', 'http://', '/', '#')):
                abs_path = u'file://%s/%s' % (
                    os.path.dirname(filename), src)
                tag = tag.replace(src, abs_path)
            return tag
        RE_SOURCES = re.compile(
            """(?P<tag><(?:img|script|a)[^>]+(?:src|href)=["'](?P<src>[^"']+)[^>]*>)""")
        html = RE_SOURCES.sub(tag_fix, html)
        return html

    def convert_markdown(self, markdown):
        ''' convert input markdown to HTML, with github or builtin parser '''

        markdown_html = u'cannot convert markdown'
        # convert the markdown
        markdown_html = markdown2.markdown(markdown, extras=[
                                           'footnotes', 'toc', 'fenced-code-blocks', 'cuddled-lists', 'wiki-tables'])
        toc_html = markdown_html.toc_html
        if toc_html:
            toc_markers = ['[toc]', '[TOC]', '<!--TOC-->']
            for marker in toc_markers:
                markdown_html = markdown_html.replace(marker, toc_html)

        # postprocess the html from internal parser
        markdown_html = self.postprocessor(markdown_html)

        return markdown_html

    def get_title(self, markdown):
        title_match = re.search(r'<h1.*?>(.+?)</h1>', markdown, re.S)
        if title_match:
            return title_match.group(1)
        else:
            return ''

    def run(self):
        contents = self.get_contents(open(self.filename).read())

        markdown_html = self.convert_markdown(contents)

        full_html = u'<!DOCTYPE html>'
        full_html += '<html><head><meta charset="utf-8">'
        full_html += '<title>' + self.get_title(markdown_html) + '</title>'
        full_html += ''.join([
            # '<link rel="stylesheet" type="text/css" href="{0}bootstrap/css/bootstrap.min.css">'.format(settings['host']),
            '<link rel="stylesheet" type="text/css" href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.css">',
            '<link rel="stylesheet" type="text/css" href="http://cdn.staticfile.org/font-awesome/4.0.3/css/font-awesome.min.css">',
            '<link rel="stylesheet" type="text/css" href="{0}markdown/markdown.css">'.format(settings['host']),
            '<link rel="stylesheet" type="text/css" href="http://cdn.staticfile.org/highlight.js/8.0/styles/default.min.css">',
            '<link rel="stylesheet" type="text/css" href="/static/affix.css">',
            '<style type="text/css">body{padding-bottom: 200px;} pre code{max-height: 100%;}</style><style></style>'
        ])
        full_html += self.getCSS()
        # full_html += self.getHighlight()
        full_html += self.getMathJax()
        full_html += ('</head><body><div class="container-fluid">'
                      '<div class="row-fluid"><div class="span2" id="header"></div>'
                      '<div class="span10">')
        full_html += markdown_html
        full_html += '</div></div></div>'
        full_html += ''.join([
            '<script type="text/javascript" src="http://cdn.staticfile.org/jquery/2.1.1-rc2/jquery.min.js"></script>',
            '<script type="text/javascript" src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>',
            # '<script type="text/javascript" src="{0}highlight/highlight.min.js"></script>'.format(settings['host']),
            '<script type="text/javascript" src="http://cdn.staticfile.org/highlight.js/8.0/highlight.min.js"></script>',
            '<script type="text/javascript" src="{0}markdown/markdown.js"></script>'.format(settings['host']),
            '<script type="text/javascript" src="/static/affix.js"></script>',
            # '<script type="text/javascript">$(function() {emojify.run();})</script>'
        ])
        full_html += '</body>'
        full_html += '</html>'
        full_html = self.process_local_img(full_html)
        return full_html

    def process_local_img(self, html):
        return re.sub(
            r'<img src="file://.*?/img/(.+?)">',
            r'<img src="img/\1">',
            html
        )
