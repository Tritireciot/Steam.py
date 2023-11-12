APP=secdim.lab.python
.SILENT:
.PHONY: all build test securitytest clean header
all: build

test: header build
	echo -e "\033[1;33m\n[i] Running functionality tests\033[0m\n"
	docker run --rm ${APP} sh -c "python manage.py test --no-color --noinput --keepdb program.test_usability" \
		&& echo -e "\033[1;32m\n[i] Well done! All functionality tests have been passed\033[0m\n"\
		|| echo -e "\033[1;31m\n[!] Oh, no! Program has functionality bug(s)! Try again\033[0m\n"

securitytest: header build
	echo -e "\033[1;33m\n[i] Running security tests\033[0m\n"
	docker run --rm ${APP} sh -c "python manage.py test --no-color --noinput --keepdb program.test_security" \
		&& echo -e "\033[1;32m\n[i] Well done! All security tests have been passed\033[0m\n"\
		|| echo -e "\033[1;31m\n[!] Oh, no! Program has security bug(s)! Try again\033[0m\n"

build: header build
	echo -e "\033[1;33m\n[i] Building the program\033[0m\n"
	docker build --rm --tag=$(APP) .
	echo -e "\033[1;32m\n[i] Done! Program is ready to run\033[0m\n"\

run: build
	docker run -p 8080:8080 --rm $(APP)

debug: build
	docker run -p 8080:8080 --rm -it -v "${PWD}/src:/app" ${APP} sh

clean:
	docker image rm $(APP)
	docker system prune
	docker image prune -f


define HEADER

   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   %%%%%%%%%%%%%%              %%%%%%%%%%%%
   %%%%%%%%%%%                  ,%%%%%%%%%%
   %%%%%%%%%%         *%%%%*    %%%%%%%%%%%
   %%%%%%%%%%        %%%%%%%%%%%%%%%%%%%%%%
   %%%%%%%%%%%             *%%%%%%%%%%%%%%%
   %%%%%%%%%%%%%               .%%%%%%%%%%%
   %%%%%%%%%%%%%%%%%%            %%%%%%%%%%
   %%%%%%%%%%%%%%%%%%%%%%%        %%%%%%%%%
   %%%%%%%%%%      .%%%%.         %%%%%%%%%
   %%%%%%%%%%                   .%%%%%%%%%%
   %%%%%%%%%%%%,             ,%%%%%%%%%%%%%
   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
              play.secdim.com
endef
export HEADER

header:
	@echo -e "\033[1;35m$$HEADER\033[0m"
