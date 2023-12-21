# EmberMaker

## Purpose
EmberMaker is a scientific graphic library aimed at (re)producing "burning ember" diagrams 
of the style used in IPCC (Intergovernmental Panel on Climate Change) reports.

EmberMaker was formerly a part of the EmberFactory project: https://pypi.org/project/EmberFactory/. 
This is now a separate project, which provides an API for drawing burning ember and related diagrams. 
The EmberFactory project now focuses on the web interface and uses EmberMaker for reading ember data and drawing.

## How to use
If you need to produce ember diagrams from your data, first consider using the [EmberFactory](https://pypi.org/project/EmberFactory/).

For specific developments, this library may help you:
### Access within python (see /examples/python): 
- 'create_and_draw_embers.py' is the shorter and simpler. It illustrates a few functions constructing embers from data.
- 'draw_embers_from_file.py' reads 'traditional' ember Excel sheets and shows how an x-y plot can be added.
- 'test_error_reporting.py' illustrates a few cases which produce warning or error messages and how to access these.
### Access from R (see /examples/R):
- 'create_and_draw_embers.R' illustrates functions constructing embers, within an R script and using data produced in R.

Creating embers only needs calling a few functions (as further illustrated in 'draw_embers_from_file.py'):

- Create an ember: <br/>
`be = emb.Ember(haz_valid=[0, 5])` Defining a valid range for the 'hazard metric' (typically GMST) is mandatory.
- Create one or more transitions within this ember <br/>
`be.trans_create(name='undetectable to moderate', min=0.6, max=1.4, confidence='very high')`
- Create an ember graph <br/>
`egr = EmberGraph('test_file', grformat="PDF")`
- Add ember to graph (creating an ember group automatically; a list of embers would work as well): <br/>
`egr.add(be)`
- Actually produce the diagram <br/>
`egr.draw()`

As this is the first "standalone" version, the API functions may be improved in the future, as well as more documented.
We are interested in learning how you use this and any difficult you might face, to steer future development, thanks!

## Development history
The EmberFactory software was created by philippe.marbaix -at- uclouvain.be at the end of 2019.
The first objective was to produce figure 3 of Zommers et al. 2020 ([doi.org/10/gg985p](https://doi.org/10/gg985p)).
