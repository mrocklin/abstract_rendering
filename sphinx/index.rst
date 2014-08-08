.. Abstract Rendering documentation master file, created by
   sphinx-quickstart on Mon Jun 30 11:31:58 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Abstract Rendering
==============================================
.. toctree::
   :hidden:
   :maxdepth: 2
   
   examples.rst
   api.rst

Abstract rendering (AR) is a framework for analyzing and improving visualizations.
The basic idea is that visualizations are useful when the pixels meaningfully 
correspond to source data.  By making that link more explicit, AR
enables a number of useful techniques for working with data of all sizes.


InfoVis Reference Model
-----------------------
AR focuses on information visualization style visualizations, 2D representations 
of abstract data, rather than scientific visualization. AR interrupts the standard
visualization pipeline and provides the opportunity for further analysis.  To understand
the process and opportunities, first an overview of the InfoVis Reference Model (Chi'99)

The InfoVis reference model defines four stages:
- Source Data: Raw data
- Data Tables: Organized and schematized
- Visual Abstractions: Geometric representations such as points, shapes and colors
- Views: Displayed on the screen

The transitions between these four stages are:
- Data Transformations: Convert source data into tables (or tables into further tables)
- Visual Mappings: Convert data tables into visual abstractions
- View Transformations: Convert visual mappings into concrete representations

Abstract rendering steps in as a type of view transformation.  However, instead of
producing an image to be displayed on the screen, it builds a data table!  This
new data table is a grid structure that correspond to pixels on the screen.  Instead of 
using colors, it uses other data values to describe the values that underly the 
visual abstractions that would have painted onto corresponding pixels.  

For example, the Anderson's Iris dataset data is often presented as petal width vs. petal length.
Each data point also has a species associated with it.  Visual mapping places each
observation at an X/Y position and colors it according to the species.
View transformations put those mappings at a specific location on the screen and fill in 
the points with colors.  Otherwise said, standard rendering produces a table of colors. 
*Abstract* rendering retains the visual mappings and the view transformations but is 
does not necessarily produce a grid of colors.  Instead, the grid may be populated by
a dictionary with keys for each species and values for the number of observations whose
visual abstraction touched that pixel (under the current view transformation).  
This new data table is rich with information both about the underlying dataset and how it
is being visualized, providing many opportunities to improve the visualization.

Abstract Rendering
-------------------

Abstract rendering is achieved by four different function types, 
cooperating in (at least) two phases.  When properly combined,
instances of the four function roles first produce a grid of bin
values and then produce a new visual representation.

The four function roles are:

- Selector: Determines which visual abstractions correspond to which bins.
  The selector often corresponds to classical visualization algorithms
  such as applying affine transforms or running the Bressenham line algorithm.
- Info: Because AR does not (necessarily) combine colors, some alternative
  value must be provided for each visual abstraction.  The info function
  provides that data value.  This may be as simple as a constant for all inputs
  or returning the category from the source data.
- Aggregator: Combines info values that land in the same bin.  Max, Sum, Last, First
  are all useful aggregator functions.
- Shader: Transforms sets of bin values into new forms.  This may be new sets of bin values,
  an image or new geometric abstractions (such as ISO contours).

The first three function roles (Selector, Info and Aggregator) transform visual
abstractions into grids of values, called 'bin values', 'bin grids' or sometimes 'aggregates'.
This first phase is called 'aggregation' and is executed on the visual abstractions.

Shaders are run on the results of aggregation to analyze and re-represent the resulting
values.  A typical shader pipeline is usually three or four stages long.  Shader chains
typically end with a new image, that can be directly displayed.  However, if a shader chain
ends with a new set of visual abstractions, a new round of abstract rendering could be applied.
Whether working with one shader or a chain of many, whether it ends in an image, a geometric
representation or a boolean value, all shader chains start with a grid of bin values.  
Shading is, therefore, considered the second phase of abstract rendering.

Contact
-------
For questions, please contact Joseph Cottam (jcottam at indiana.edu).


Thanks
------

Abstract rendering is developed with funding from `DARPA <http://www.darpa.mil>`_'s
`XDATA <http://www.darpa.mil/Our_Work/I2O/Programs/XDATA.aspx>`_ program and
support from `Continuum Analytics <http://http://continuum.io/>`_.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

