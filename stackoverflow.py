import datetime
from abc import ABC, abstractmethod

class User:
    ID = 0
    def __init__(self, username, email) -> None:
        self.id = type(self).ID
        self.username = username
        self.email = email
        type(self).ID += 1
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
    tag_set = set()
    def __init__(self, title) -> None:
        self.id = type(self).ID
        type(self).ID += 1
        if title not in type(self).tag_set:
            self.title = title
            type(self).tag_set.add(title)
        else:
            raise Exception("Tag already exists.")


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
        tags = [self.addTag(title) for title in tag_titles]
        question = Question(user, title, content, tags)
        self.questions.append(question)
        return question

    def addAnswer(self, user, question, content):
        answer = Answer(user, question, content)
        self.answers.append(answer)
        question.answers.append(answer)
        return answer

    def addCommentToQuestion(self, user, question, comment):
        comment_obj = Comment(user, question, comment)
        self.comments.append(comment_obj)
        return comment_obj

    def addCommentToAnswer(self, user, answer, comment):
        comment_obj = Comment(user, answer, comment)
        self.comments.append(comment_obj)
        return comment_obj

    def addVoteToQuestion(self, user, question, vote):
        vote_obj = Vote(user, question, vote)
        self.votes.append(vote_obj)
        return vote_obj

    def addVoteToAnswer(self, user, answer, vote):
        vote_obj = Vote(user, answer, vote)
        self.votes.append(vote_obj)
        return vote_obj

    def addTag(self, title):
        try:
            tag = Tag(title)
            self.tags.append(tag)
            return tag
        except Exception as e:
            for tag in self.tags:
                if tag.title == title:
                    return tag

    def findUser(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def findQuestion(self, question_id):
        for question in self.questions:
            if question.id == question_id:
                return question
        return None

    def findAnswer(self, answer_id):
        for answer in self.answers:
            if answer.id == answer_id:
                return answer
        return None
