.. figure:: docs/assets/outset-wordmark.png
   :target: https://github.com/mmore500/outset
   :alt: outset wordmark

|PyPi| |CI| |Deploy Sphinx documentation to Pages| |GitHub stars|

Easily indicate zoom plot areas in Matplotlib

- Free software: MIT license
- Documentation: https://mmore500.com/outset
- Repository: https://github.com/mmore500/outset


Features
--------

Gallery
-------

.. figure:: docs/assets/outset-gallery-collage.png
   :target: https://mmore500.com/outset/gallery.html
   :alt: outset gallery collage

Check out the project's `gallery page <https://mmore500.com/outset/gallery.html>`_ for example heatmap, imshow, kde lineplot, regplot, scatterplot, patch, and more visualizations created with ``outset``.

Basic Usage
-----------

API Overview
------------

* `outset.OutsetGrid <https://mmore500.com/outset/_autosummary/outset.OutsetGrid.html>`_

   * render a source plot and zoom regions over it (e.g., "outsets") on a multiplot lattice
   * designate zoom regions directly, or as regions containing data subsets
   * object-oriented, tidy data compatible interface a la `FacetGrid`

* `outset.inset_outsets <https://mmore500.com/outset/_autosummary/outset.inset_outsets.html>`_

   * rearrange a `FacetGrid` to place outset zoom regions as insets over the original source axes

* `outset.marqueeplot <https://mmore500.com/outset/_autosummary/outset.marqueeplot.html>`_

   * axis-level "tidy data" interface to draw marquees framing specified subsets of data

* `outset.draw_marquee <https://mmore500.com/outset/_autosummary/outset.draw_marquee.html>`_

   * low-level interface to draw individual marquee annotations


Customizing Extensions
^^^^^^^^^^^^^^^^^^^^^^

Callout mark glyphs:

.. image:: docs/assets/callout-mark-glyphs.png
   :alt: comparison of available glyphs

* |MarkAlphabeticalBadges|_
* |MarkArrow|_
* |MarkInlaidAsterisk|_
* |MarkMagnifyingGlass|_
* |MarkRomanBadges|_

.. |MarkAlphabeticalBadges| replace:: ``MarkAlphabeticalBadges``
.. _MarkAlphabeticalBadges: https://mmore500.com/outset/_autosummary/outset.mark.MarkAlphabeticalBadges.html

.. |MarkArrow| replace:: ``MarkArrow``
.. _MarkArrow: https://mmore500.com/outset/_autosummary/outset.mark.MarkArrow.html

.. |MarkInlaidAsterisk| replace:: ``MarkInlaidAsterisk``
.. _MarkInlaidAsterisk: https://mmore500.com/outset/_autosummary/outset.mark.MarkInlaidAsterisk.html

.. |MarkMagnifyingGlass| replace:: ``MarkMagnifyingGlass``
.. _MarkMagnifyingGlass: https://mmore500.com/outset/_autosummary/outset.mark.MarkMagnifyingGlass.html

.. |MarkRomanBadges| replace:: ``MarkRomanBadges``
.. _MarkRomanBadges: https://mmore500.com/outset/_autosummary/outset.mark.MarkRomanBadges.html

Callout layout tweaks:

* `TweakReflect <https://mmore500.com/outset/_autosummary/outset.tweak.TweakReflect.html>`_
* `TweakSpreadArea <https://mmore500.com/outset/_autosummary/outset.tweak.TweakSpreadArea.html>`_

Read the full API documentation `here <https://mmore500.com/outset/_autosummary/outset.html#module-outset>`_.

Install
-------

``python3 -m pip install outset``

Citation
--------

Contributing
------------

This project welcomes contributions and suggestions. Our documentation includes `detailed information to get you started <https://mmore500.com/outset/contributing.html#>`__.

.. |PyPi| image:: https://img.shields.io/pypi/v/outset.svg
   :target: https://pypi.python.org/pypi/outset
.. |CI| image:: https://github.com/mmore500/outset/actions/workflows/CI.yml/badge.svg
   :target: https://github.com/mmore500/outset/actions
.. |Deploy Sphinx documentation to Pages| image:: https://github.com/mmore500/outset/actions/workflows/sphinx.yml/badge.svg
   :target: https://github.com/mmore500/outset/actions/workflows/sphinx.yml
.. |GitHub stars| image:: https://img.shields.io/github/stars/mmore500/outset.svg?style=round-square&logo=github&label=Stars&logoColor=white
   :target: https://github.com/mmore500/outset
