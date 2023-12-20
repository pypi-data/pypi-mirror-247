# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['import_export_extensions',
 'import_export_extensions.admin',
 'import_export_extensions.admin.forms',
 'import_export_extensions.admin.mixins',
 'import_export_extensions.admin.model_admins',
 'import_export_extensions.api',
 'import_export_extensions.api.serializers',
 'import_export_extensions.api.views',
 'import_export_extensions.migrations',
 'import_export_extensions.models']

package_data = \
{'': ['*'],
 'import_export_extensions': ['static/import_export_extensions/css/admin/*',
                              'static/import_export_extensions/css/widgets/*',
                              'static/import_export_extensions/js/admin/*',
                              'static/import_export_extensions/js/widgets/*',
                              'templates/admin/import_export_extensions/*']}

install_requires = \
['celery[redis]>=5.3.6,<6.0.0',
 'django-extensions>=3.2.3,<4.0.0',
 'django-filter>=23.4,<24.0',
 'django-import-export>=3.3.3,<4.0.0',
 'django-picklefield>=3.1,<4.0',
 'django>=3.2',
 'djangorestframework>=3.14.0,<4.0.0',
 'drf-spectacular>=0.26.5,<0.27.0',
 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'django-import-export-extensions',
    'version': '0.5.0',
    'description': 'Extend functionality of `django-import-export`',
    'long_description': '===============================\ndjango-import-export-extensions\n===============================\n\n.. image:: https://github.com/saritasa-nest/django-import-export-extensions/actions/workflows/checks.yml/badge.svg\n    :target: https://github.com/saritasa-nest/django-import-export-extensions/actions/workflows/checks.yml\n    :alt: Build status on Github\n\n.. image:: https://coveralls.io/repos/github/saritasa-nest/django-import-export-extensions/badge.svg?branch=main\n    :target: https://coveralls.io/github/saritasa-nest/django-import-export-extensions?branch=main\n    :alt: Test coverage\n\n.. image:: https://img.shields.io/badge/python%20versions-3.9%20%7C%203.10%20%7C%203.11-blue\n    :target: https://pypi.org/project/django-import-export-extensions/\n    :alt: Supported python versions\n\n.. image:: https://img.shields.io/badge/django--versions-3.2%20%7C%204.0%20%7C%204.1%20%7C%204.2-blue\n    :target: https://pypi.org/project/django-import-export-extensions/\n    :alt: Supported django versions\n\n.. image:: https://readthedocs.org/projects/django-import-export-extensions/badge/?version=latest\n    :target: https://django-import-export-extensions.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. image:: https://static.pepy.tech/personalized-badge/django-import-export-extensions?period=month&units=international_system&left_color=gray&right_color=blue&left_text=Downloads/month\n    :target: https://pepy.tech/project/django-import-export-extensions\n    :alt: Downloading statistic\n\nDescription\n-----------\n``django-import-export-extensions`` extends the functionality of\n`django-import-export <https://github.com/django-import-export/django-import-export/>`_\nadding the following features:\n\n* Import/export resources in the background via Celery\n* Manage import/export jobs via Django Admin\n* DRF integration that allows to work with import/export jobs via API\n* Support `drf-spectacular <https://github.com/tfranzel/drf-spectacular>`_ generated API schema\n* Additional fields and widgets (FileWidget, IntermediateM2MWidget, M2MField)\n\nInstallation\n------------\n\nTo install ``django-import-export-extensions``, run this command in your terminal:\n\n.. code-block:: console\n\n    $ pip install django-import-export-extensions\n\nAdd ``import_export`` and ``import_export_extensions`` to ``INSTALLED_APPS``\n\n.. code-block:: python\n\n    # settings.py\n    INSTALLED_APPS = (\n        ...\n        "import_export",\n        "import_export_extensions",\n    )\n\nRun ``migrate`` command to create ImportJob/ExportJob models and\n``collectstatic`` to let Django collect package static files to use in the admin.\n\n.. code-block:: shell\n\n    $ python manage.py migrate\n    $ python manage.py collectstatic\n\n\nUsage\n-----\n\nPrepare resource for your model\n\n.. code-block:: python\n\n    # apps/books/resources.py\n    from import_export_extensions.resources import CeleryModelResource\n\n    from .. import models\n\n\n    class BookResource(CeleryModelResource):\n\n        class Meta:\n            model = models.Book\n\nUse ``CeleryImportExportMixin`` class and set ``resource_class`` in admin model\nto import/export via Django Admin\n\n.. code-block:: python\n\n    # apps/books/admin.py\n    from django.contrib import admin\n\n    from import_export_extensions.admin import CeleryImportExportMixin\n\n    from .. import resources\n\n\n    @admin.register(models.Book)\n    class BookAdmin(CeleryImportExportMixin, admin.ModelAdmin):\n        resource_class = resources.BookResource\n\n\nPrepare view sets to import/export via API\n\n.. code-block:: python\n\n    # apps/books/api/views.py\n    from .. import resources\n\n    from import_export_extensions.api import views\n\n\n    class BookExportViewSet(views.ExportJobViewSet):\n        resource_class = resources.BookResource\n\n\n    class BookImportViewSet(views.ImportJobViewSet):\n        resource_class = resources.BookResource\n\n\nDon\'t forget to `configure Celery <https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html>`_\nif you want to run import/export in background\n\n\nLinks:\n------\n* Documentation: https://django-import-export-extensions.readthedocs.io.\n* GitHub: https://github.com/saritasa-nest/django-import-export-extensions/\n* PyPI: https://pypi.org/project/django-import-export-extensions/\n\nLicense:\n--------\n* Free software: MIT license\n',
    'author': 'Saritasa',
    'author_email': 'pypi@saritasa.com',
    'maintainer': 'Nikita Azanov',
    'maintainer_email': 'nikita.azanov@saritasa.com',
    'url': 'https://github.com/saritasa-nest/django-import-export-extensions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
