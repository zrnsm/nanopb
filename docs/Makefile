INPUTS = index.md concepts.md security.md migration.md
# index.html concepts.html reference.html security.html migration.html whats_new.html

all: $(INPUTS:.md=.html)

tmp_menu.html: $(INPUTS)
	echo '<div id="index">' > $@
	(echo '<h2>Documentation index</h2>'; \
	 for file in $^; do echo -n '1. ['; sed -n '1 s!^# Nanopb: !! p' $$file; \
	 echo -n "]("; echo $$file | sed 's/.md/.html)/' ; done;) | \
	 pandoc -f markdown -t html5 >> $@
	echo '</div>' >> $@

%.html: %.md tmp_menu.html
	sed '1 s!#!%!' $< | \
	pandoc -s -f markdown -t html5 -c lsr.css --toc --toc-depth=3 \
	 --variable 'header-includes=<link href="favicon.ico" type="image/x-icon" rel="shortcut icon" />' \
	 --indented-code-classes=c \
	 -o $@
	sed -i 's!<nav[^>]*>!\0<b>Contents:</b>!' $@
	sed -i '/<nav/e cat tmp_menu.html' $@
#	rst2html --field-name-limit=32 --stylesheet=lsr.css --link-stylesheet $< $@
#	sed -i 's!</head>!<link href="favicon.ico" type="image/x-icon" rel="shortcut icon" />\n</head>!' $@
