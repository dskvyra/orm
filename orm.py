import  orm_supplies
import models
from models import *

QOUTE_VALUE_STRING = """'{}'"""
SELECT_STRING = """SELECT * FROM {table_name} WHERE {table_name}_id = %s;"""
UPDATE_STRING = """UPDATE {table_name} SET {field_names} = ({field_values}) WHERE {table_name}_id = %s;"""
INSERT_STRING = """INSERT INTO {table_name} ({field_names}) VALUES ({field_values});"""
DELETE_STRING = """DELETE FROM {table_name} WHERE {table_name}_id = %s;"""
SELECT_ALL = """SELECT * FROM {table_name};"""
RELATION_STRING = """SELECT * FROM {relation_name} WHERE {table_name}_id = %s;"""
JOIN = """SELECT * FROM {relation_table_name} NATURAL JOIN {result_table} WHERE {table_name}_id = %s;"""

class Entity(object):
	_db = orm_supplies.orm_db()

	def __init__(self, table_id = None):
		self._fields_dict = {}
		self._table_id = table_id
		self._table_name = self.__class__.__name__.lower()
		self._loaded = False

	def __str__(self):
		s = []

		for field_name, field_value in self._fields_dict.items():
				s.append('%s =  %s' % (field_name, field_value))
		return '{} with ID#{} : {}'.format(self.__class__.__name__, 
						self._table_id,
						', '.join(s))

	def __getattr__(self, attr):
		if attr in self._fields:
			self._load(attr)
			return self._fields_dict['%s_%s' % (self._table_name, attr)]
		elif attr in self._parents:
			self._load(attr)
			return self._build_parents(attr)
		elif attr in self._children.keys():
			return self._build_children(attr)
		elif attr in self._siblings.keys():
			return self._build_siblings(attr)
		else:
			raise AttributeError('404') 

	def __setattr__(self, attr, attr_value):
		if attr in self._fields:
			self._fields_dict['%s_%s' % (self._table_name, attr)] = attr_value
		elif attr in self._parents:
			self._fields_dict['%s_id' % attr] = attr_value._table_id
		else:
			object.__setattr__(self, attr, attr_value)

	def _load(self, field):
		if self._loaded != True:
			query = SELECT_STRING.format(table_name = self._table_name,
							table_id = self._table_id)
			self._db.cursor.execute(query, (self._table_id,))
			self._loaded = True
			self._fields_dict = self._db.cursor.fetchone()

	def _build_parents(self, parent_name):
		parent_id = self._fields_dict['%s_id' % parent_name]
		parent_class = parent_name.title()
		parent = getattr(models, parent_class)
		
		return parent(parent_id)

	def _build_children(self, child_name):
		child_name = self._children[child_name].lower()
		query = RELATION_STRING.format(relation_name = child_name,
						table_name = self._table_name,
						table_id = self._table_id)
		self._db.cursor.execute(query, (self._table_id,))

		raw_children = self._db.cursor.fetchall()
		child_class_name = getattr(models, child_name.title())
		children = []
		
		for raw_child in raw_children:
			child = child_class_name(raw_child['%s_id' %child_name])
			child._fields_dict = dict(raw_child)
			child._loaded = True
			children.append(child)
		
		return children

	def _build_query(self, template, field_names, place_amount):
	        places = ', '.join(['%s'] * place_amount)
	        field_names = ', '.join(field_names)
	        query =  template.format(table_name = self._table_name,
	                               field_names = field_names,
	                               field_values = places)

	        return query

	def _build_siblings(self, sibling_name):
		sibling_name = self._siblings[sibling_name].lower()
		relation_table = '_'.join(sorted([sibling_name, self._table_name]))
		query = JOIN.format(relation_table_name = sibling_name,
				result_table = relation_table,
				table_name = self._table_name,
				table_id = self._table_id)

		self._db.cursor.execute(query, (self._table_id,))

		raw_siblings = self._db.cursor.fetchall()
		sibling_class_name = getattr(models, sibling_name.title())
		siblings = []
		
		for raw_sibling in raw_siblings:
			sibling = sibling_class_name(raw_sibling['%s_id' % sibling_name])
			sibling._fields_dict = dict(raw_sibling)
			sibling._loaded = True
			siblings.append(sibling)

		return siblings
		
	@classmethod
	def all(cls):
		table_name = cls.__name__.lower()
		class_name = cls
		query = SELECT_ALL.format(table_name = table_name)

		cls._db.cursor.execute(query)
		raw_entities = cls._db.cursor.fetchall()
		class_entities = []
		
		for raw_table in raw_entities:
			table = class_name(raw_table['%s_id' % table_name])
			table._fields_dict = raw_table
			table._loaded = True
			class_entities.append(table)

		return class_entities
	
	def _update(self):
		field_names = []
		field_values = []

		for field_name, field_value in self._fields_dict.items():
			field_names.append(field_name)
			field_values.append(QOUTE_VALUE_STRING.format(field_value))
		query = self._build_query(UPDATE_STRING, field_names, field_values)
		field_values.append((self._table_id,))
		self._db.cursor.execute(query, field_values)
		self._db.commit()

	def _insert(self):
		field_names = []
		field_values = []

		for field_name, field_value in self._fields_dict.items():
			field_names.append(field_name)
			field_values.append(QOUTE_VALUE_STRING.format(field_value))
		query = self._build_query(INSERT_STRING, field_names, len(field_values))

		self._db.cursor.execute(query, field_values)
		self._db.commit()

	def save(self):
		if self._table_id != None:
			self._update()
		else:
			self._insert()

	def delete(self):
		if not self._table_id:
			raise RuntimeError

		query = DELETE_STRING.format(table_name = self._table_name,
						table_id = self._table_id)

		self._db.cursor.execute(query, (self._table_id,))


if __name__ == '__main__':
	t = Tag(1)
	print t.value
	a = Article(1)
	print a.title
	a.title = 'test1'
	print a.title
	print a.text
	ab = Article()
	ab.title = 'ess'
	ab.save()
	print(a.title)
	print(a.category.title)

	for each in Article.all():
		print each.title

	category = Category(2)
	for article in category.articles: # select * from article where category_id=?
		print(article.text)

	article = Article(1)
	for tag in article.tags: # select * from tag natural join article_tag where article_id=?
	   print(tag.value)

	article.category = Category(2)
	print article.category