# Copyright (c) 2015-2016 Contributors as noted in the AUTHORS file
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

image_name = alidron/demo-zwave-react

container_name = demo-zwave-react

run_args = --net=host

.PHONY: clean clean-dangling build run-demo stop logs

clean:
	docker rmi $(image_name) || true

clean-dangling:
	docker rmi `docker images -q -f dangling=true` || true

build: clean-dangling
	docker build --force-rm=true -t $(image_name) .

run-demo:
	docker run -it --rm --name=$(container_name) $(run_args) $(image_name)

stop:
	docker stop -t 1 $(container_name)
	docker rm $(container_name)

logs:
	docker logs -f $(container_name)
