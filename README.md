# DevelopmentScripts

Various scripts used in KSS software development

## Description

Currently this includes the following:

* _dockerclean.py_: Cleans out unused things from the local docker environment. 
* _git-recurse.sh_: Recursively applies a git command to all repositories beneath the current directory.
* _git-set-local-user.sh_: Recursively sets the local user in all repositories beneath the current directory. This
is most useful for contractors that support different customers each of whom presumably wants things
checked in using a name and email specific to them.
* _open-xcode-project.sh_: Opens the given directory in Xcode.
* _prettyprint.py_: Reads its input stream and pretty prints it, if possible, to the output stream.
* _set-links.sh_: Sets symbolic links for each `.sh` and `.py` file in the local directory into the target directory.
The typical use for this is to allow an existing path to contain links to the checked out versions of the
scripts in this project.

## Dependancies

* _docker_: Needed for _dockerclean.py_.
* _git_: Needed for _git-..._.
* _Xcode_: Needed for _open-xcode-project.sh_.
* _pylint_ and _shellcheck_: Needed for the static analysis `make analyze` to work.
