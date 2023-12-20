"""test SymbolTable module."""

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

# utils import
import asyncio
import os
import sys
import time
import signal
from typing import List, Optional

# pytest
from unittest import IsolatedAsyncioTestCase, SkipTest

# antlr4
from antlr4 import TerminalNode
from antlr4.Token import CommonToken
from antlr4.tree.Tree import TerminalNodeImpl

# user relative imports
from symbolTable.SymbolTable import SymbolTable, NamespaceSymbol, ClassSymbol, InterfaceSymbol, FieldSymbol, MethodSymbol, BlockSymbol, VariableSymbol, FundamentalType, LiteralSymbol, DuplicateSymbolError, ScopedSymbol, SymbolTableOptions, RoutineSymbol, \
    Symbol

# fail relative import beyond top-level package
# try:
#     from ..exampleLSPServer.symbolTable.SymbolTable import SymbolTable, NamespaceSymbol, ClassSymbol, InterfaceSymbol, FieldSymbol, MethodSymbol, BlockSymbol, VariableSymbol, FundamentalType, LiteralSymbol, DuplicateSymbolError, ScopedSymbol, SymbolTableOptions, RoutineSymbol, Symbol
# except Exception as inst:
#     # debug import
#     import sys, os
#     from pprint import pprint
#     pprint(sys.path)
#     raise SkipTest("Skipping all tests in test_feature.py")


if not os.path.join(sys.path[0], 'build-python') in sys.path:
    sys.path.append(os.path.join(sys.path[0], 'build-python'))

dummyNode: TerminalNode = TerminalNodeImpl(CommonToken((None, None), -2, 0, 10, 20))


class Executor:
    """In most cases, you can just use the 'execute' instance as a
    function, i.e. y = await execute(f, a, b, k=c) => run f(a, b, k=c) in
    the executor, assign result to y. The defaults can be changed, though,
    with your own instantiation of Executor, i.e. execute =
    Executor(nthreads=4)"""

    def __init__(self, loop=asyncio.get_event_loop(), nthreads=1):
        from concurrent.futures import ThreadPoolExecutor
        self._ex = ThreadPoolExecutor(nthreads)
        self._loop = loop

    def __call__(self, f, *args, **kw):
        from functools import partial
        return self._loop.run_in_executor(self._ex, partial(f, *args, **kw))


class TestTimeout(Exception):
    pass


class test_timeout:
    def __init__(self, seconds, error_message=None):
        if error_message is None:
            error_message = 'test timed out after {}s.'.format(seconds)
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TestTimeout(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.alarm(0)


async def createClassSymbolTable(name: str, counts: List[int], namespaces: Optional[List[str]] = None) -> SymbolTable:
    symbolTable = SymbolTable(name, SymbolTableOptions(False))

    nsSymbols: List[Optional[NamespaceSymbol]] = []
    nsIndex = 0
    nsCount = 1
    if namespaces is not None and len(namespaces) > 0:
        nsCount = len(namespaces)
        for i in range(nsCount):
            nsSymbols.append(await symbolTable.add_new_namespace_from_path(None, namespaces[i]))
    else:
        nsSymbols.append(None)

    for i in range(counts[0]):
        classSymbol = symbolTable.add_new_symbol_of_type(ClassSymbol, nsSymbols[nsIndex], 'class%s' % i, [], [])
        interfaceSymbol = symbolTable.add_new_symbol_of_type(InterfaceSymbol, None, 'interface%s' % i, [])

        for j in range(counts[2]):
            symbolTable.add_new_symbol_of_type(FieldSymbol, classSymbol, 'field%s' % j)
            symbolTable.add_new_symbol_of_type(FieldSymbol, interfaceSymbol, 'field%s' % j)

        for j in range(counts[1]):
            method = symbolTable.add_new_symbol_of_type(MethodSymbol, classSymbol, 'method%s' % j)
            symbolTable.add_new_symbol_of_type(MethodSymbol, interfaceSymbol, 'method%s' % j)

            # Blocks are created and added in an alternative way (only for classes).
            block1 = symbolTable.add_new_symbol_of_type(BlockSymbol, None, 'block1')  # Block at top level.
            symbolTable.add_new_symbol_of_type(VariableSymbol, block1, "var1", 17, FundamentalType.integerType)
            block2 = symbolTable.add_new_symbol_of_type(BlockSymbol, None, 'block2')
            symbol = symbolTable.add_new_symbol_of_type(VariableSymbol, block2, 'var1', 3.142, FundamentalType.floatType)
            if j == 1:
                symbol.context = dummyNode

            # Now move the blocks from global level to the method.
            method.addSymbol(block1)
            method.addSymbol(block2)

        nsIndex += 1
        if nsIndex == nsCount:
            nsIndex = 0

    for i in range(counts[3]):
        symbolTable.add_new_symbol_of_type(VariableSymbol, None, 'globalVar%s' % i, 42, FundamentalType.integerType)

    for i in range(counts[4]):
        symbolTable.add_new_symbol_of_type(
            LiteralSymbol, None, 'globalConst%s' % i, "string constant",
            FundamentalType.stringType
        )

    return symbolTable


# async def symTable() -> SymbolTable:
#     '''
#     pre 3.8 async def and await syntax for call asyncio.run(symTable())
#
#     :return:
#     '''
#     result = await createClassSymbolTable("main", [3, 3, 4, 5, 5])
#
#     return result

class SymbolTableTest(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        dummyNode.text = 'Dummy'

        # p = ProcessPoolExecutor(2) # Create a ProcessPool with 2 processes
        self.execute = Executor()

    async def test_Single_table_base(self):
        self.symbolTable: SymbolTable = await createClassSymbolTable("main", [3, 3, 4, 5, 5])
        self.info = self.symbolTable.info()

        self.assertEqual(self.info.dependencyCount, 0)
        self.assertEqual(self.info.symbolCount, 16)  # 5 + 5 top level symbols + 3 classes + 3 interfaces.

        with self.assertRaises(DuplicateSymbolError) as ctx:
            self.symbolTable.add_new_symbol_of_type(VariableSymbol, None, "globalVar3")
        self.assertEqual(ctx.exception.args[0]["message"], "Attempt to add duplicate symbol 'globalVar3'")

        class1 = await self.symbolTable.resolve("class1")
        self.assertIsInstance(class1, ClassSymbol)
        method2 = await class1.resolve("method2")
        self.assertIsInstance(method2, MethodSymbol)
        scopes = await method2.directScopes()
        self.assertEqual(len(scopes), 2)  # 2 anonymous blocks.
        block1 = scopes[0]
        self.assertIsInstance(block1, ScopedSymbol)

        with self.assertRaises(DuplicateSymbolError) as ctx:
            duplicateMethod = self.symbolTable.add_new_symbol_of_type(MethodSymbol, None, "method2")
            class1.addSymbol(duplicateMethod)  # Must throw.
        self.assertEqual(ctx.exception.args[0]["message"], "Attempt to add duplicate symbol 'method2'")

        variable = await block1.resolve("globalVar3")  # Resolves to the global var 3.
        self.assertIsInstance(variable, VariableSymbol)
        self.assertEqual(variable.root(), self.symbolTable)

        variable = await block1.resolve("globalVar3", True)  # Try only local vars.

        self.assertEqual(variable, None)

        variable = await block1.resolve("var1")  # Now resolves to local var.
        self.assertEqual(variable.root(), class1)
        self.assertEqual(variable.get_parent_of_type(MethodSymbol), method2)

        methods = await class1.get_symbols_of_type(MethodSymbol)
        self.assertEqual(len(methods), 3)
        symbols = await method2.get_symbols_of_type(ScopedSymbol)
        self.assertEqual(len(symbols), 2)
        self.assertEqual(await block1.resolve("class1", False), class1)

        symbolPaths = variable.symbolPath()
        self.assertEqual(len(symbolPaths), 5)
        self.assertEqual(symbolPaths[0].name, "var1")
        self.assertEqual(symbolPaths[1].name, "block1")
        self.assertEqual(symbolPaths[2].name, "method2")
        self.assertEqual(symbolPaths[3].name, "class1")
        self.assertEqual(symbolPaths[4].name, "main")

        self.assertEqual(method2.qualifiedName(), "class1.method2")
        self.assertEqual(method2.qualifiedName("-", True), "main-class1-method2")
        self.assertEqual(variable.qualifiedName(), "block1.var1")
        self.assertEqual(variable.qualifiedName("#"), "block1#var1")
        self.assertEqual(variable.qualifiedName(".", False, True), "block1.var1")
        self.assertEqual(variable.qualifiedName(".", True, False), "main.class1.method2.block1.var1")
        self.assertEqual(variable.qualifiedName(".", True, True), "main.class1.method2.block1.var1")

        allSymbols = await self.symbolTable.get_all_nested_symbols()
        self.assertEqual(len(allSymbols), 94)

        symbolPath = allSymbols[59].qualifiedName(".", True)
        self.assertEqual(symbolPath, "main.class1.method2.block1.var1")

        foundSymbol = self.symbolTable.symbol_from_path("main.class2.method0.block2.var1")
        self.assertEqual(foundSymbol, allSymbols[78])

        self.assertEqual(self.symbolTable, self.symbolTable.symbolTable())

    async def test_Single_table_stress(self):
        print('Started stress test at %s' % time.strftime('%X'))
        st = time.time()
        try:
            with test_timeout(20000):
                # TODO multithreading
                # symbolTable = await self.execute(createClassSymbolTable, name= "table", counts= [300, 30, 20, 1000,
                # 1000])
                symbolTable = await createClassSymbolTable("table", [300, 30, 20, 1000, 1000])

                symbols = await symbolTable.get_all_nested_symbols()

                self.assertEqual(len(symbols), 68600)
                symbols = await symbolTable.get_nested_symbols_of_type(ClassSymbol)
                self.assertEqual(len(symbols), 300)
                symbols = await symbolTable.get_nested_symbols_of_type(MethodSymbol)
                self.assertEqual(len(symbols), 18000)
                symbols = await symbolTable.get_nested_symbols_of_type(ScopedSymbol)
                self.assertEqual(len(symbols), 36600)

                # Includes class fields.
                symbols = await symbolTable.get_nested_symbols_of_type(VariableSymbol)
                self.assertEqual(len(symbols), 31000)
                symbols = await symbolTable.get_nested_symbols_of_type(FieldSymbol)
                self.assertEqual(len(symbols), 12000)
                symbols = await symbolTable.get_nested_symbols_of_type(LiteralSymbol)
                self.assertEqual(len(symbols), 1000)

                # symbols = symbolTable.getAllNestedSymbolsSync()
                #
                # self.assertEqual(len(symbols),68600)
                # symbols = symbolTable.getNestedSymbolsOfTypeSync(ClassSymbol)
                # self.assertEqual(len(symbols),300)
                # symbols = symbolTable.getNestedSymbolsOfTypeSync(MethodSymbol)
                # self.assertEqual(len(symbols),18000)
                # symbols = symbolTable.getNestedSymbolsOfTypeSync(ScopedSymbol)
                # self.assertEqual(len(symbols),36600)
                #
                # # Includes class fields.
                # symbols = symbolTable.getNestedSymbolsOfTypeSync(VariableSymbol)
                # self.assertEqual(len(symbols),31000)
                # symbols = symbolTable.getNestedSymbolsOfTypeSync(FieldSymbol)
                # self.assertEqual(len(symbols),12000)
                # symbols = symbolTable.getNestedSymbolsOfTypeSync(LiteralSymbol)
                # self.assertEqual(len(symbols),1000)

        except TestTimeout:
            assert False
        finally:
            print('Execution time for stress test: %f seconds' % (time.time() - st))
            print('Finished stress test at %s' % time.strftime('%X'))

    async def test_single_table_namespace(self):
        symbolTable = await createClassSymbolTable(
            "main", [30, 10, 10, 100, 100],
            ["ns1", "ns2", "ns1.ns3.ns5", "ns1.ns4.ns6.ns8"]
        )

        namespaces = await symbolTable.get_nested_symbols_of_type(NamespaceSymbol)
        self.assertEqual(len(namespaces), 7)

        # This call does a depth-first search, so all the deeper nested namespaces appear at the lower indexes
        # and the less nested ones at the end of the list.
        methods = await symbolTable.get_nested_symbols_of_type(MethodSymbol)
        self.assertEqual(len(methods), 600)
        self.assertEqual(methods[2].qualifiedName(".", True), "main.ns1.ns3.ns5.class2.method2")
        self.assertEqual(methods[299].qualifiedName(".", True), "main.ns2.class29.method9")

    async def test_multi_table(self):
        # Interactions between linked symbol tables. We use 5 tables here:
        # - the main table as in the single table tests.
        # - a system functions table
        # - a table with variables, which has 2 other dependencies (functions in same namespace as system
        #   functions and one in a different namespace)
        main = await createClassSymbolTable("main", [30, 10, 10, 100, 100])
        systemFunctions = SymbolTable("system functions", SymbolTableOptions(False))
        namespace1 = systemFunctions.add_new_symbol_of_type(NamespaceSymbol, None, "ns1")
        for i in range(333):
            systemFunctions.add_new_symbol_of_type(RoutineSymbol, namespace1, 'func%s' % i)
        main.addDependencies(systemFunctions)

        libFunctions = SymbolTable("library functions", SymbolTableOptions(False))
        namespace2 = libFunctions.add_new_symbol_of_type(NamespaceSymbol, None, "ns2")
        for i in range(444):
            # Same names as in the system functions but different namespace.
            libFunctions.add_new_symbol_of_type(RoutineSymbol, namespace2, 'func%s' % i)

        libVariables = SymbolTable("library variables", SymbolTableOptions(False))

        # Like for the system functions.
        namespace3 = libVariables.add_new_symbol_of_type(NamespaceSymbol, None, "ns1")
        for i in range(555):
            libVariables.add_new_symbol_of_type(VariableSymbol, namespace3, 'var%s' % i)

        libFunctions2 = SymbolTable("library functions 2", SymbolTableOptions(False))
        namespace4 = libFunctions2.add_new_symbol_of_type(NamespaceSymbol, None, "ns1")
        for i in range(666):
            # Same names as in the system functions but different namespace.
            libFunctions2.add_new_symbol_of_type(RoutineSymbol, namespace4, 'func%s' % i)

        libVariables.addDependencies(libFunctions, libFunctions2)
        main.addDependencies(systemFunctions, libVariables)

        # Note: namespaces are handled in the context of their parent.
        # Symbols in a namespace/module/library are accessible from their parent.
        allSymbols = await main.get_all_symbols(Symbol)
        self.assertEqual(len(allSymbols), 2262)

        allSymbols = await main.get_all_symbols(RoutineSymbol)
        self.assertEqual(len(allSymbols), 1443)

        # System functions alone + the namespace.
        self.assertEqual(len(await systemFunctions.get_all_symbols(Symbol)), 334)

        # Lib functions alone + the namespace.
        self.assertEqual(len(await libFunctions.get_all_symbols(Symbol)), 445)

        # Lib variables + lib functions + namespaces.
        self.assertEqual(len(await libVariables.get_all_symbols(Symbol)), 1668)

        # Lib functions in "ns1" only + the namespace.
        self.assertEqual(len(await libFunctions2.get_all_symbols(RoutineSymbol)), 666)

    async def test_symbol_navigation(self):
        symbolTable = await createClassSymbolTable("main", [10, 10, 10, 20, 34], [])

        namespaces = await symbolTable.get_nested_symbols_of_type(NamespaceSymbol)
        self.assertEqual(len(namespaces), 0)

        # Does not include constant values (which are literals). Still such variables may appear in
        # below navigation methods and are compared by name, instead of reference.
        variables = await symbolTable.get_nested_symbols_of_type(VariableSymbol)
        self.assertEqual(len(variables), 420)

        # A class member.
        field7 = variables[211]
        self.assertIsNotNone(field7)
        self.assertEqual(field7.firstSibling(), variables[210])
        self.assertEqual(field7.lastSibling().name, "method9")
        self.assertEqual(field7.previousSibling(), variables[210])
        self.assertEqual(field7.nextSibling(), variables[212])

        self.assertEqual(field7.firstSibling().firstSibling().firstSibling().firstSibling(), field7.firstSibling())
        self.assertEqual(field7.lastSibling().lastSibling().lastSibling().lastSibling(), field7.lastSibling())
        self.assertEqual(field7.firstSibling().lastSibling().firstSibling().firstSibling(), field7.firstSibling())
        self.assertEqual(field7.lastSibling().firstSibling().firstSibling().lastSibling(), field7.lastSibling())

        self.assertIsInstance(field7.parent(), InterfaceSymbol)

        parent7: InterfaceSymbol = field7.parent()
        self.assertEqual(parent7.indexOfChild(field7), 1)
        self.assertEqual(parent7.firstChild(), field7.firstSibling())
        self.assertEqual(parent7.lastChild(), field7.lastSibling())

        # A local variable (a single one in a block).
        var1 = variables[286]
        self.assertIsNotNone(var1)
        self.assertEqual(var1.firstSibling(), var1)
        self.assertEqual(var1.lastSibling().name, "var1")
        self.assertIsNone(var1.previousSibling())
        self.assertIsNone(var1.nextSibling())

        self.assertEqual(var1.firstSibling().firstSibling().firstSibling().firstSibling(), var1.firstSibling())
        self.assertEqual(var1.lastSibling().lastSibling().lastSibling().lastSibling(), var1.lastSibling())
        self.assertEqual(var1.firstSibling().lastSibling().firstSibling().firstSibling(), var1.firstSibling())
        self.assertEqual(var1.lastSibling().firstSibling().firstSibling().lastSibling(), var1.lastSibling())

        block1: ScopedSymbol = var1.parent()
        self.assertEqual(block1.indexOfChild(field7), -1)
        self.assertEqual(block1.indexOfChild(var1), 0)
        self.assertEqual(block1.firstChild(), var1.firstSibling())
        self.assertEqual(block1.lastChild(), var1.lastSibling())

        # A global variable.
        var15 = variables[19]
        self.assertIsNotNone(var15)
        self.assertEqual(var15.firstSibling(), symbolTable.firstChild())
        self.assertEqual(var15.lastSibling().name, "globalConst33")
        self.assertEqual(var15.previousSibling(), variables[18])
        self.assertEqual(var15.nextSibling().name, "globalConst0")

        self.assertIsInstance(var15.parent(), SymbolTable)

        st1: ScopedSymbol = var15.parent()
        self.assertEqual(st1.indexOfChild(var15), 39)
        self.assertEqual(st1.firstChild(), var15.firstSibling())
        self.assertEqual(st1.lastChild(), var15.lastSibling())

        next = variables[284].next()
        self.assertIsNotNone(next)
        self.assertEqual(next.qualifiedName(".", True), "main.class6.method7.block1.var1")

        symbol = await symbolTable.symbol_with_context(dummyNode)
        self.assertIsNotNone(symbol)
        self.assertEqual(symbol.qualifiedName(".", True), "main.class0.method1.block2.var1")
