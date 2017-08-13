all:
	source activate aind
	python -m tournament.py 
	pandoc -S cv-body.md -o cv-body.tex
	perl -p -i -e "s/---\ntitle:/---\nlayout: post\ntitle:/g" cv-body.tex
	perl -p -i -e "s/M.Sc./M.Sc.\\\/g" cv-body.tex
	perl -p -i -e "s/B.Sc./B.Sc.\\\/g" cv-body.tex
	latexmk -pdf IderChithamCV.tex
	pandoc cv-body.md -o cv-body-clean.md
	cat cv-header.txt cv-body-clean.md > IderChithamCV.txt
	perl -p -i -e "s/–/--/g" IderChithamCV.txt
	rm cv-body.md
	#rm cv-body.tex
	rm cv-body-clean.md
	rm *.log *.out *.aux *.fdb_latexmk *.fls
	# and pre-process the HTML with pandoc
	# because redcarpet markdown doesn't do definition lists
	sed -i '.original' "s/$/$$/g" cv-pandoc-mod.md
	pandoc -S heuristic_analysis.md -o heuristic_analysis.pdf
	#modify html cv for pretty render
	sed -i '.original' 's~</h2>~</h2><br>~g' cv.html
	sed -i '.original' 's~<p><strong>~<strong>~g' cv.html
	sed -i '.original' 's~</strong></p>~</strong>~g' cv.html
	cp IderChithamCV.pdf ~/Dropbox/public/IderChithamCV.pdf
	rm *.original
	#rm cv-temp.html, cv-pandoc-mod.md, index-pre.txt, cv-pandoc.txt

list:
	conda list > conda_list.md