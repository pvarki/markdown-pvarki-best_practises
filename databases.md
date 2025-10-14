# Database guidelines

## Use Postgres

Or PostGIS in case the GIS extensions are needed. Many ORMs and other abstractions work best with pg
and it also has very handy native JSON datatype for those who don't want to design their schemas (aka NoSQL)
or just for some random extra info that generally does not need to be queried often.

## User abstraction layers of the language

**Never** construct queries by simple string formatting/concatenation, that way lies [SQL injections][bobtable]

For Python at very least use [SQLAlchemy][sa] (and use it correctly), for pretty nice ORM/abstraction that plays
very nice with asyncio (SQLAlchemy is only just getting there) check out [Gino][gino]

[bobtable]: https://xkcd.com/327/
[gino]: https://python-gino.org/
[sa]: https://docs.sqlalchemy.org/en/20/

## In OO languages abstract db access to classes

Regardless of using ORM or not, make a class that abstracts database
access to data behind OO API so when database implementationd details
inevitably change it's easy to change them just in the abstraction
instead of all the places that used the same copy-pasted queries to
access the data.

Be DRY (Don't Repeat Yourself)
