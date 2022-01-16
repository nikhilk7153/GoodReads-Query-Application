from bson.json_util import dumps
from pymongo import MongoClient
import re

mongo = client = MongoClient("mongodb+srv://nikhilk5:fluffy63@cluster0.pj5mb.mongodb.net/Goodreads?retryWrites=true&w=majority")
db = mongo["Goodreads"]
serverStatusResult = db.command("serverStatus")

class QueryParser:

    '''
    The following code is meant to serve as an implementation for a query language interpreter and is meant to represent
    a simplified version of the Elasticsearch's query language. Specifically, this class implements the >, <, :, .,
    "OR", "NOT," "AND", and "", operators for querying specific types. This will perform a MongoDB query to get the data.
    '''

    @staticmethod
    def createSeparateQueries(queryString):
        '''
        Decomposes the string by splitting the query into it's and/or components and sends it for further splitting
        :param queryString: is the queryString that is specified by the users
        '''
        queries = None
        chainType = None

        if "AND" in queryString:
            chainType = "AND"
            queries = QueryParser.splitANDandOR(queryString, "AND")

        elif "OR" in queryString:
            chainType = "OR"
            queries = QueryParser.splitANDandOR(queryString, "OR")
        else:
            queries = [queryString]

        return QueryParser.getQueryParts(queries, chainType)


    def getQueryParts(queries, chainType):
        '''
        Function splits the queries into their operator, field, and value
        :param queries: a list of all the queries that need to be performed after splitting with and/or
        :param chainType: tells whether there is an "AND", "OR", or other type of split
        :param queryString: gives the original user string
        '''

        decomposedQueries = []
        decomposedQueries.append(chainType)

        for query in queries:

            object = QueryParser.splitByDot(query)[0]
            fieldAndExpression = QueryParser.splitByDot(query)[1]

            field = QueryParser.splitByColon(object, fieldAndExpression)[0]
            expression = QueryParser.splitByColon(object, fieldAndExpression)[1]

            operator = QueryParser.findOperator(expression)[0]
            value = QueryParser.findOperator(expression)[1]
            value = QueryParser.modifyValueType(field, value)
            QueryParser.isValidOperator(value, operator)
            decomposedQueries.append({"object": object, "field": field, "operator": operator, "value": value})

        return QueryParser.executeMongoQuery(decomposedQueries)

    def splitANDandOR(queryString, oper_name):
        '''
        Splits the original query and checks if there are any AND/OR operator
        :param queryString: the original query string that is specified by the user
        :param oper_name: specifies the operator name (either AND/OR)
        :return: The queryStrings after splitting on the AND/OR
        '''

        leftTrimmed = queryString.lstrip(" ")
        fullTrimmed = leftTrimmed.rstrip(" ")
        regexStr = r"\s+" + oper_name + "\s+"

        if oper_name in fullTrimmed and re.split(regexStr, fullTrimmed)[0] == "":
            raise ValueError("Insert an expression before " + oper_name + " statement")

        statements = fullTrimmed.split(oper_name)

        if fullTrimmed.split(oper_name)[len(statements) - 1] == "":
            raise ValueError("Insert an expression after " + oper_name + " statement")

        return statements

    def splitByDot(statement):
        '''
        Splits the query statement into the object and the component which contains the field and the expression
        :param statement: is query on which the split will be performed
        :return an array which is provides the two components following the split
        '''

        statement = statement.rstrip().lstrip()

        if "." not in statement:
            raise ValueError("Need to invoke operator on a field for object")

        object = statement.split(".", 1)[0]
        if QueryParser.isValidObject(object):
            fieldAndExpression = statement.split(".", 1)[1]
            return [object, fieldAndExpression]

    def splitByColon(object, fieldAndExpression):
        '''
        Splits the queryString and returns its field and expression
        :param queryString: gives the original query string
        :param fieldAndExpression: is the string corresponding to the field and the expression following it
        :return: the field and expression separately
        '''

        if ":" in fieldAndExpression:
            field = fieldAndExpression.split(":", 1)[0]
            QueryParser.isValidField(object, field)
            expression = fieldAndExpression.split(":", 1)[1]
            return [field, expression]
        else:
            raise ValueError("Need to use a valid operator to specify the query you need to")

    def isValidObject(object):
        '''
        Determines whether or not the object is a book or author
        :param object: the string that is obtained from the left-hand side of the split with the "." operator
        :return: whether or not the string is an author or book
        '''

        if object == "book" or object == "author":
            return True
        else:
            raise ValueError("Please specify a valid object")

    def isValidField(object, field):
        '''
        Returns whether or not the field is valid or not.
        :param object: either a book or author for which we are trying to get the object field
        :param field: the field which is being queried for the object
        :return: whether or not the field is valid
        '''

        if object == "book":

            bookFieldList = ["book_url", "title", "book_id", "ISBN",
                             "author_url", "author", "rating",
                             "rating_count", "review_count", "image_url",
                             "similar_books"]

            if field not in bookFieldList:
                raise ValueError("Please enter a valid book field")

        if object == "author":
            authorFieldList = ["name", "author_url", "author_id",
                               "rating", "rating_count", "review_count",
                               "image_url", "related_authors", "author_books"]

            if field not in authorFieldList:
                raise ValueError("Please enter a valid author field")

        return True

    def modifyValueType(field, value):
        '''
        Checks that the value is an appropriate one for the field and modifies it from a string if a float or int
        :param field: the field that will be queried for
        :param value: the value that the user is searching for
        :return: value that will be queried for
        '''

        integer_fields = ["book_id", "author_id", "rating_count", "review_count", "ISBN"]
        float_fields = ["rating"]
        string_fields = ["image_url", "book_url", "author_url", "name", "author", "title"]

        if field in integer_fields:
            if value.isdigit():
                return int(value)
            else:
                raise ValueError("Please enter a valid value for " + field)

        elif field in float_fields:
            try:
                float(value)
                return float(value)
            except:
                raise ValueError("Please enter a valid value for " + field)

        else:
            if isinstance(value, str) and value.isdigit() is not True:
                return value
            else:
                raise ValueError("Please enter a valid value for " + field)

    def isValidOperator(value, operator):
        '''
        Returns whether or not the operator is valid one based on the value that is being invoked on it
        :param value: specifies the value that will be invoked for this class
        :param operator: specifies the operator that will be in
        :return: a boolean to indicate whether or not the operator is a good one or not
        '''

        if operator == ">" or operator == "<":
            if isinstance(value, str):
                raise ValueError("Operator cannot be invoked on this value")
        return True

    def findOperator(expression):
        '''
        :param expression: gives the expression which contains the operator and the value which is being operated on it
        :return: the operator separated by the string based on which operator is being invoked
        '''

        if "NOT" in expression:
            return QueryParser.getOperatorAndValue("NOT", expression)
        elif ">" in expression:
            return QueryParser.getOperatorAndValue(">", expression)
        elif "<" in expression:
            return QueryParser.getOperatorAndValue("<", expression)
        elif "\"" in expression:
            return QueryParser.getOperatorAndValue("\"", expression)
        else:
            return QueryParser.getOperatorAndValue("Regex", expression)

    def getOperatorAndValue(operator, expression):
        '''
        Returns the operator and the value for the string
        :param operator: provides the operator that will be invoked on this string
        :param expression: string containing the operator and the value being invoked on it
        :return: The value and the operator that will be invoked on it
        '''

        expression = expression.rstrip().lstrip()

        if operator == "Regex":
            return ["Regex", expression]
        elif operator == "\"":
            expression = expression.strip('"')
            return ["\"", expression]
        else:
            value = re.split(operator, expression)[1].rstrip().lstrip()
        return [operator, value]

    def executeMongoQuery(decomposedQuery):
        '''
        Executes the MongoDB Query after a call to the function
        :param decomposedQuery: dictionary hold the object, field, operator, and value for the decomposed query
        :return: the MongoQuery
        '''
        chainType = decomposedQuery[0]
        object = decomposedQuery[1]["object"]
        field = decomposedQuery[1]["field"]
        value = decomposedQuery[1]["value"]
        queryResult = []
        first_clause = QueryParser.initializefindClause(decomposedQuery[1])

        if chainType == "AND":
            second_clause = QueryParser.initializefindClause(decomposedQuery[2])
            queryResult = db.get_collection(object).find({"$and": [first_clause, second_clause]})
        elif chainType == "OR":
            second_clause = QueryParser.initializefindClause(decomposedQuery[2])
            queryResult = db.get_collection(object).find({"$or": [first_clause, second_clause]})
        else:

            queryResult = db.get_collection(object).find(first_clause)

        return dumps(list(queryResult))

    def initializefindClause(decomposedQuery):
        '''
        Returns the MongoDB query that will be used inside the find() operator
        :param decomposedQuery: dictionary holding the object, field, operator, and value for the decomposed query
        :return: a dictionary which will be used for the MongoDB query
        '''

        field = decomposedQuery["field"]
        operator = decomposedQuery["operator"]
        value = decomposedQuery["value"]
        if operator == "<":
            return {field: {"$lt": value}}
        elif operator == ">":
            return {field: {"$gt": value}}
        elif operator == "NOT":
            return {field: {"$not": {"$eq": value}}}
        elif operator == "Regex" and isinstance(value, str):
            return {field: {"$regex": value}}
        elif operator == "\"" or isinstance(value, int):
            return {field: value}
