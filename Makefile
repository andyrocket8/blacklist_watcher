_BUILD_ARGS_IMAGE_NAME ?= blacklist-watcher
_BUILD_ARGS_RELEASE_TAG ?= latest
_BUILD_ARGS_DOCKERFILE ?= ./src/Dockerfile

_builder:
		docker build -t ${_BUILD_ARGS_IMAGE_NAME} -f ${_BUILD_ARGS_DOCKERFILE} .

_clean_builder:
		docker build -t ${_BUILD_ARGS_IMAGE_NAME} --no-cache -f ${_BUILD_ARGS_DOCKERFILE} .

_check:
		bash .git/hooks/pre-commit

build:
		$(MAKE) _builder

clean_build:
		$(MAKE) _clean_builder

check:
		$(MAKE) _check