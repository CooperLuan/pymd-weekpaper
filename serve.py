# -*- encoding: UTF-8 -*-

"""
Week Paper Borwser
on port 8888
run as daemon
view by:
    / current week
    /0801
"""
import os
import re
from datetime import datetime, date

from MarkdownPreview import MarkdownPreview

import tornado.ioloop
import tornado.web
from dateutil.relativedelta import relativedelta, weekday, MO
from dateutil.parser import parse


def _auto_gen_weekly():
    filename = (date.today() + relativedelta(
        weekday=weekday(0, -1))).strftime('%Y%m%d Week.md')
    filename = os.path.join(
        os.path.dirname(os.path.dirname(MarkdownPreview.__file__)),
        'posts', filename)
    if not os.path.exists(filename):
        open(filename, 'w').write(open('posts/default.md').read())


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        filename = (date.today() + relativedelta(
            weekday=weekday(0, -1))).strftime('%Y%m%d Week.md')
        filename = os.path.join(
            os.path.dirname(os.path.dirname(MarkdownPreview.__file__)),
            'posts', filename)
        _auto_gen_weekly()
        html = MarkdownPreview.MarkdownPreviewCommand(
            filename
        ).run().encode('utf-8')
        self.write(html)


class MarkdownHandler(tornado.web.RequestHandler):

    def get(self):
        path = self.get_argument('input-path', None)
        if path is not None and os.path.exists(path):
            content = MarkdownPreview.MarkdownPreviewCommand(
                path
            ).run().encode('utf-8')
            content = re.search(
                r'\<body\>(.+?)\<\/body\>', content, re.S).group(1)
            content = re.sub(
                r'\<code\>:::json\n', r'<code class="ruby">', content, re.S)
        else:
            content = ''
        self.render('md.html', path=path or '', content=content)


class WeekHandler(tornado.web.RequestHandler):

    def get(self, week):
        if week == 'favicon.ico':
            return
        week = '%d%s' % (date.today().year, week) if len(week) <= 4 else week
        filename = (parse(week) + relativedelta(
            weekday=weekday(0, -1))).strftime('%Y%m%d Week.md')
        filename = os.path.join(
            os.path.dirname(os.path.dirname(MarkdownPreview.__file__)),
            'posts',
            filename)
        _auto_gen_weekly()
        html = MarkdownPreview.MarkdownPreviewCommand(
            filename
        ).run().encode('utf-8')
        self.write(html)


class SmartHandler(tornado.web.RequestHandler):

    def get(self, uri):
        # -1/-2/-3...
        if re.match(r'-\d+', uri):
            self.redirect(
                (datetime.now() + relativedelta(weekday=MO(int(uri) - 1))).strftime('%Y%m%d'))
        elif uri in ('last'):
            self.redirect(
                (datetime.now() + relativedelta(weekday=MO(-2))).strftime('%Y%m%d'))
        elif uri == 'build':
            path = self.get_argument('input-path')
            html = MarkdownPreview.MarkdownPreviewCommand(
                path
            ).run().encode('utf-8')
            html = re.sub(
                r'\<code\>:::json\n', r'<code class="ruby">', html, re.S)
            open(path.replace('.md', '.html'), 'w').write(html)
            self.write(html)

if __name__ == "__main__":
    application = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/md", MarkdownHandler),
            (r"/(\d+?)", WeekHandler),
            (r"/(.+)", SmartHandler)
        ],
        debug=True,
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
    )
    application.listen(5566)
    tornado.ioloop.IOLoop.instance().start()
