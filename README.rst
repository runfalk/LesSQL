LesSQL
======
LesSQL, pronounced *Less sequel*, allows you to be more productive by writing complex and boilerplate SQL for you. It is inspired by Canonical's excellent `Storm ORM <https://storm.canonical.com/>`_. Sadly its development has slowed down a lot in recent years, and there hasn't been a release since 2013. LesSQL aims to be a spiritual successor of Storm, though not necessarily a 1:1 feature parity.


Problems with Storm
-------------------
No python 3 support
  Python 3 support `is not in development <https://bugs.launchpad.net/storm/+bug/1530734>`_. Since Python 2's end of life is closing in (2020), and lots of libraries support Python 3 now, it's holding back Python 3 adoption (for me).
No support for Psycopg2 2.5 and later (released 13 Apr 2013)
  No `support for Psycopg2 <https://bugs.launchpad.net/storm/+bug/1170063>`_ 2.5 and later. Though fixes are in trunk they are still unreleased. This means hacks are required to get JSON and JSONB types working.
No common table expression support
  No support for common table expressions, though there has been `a proposed solution <https://code.launchpad.net/~lifeless/storm/with/+merge/52630>`_ since 2011.
No easy custom type support
  PostgreSQL has excellent support for compound data types. In many applications ``timestamprange`` or ``daterange`` are much better than working with ``date_start`` and ``date_end`` columns. Implementing these require `quite a bit of effort <https://github.com/runfalk/stormspans>`_.
Sparse documentation
  Storm's documentation is unfinished and doesn't describe many core features. Its API documentation is also very incomplete making it difficult to extend functionality.
Global debuging hooks
  Debugging hooks are global across all threads always, which may or may not cause issues. Web applications often run many concurrent threads, and adding a debugger globally which may only be needed for a particular request or connection adds unnecessary complexity and degrades performance.
No unit testing support
  Storm has no built-in facilities to simplify testing, such as providing fake data, eliminating the need for a real database in many tests. A problem with running tests against a live database is that it is very time consuming to rebuild fixtures for


Why not contribute to Storm?
----------------------------
Its development is restricted by the requirements of Launchpad and has stagnated. Despite some bugs being fixed in trunk for years there hasn't been a new release. It seems other projects have moved away from Storm in favor of `SQLAlchemy <http://www.sqlalchemy.org/>`_.


Why not fork Storm?
-------------------
Storm carries a lot of legacy and cleaning up its codebase would take considerable effort. It would probably take as long as rewriting the core functionality from scratch. It is also a learning experience to design this from the ground up.
