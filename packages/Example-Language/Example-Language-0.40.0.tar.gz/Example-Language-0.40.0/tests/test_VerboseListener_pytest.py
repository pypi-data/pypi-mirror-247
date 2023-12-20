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

# pytest
import pytest

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


class TestVerboseListener:
    # parser/listener set up
    @pytest.fixture(scope="function")
    def setup(self, request) -> None:
        # set listener
        self.errorListener = VerboseListener()
        # create input stream of characters for lexer
        inputStream = InputStream(request.param)

        # create lexer and parser objects and token stream pipe between them
        self.lexer = exampleDslLexer(inputStream)
        self.lexer.removeErrorListeners()
        self.lexer.addErrorListener(self.errorListener)

        tokenStream = CommonTokenStream(self.lexer)

        self.parser = exampleDslParser(tokenStream)
        self.parser.removeErrorListeners()
        self.parser.addErrorListener(self.errorListener)

    @pytest.mark.parametrize("setup", ["c = a + b()\n"], indirect=["setup"])
    def test_valid_input(self, setup):
        # launch parser by invoking rule 'prog'
        ast = self.parser.prog()

        # check for no symbols in errorListener
        assert len(self.errorListener.symbol) == 0

    @pytest.mark.parametrize("setup", ["c = + b()\n"], indirect=["setup"])
    def test_invalid_input(self, setup):
        ast = self.parser.prog()

        # check for '+' symbol in errorListener
        assert self.errorListener.symbol == '+'
