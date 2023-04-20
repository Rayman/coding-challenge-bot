all: dfs_min.py astar_min.py

dfs_min.py: dfs.py Makefile
	pyminify dfs.py --rename-globals --remove-literal-statements --remove-asserts --remove-debug --output dfs_min.py
	sed -i 's/\bcurrent_score\b/z/g' dfs_min.py
	sed -i 's/\bdepth\b/y/g' dfs_min.py
	sed -i 's/\bgrid\b/x/g' dfs_min.py
	sed -i 's/\bhistory\b/v/g' dfs_min.py
	sed -i 's/\bmax_depth\b/r/g' dfs_min.py
	sed -i 's/\bscore_grid\b/s/g' dfs_min.py

astar_min.py: astar.py Makefile
	pyminify astar.py --rename-globals --remove-literal-statements --remove-asserts --remove-debug --output astar_min.py
	sed -i 's/\bcurrent_score\b/z/g' astar_min.py
	sed -i 's/\bdepth\b/y/g' astar_min.py
	sed -i 's/\bgrid\b/x/g' astar_min.py
	sed -i 's/\bheap\b/w/g' astar_min.py
	sed -i 's/\bhistory\b/v/g' astar_min.py
	sed -i 's/\bmax_depth\b/u/g' astar_min.py
	sed -i 's/\bneighbors\b/t/g' astar_min.py
	sed -i 's/\bpossible_neighbor\b/s/g' astar_min.py
	sed -i 's/\bprevious_positions\b/r/g' astar_min.py
	sed -i 's/\bscore_grid\b/q/g' astar_min.py
	sed -i 's/\bupper_bound\b/p/g' astar_min.py
