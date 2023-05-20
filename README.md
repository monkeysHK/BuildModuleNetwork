# A Fun Project

This project is about building a graph visualization of module dependencies of Hypixel SkyBlock Wiki.

## How it works

- With a user-defined list or an API requested list of all module pages as starting pages, using BFS, the program will crawl through its dependencies, dependencies of dependencies, and so on.
- To get the dependencies, the program will first request the page content using MediaWiki's API, then detect its module dependencies.
- The detection of module dependencies is solely string pattern detection based on how wiki users import their modules.
- After that, it builds the nodes and edges in a directed graph.
- Except for version 1.2, if module A imports (hense depends on) module B, an arrow will point from B to A.

## How to see

- The generated HTML is in the `docs` directory.
- It is also available on my [github page](https://monkeyshk.github.io/BuildModuleNetwork).

## How to run

- To generate the HTML again, there are two files (in `src` directory) to run:
    - `makegraph.py` builds the dependencies graph and save the dict in a file.
    - `buildnetwork.py` uses the file that makegraph provides, and builds the network visualization.

## Changelog
| Version | Changes |
| ------- | ------- |
| 1.0 | Initial Publish |
| 1.1 | New color for data pages. Directed graph |
| 1.2 | New color for external pages. Fixed first letter casing. Now uses all existing modules as starting points. A change in arrow direction |
| 1.3 | Minor fixes. Reverted change in arrow direction |