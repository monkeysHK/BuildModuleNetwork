# Module Dependency Visualization

This is a fun project to build a graph visualization for the module dependencies of Hypixel SkyBlock Wiki.

View it on:  
https://monkeyshk.github.io/BuildModuleNetwork/default.html  
https://monkeyshk.github.io/BuildModuleNetwork/hierarchical.html  

## Screenshots

![Screenshot for Default Version](/screenshot-default.jpg)
![Screenshot for Hierarchical Version](/screenshot-hierarchical.jpg)

## Structure

The source files are in the `src` directory. The generated intermediate files are in the `build` directory. The generated HTML file is in the `docs` directory.

## Running

Set up environment. If conda is used, run:

```
conda create -n buildmodulenetwork python=3.12 -y
conda activate buildmodulenetwork
conda install --file requirements.txt -y
```

First, generate the module dependency graph:

```
python src/makegraph.py
```

This updates the intermediate files in the `build` directory.

Then, generate the HTML file:

```
python src/buildnetwork.py
```

This creates the HTML file in the `docs` directory.

## How It Works

With a user-defined list or an API requested list of all module pages as starting pages, using BFS, the program will crawl through its dependencies, dependencies of dependencies, and so on.

To get the dependencies, the program will first request the page content using MediaWiki's API, then detect its module dependencies.

The detection of module dependencies is solely string pattern detection based on how wiki users import their modules.

After that, it builds the nodes and edges in a directed graph following the USES and COMPRISES relation. Note that this program cannot differentiate between USES and COMPRISES relations. We call all of them USES relations for convenience. If module A imports (USES) module B, an arrow points from A to B.

## Changelog

| Version | Changes |
| ------- | ------- |
| 1.4 | Use dark mode. Add hierarchical version. The arrow direction is reversed again to follow the USES relation |
| 1.3 | Minor fixes. Reverted change in arrow direction |
| 1.2 | New color for external pages. Fixed first letter casing. Now uses all existing modules as starting points. A change in arrow direction |
| 1.1 | New color for data pages. Directed graph |
| 1.0 | Initial Release |
