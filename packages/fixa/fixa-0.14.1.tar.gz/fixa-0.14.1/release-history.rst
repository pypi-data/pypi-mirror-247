.. _release_history:

Release and Version History
==============================================================================


Backlog (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.14.1 (2023-12-22)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``deployment_pattern.py`` module.
- add ``aws_s3_static_website_hosting.py`` module.
- add ``aws_stepfunctions_version_and_alias.py`` module.
- add new feature related to blue/green and canary deployment to ``aws_lambda_version_and_alias.py`` module, bump version to 0.2.1.


0.13.1 (2023-12-13)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``nest_logger.NestedLogger.emoji_block`` method.
- add ``env_var.py`` module.
- add ``git_cli.create_local_git_tag`` function.
- add ``git_cli.delete_local_git_tag`` function.
- add ``aws.aws_sts.mask_user_id`` function.
- add ``aws.aws_sts.get_caller_identity`` function.
- add ``aws.aws_sts.get_account_alias`` function.


0.12.1 (2023-12-03)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``aws.aws_sts`` module.
- add ``jsonutils.py`` module.
- add ``conventional_commits`` module.
- add ``semantic_branch`` module.
- add ``aws.aws_lambda_version_and_alias`` module.

**Miscellaneous**

- add ``__version__`` variable to all modules.


0.11.1 (2023-10-24)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``aws.aws_athena_query.py`` module. This module allow user to use parquet file to store Athena query result. It returns the athena query result as a ``polars.LazyFrame``.
- add ``better_fuzzywuzzy.py`` module. This module allow user to fuzzy search any complex Python object.

**Bugfixes**

- fix a bug that the ``nest_logger.py`` ruler didn't render the align symbol correctly.


0.10.2 (2023-09-10)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- fix a bug that  ``aws.aws_s3_search.py`` module cannot find the correct s3_client to get metadata.
- ``aws.aws_s3_search.py`` module now allow user to ignore metadata or tags when creating the database.


0.10.1 (2023-09-10)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``aws.aws_s3_lock.py`` module. It is a S3 based distributive lock implementation.
- add ``aws.aws_s3_tracker.py`` module. It is a S3 based progress tracker implementation.
- add ``aws.aws_s3_search.py`` module. It boost searching lots of s3 object without hitting the list_object API over and over again.


0.9.1 (2023-08-26)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``better_pathlib.get_dir_here()`` method.
- add ``nested_logger.NestedLogger.indent()`` context manager to create additional indent.

**Bugfixes**

- fix a bug that `nested_logger.NestedLogger` does not reset the ``_pipes`` to previous when there is an error in the context manager logic.


0.8.1 (2023-07-31)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``waiter.Waiter`` for retry and long polling pattern.
- add ``iterable.group_by`` function.
- add ``aws.aws_s3_uri.py`` module.
- add ``aws.aws_dynamodb_export_to_s3.py`` module.


0.7.1 (2023-05-27)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``hashes.Hashes.of_folder`` and ``hashes.Hashes.of_paths``.
- add ``git_cli.locate_dir_repo``.

**Minor Improvements**

- add edge case handling for ``better_pathlib.temp_cwd``.

**Bugfixes**

**Miscellaneous**


0.6.1 (2023-05-26)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``build_dist`` module to build the source distribution of Python.


0.5.3 (2023-05-12)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- allow mini string template in ``nest_logger.NestedLogger.pretty_log``, ``nest_logger.NestedLogger.start_and_end``.


0.5.2 (2023-05-11)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Miscellaneous**

- add ``get_names`` method for most of enum class in ``better_enum`` module
- add ``error_emoji`` argument to ``nest_logger.NestedLogger.start_and_end`` decorator.


0.5.1 (2023-05-05)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``better_pathlib``
- add ``dataclass_dataframe``
- add ``pytest_cov_helper``
- add ``better_enum``
- add ``runtime``
- add ``os_platform``
- add ``git_cli``

**Minor Improvements**

- improve code coverage test


0.4.1 (2023-02-25)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``nested_logger.block``

**Miscellaneous**

- add more jupyter notebook examples


0.3.2 (2023-02-08)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- by default, ``nest_logger.py`` no longer create the default logger.


0.3.1 (2023-02-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- ``nest_logger.py`` new features:
    - allow to customize pipe character
    - ``nested()`` context manager is now smarter
    - ``disabled()`` context manager can temporarily disable the logger


0.2.1 (2023-02-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``nest_logger.py``


0.1.1 (2023-02-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release
- add ``binarysearch.py``
- add ``hashes.py``
- add ``iterable.py``
- add ``rnd.py``
- add ``timer.py``
