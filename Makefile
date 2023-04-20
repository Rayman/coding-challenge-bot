all: smarter_min.py search_min.py

smarter_min.py: smarter.py Makefile
	pyminify smarter.py --rename-globals --remove-literal-statements --remove-asserts --remove-debug --output smarter_min.py
	sed -i 's/\bcurrent_score\b/z/g' smarter_min.py
	sed -i 's/\bdepth\b/y/g' smarter_min.py
	sed -i 's/\bgrid\b/x/g' smarter_min.py
	sed -i 's/\bhistory\b/v/g' smarter_min.py
	sed -i 's/\bmax_depth\b/r/g' smarter_min.py
	sed -i 's/\bscore_grid\b/s/g' smarter_min.py

search_min.py: search.py Makefile
	pyminify search.py --rename-globals --remove-literal-statements --remove-asserts --remove-debug --output search_min.py
	sed -i 's/\bcurrent_score\b/z/g' search_min.py
	sed -i 's/\bdepth\b/y/g' search_min.py
	sed -i 's/\bgrid\b/x/g' search_min.py
	sed -i 's/\bheap\b/w/g' search_min.py
	sed -i 's/\bhistory\b/v/g' search_min.py
	sed -i 's/\bmax_depth\b/u/g' search_min.py
	sed -i 's/\bneighbors\b/t/g' search_min.py
	sed -i 's/\bpossible_neighbor\b/s/g' search_min.py
	sed -i 's/\bprevious_positions\b/r/g' search_min.py
	sed -i 's/\bscore_grid\b/q/g' search_min.py
	sed -i 's/\bupper_bound\b/p/g' search_min.py
