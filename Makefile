#
# Copyright 2016 Yufei Li <yufeiminds@gmail.com>
#

help:
	@echo "XWeb micro framework"
	@echo "--------------------"
	@echo "test    Run tests"

test:
	nosetests --with-coverage --cover-html --cover-package=xweb
