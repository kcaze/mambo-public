/* test_bdblock.js */

ui.debug.addDebugData('bdblock', {
	url : '5/5/100089082/12345o51g4i3i',
	failcheck : [
		['bdBranchExBP',"pzprv3/bdblock/5/5/1 2 3 4 5 /. . . . . /. . . . 5 /1 . 4 . . /. 3 . . . /. 1 1 1 1 . /. . . . . . /. 1 . . . . /. . . . . 1 /1 . . . . . /. . . 1 . . /1 0 0 0 /1 0 0 0 /1 0 0 0 /1 0 0 0 /0 0 0 0 /0 0 0 0 0 /0 0 0 0 0 /0 0 0 0 0 /1 1 1 0 0 /"],
		['bdCrossExBP', "pzprv3/bdblock/5/5/1 2 3 4 5 /. . . . . /. . . . 5 /1 . 4 . . /. 3 . . . /. 1 1 1 1 . /. . . . . . /. 1 . . . . /. . . . . 1 /1 . . . . . /. . . 1 . . /1 0 0 0 /1 0 0 0 /1 1 0 0 /0 1 1 0 /0 0 1 0 /0 0 0 0 0 /0 1 0 0 0 /0 1 1 0 0 /1 1 0 0 0 /"],
		['bkNoNum',     "pzprv3/bdblock/5/5/1 2 3 4 5 /. . . . . /. . . . 5 /1 . 4 . . /. 3 . . . /. 1 1 1 1 . /. . . . . . /. 1 . . . . /. . . . . 1 /1 . . . . . /. . . 1 . . /1 0 0 0 /1 0 0 0 /1 1 0 0 /0 1 1 0 /0 0 1 0 /0 0 0 0 0 /0 1 0 0 0 /0 0 0 1 1 /1 1 0 0 0 /"],
		['bkPlNum',     "pzprv3/bdblock/5/5/1 2 3 4 5 /. . . . . /. . . . 5 /1 . 4 . . /. 3 . . . /. 1 1 1 1 . /. . . . . . /. 1 . . . . /. . . . . 1 /1 . . . . . /. . . 1 . . /0 1 0 0 /0 1 0 0 /0 1 0 0 /0 1 0 0 /0 0 0 0 /0 0 0 0 0 /0 0 0 0 0 /0 0 0 0 0 /1 1 0 0 0 /"],
		['bkSepNum',    "pzprv3/bdblock/5/5/1 2 3 4 5 /. . . . . /. . . . 5 /1 . 4 . . /. 3 . . 1 /. 1 1 1 1 . /. . . . . . /. 1 . . . . /. . . . 1 1 /1 . . . . . /. . . 1 1 . /1 1 1 1 /1 1 1 1 /1 0 1 1 /1 1 0 1 /0 0 1 1 /0 0 0 0 0 /0 1 0 0 0 /0 0 1 0 1 /1 0 1 0 0 /"],
		['bdDeadEnd',   "pzprv3/bdblock/5/5/1 2 3 4 5 /. . . . . /. . . . 5 /1 . 4 . . /. 3 . . . /. 1 1 1 1 . /. . . . . . /. 1 . . . . /. . . . . 1 /1 . . . . . /. . . 1 1 . /1 1 1 1 /1 1 1 1 /1 0 1 1 /1 1 0 0 /0 0 1 1 /0 0 0 0 0 /0 1 0 0 0 /0 0 1 0 1 /1 0 1 0 0 /"],
		['bdCountLt3BP',"pzprv3/bdblock/5/5/1 2 3 4 5 /. . . . . /. . . . 5 /1 . 4 . . /. 3 . . . /. 1 1 1 1 . /. . . . . . /. 1 . . . . /. . . . . 1 /1 . . . . . /. . . 1 1 . /1 1 1 1 /1 1 1 1 /1 0 1 1 /1 1 0 0 /0 0 1 0 /0 0 0 0 0 /0 1 0 0 0 /0 0 1 0 1 /1 0 1 0 0 /"],
		['bdIgnoreBP',  "pzprv3/bdblock/5/5/1 2 3 4 5 /. . . . . /. . . . 5 /1 . 4 . . /. 3 . . . /. 1 1 1 1 . /. . . . . . /. 1 . . . . /. . . . . 1 /1 . . . 1 . /. . . 1 . . /1 1 1 1 /1 1 1 1 /1 0 1 1 /1 1 0 0 /0 0 1 0 /0 0 0 0 0 /0 1 0 0 0 /0 0 1 0 1 /1 0 1 0 0 /"],
		[null,          "pzprv3/bdblock/5/5/1 2 3 4 5 /. . . . . /. . . . 5 /1 . 4 . . /. 3 . . . /. 1 1 1 1 . /. . . . . . /. 1 . . . . /. . . . . 1 /1 . . . . . /. . . 1 . . /1 1 1 1 /1 1 1 1 /1 -1 1 1 /1 1 -1 -1 /-1 -1 1 -1 /0 0 -1 -1 0 /0 1 -1 -1 0 /0 -1 1 -1 1 /1 -1 1 -1 -1 /"]
	],
	inputs : [
		/* ?????????????????????????????? */
		{ input:["newboard,1,1", "editmode"] },
		{ input:["mouse,left, 0,0", "mouse,left, 2,0", "mouse,left, 0,0" ],
		  result:"pzprv3/bdblock/1/1/. /. 1 /. . //" }
		/* ???????????????????????????nurikabe???????????????????????? */
		/* ???????????????sashigane???????????????????????? */
	]
});
