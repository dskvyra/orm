# from orm import Entity

# class Article(Entity):
#     _fields = ['title', 'text']
#     _parents = ['category']
#     _children = []
#     _siblings = ['tags']

# class Category(Entity):
#     _fields = ['title']
#     _parents = []
#     _children = ['articles']
#     _siblings = []

# class Tag(Entity):
#     _fields = ['value']
#     _parents = []
#     _children = []
#     _siblings = ['articles']

from orm import Entity

class Article(Entity):
    _fields = ['title', 'text']
    _parents = ['category']
    _children = {}
    _siblings = {'tags':'Tag'}

class Category(Entity):
    _fields = ['title']
    _parents = []
    _children = {'articles':'Article'}
    _siblings = {}

class Tag(Entity):
    _fields = ['value']
    _parents = []
    _children = {}
    _siblings = {'articles':'Article'}

