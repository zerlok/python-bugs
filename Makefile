POETRY_RUN := PYTHONPATH=src poetry run
CELERY_RUN := $(POETRY_RUN) celery -A mytasks.tasks
CELERY_WORKER_OPTIONS := --pidfile $(PWD)/myworker.pid --logfile $(PWD)/myworker.log

NORMAL_TEST_CLEANUP := $(CELERY_RUN) control shutdown; rm -f *.log; rm -f *.pid; docker-compose down -v
PYTEST_TEST_CLEANUP := docker ps -aq --filter "label=creator=pytest-docker-tools" | xargs -r docker rm -f


.PHONY: all
all: clean install tests

.PHONY: clean
clean: clean-tests
	-rm -r $(shell poetry env info -p)


.PHONY: clean-tests
clean-tests:
	-$(NORMAL_TEST_CLEANUP)
	-$(PYTEST_TEST_CLEANUP)

.PHONY: install
install:
	poetry install

.PHONY: tests
tests: clean-tests test-normal-call test-pytest-call


.PHONY: test-normal-call
test-normal-call:
	docker-compose up -d redis
	sleep 3
	$(CELERY_RUN) worker -D $(CELERY_WORKER_OPTIONS)
	sleep 3
	$(CELERY_RUN) inspect ping -t 5
	$(POETRY_RUN) python src/mytasks/call.py

	-$(NORMAL_TEST_CLEANUP)

.PHONY: test-pytest-call
test-pytest-call:
	-$(POETRY_RUN) pytest
	-$(PYTEST_TEST_CLEANUP)
