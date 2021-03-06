/ NIRSpec configuration (NIRSpec only)

FILTER    = input('FWA_POS')   /       name of the filter element used
GRATING   = input('GWA_POS')   /       name of the grating element used
GWAXTILT  = input('GWA_XTIL') or 0.0  /       grating x tilt
GWAYTILT  = input('GWA_YTIL') or 0.0  /       grating y tilt
FXD_SLIT  = 'NONE'            /       name of fixed slit aperture used
MSASTATE  = 'CONFIGURED'            /       state of MSA: all open, all closed, configured
FOCUSPOS  =   0.0              /       [mm] focus position for NIRSpec

