CREATE TABLE "category" (
category_id serial,
category_title varchar(50),
category_created timestamp NOT NULL DEFAULT current_timestamp,
category_updated timestamp DEFAULT NULL,
PRIMARY KEY (category_id)
);

CREATE TABLE "tag" (
tag_id serial,
tag_value varchar(50),
tag_created timestamp NOT NULL DEFAULT current_timestamp,
tag_updated timestamp DEFAULT NULL,
PRIMARY KEY (tag_id)
);

CREATE TABLE "article" (
article_id serial,
article_text text,
article_title varchar(50),
article_created timestamp NOT NULL DEFAULT current_timestamp,
article_updated timestamp DEFAULT NULL,
PRIMARY KEY (article_id)
);

ALTER TABLE "article" ADD COLUMN category_id integer;
ALTER TABLE "article" ADD CONSTRAINT fk_article_category FOREIGN KEY (category_id) REFERENCES "category" (category_id);

CREATE TABLE article_tag (
article_id integer REFERENCES article (article_id) ON UPDATE CASCADE ON DELETE CASCADE,
tag_id integer REFERENCES tag (tag_id) ON UPDATE CASCADE,
CONSTRAINT article_tag_pkey PRIMARY KEY (article_id,tag_id)
);

insert into "tag" (tag_value) values ('Hello1');
insert into "tag" (tag_value) values ('Hello2');
insert into "tag" (tag_value) values ('Hello3');
insert into "tag" (tag_value) values ('Hello4');
insert into "tag" (tag_value) values ('Hello5');

insert into "category" (category_title) values ('Uno');
insert into "category" (category_title) values ('Uno1');
insert into "category" (category_title) values ('Uno2');
insert into "category" (category_title) values ('Uno3');
insert into "category" (category_title) values ('Uno4');

insert into "article" (category_id, article_title, article_text) values (1, 'zzz11', '1Hello5sfdsfdsfsdf');
insert into "article" (category_id, article_title, article_text) values (1, 'zzz12', '2Hello5sfdsfdsfsdf');
insert into "article" (category_id, article_title, article_text) values (3, 'zzz123', '12Hello5sfdsfdsfsdf');
insert into "article" (category_id, article_title, article_text) values (2, 'zzz134', '32Hello5sfdsfdsfsdf');
insert into "article" (category_id, article_title, article_text) values (1, 'zzz132', '42Hello5sfdsfdsfsdf');
insert into "article" (category_id, article_title, article_text) values (2, 'zzz155', '321Hello5sfdsfdsfsdf');

insert into article_tag (article_id, tag_id) values (1, 2)
insert into article_tag (article_id, tag_id) values (1, 3)
insert into article_tag (article_id, tag_id) values (1, 1)
insert into article_tag (article_id, tag_id) values (2, 2)
insert into article_tag (article_id, tag_id) values (2, 1)
