SHELL = /bin/bash

GITWORKTREE = /var/www/slavdict
GITDIR = /usr/local/src/wwwgit/slavdict.git
SETTINGS_FILE = slavdict/settings.py
DATE_TIME := $(shell date +%Y-%m-%d--%H-%M)

IS_PRODUCTION = production
IS_DEVELOPMENT = development
SLAVDICT_ENVIRONMENT ?= ${IS_PRODUCTION}
PYTHON = pipenv run python
ifeq (${SLAVDICT_ENVIRONMENT}, ${IS_PRODUCTION})
  GIT = git --work-tree=${GITWORKTREE} --git-dir=${GITDIR}
else
  GIT = git
endif

JSLIBS_PATH := $(shell ${PYTHON} ${SETTINGS_FILE} --jslibs-path)
JSLIBS_FILES := ${JSLIBS_PATH}*.{js,map,txt,swf}
JSLIBS_VERSION_FILE := ${JSLIBS_PATH}version.txt
JSLIBS_NEW_VERSION := $(shell ${PYTHON} ${SETTINGS_FILE} --jslibs-version)
JSLIBS_OLD_VERSION := $(shell cat ${JSLIBS_VERSION_FILE} 2>/dev/null)

LOCCHDIR = /root/slavdict-local-changes-untracked
DIFFFILE = /root/slavdict-local-changes-${DATE_TIME}.diff

RESOURCE_VERSION = sass/_resource_version.sass

default: indesign

shell:
	PYTHONSTARTUP=etc/django_shell_rc.py ${PYTHON} ./manage.py shell

restart: stop update start

update: copydiff destroy_loc_changes checkout collectstatic fixown migrate

killbg:
	test ! -e .bgpids || ( xargs -a .bgpids kill ; rm .bgpids ; true )

run: killbg collectstatic
	@echo "Запуск сервера в тестовом окружении..."
ifeq (${SLAVDICT_ENVIRONMENT}, ${IS_DEVELOPMENT})
	livereload static & echo $$! >>.bgpids
	compass watch & echo $$! >>.bgpids
	trap 'trap - INT TERM ERR; $(MAKE) killbg' INT TERM ERR; \
		${PYTHON} ./manage.py runserver
else
	@echo "Окружение не является тестовым"
	false
endif

stop:
ifeq (${SLAVDICT_ENVIRONMENT}, ${IS_PRODUCTION})
	sudo service nginx stop
	sudo service uwsgi stop slavdict
endif

start:
ifeq (${SLAVDICT_ENVIRONMENT}, ${IS_PRODUCTION})
	sudo service uwsgi start slavdict
	sudo service nginx start
endif

copydiff:
ifeq (${SLAVDICT_ENVIRONMENT}, ${IS_PRODUCTION})
	mkdir -p ${LOCCHDIR}
	${GIT} diff --no-color >${DIFFFILE}
	test -s ${DIFFFILE} || rm -f ${DIFFFILE}
	${GIT} status -s | grep --color=never '?? ' | cut -c4- \
		| xargs -I '{}' rsync -av '{}' ${LOCCHDIR}/
	${GIT} status -s | grep --color=never '?? ' | cut -c4- \
		| xargs -I '{}' rm -fr '{}'
endif

destroy_loc_changes:
ifeq (${SLAVDICT_ENVIRONMENT}, ${IS_PRODUCTION})
	${GIT} reset --hard HEAD
endif

checkout:
ifeq (${SLAVDICT_ENVIRONMENT}, ${IS_PRODUCTION})
	${GIT} pull origin master
endif

_revert:
ifeq (${SLAVDICT_ENVIRONMENT}, ${IS_PRODUCTION})
	${GIT} reset --hard HEAD^
endif

revert: _revert collectstatic fixown

fixown:
ifeq (${SLAVDICT_ENVIRONMENT}, ${IS_PRODUCTION})
	chown -R www-data:www-data ./
	chmod u+x bin/*.sh
endif

collectstatic: hash
	test -e ${RESOURCE_VERSION} || touch ${RESOURCE_VERSION}
	compass compile -e ${SLAVDICT_ENVIRONMENT}
	${PYTHON} ./manage.py collectstatic --noinput

migrate:
	${PYTHON} ./manage.py migrate

clean:
	-find -name '*.pyc' -execdir rm '{}' \;
	-rm -f static/*.css
	-rm -f ${JSLIBS_FILES}
	-rm -fR .sass-cache/
	-rm -fR .static/*

jslibs:
	if [ "${JSLIBS_OLD_VERSION}" != "${JSLIBS_NEW_VERSION}" ];\
	then \
		rm -f ${JSLIBS_FILES} ; \
		${PYTHON} ${SETTINGS_FILE} --jslibs | xargs -n3 wget ; \
		echo ${JSLIBS_NEW_VERSION} > ${JSLIBS_VERSION_FILE} ; \
	fi

hash: jslibs
	test -e .temp_hash && rm .temp_hash || true
	${GIT} ls-tree --name-only -r HEAD -- sass static \
		| xargs sha256sum >>.temp_hash
	find static/js/outsourcing -type f -iname '*.js' \
		-exec sha256sum '{}' \; >>.temp_hash
	sort .temp_hash -o .temp_hash
	sha256sum .temp_hash | cut -c1-8 >.hash
	echo '$$shash:' "'$$(cat .hash)'" >${RESOURCE_VERSION}

scp:
ifeq (${SLAVDICT_ENVIRONMENT}, ${IS_DEVELOPMENT})
	rsync bin/indesign_xml_dumper.py dilijnt0:/var/www/slavdict/bin/
	ssh dilijnt0 chown www-data:www-data /var/www/slavdict/bin/indesign_xml_dumper.py
	rsync -av templates/indesign dilijnt0:/var/www/slavdict/templates/
	ssh dilijnt0 chown -R www-data:www-data /var/www/slavdict/templates/indesign/
endif

indesign:
ifeq (${SLAVDICT_ENVIRONMENT}, ${IS_DEVELOPMENT})
	rsync -av bin dilijnt0:/var/www/slavdict/
	rsync -av slavdict/jinja_extensions dilijnt0:/var/www/slavdict/slavdict/
	rsync -av  templates/indesign dilijnt0:/var/www/slavdict/templates/
	[ ! -e .args ] && ( \
		echo '--split-by-letters' >.args ; \
		echo '--split-nchars=50000' >>.args ; \
		echo '--output-pattern=/root/slavdict-indesign-#.xml' >>.args ) \
		|| echo "file '.args' exists"
	rsync .args dilijnt0:/root/
	ssh dilijnt0 chown -R www-data:www-data /var/www/slavdict/
	ssh dilijnt0 rm -f /root/slavdict-indesign-*.xml
	ssh dilijnt0 nohup /var/www/slavdict/bin/remote_indesign_xml_dumper.sh
	scp dilijnt0:/root/slavdict-indesign-*.xml .temp/
endif

listen-indesign:
ifeq (${SLAVDICT_ENVIRONMENT}, ${IS_DEVELOPMENT})
	ls .list bin/indesign_xml_dumper.py templates/indesign/* | entr bash -c 'time cat .list | xargs ${PYTHON} bin/indesign_xml_dumper.py >/home/nurono/VirtualBox\ SharedFolder/slavdict-indesign.xml'
endif

install:
	command -v gem && sudo gem install || echo 'gem is not installed'; false
	command -v pipenv && pipenv install || echo 'pipenv is not installed'; false

.PHONY: \
    checkout \
    clean \
    collectstatic \
    copydiff \
    default \
    destroy_loc_changes \
    fixown \
    install \
    jslibs \
    hash \
    listen-indesign \
    migrate \
    migrestart \
    restart \
    revert \
    _revert \
    run \
    start \
    stop \
    scp \
    update \


