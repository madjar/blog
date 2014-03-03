html:
	pelican

clean:
	[ ! -d output ] || rm -rf output

publish: clean
	pelican -s publishconf.py

github: publish
	ghp-import output -m"Blog update"
	git push origin gh-pages

