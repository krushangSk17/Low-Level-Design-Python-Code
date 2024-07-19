"""
BLUEPRINT TO UNDERSTAND IT BETTER
LLD STACKOVERFLOW SIMULATION SYSTEM

Classes:
1. User: Represents platform users.
   - Attributes: id, username, email, reputation, questions, answers, comments

2. Commentable (ABC): Abstract base class for items that can be commented on.
   - Methods: addComment(user, comment), getComments()

3. Votable (ABC): Abstract base class for items that can receive votes.
   - Methods: addVote(user, vote), getVotes()

4. Question: Represents questions posted by users.   - Inherits: Commentable, Votable
   - Attributes: id, title, content, tags, author, creationDate, answers, comments, votes
   - Methods: addComment, getComments, addVote, getVotes

5. Answer: Represents answers to questions.   - Inherits: Commentable, Votable
   - Attributes: id, question, content, author, creationDate, comments, votes, isAccepted
   - Methods: addComment, getComments, addVote, getVotes

6. Comment: Represents comments on questions or answers.
   - Attributes: id, comment, author, creationDate, commentable

7. Vote: Represents votes on questions or answers.
   - Attributes: id, vote, author, creationDate, votable

8. Tag: Represents tags associated with questions.
   - Attributes: id, title, questions
   - Methods: addQuestion()

9. StackOverFlow: Manages the overall operations of the platform.
   - Attributes: users, questions, answers, comments, votes, tags
   - Methods: addUser, addQuestion, getOrCreateTag, addAnswer, addCommentToQuestion, addCommentToAnswer, addVoteToQuestion, addVoteToAnswer, findUser, findQuestion, findAnswer

Usage:
- Initialize the system.
- Add and manage users, questions, answers, comments, and votes.
- Link questions with tags and manage tag associations.
"""


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


if __name__ == "__main__":
    # Create the StackOverFlow platform instance
    platform = StackOverFlow()

    # Adding some users
    user1 = platform.addUser("john_doe", "john@example.com")
    user2 = platform.addUser("jane_smith", "jane@example.com")

    # Print user information
    print("Users:")
    for user in platform.users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")

    # Adding some tags
    tag1 = platform.getOrCreateTag("python")
    tag2 = platform.getOrCreateTag("machine-learning")

    # Adding questions
    question1 = platform.addQuestion(user1, "How to use lists in Python?", "I'm new to Python and need help with lists.", ["python"])
    question2 = platform.addQuestion(user2, "What is machine learning?", "Can someone explain what machine learning is?", ["machine-learning", "python"])

    # Adding answers
    answer1 = platform.addAnswer(user2, question1, "Lists in Python are created by placing the items inside square brackets [].")
    answer2 = platform.addAnswer(user1, question2, "Machine learning is a field of AI that uses statistical techniques to give computer systems the ability to 'learn'.")

    # Adding comments
    comment1 = platform.addCommentToQuestion(user2, question1, "This is a great question!")
    comment2 = platform.addCommentToAnswer(user1, answer1, "Thanks for the explanation.")

    # Adding votes
    vote1 = platform.addVoteToQuestion(user2, question1, 1)
    vote2 = platform.addVoteToAnswer(user1, answer1, 1)

    # Printing the details of questions, answers, comments, and votes
    print("\nQuestions:")
    for question in platform.questions:
        print(f"Title: {question.title}, Content: {question.content}, Tags: {[tag.title for tag in question.tags]}")
        print("Comments on Question:")
        for comment in question.getComments():
            print(f"  {comment[0].username} said: {comment[1]}")
        print("Votes on Question:")
        for vote in question.getVotes():
            print(f"  {vote[0].username} voted: {vote[1]}")
        print("Answers:")
        for answer in question.answers:
            print(f"  {answer.author.username} answered: {answer.content}")
            print("  Comments on Answer:")
            for comment in answer.getComments():
                print(f"    {comment[0].username} said: {comment[1]}")
            print("  Votes on Answer:")
            for vote in answer.getVotes():
                print(f"    {vote[0].username} voted: {vote[1]}")

    # Printing tags and associated questions
    print("\nTags and Associated Questions:")
    for tag in platform.tags:
        print(f"Tag: {tag.title}")
        for question in tag.questions:
            print(f"  Question: {question.title}")
