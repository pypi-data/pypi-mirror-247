gitdb
=====

``python-gitdb`` is a small Python module that allows to use a git repository
as key-value-store. The data can be serialized by different Serializers.

Attention! The integration of a remote repository is rudimental, i.e., push and pull
currently only works via soft resets.


Serializers
-----------

There are several serializers provided to store the data:

    * JsonSerializer        (included without further modules)
    * BJsonSerializer
    * YamlSerializer
    * MsgPackSerializer

Depending on the selected serializer, the corresponding module must be
installed.


Setup
-----

::

    poetry install python-gitdb


Usage
-----

::

    from gitdb import GitDb
    from gitdb.serializers.jsonserializer import JsonSerializer

    # git repository that is used as database
    REPO = "/your/path/to/the/repository"

    # prepare the git repository database
    gitdb = GitDb(REPO, serializer=JsonSerializer)

    # add two entries
    gitdb.set("key_a", "test")
    gitdb.set("key_b", {"a": 1, "b": 2})

    # load two entries
    print(gitdb.get("key_a"))
    print(gitdb.get("key_b"))
