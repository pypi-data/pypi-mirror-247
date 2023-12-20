``eradiate.pipelines``
======================

.. automodule:: eradiate.pipelines

.. py:currentmodule:: eradiate.pipelines

Basic pipeline infrastructure
-----------------------------
.. autosummary::
   :toctree: generated/autosummary/

   Pipeline
   PipelineStep

Gather step
-----------
.. autosummary::
   :toctree: generated/autosummary/

   GatherMono
   GatherCKD

Aggregate steps
---------------
.. autosummary::
   :toctree: generated/autosummary/

   AggregateCKDQuad
   AggregateRadiosity

Assemble steps
--------------
.. autosummary::
   :toctree: generated/autosummary/

   AddViewingAngles
   AddIllumination
   AddSpectralResponseFunction

Compute steps
-------------
.. autosummary::
   :toctree: generated/autosummary/

   ComputeReflectance
   ComputeAlbedo
   ApplySpectralResponseFunction
