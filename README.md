# A Fun Project

This project is about building a graph visualization of Module Dependencies of Hypixel SkyBlock Wiki.

## How it works

- Using a user-defined list of starting pages, and using BFS, the program will crawl through its dependencies, dependencies of dependencies, and so on.
- To get the dependencies, the program will first request the page content using MediaWiki's API, then detect its module dependencies.
- The detection of module dependencies is solely string pattern detection based on how wiki users import their modules.

## How to see

- The generated HTML is in the `docs` directory.
- It is also available on my [github page](https://monkeyshk.github.io/BuildModuleNetwork)

## How to run

- To generate the HTML again, there are two files (in `src` directory) to run:
- `makegraph.py` builds the dependencies graph and save the dict in a file.
- `buildnetwork.py` uses the file that makegraph provides, and builds the network visualization.

## Changelog
| Version | Changes |
| ------- | ------- |
| 1.0 | Initial Publish |