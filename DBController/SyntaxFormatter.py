import abc

class SyntaxFormatter:
    __metaclass__ = abc.ABCMeta

    __keywordsSingle   = ["SELECT ", "FROM ", "GROUP BY ", "HAVING ", "WHERE "]
    __keywordsMultiple = ["JOIN ", "ON ", "IS ", "IN ", "LIKE ", "AND ", "OR ", "NOT "]

    @staticmethod
    def __addSchemaAfter(keyword, command):
        if keyword in command:
            command = command[:command.index(keyword) + len(keyword)] + "PROJECT1." + command[command.index(keyword) + len(keyword):]
        return command
    @staticmethod
    def __addSchemaAfterMultiple(keyword, command):
        lastKeywordPosition = 0
        while keyword in command[lastKeywordPosition:]:
            command = SyntaxFormatter.__addSchemaAfter(keyword, command[lastKeywordPosition:])
            lastKeywordPosition = command[lastKeywordPosition:].index(keyword) + len(keyword)
        return command
    @staticmethod
    def __addSchemaToTables(command):
        command = SyntaxFormatter.__addSchemaAfter("FROM ", command)
        command = SyntaxFormatter.__addSchemaAfterMultiple("JOIN ", command)
        return command



    @staticmethod
    def __upperKeyword(keyword, command):
        if keyword in command.upper():
            command = command[:command.upper().index(keyword)] + keyword + command[command.upper().index(keyword) + len(keyword):]
        return command
    @staticmethod
    def __upperKeywordMultiple(keyword, command):
        lastKeywordPosition = 0
        while keyword in command[lastKeywordPosition:].upper():
            command = SyntaxFormatter.__upperKeyword(keyword, command[lastKeywordPosition:])
            lastKeywordPosition = command[lastKeywordPosition:].index(keyword) + len(keyword)
        return command
    @staticmethod
    def __upperKeywords(command):
        for keyword in SyntaxFormatter.__keywordsSingle:
            command = SyntaxFormatter.__upperKeyword(keyword, command)

        for keyword in SyntaxFormatter.__keywordsMultiple:
            command = SyntaxFormatter.__upperKeywordMultiple(keyword, command)

        return command



    @staticmethod
    def formatCommand(command):
        if str(command).startswith("select") or str(command).startswith("SELECT"):
            command = SyntaxFormatter.__addSchemaToTables(command)
        return command