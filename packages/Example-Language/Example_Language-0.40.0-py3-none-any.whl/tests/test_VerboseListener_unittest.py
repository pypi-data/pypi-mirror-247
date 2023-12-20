"""exampleDsl test."""

__author__ = 'sgu'

#  Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# unittest
from unittest import SkipTest, TestCase

# antlr
from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.InputStream import InputStream

# user relative imports
from cst.verbose_listener import VerboseListener
from gen.python.exampleDsl.exampleDslLexer import exampleDslLexer
from gen.python.exampleDsl.exampleDslParser import exampleDslParser

# fail relative import beyond top-level package
# try:
#     from ..exampleLSPServer.cst.VerboseListener import VerboseListener
#     from ..exampleLSPServer.gen.python.exampleDsl.exampleDslLexer import exampleDslLexer
#     from ..exampleLSPServer.gen.python.exampleDsl.exampleDslParser import exampleDslParser
# except Exception as inst:
#     # debug import
#     import sys, os
#     from pprint import pprint
#
#     pprint( sys.path )
#     raise SkipTest( "Skipping all tests in test_feature.py" )


class TestVerboseListener(TestCase):

    def setup(self, msg: str = "") -> exampleDslParser:
        # set listener
        self.errorListener = VerboseListener()
        # create input stream of characters for lexer
        inputStream = InputStream(msg)

        # create lexer and parser objects and token stream pipe between them
        lexer = exampleDslLexer(inputStream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(self.errorListener)

        tokenStream = CommonTokenStream(lexer)

        parser = exampleDslParser(tokenStream)
        parser.removeErrorListeners()
        parser.addErrorListener(self.errorListener)

        return parser

    def test_valid_input(self):
        # launch parser by invoking rule 'prog'
        parser = self.setup("c = a + b()\n")
        ast = parser.prog()

        # check for no symbols in errorListener
        self.assertEqual(len(self.errorListener.symbol), 0)

    def test_invalid_input(self):
        parser = self.setup("c = + b()\n")
        ast = parser.prog()

        # check for '+' symbol in errorListener
        self.assertEqual(self.errorListener.symbol, '+')
