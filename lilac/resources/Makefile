# Makefile to manage blog

help:
	@echo "Help message:"
	@echo "  build  -  to build markdown to html"
	@echo "  server -  to start web server and watch"
	@echo "  clean  -  to remove htmls built by lilac"

build:
	lilac build

clean:
	rm -rf post page tag 404.html about.html archives.html feed.atom index.html tags.html 

server:
	lilac server
