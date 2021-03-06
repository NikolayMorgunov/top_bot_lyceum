import os
import typing
import unittest
from collections import Counter, OrderedDict
from typing import List, Tuple, Any

from lyceum_api.issue import IssueParser
from lyceum_api.parser import Parser, Tag

dirname = os.path.dirname(__file__)

HtmlState = Tuple[str,
                  str,
                  Tuple[Any],
                  typing.Counter[str],
                  typing.Counter[str]]


class TestParser(Parser):
    def __init__(self):
        super(TestParser, self).__init__()
        self.state: List[HtmlState] = []

    def add_state(self, what, t: Tag):
        self.state.append((what, t.name,
                           tuple(OrderedDict(**t.attrs).items()),
                           +self._classes, +self._tags))

    def on_starttag(self, t: Tag):
        self.add_state('open', t)

    def on_endtag(self, t: Tag):
        self.add_state('close', t)


class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.parser = TestParser()

    def tearDown(self):
        del self.parser

    def test_div_with_class(self):
        s = '<div class="a"></div>'
        state = [('open', 'div', (('class', 'a'),),
                  Counter(), Counter()),
                 ('close', 'div', (('class', 'a'),),
                  Counter(), Counter())]

        self.parser.feed(s)
        self.assertListEqual(self.parser.state, state)

    def test_two_tags(self):
        s = ('<div class = "a">'
             '  <x type="y" class="b"></x>'
             '<y type="z" class="c"></y>'
             '</div>')
        state = [('open', 'div', (('class', 'a'),),
                  Counter(), Counter()),
                 ('open', 'x', (('type', 'y'), ('class', 'b')),
                  Counter('a'), Counter({'div': 1})),
                 ('close', 'x', (('type', 'y'), ('class', 'b')),
                  Counter('a'), Counter({'div': 1})),
                 ('open', 'y', (('type', 'z'), ('class', 'c')),
                  Counter('a'), Counter({'div': 1})),
                 ('close', 'y', (('type', 'z'), ('class', 'c')),
                  Counter('a'), Counter({'div': 1})),
                 ('close', 'div', (('class', 'a'),),
                  Counter(), Counter())]

        self.parser.feed(s)
        self.assertListEqual(self.parser.state, state)

    def test_void_elements(self):
        s = ('<div class = "a">'
             '  <x type="y" class="b"><img class="a d"></x>'
             '<y type="z" class="c"></y>'
             '</div>')
        state = [('open', 'div', (('class', 'a'),),
                  Counter(), Counter()),
                 ('open', 'x', (('type', 'y'), ('class', 'b')),
                  Counter('a'), Counter({'div': 1})),
                 ('open', 'img', (('class', 'a d'),),
                  Counter('ab'), Counter(['div', 'x'])),
                 ('close', 'x', (('type', 'y'), ('class', 'b')),
                  Counter('a'), Counter({'div': 1})),
                 ('open', 'y', (('type', 'z'), ('class', 'c')),
                  Counter('a'), Counter({'div': 1})),
                 ('close', 'y', (('type', 'z'), ('class', 'c')),
                  Counter('a'), Counter({'div': 1})),
                 ('close', 'div', (('class', 'a'),),
                  Counter(), Counter())]

        self.parser.feed(s)
        self.assertListEqual(self.parser.state, state)


class IssueParserTestCase(unittest.TestCase):
    comments = [{'author_href': '/users/vasiliy-pupkin2017/',
                 'author': 'Василий Пупкин',
                 'text': 'Отправлено на проверку',
                 'files': ['https://lyceum.net/files/'
                           'e314cb37-0ff3-44fd-9525-e7c91e2e6ba8/'
                           'Kolichestvo%20minut%20v%20godu.py']},
                {'author_href': None,
                 'author': 'Лицей Бот',
                 'text': 'Вердикт: ok',
                 'files': []},
                {'author_href': '/users/monty/',
                 'author': 'Монти Пайтон',
                 'text': 'тест',
                 'files': []}]
    task_text = ('```\ndays_per_year = 365\n```\n'
                 '```\nhours_per_day = 24\n```\n'
                 '```\nminutes_per_hour = 60\n```\n'
                 ' Lorem Ipsum - это текст-"рыба", часто'
                 ' используемый в печати и вэб-дизайне.'
                 ' Lorem Ipsum является стандартной "рыбой"'
                 ' для текстов на латинице с начала XVI века.'
                 ' Формат вывода Выводится одно число.')

    @classmethod
    def setUpClass(cls):
        cls.parser = IssueParser()

    def _feed_file(self, file):
        file_path = os.path.join(dirname, file)
        with open(file_path, encoding='utf-8') as f:
            self.parser.feed(f.read())

    def _check_comments(self):

        parser_comments = [vars(c) for c in self.parser.comments]
        self.assertListEqual(parser_comments, self.comments)

    def _check_task(self):
        self.assertEqual(self.task_text, self.parser.task)

    def test_comments(self):
        self._feed_file('issue_comments.html.test')
        self._check_comments()

    def test_task(self):
        self._feed_file('issue_task.html.test')
        self._check_task()

    def test_full_page(self):
        self._feed_file('issue_page.html.test')
        self._check_task()
        self._check_comments()

        self.assertEqual('iPTiuyP6wvLCKlKJwNkR1WOKUtVJK8N1',
                         self.parser.token)
