# Makefile to manage blog

help:
	@echo "Help message:"
	@echo "  help   -  show this help message"
	@echo "  start  -  start a web sever and watch to auto rebuild"
	@echo "  build  -  to build markdown to html"
	@echo "  clean  -  to remove htmls built by lilac"

build:
	lilac build

start:
	lilac build --watch --server

clean:
	rm -rf post page tag 404.html about.html archives.html feed.atom index.html tags.html 
