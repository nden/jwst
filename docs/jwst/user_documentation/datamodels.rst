===============
JWST Datamodels
===============

The `jwst` package also contains the interface for JWST Datamodels. JWST data
consists of a mix of FITS and ASDF (to seralize world coordinate system
information) - datamodels were designed to abstract away these intricicies and
provide a simple interface to the data. 