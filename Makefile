html:
	pelican

clean:
	[ ! -d output ] || rm -rf output

publish:
	pelican -s publishconf.py

github: publish
	ghp-import output
	git push origin gh-pages

