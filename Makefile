YLDME_UPLOADS= 	/home/pbui/.config/yldme/uploads
COMMON= 	scripts/yasb.py templates/base.tmpl $(wildcard static/yaml/*.yaml)
LOGFILE=	/home/pbui/.weechat/logs/irc.snoonet.\#paperboy.weechatlog 
RSYNC_FLAGS= 	-rv --copy-links --progress --exclude="*.swp" --exclude="*.yaml" --size-only
YAML=		$(shell ls pages/*.yaml)
HTML= 		$(YAML:.yaml=.html)

%.html:		%.yaml $(COMMON) $(LOGFILE)
	./scripts/yasb.py $< > $@

all:		$(HTML)

install:	all
	cp pages/index.html $(YLDME_UPLOADS)/startpage

clean:
	rm -f $(HTML)
