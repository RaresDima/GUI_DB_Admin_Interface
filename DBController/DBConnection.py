import cx_Oracle
from SyntaxFormatter import *

class DBConnection:
    def __init__(self, addr):
        self.__dbAddress = addr
        self.__dbConnection = cx_Oracle.connect(self.__dbAddress)
        self.__dbCursor = self.__dbConnection.cursor()
        self.__statementResult = []



    # Every method of this class will print the error codes and messages to the console in case they are encountered, also returning the error message

    @staticmethod
    def connect(username, password, dbAddress): # Connects to the Oracled DB at the specified address using the given username and password
        try:

            return DBConnection(str(username + "/" + password + "@" + dbAddress))

        except cx_Oracle.Error as e:

            e, = e.args
            print "ERROR", e.message
            return e.message

    def close(self): # Closes the connection to the DB
        try:

            self.__dbCursor.close()
            self.__dbConnection.close()

        except cx_Oracle.Error as e:

            e, = e.args
            print "ERROR", e.message
            return e.message

    def version(self): # Returns the version of the connected DB
        try:

            return self.__dbConnection.version

        except cx_Oracle.Error as e:

            e, = e.args
            print "ERROR", e.message
            return e.message

    def execute(self, command): # Formats the given string and executes it as an SQL command, returning a list of tuples corresponding to the result
        try:

            command = SyntaxFormatter.formatCommand(command)
            self.__dbCursor.execute(command)
            self.__statementResult = self.__dbCursor.fetchall()
            return self.__statementResult

        except cx_Oracle.Error as e:

            e, = e.args

            if str(command).startswith("select") or str(command).startswith("SELECT"):
                print "ERROR", e.message
                return "ERROR " + e.message
            else:
                print "ERROR", e#.message
                return "ERROR " + e#.message


    def getResults(self, n): # Returns a list of tuples corresponding to the first n results of the last executed command
        try:

            return self.__statementResult[:n-1]

        except cx_Oracle.Error as e:

            e, = e.args
            print "ERROR", e.message
            return e.message
    def getResultsAll(self): # Returns a list of tuples corresponding to the results of the last executed command
        try:

            return self.__statementResult

        except cx_Oracle.Error as e:

            e, = e.args
            print "ERROR", e.message
            return e.message
    def getResultsInRange(self, start, stop): # Returns a list of tuples corresponding to the results of the last executed command, with an index in the [start, stop] range
        try:

            return self.__statementResult[start:stop]

        except cx_Oracle.Error as e:

            e, = e.args
            print "ERROR", e.message
            return e.message
    def getResultsInPagesOf(self, pageSize): # Returns a list of "pages", lists of tuples, corresponding to the results of the last executed command
        try:

            pages       = int(len(self.__statementResult) / pageSize)
            resultPages = []

            for i in range(pages):
                resultPages.append(self.__statementResult[i*pageSize : i*pageSize + pageSize])

            resultPages.append(self.__statementResult[pages*pageSize:])

            return resultPages

        except cx_Oracle.Error as e:

            e, = e.args
            print "ERROR", e.message
            return e.message

    def callFunction(self, funcName, returnType, parameters): # Calls the DB funtion with the given name and arguments, returning the result as a variable of the given type
        try:

            return self.__dbCursor.callfunc(funcName, returnType, parameters)

        except cx_Oracle.Error as e:

            e, = e.args
            print "ERROR", e.message
            return e.message
    def callProcedure(self, procName, parameters): # Calls the provided procedure with the provided arguments, returning a copy of the parameres list, with the "out" parameters modified
        try:

            return self.__dbCursor.callproc(procName, parameters)

        except cx_Oracle.Error as e:

            e, = e.args
            print "ERROR", e.message
            return e.message