class UserNotUniqueException(Exception):
    def UserNotUniqueException(self):
        raise UserNotUniqueException('User is not unique')


class EmailNotSentException(Exception):
    pass


class TokenMissingException(Exception):
    pass


