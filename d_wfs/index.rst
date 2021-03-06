.. _sec-driving-functions-wfs:

Driving functions for WFS
-------------------------

In the following, the driving functions for |WFS| in the frequency and temporal
domain for selected source models are presented. The temporal domain functions
consist of a filtering of the source signal and a weighting and delaying of the
individual secondary source signals. This property allows for a very efficient
implementation of |WFS| driving functions in the temporal domain. It is one of the
main advantages of |WFS| in comparison to most of the |NFC-HOA|, |SDM| solutions
discussed above.


.. _sec-driving-functions-wfs-plane-wave:

Plane Wave
~~~~~~~~~~

.. plot::
    :context: close-figs
    :nofigs:

    nk = 0, -1, 0  # direction of plane wave
    omega = 2 * np.pi * 1000  # frequency
    xref = 0, 0, 0  # 2.5D reference point
    x0, n0, a0 = sfs.array.circular(200, 1.5)
    grid = sfs.util.xyz_grid([-1.75, 1.75], [-1.75, 1.75], 0, spacing=0.02)
    d = sfs.mono.drivingfunction.wfs_25d_plane(omega, x0, n0, nk, xref)
    a = sfs.mono.drivingfunction.source_selection_plane(n0, nk)
    twin = sfs.tapering.tukey(a, .3)
    p = sfs.mono.synthesized.generic(omega, x0, n0, d * twin * a0 , grid,
        source=sfs.mono.source.point)
    normalization = 0.5
    sfs.plot.soundfield(normalization * p, grid)
    sfs.plot.secondarysource_2d(x0, n0, grid)

.. plot::
    :context:
    :include-source: false
    :nofigs:

    save_fig('wfs-25d-plane-wave')

.. _fig-wfs-25d-plane-wave:

.. figure:: wfs-25d-plane-wave.*
    :align: center

    Sound pressure for a monochromatic plane wave synthesized with 2.5D
    |WFS| :eq:`D.wfs.ps.2.5D`.  Parameters: :math:`\n_k = (0, -1, 0)`,
    :math:`\xref = (0, 0, 0)`, :math:`f = 1` kHz.

By inserting the source model of a plane wave :eq:`S.pw` into :eq:`D_wfs`
and :eq:`D25D_wfs` it follows

.. math::
    :label: D.wfs.pw

    D(\x_0,\w) = 2 w(\x_0) A(\w)
        \i\wc  \scalarprod{\n_k}{\n_{\x_0}}
        \e{-\i\wc  \scalarprod{\n_k}{\x_0}},

.. math::
    :label: D.wfs.pw.2.5D

    D_\text{2.5D}(\x_0,\w) = 2 w(\x_0) A(\w)
        \sqrt{2\pi|\xref-x_0|}
        \sqrt{\i\wc } \scalarprod{\n_k}{\n_{\x_0}}
        \e{-\i\wc  \scalarprod{\n_k}{\x_0}}.

Transferred to the temporal domain via an inverse Fourier transform :eq:`ifft`,
it follows

.. math::
    :label: d.wfs.pw

    d(\x_0,t) = 2 a(t) * h(t) * w(\x_0) \scalarprod{\n_k}{\n_{\x_0}}
        \dirac{t - \frac{\scalarprod{\n_k}{\x_0}}{c}},

.. math::
    :label: d.wfs.pw.2.5D

    \begin{aligned}
        d_\text{2.5D}(\x_0,t) =& 2 a(t) * h_\text{2.5D}(t) * w(\x_0)
            \sqrt{2\pi|\xref-x_0|} \\
            &\cdot \scalarprod{\n_k}{\n_{\x_0}}
            \dirac{t - \frac{\scalarprod{\n_k}{\x_0}}{c}},
    \end{aligned}

where

.. math::
    :label: h.wfs

    h(t) = \mathcal{F}^{-1}\left\{\i\wc \right\},

and

.. math::
    :label: h.wfs.2.5D

    h_\text{2.5D}(t) = \mathcal{F}^{-1}\left\{
        \sqrt{\i\wc }\right\}

denote the so called pre-equalization filters in |WFS|.

The window function :math:`w(\x_0)` for a plane wave as source model can be
calculated after :cite:`Spors2008` as

.. math::
    :label: wfs.pw.selection

    w(\x_0) = 
        \begin{cases}
            1 & \scalarprod{\n_k}{\n_{\x_0}} > 0 \\
            0 & \text{else}
        \end{cases}


.. _sec-driving-functions-wfs-point-source:

Point Source
~~~~~~~~~~~~

.. plot::
    :context: close-figs
    :nofigs:

    xs = 0, 2.5, 0  # position of source
    omega = 2 * np.pi * 1000  # frequency
    xref = 0, 0, 0  # 2.5D reference point
    x0, n0, a0 = sfs.array.circular(200, 1.5)
    grid = sfs.util.xyz_grid([-1.75, 1.75], [-1.75, 1.75], 0, spacing=0.02)
    d = sfs.mono.drivingfunction.wfs_25d_point(omega, x0, n0, xs, xref)
    a = sfs.mono.drivingfunction.source_selection_point(n0, x0, xs)
    twin = sfs.tapering.tukey(a, .3)
    p = sfs.mono.synthesized.generic(omega, x0, n0, d * twin * a0 , grid,
        source=sfs.mono.source.point)
    normalization = 1.3
    sfs.plot.soundfield(normalization * p, grid)
    sfs.plot.secondarysource_2d(x0, n0, grid)

.. plot::
    :context:
    :include-source: false
    :nofigs:

    save_fig('wfs-25d-point-source')

.. _fig-wfs-25d-point-source:

.. figure:: wfs-25d-point-source.*
    :align: center

    Sound pressure for a monochromatic point source synthesized with 2.5D
    |WFS| :eq:`D.wfs.ps.2.5D`.  Parameters: :math:`\xs = (0, 2.5, 0)` m,
    :math:`\xref = (0, 0, 0)`, :math:`f = 1` kHz.

By inserting the source model for a point source :eq:`S.ps` into :eq:`D_wfs`
it follows

.. math::
    :label: D.wfs.ps.woapprox

    D(\x_0,\w) =
        \frac{1}{2\pi} A(\w) w(\x_0) \i\wc
        \left(1 + \frac{1}{\i\wc|\x_0-\xs|} \right)
        \frac{\scalarprod{\x_0-\xs}{\n_{\x_0}}}{|\x_0-\xs|^2}
        \e{-\i\wc |\x_0-\xs|}.

Under the assumption of :math:`\wc |\x_0-\xs| \gg 1`,
:eq:`D.wfs.ps.woapprox` can be approximated by :cite:`Schultz2016`, eq. (2.118)

.. math::
    :label: D.wfs.ps

    D(\x_0,\w) = \frac{1}{2\pi} A(\w) w(\x_0) \i\wc
        \frac{\scalarprod{\x_0-\xs}{\n_{\x_0}}}{|\x_0-\xs|^2}
        \e{-\i\wc |\x_0-\xs|}.

It has the advantage that its temporal domain version could again be implemented
as a simple weighting- and delaying-mechanism.

To reach at 2.5D for a point source, we will start in 3D and apply stationary
phase approximations instead of directly using :eq:`D25D_wfs` -- see discussion
after :cite:`Schultz2016`, (2.146). Under the assumption of :math:`\frac{\omega}{c}
(|\x_0-\xs| + |\x-\x_0|) \gg 1` it then follows :cite:`Schultz2016`, eq.
(2.137), :cite:`Start1997`, eq. (3.10, 3.11)

.. math::
    :label: D.wfs.ps.2.5D

    \begin{aligned}
        D_\text{2.5D}(\x_0,\w) =&
            \frac{1}{\sqrt{2\pi}} A(\w) w(\x_0) \sqrt{\i\wc}
            \sqrt{\frac{|\xref-\x_0|}{|\xref-\x_0|+|\x_0-\xs|}} \\
            &\cdot \frac{\scalarprod{\x_0-\xs}{\n_{\x_0}}}
            {|\x_0-\xs|^{\frac{3}{2}}}
            \e{-\i\wc |\x_0-\xs|},
    \end{aligned}

whereby :math:`\xref` is a reference point at which the synthesis is correct.
A second stationary phase approximation can be applied to reach at
:cite:`Schultz2016`, eq. (2.131, 2.141), :cite:`Start1997`, eq. (3.16, 3.17)

.. math::
    :label: D.wfs.ps.2.5D.refline

    \begin{aligned}
        D_\text{2.5D}(\x_0,\w) =&
            \frac{1}{\sqrt{2\pi}} A(\w) w(\x_0) \sqrt{\i\wc}
            \sqrt{\frac{d_\text{ref}}{d_\text{ref}+d_\text{s}}} \\
            &\cdot \frac{\scalarprod{\x_0-\xs}{\n_{\x_0}}}
            {|\x_0-\xs|^{\frac{3}{2}}}
            \e{-\i\wc |\x_0-\xs|},
    \end{aligned}

which is the traditional formulation of a point source in |WFS| as given by eq.
(2.27) in :cite:`Verheijen1997` [#F1]_. Now :math:`d_\text{ref}` is the distance
of a line parallel to the secondary source distribution and :math:`d_\text{s}`
the shortest possible distance from the point source to the linear secondary
source distribution.

The default |WFS| driving functions for a point source in the SFS Toolbox are
:eq:`D.wfs.ps` and :eq:`D.wfs.ps.2.5D`.  Transferring both to the temporal
domain via an inverse Fourier transform :eq:`ifft` it follows

.. math::
    :label: d.wfs.ps

    d(\x_0,t) = \frac{1}{2{\pi}} a(t) * h(t) * w(\x_0)
        \frac{\scalarprod{\x_0-\xs}{\n_{\x_0}}}{|\x_0-\xs|^2}
        \dirac{t-\frac{|\x_0-\xs|}{c}},

.. math::
    :label: d.wfs.ps.2.5D

    \begin{aligned}
        d_\text{2.5D}(\x_0,t) =&
            \frac{1}{\sqrt{2\pi}} a(t) * h_\text{2.5D}(t) * w(\x_0)
            \sqrt{\frac{|\xref-\x_0|}{|\x_0-\xs|+|\xref-\x_0|}} \\
            &\cdot \frac{\scalarprod{\x_0-\xs}{\n_{\x_0}}}
            {|\x_0-\xs|^{\frac{3}{2}}}
            \dirac{t-\frac{|\x_0-\xs|}{c}}, \\
    \end{aligned}

.. math::
    :label: d.wfs.ps.2.5D.refline

    \begin{aligned}
    d_\text{2.5D}(\x_0,t) =&
        \frac{1}{\sqrt{2\pi}} a(t) * h_\text{2.5D}(t) * w(\x_0)
        \sqrt{\frac{d_\text{ref}}{d_\text{ref}+d_\text{s}}} \\
        &\cdot \frac{\scalarprod{\x_0-\xs}{\n_{\x_0}}}
        {|\x_0-\xs|^{\frac{3}{2}}}
        \dirac{t-\frac{|\x_0-\xs|}{c}}.
    \end{aligned}

The window function :math:`w(\x_0)` for a point source as source model can be
calculated after :cite:`Spors2008` as

.. math::
    :label: wfs.ps.selection

    w(\x_0) = 
        \begin{cases}
            1 & \scalarprod{\x_0-\xs}{\n_{\x_0}} > 0 \\
            0 & \text{else}
        \end{cases}


.. _sec-driving-functions-wfs-line-source:

Line Source
~~~~~~~~~~~

.. plot::
    :context: close-figs
    :nofigs:

    xs = 0, 2.5, 0  # position of source
    omega = 2 * np.pi * 1000  # frequency
    x0, n0, a0 = sfs.array.circular(200, 1.5)
    grid = sfs.util.xyz_grid([-1.75, 1.75], [-1.75, 1.75], 0, spacing=0.02)
    d = sfs.mono.drivingfunction.wfs_2d_line(omega, x0, n0, xs)
    a = sfs.mono.drivingfunction.source_selection_line(n0, x0, xs)
    twin = sfs.tapering.tukey(a, .3)
    p = sfs.mono.synthesized.generic(omega, x0, n0, d * twin * a0 , grid,
        source=sfs.mono.source.point)
    normalization = 7
    sfs.plot.soundfield(normalization * p, grid)
    sfs.plot.secondarysource_2d(x0, n0, grid)

.. plot::
    :context:
    :include-source: false
    :nofigs:

    save_fig('wfs-25d-line-source')

.. _fig-wfs-25d-line-source:

.. figure:: wfs-25d-line-source.*
    :align: center

    Sound pressure for a monochromatic line source synthesized with 2D
    |WFS| :eq:`D.wfs.ls`.  Parameters: :math:`\xs = (0, 2.5, 0)` m,
    :math:`\xref = (0, 0, 0)`, :math:`f = 1` kHz.

For a line source its orientation :math:`\n_\text{s}` has an influence on the
synthesized sound field as well.  Let :math:`|\vec{v}|` be the distance between
:math:`\x_0` and the line source with

.. math::
    :label: v.ls

    \vec{v} = \x_0-\xs - \scalarprod{\x_0-\xs}{\n_\text{s}} \n_\text{s},

where :math:`|\n_\text{s}| = 1`. For a 2D or 2.5D secondary source setup and
a line source orientation perpendicular to the plane where the
secondary sources are located this automatically simplifies to :math:`\vec{v} =
\x_0 - \xs`.

By inserting the source model for a line source :eq:`S.ls` into :eq:`D_wfs`
and :eq:`D25D_wfs` and calculating the derivate of the Hankel function after
`<http://dlmf.nist.gov/10.6.E6>`_ it follows

.. math::
    :label: D.wfs.ls

    D(\x_0,\w) = -\frac{1}{2}A(\w) w(\x_0) \i\wc
        \frac{\scalarprod{\vec{v}}{\n_{\x_0}}}{|\vec{v}|}
        \Hankel{2}{1}{\wc |\vec{v}|},

.. math::
    :label: D.wfs.ls.2.5D

    D_\text{2.5D}(\x_0,\w) =
        -\frac{1}{2}g_0 A(\w) w(\x_0) \sqrt{\i\wc}
        \frac{\scalarprod{\vec{v}}{\n_{\x_0}}}{|\vec{v}|}
        \Hankel{2}{1}{\wc |\vec{v}|}.


Applying :math:`\Hankel{2}{1}{\zeta} \approx -\sqrt{\frac{2}{\pi\i}\zeta}
\e{-\i\zeta}` for :math:`z\gg1` after :cite:`Williams1999`, eq. (4.23) and
transferred to the temporal domain via an inverse Fourier transform :eq:`ifft`
it follows

.. math::
    :label: d.wfs.ls

    d(\x_0,t) = \sqrt{\frac{1}{2\pi}} a(t) * h(t) * w(\x0)
        \frac{\scalarprod{\vec{v}}{\n_{\x_0}}}{|\vec{v}|^{\frac{3}{2}}}
        \dirac{t-\frac{|\vec{v}|}{c}},

.. math::
    :label: d.wfs.ls.2.5D

    d_\text{2.5D}(\x_0,t) =
        g_0 \sqrt{\frac{1}{2\pi}} a(t) *
        {\mathcal{F}^{-1}\left\{\sqrt{\frac{c}
        {\i\w}}\right\}} * w(\x0)
        \frac{\scalarprod{\vec{v}}{\n_{\x_0}}}{|\vec{v}|^{\frac{3}{2}}}
        \dirac{t-\frac{|\vec{v}|}{c}},

The window function :math:`w(\x_0)` for a line source as source model can be
calculated after :cite:`Spors2008` as

.. math::
    :label: wfs.ls.selection

    w(\x_0) = 
        \begin{cases}
            1 & \scalarprod{\vec{v}}{\n_{\x_0}} > 0 \\
            0 & \text{else}
        \end{cases}


.. _sec-driving-functions-wfs-focused-source:

Focused Source
~~~~~~~~~~~~~~

.. plot::
    :context: close-figs
    :nofigs:

    xs = 0, 0.5, 0  # position of source
    ns = 0, -1, 0  # direction of source
    omega = 2 * np.pi * 1000  # frequency
    xref = 0, 0, 0  # 2.5D reference point
    x0, n0, a0 = sfs.array.circular(200, 1.5)
    grid = sfs.util.xyz_grid([-1.75, 1.75], [-1.75, 1.75], 0, spacing=0.02)
    d = sfs.mono.drivingfunction.wfs_25d_focused(omega, x0, n0, xs, xref)
    a = sfs.mono.drivingfunction.source_selection_focused(ns, x0, xs)
    twin = sfs.tapering.tukey(a, .3)
    p = sfs.mono.synthesized.generic(omega, x0, n0, d * twin * a0 , grid,
        source=sfs.mono.source.point)
    normalization = 1
    sfs.plot.soundfield(normalization * p, grid)
    sfs.plot.secondarysource_2d(x0, n0, grid)

.. plot::
    :context:
    :include-source: false
    :nofigs:

    save_fig('wfs-25d-focused-source')

.. _fig-wfs-25d-focused-source:

.. figure:: wfs-25d-focused-source.*
    :align: center

    Sound pressure for a monochromatic focused source synthesized with 2.5D
    |WFS| :eq:`D.wfs.fs.2.5D`.  Parameters: :math:`\xs = (0, 0.5, 0)` m,
    :math:`\n_\text{s} = (0, -1, 0)`, :math:`\xref = (0, 0, 0)`, :math:`f = 1`
    kHz.

As mentioned before, focused sources exhibit a field that converges in a focal
point inside the audience area. After passing the focal point, the field becomes
a diverging one as can be seen in :numref:`fig-wfs-25d-focused-source`. In order
to choose the active secondary sources, especially for circular or spherical
geometries, the focused source also needs a direction :math:`\n_\text{s}`.

The driving function for a focused source is given by the time-reversed
versions of the driving function for a point source :eq:`d.wfs.ps` and
:eq:`d.wfs.ps.2.5D` as

.. math::
    :label: D.wfs.fs

    D(\x_0,\w) = \frac{1}{2\pi} A(\w) w(\x_0) \i\wc
        \frac{\scalarprod{\x_0-\xs}{\n_{\x_0}}}{|\x_0-\xs|^2}
        \e{\i\wc |\x_0-\xs|}.

The 2.5D driving functions are given by the time-reversed version of
:eq:`d.wfs.ps.2.5D` for a reference point after :cite:`Verheijen1997`,
eq. (A.14) as

.. math::
    :label: D.wfs.fs.2.5D

    \begin{aligned}
        D_\text{2.5D}(\x_0,\w) =&
            \frac{1}{\sqrt{2\pi}} A(\w) w(\x_0) \sqrt{\i\wc}
            \sqrt{\frac{|\xref-\x_0|}{||\x_0-\xs|-|\xref-\x_0||}} \\
            &\cdot \frac{\scalarprod{\x_0-\xs}{\n_{\x_0}}}
                        {|\x_0-\xs|^{\frac{3}{2}}}
            \e{\i\wc |\x_0-\xs|},
    \end{aligned}

and the time reversed version of :eq:`d.wfs.ps.2.5D.refline` for a reference
line, compare :cite:`Start1997`, eq. (3.16)

.. math::
    :label: D.wfs.fs.2.5D.refline

    \begin{aligned}
        D_\text{2.5D}(\x_0,\w) =&
            \frac{1}{\sqrt{2\pi}} A(\w) w(\x_0) \sqrt{\i\wc}
            \sqrt{\frac{d_\text{ref}}{d_\text{ref}-d_\text{s}}} \\
            &\cdot \frac{\scalarprod{\x_0-\xs}{\n_{\x_0}}}
                        {|\x_0-\xs|^{\frac{3}{2}}}
            \e{\i\wc |\x_0-\xs|},
    \end{aligned}

where :math:`d_\text{ref}` is the distance of a line parallel to the secondary
source distribution and :math:`d_\text{s}` the shortest possible distance from
the focused source to the linear secondary source distribution.

Transferred to the temporal domain via an inverse Fourier transform :eq:`ifft` it
follows

.. math::
    :label: d.wfs.fs

    d(\x_0,t) = \frac{1}{2{\pi}} a(t) * h(t) * w(\x_0)
        \frac{\scalarprod{\x_0-\xs}{\n_{\x_0}}}{|\x_0-\xs|^2}
        \dirac{t+\frac{|\x_0-\xs|}{c}},

.. math::
    :label: d.wfs.fs.2.5D

    \begin{aligned}
        d_\text{2.5D}(\x_0,t) =&
            \frac{1}{\sqrt{2\pi}} a(t) * h_\text{2.5D}(t) * w(\x_0)
            \sqrt{\frac{|\xref-\x_0|}{||\x_0-\xs|-|\xref-\x_0||}} \\
            &\cdot \frac{\scalarprod{\x_0-\xs}{\n_{\x_0}}}
                        {|\x_0-\xs|^{\frac{3}{2}}}
            \dirac{t+\frac{|\x_0-\xs|}{c}}, \\
    \end{aligned}

.. math::
    :label: d.wfs.fs.2.5D.refline

    \begin{aligned}
        d_\text{2.5D}(\x_0,t) =&
            \frac{1}{\sqrt{2\pi}} a(t) * h_\text{2.5D}(t) * w(\x_0)
            \sqrt{\frac{d_\text{ref}}{d_\text{ref}-d_\text{s}}} \\
            &\cdot \frac{\scalarprod{\x_0-\xs}{\n_{\x_0}}}
                        {|\x_0-\xs|^{\frac{3}{2}}}
            \dirac{t+\frac{|\x_0-\xs|}{c}}.
    \end{aligned}

In this document a focused source always refers to the time-reversed version of a
point source, but a focused line source can be defined in the same way starting
from :eq:`D.wfs.ls`

.. math::
    :label: D.wfs.fs.ls

    D(\x_0,\w) = -\frac{1}{2}A(\w) w(\x_0) \i\wc 
        \frac{\scalarprod{\x_0-\xs}{\n_{\x_0}}}{|\x_0-\xs|}
        \Hankel{1}{1}{\wc |\x_0-\xs|}.

Transferred to the temporal domain via an inverse Fourier transform :eq:`ifft`
it follows

.. math::
    :label: d.wfs.fs.ls

    d(\x_0,t) = \sqrt{\frac{1}{2\pi}} a(t) * h(t) * w(\x0)
        \frac{\scalarprod{\x_0-\xs}{\n_{\x_0}}}{|\x_0-\xs|^{\frac{3}{2}}}
        \dirac{t+\frac{|\x_0-\xs|}{c}}.

The window function :math:`w(\x_0)` for a focused source can be calculated as

.. math::
    :label: wfs.fs.selection

    w(\x_0) = 
        \begin{cases}
            1 & \scalarprod{\n_\text{s}}{\xs-\x_0} > 0 \\
            0 & \text{else}
        \end{cases}


.. [#F1]
    Whereby :math:`r` corresponds to :math:`|\x_0-\xs|` and :math:`\cos\varphi`
    to :math:`\frac{\scalarprod{\x_0-\xs}{\n_{\x_0}}}{|\x_0-\xs|}`.

.. vim: filetype=rst spell:
