import logging
from typing import Optional, Any
from pathlib import Path


from pygit2 import (
    discover_repository,
    init_repository,
    Repository,
    IndexEntry,
    GIT_FILEMODE_BLOB,
    Signature,
    Remote,
    RemoteCallbacks,
    Keypair,
    GIT_MERGE_ANALYSIS_UP_TO_DATE,
    GIT_MERGE_ANALYSIS_NORMAL,
    GIT_MERGE_ANALYSIS_FASTFORWARD,
    GIT_RESET_SOFT
)

# from gitdb.exceptions import GitDbException
from gitdb.serializers.baseserializer import BaseSerializer
from gitdb.serializers.jsonserializer import JsonSerializer


# prepare logger
log = logging.getLogger(__name__)


class GitDb:
    """
    main class to interact with the git repository as database
    """
    def __init__(
        self,
        repo_path: str,
        serializer: BaseSerializer = JsonSerializer,
    ):
        self._repo: Repository = self._get_or_create_repo(
            repo_path=repo_path
        )
        self._serializer = serializer()

        # no remote information on startup
        self._username = None
        self._pubkey = None
        self._privkey = None
        self._passphrase = None

    def _get_or_create_repo(self, repo_path: str) -> Repository:
        """
        Get repository of existing path or create new repository,
        if it does not exist

        :param repo_path: repository path
        :type repo_path: str
        :return: repository
        :rtype: Repository
        """
        discovered_repo_path = discover_repository(repo_path)
        if discovered_repo_path is not None:
            log.debug("using existing repository '%s'", repo_path)
            repo = Repository(discovered_repo_path)

        else:
            log.debug("initializing new repository '%s'", repo_path)
            repo = init_repository(
                path=repo_path,
                bare=True
            )

        return repo

    def init_remote(
        self,
        remote_url: str,
        remote_name: str = "origin",
        username: str = "git",
        pubkey: str = "~/.ssh/id_rsa.pub",
        privkey: str = "~/.ssh/id_rsa",
        passphrase: Optional[str] = None
    ):
        """
        initialize remote directory

        :param remote_url: remote URL
        :type remote_url: str
        :param remote_name: remote name, defaults to "origin"
        :type remote_name: str, optional
        :param username: username, defaults to "git"
        :type username: str, optional
        :param pubkey: public key, defaults to "~/.ssh/id_rsa.pub"
        :type pubkey: str, optional
        :param privkey: private key, defaults to "~/.ssh/id_rsa"
        :type privkey: str, optional
        :param passphrase: passphrase, defaults to None
        :type passphrase: Optional[str], optional
        """
        self._username = username
        self._pubkey = Path(pubkey).expanduser().as_posix()
        self._privkey = Path(privkey).expanduser().as_posix()
        self._passphrase = passphrase
        self._remote_name = remote_name

        if self.get_remote(remote_name) is None:
            # add remote URL to the config
            log.debug(
                "adding new remote '%s' to '%s'", remote_name, remote_url
            )
            self.repo.remotes.create(remote_name, remote_url)

    @property
    def repo(self) -> Repository:
        """
        get repository

        :return: repository
        :rtype: Repository
        """
        return self._repo

    @property
    def serializer(self) -> BaseSerializer:
        """
        get serializer

        :return: serializer
        :rtype: BaseSerializer
        """
        return self._serializer

    @property
    def keypair(self) -> Keypair:
        """
        keypair based on initialized parameters

        :return: keypair
        :rtype: Keypair
        """
        return Keypair(
            self._username,
            self._pubkey,
            self._privkey,
            self._passphrase
        )

    def get_remote(self, name: str = "origin") -> Optional[Remote]:
        """
        get remote repository of given name

        :param name: remote name, defaults to "origin"
        :type name: str, optional
        :return: remote
        :rtype: Optional[Remote]
        """
        for remote in self.repo.remotes:
            if remote.name == name:
                return remote

        return None

    def add_remote(self, url: str, name: str = "origin") -> None:
        """
        add remote location

        :param url: remote URL
        :type url: str
        :param name: name, defaults to "origin"
        :type name: str, optional
        """
        if self.get_remote(name) is None:
            # not existing yet => create new remote
            log.debug("adding new remote '%s' to '%s'", name, url)
            self.repo.remotes.create(name, url)

    def push(
        self,
        ref: str = "refs/heads/master",
        remote_name: Optional[str] = None
    ) -> None:
        """
        push all changes to the remove location

        :param ref: ref, defaults to "refs/heads/master:refs/heads/master"
        :type ref: str, optional
        :param remote_name: remote name, defaults to None
        :type remote_name: Optional[str], optional
        """
        # get remote repository
        remote = self.get_remote(remote_name or self._remote_name)

        # push data to remote repository
        remote.push(
            specs=[ref],
            callbacks=RemoteCallbacks(credentials=self.keypair)
        )

    def pull(
        self,
        remote_name: Optional[str] = None,
        branch: str = "master"
    ):
        # get remote repository content
        remote = self.get_remote(remote_name or self._remote_name)
        remote.fetch(
            callbacks=RemoteCallbacks(credentials=self.keypair)
        )

        remote_head = self.repo.lookup_reference(
            f"refs/remotes/origin/{branch}"
        ).target

        merge_result, _ = self.repo.merge_analysis(remote_head)
        if merge_result & GIT_MERGE_ANALYSIS_UP_TO_DATE:
            # already up-to-date, so nothing to do here
            log.debug(
                f"local repository is already in sync with remote "
                f"branch '{remote_head}'"
            )
            return

        elif merge_result & GIT_MERGE_ANALYSIS_NORMAL:
            # try to merge

            # TODO: currently soft reset is applied
            # later on figure out if merge is possible on bare repo
            log.debug(
                f"doing soft reset on local branch to remote "
                f"branch {remote_head}"
            )
            self.repo.reset(remote_head, GIT_RESET_SOFT)

            # log.debug(f"trying to merge local with remote '{remote_head}'")
            # self.repo.merge(remote_head)

            # if self.repo.index.conflicts is not None:
            #     # show all conflics
            #     for conflict in self.repo.index.conflicts:
            #         log.error("conflict error in '%s'", conflict[0].path)

            #     raise GitDbException(
            #         f"{len(self.repo.index.conflicts)} conflict(s) while "
            #         f"merging '{remote_head}'!"
            #     )

            # # commit the merge
            # self.commit(
            #     message=f"merged '{remote_head}'",
            #     additional_parents=[remote_head]
            # )

            # complete merge, otherwise git command will assume
            # that merge is still on-going
            self.repo.state_cleanup()

        elif merge_result & GIT_MERGE_ANALYSIS_FASTFORWARD:
            # fast-forward merge

            # TODO: currently soft reset is applied
            # later on figure out if merge is possible on bare repo
            log.debug(
                f"doing soft reset on local branch to remote "
                f"branch {remote_head}"
            )
            self.repo.reset(remote_head, GIT_RESET_SOFT)

            # self.repo.checkout_tree(self.repo.get(remote_head))
            # try:
            #    master_ref = self.repo.lookup_reference(
            #        f"refs/heads/{branch}"
            #    )
            #    master_ref.set_target(remote_head)
            #
            # except KeyError:
            #    self.repo.create_branch(branch, self.repo.get(remote_head))

    def set(
        self, k: str,
        data: bytes,
        auto_commit: bool = True
    ):
        """
        Set a value by its key to the git repository database.
        If auto_commit is True, the value will directly be committed.

        :param k: key
        :type k: str
        :param data: data
        :type data: bytes
        :param auto_commit: if True, data will be committed, defaults to True
        :type auto_commit: bool, optional
        """
        log.debug(
            "storing for key '%s': %s", k, data
        )

        # serialize the data
        s = self.serializer.serialize(obj=data)

        log.debug("serialized data: %s", s)

        # store given data as blob and obtain object ID
        oid = self.repo.create_blob(s)

        # create index entry for object ID and add it
        index_entry = IndexEntry(
            path=k,
            object_id=oid,
            mode=GIT_FILEMODE_BLOB
        )
        self.repo.index.add(index_entry)
        self.repo.index.write()

        if auto_commit is True:
            # automatically commit the data to git
            self.commit()

    def get(
        self,
        k: str
    ) -> Any:
        """
        Get value from git repository database by given key.

        :param k: key
        :type k: str
        :return: value from database
        :rtype: Any
        """
        # get last commit from repository
        last_commit = self.repo[self.repo.head.target]

        data = last_commit.tree[k].data

        log.debug("obtained data for key '%s': %s", k, data)

        # get object data from tree and deserialize it
        obj = self.serializer.deserialize(data)
        log.debug("deserialized data: %s", obj)

        return obj

    def delete(
        self,
        k: str,
        auto_commit: bool = True
    ) -> None:
        """
        Delete data by its key from git repository database

        :param k: key
        :type k: str
        :param auto_commit: if True, data is committed,
                            defaults to True
        :type auto_commit: bool, optional
        """
        self.repo.index.remove(k)

        if auto_commit is True:
            # automatically commit the data to git
            self.commit()

    def commit(
        self,
        message: str = "auto-commit",
        signature: Optional[Signature] = None,
        additional_parents: list[str] = []
    ):
        """
        commit data in git repository

        :param message: message used for commit, defaults to "auto-commit"
        :type message: str, optional
        :param signature: signature used for commit; if not provided the
                          default signature is used, defaults to None
        :type signature: Optional[Signature], optional
        :param additional_parents: additional parents, defaults to []
        :type additional_parents: str
        """
        # use given signature or if not provided the default
        signature = signature or self.repo.default_signature

        if "master" not in self.repo.branches:
            # initial commit
            ref = "refs/heads/master"
            parents = []

        else:
            # all following commits
            parent, ref = self.repo.resolve_refish(
                refish=self.repo.head.name
            )
            ref = ref.name
            parents = [parent.oid]

        # write the tree
        tree = self.repo.index.write_tree()

        # create the commit
        self.repo.create_commit(
            ref,
            signature,
            signature,
            message,
            tree,
            parents + additional_parents
        )

        # write blob to disk
        self.repo.index.write()

        log.debug(
            "writing commit '%s' by %s to disk", message, signature
        )
