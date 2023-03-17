from maptools import MapRoutine
import os

os.environ.get('NVCIM_HOME')
routine = MapRoutine(mapname='sasa')
routine.run()