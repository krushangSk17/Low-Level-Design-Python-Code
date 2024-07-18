import datetime
from abc import ABC, abstractmethod

class User:
    ID = 0
    def __init__(self, username, email) -> None:
        self.id = type(self).ID
        type(self).ID += 1
        self.username = username
        self.email = email
        self.reputation = 0
        self.questions = []
        self.answers = []
        self.comments = []

class Commentable(ABC):
    @abstractmethod
    def addComment(self, user, comment):
        pass

    @abstractmethod
    def getComments(self):
        pass

class Votable(ABC):
    @abstractmethod
    def addVote(self, user, vote):
        pass

    @abstractmethod
    def getVotes(self):
        pass

class Question(Commentable, Votable):
    ID = 0
    def __init__(self, user, title, content, tags) -> None:
        self.id = type(self).ID
        type(self).ID += 1
        self.title = title
        self.content = content
        self.tags = tags
        self.author = user
        self.creationDate = datetime.date.today()
        self.answers = []
        self.comments = []
        self.votes = []

    def addComment(self, user, comment):
        self.comments.append((user, comment))

    def getComments(self):
        return self.comments

    def addVote(self, user, vote):
        self.votes.append((user, vote))

    def getVotes(self):
        return self.votes

class Answer(Commentable, Votable):
    ID = 0
    def __init__(self, user, question, content) -> None:
        self.id = type(self).ID
        type(self).ID += 1
        self.question = question
        self.content = content
        self.author = user
        self.creationDate = datetime.date.today()
        self.comments = []
        self.votes = []
        self.isAccepted = False

    def addComment(self, user, comment):
        self.comments.append((user, comment))

    def getComments(self):
        return self.comments

    def addVote(self, user, vote):
        self.votes.append((user, vote))

    def getVotes(self):
        return self.votes

class Comment:
    ID = 0
    def __init__(self, user, commentable: Commentable, comment) -> None:
        self.id = type(self).ID
        type(self).ID += 1
        self.comment = comment
        self.author = user
        self.creationDate = datetime.date.today()
        commentable.addComment(user, comment)

class Vote:
    ID = 0
    def __init__(self, user, votable: Votable, vote) -> None:
        self.id = type(self).ID
        type(self).ID += 1
        self.vote = vote
        self.author = user
        self.creationDate = datetime.date.today()
        votable.addVote(user, vote)

class Tag:
    ID = 0
    tags = {}  # Using a dictionary to manage tags and associated questions

    def __init__(self, title) -> None:
        
        if title in Tag.tags:
            raise ValueError("Tag already exists.")
        
        self.id = type(self).ID
        type(self).ID += 1
        self.title = title
        self.questions = []
        
        Tag.tags[title] = self

    def addQuestion(self, question):
        self.questions.append(question)

class StackOverFlow:
    def __init__(self):
        self.users = []
        self.questions = []
        self.answers = []
        self.comments = []
        self.votes = []
        self.tags = []

    def addUser(self, username, email):
        user = User(username, email)
        self.users.append(user)
        return user

    def addQuestion(self, user, title, content, tag_titles):
        tags = [self.getOrCreateTag(title) for title in tag_titles]
        question = Question(user, title, content, tags)
        self.questions.append(question)
        for tag in tags:
            tag.addQuestion(question)
        return question

    def getOrCreateTag(self, title):
        if title in Tag.tags:
            return Tag.tags[title]
        else:
            return Tag(title)

    def addAnswer(self, user, question, content):
        answer = Answer(user, question, content)
        self.answers.append(answer)
        question.answers.append(answer)
        return answer

    def addCommentT
