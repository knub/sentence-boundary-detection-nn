PDFVIEWER=evince
FILE=results

show: build
	$(PDFVIEWER) $(FILE).pdf &

plot:
	cd plots && build

when-changed:
	@clear && when-changed $(FILE).tex -c 'printf "\033c" && echo "Building" && make -s build && echo "Succeeded"'

convert:
	cd plots && make convert

build:
	@mkdir -p .output
	@pdflatex -interaction=nonstopmode -halt-on-error -output-directory .output -jobname=$(FILE) $(FILE).tex 1>&2 > .output/error
	@mv .output/$(FILE).pdf .

error:
	@vim + .output/error


bibtex:
	@cp $(FILE).bib .output/ && cd .output && bibtex $(FILE) && cd ..

clean:
	rm .output/*.aux .output/*.log
