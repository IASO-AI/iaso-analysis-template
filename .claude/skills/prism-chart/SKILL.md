---
name: prism-chart
description: Create publication-quality scientific charts in GraphPad Prism style using Python/matplotlib. Use when building bar charts, scatter plots, survival curves, dose-response curves, or any scientific figure that should look like it was made in GraphPad Prism. Supports error bars, statistical annotations, grouped comparisons, and all common biomedical chart types.
---

# GraphPad Prism Style Chart Skill

Generate publication-ready scientific figures that replicate the clean, recognizable GraphPad Prism aesthetic using Python and matplotlib.

## Core Style Definition

### Prism Global Style Setup

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from scipy import stats

def apply_prism_style():
    """Apply GraphPad Prism-like global style to matplotlib."""
    mpl.rcParams.update({
        # Font: Arial is Prism's default
        'font.family': 'Arial',
        'font.size': 12,
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'axes.labelsize': 12,
        'axes.labelweight': 'bold',
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,

        # L-shaped axes: only left and bottom spines
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.linewidth': 1.5,

        # Ticks pointing outward
        'xtick.direction': 'out',
        'ytick.direction': 'out',
        'xtick.major.width': 1.5,
        'ytick.major.width': 1.5,
        'xtick.major.size': 6,
        'ytick.major.size': 6,
        'xtick.minor.visible': False,
        'ytick.minor.visible': False,

        # Clean white background, no grid
        'axes.facecolor': 'white',
        'figure.facecolor': 'white',
        'axes.grid': False,

        # Legend
        'legend.frameon': False,
        'legend.fontsize': 10,

        # Figure
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.transparent': False,
    })

# Always call this before plotting
apply_prism_style()
```

### Prism Color Palettes

```python
# ── Classic Prism Default (most recognizable) ──
PRISM_DEFAULT = {
    'colors': ['#000000', '#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00', '#A65628', '#F781BF'],
    'name': 'Classic'
}

# ── Prism ColorBlind Safe ──
PRISM_COLORBLIND = {
    'colors': ['#000000', '#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7'],
    'name': 'ColorBlind Safe'
}

# ── Prism Paired (for grouped comparisons) ──
PRISM_PAIRED = {
    'colors': ['#1F78B4', '#A6CEE3', '#33A02C', '#B2DF8A', '#E31A1C', '#FB9A99', '#FF7F00', '#FDBF6F'],
    'name': 'Paired'
}

# ── Prism Warm Tones ──
PRISM_WARM = {
    'colors': ['#E41A1C', '#FF7F00', '#FFC107', '#A65628', '#F781BF', '#984EA3'],
    'name': 'Warm'
}

# ── Prism Cool Tones ──
PRISM_COOL = {
    'colors': ['#377EB8', '#4DAF4A', '#00BCD4', '#984EA3', '#607D8B', '#795548'],
    'name': 'Cool'
}

# ── Prism Grayscale (for B&W journals) ──
PRISM_GRAYSCALE = {
    'colors': ['#000000', '#4D4D4D', '#808080', '#B3B3B3', '#D9D9D9'],
    'name': 'Grayscale'
}

# Default palette shortcut
PRISM_COLORS = PRISM_DEFAULT['colors']
```

## Chart Type Templates

### 1. Bar Chart with Error Bars and Statistical Annotations

This is the most common Prism chart type in biomedical papers.

```python
def prism_bar_chart(data, groups, values, errors=None, error_type='SEM',
                    ylabel='', title='', colors=None, figsize=(4, 5),
                    stats_pairs=None, stats_labels=None,
                    individual_points=False, point_data=None):
    """
    Prism-style bar chart with error bars and optional stats annotations.

    Parameters:
        data: dict with keys as group names, values as mean values
              OR pd.DataFrame
        groups: list of group names (x-axis labels)
        values: list of mean values for each group
        errors: list of error values (SEM or SD)
        error_type: 'SEM' or 'SD' (for label only)
        ylabel: Y-axis label
        title: Chart title
        colors: list of colors (defaults to PRISM_COLORS)
        figsize: figure size tuple
        stats_pairs: list of tuples [(0,1), (1,2)] group index pairs for stat brackets
        stats_labels: list of stat labels ['**', 'ns'] matching stats_pairs
        individual_points: whether to overlay individual data points
        point_data: list of arrays, one per group, for individual points
    """
    apply_prism_style()
    colors = colors or PRISM_COLORS

    fig, ax = plt.subplots(figsize=figsize)
    x = np.arange(len(groups))
    bar_width = 0.6

    bars = ax.bar(x, values, width=bar_width,
                  color=[colors[i % len(colors)] for i in range(len(groups))],
                  edgecolor='black', linewidth=1.0,
                  zorder=2)

    # Error bars
    if errors is not None:
        ax.errorbar(x, values, yerr=errors,
                    fmt='none', ecolor='black', elinewidth=1.5,
                    capsize=5, capthick=1.5, zorder=3)

    # Overlay individual data points (Superplot style)
    if individual_points and point_data is not None:
        for i, pts in enumerate(point_data):
            jitter = np.random.uniform(-0.15, 0.15, len(pts))
            ax.scatter(x[i] + jitter, pts, color='black',
                       s=20, alpha=0.6, zorder=4, edgecolors='none')

    # Statistical annotation brackets
    if stats_pairs and stats_labels:
        y_max = max(v + (e if errors else 0) for v, e in zip(values, errors or [0]*len(values)))
        bracket_height = y_max * 0.05
        y_start = y_max * 1.08

        for (i, j), label in zip(stats_pairs, stats_labels):
            y = y_start
            ax.plot([x[i], x[i], x[j], x[j]],
                    [y, y + bracket_height, y + bracket_height, y],
                    color='black', linewidth=1.2, clip_on=False)
            ax.text((x[i] + x[j]) / 2, y + bracket_height * 1.2, label,
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
            y_start += y_max * 0.12

    ax.set_xticks(x)
    ax.set_xticklabels(groups)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)

    # Y-axis starts at 0
    ax.set_ylim(bottom=0)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins=6, integer=False))

    plt.tight_layout()
    return fig, ax
```

### 2. Grouped Bar Chart

```python
def prism_grouped_bar(groups, subgroups, data, errors=None,
                      ylabel='', title='', colors=None, figsize=(6, 5),
                      legend_title=''):
    """
    Prism-style grouped bar chart.

    Parameters:
        groups: list of group names (x-axis)
        subgroups: list of subgroup names (legend entries)
        data: 2D array/list, shape (n_groups, n_subgroups)
        errors: 2D array/list matching data shape (optional)
        ylabel: Y-axis label
        title: Chart title
        colors: list of colors for subgroups
    """
    apply_prism_style()
    colors = colors or PRISM_COLORS

    fig, ax = plt.subplots(figsize=figsize)
    n_sub = len(subgroups)
    bar_width = 0.8 / n_sub
    x = np.arange(len(groups))

    for i, sub in enumerate(subgroups):
        offset = (i - (n_sub - 1) / 2) * bar_width
        vals = [data[g][i] for g in range(len(groups))]
        errs = [errors[g][i] for g in range(len(groups))] if errors else None

        ax.bar(x + offset, vals, width=bar_width,
               color=colors[i % len(colors)], edgecolor='black',
               linewidth=0.8, label=sub, zorder=2)

        if errs:
            ax.errorbar(x + offset, vals, yerr=errs,
                        fmt='none', ecolor='black', elinewidth=1.2,
                        capsize=3, capthick=1.2, zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(groups)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.legend(title=legend_title, loc='best')
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    return fig, ax
```

### 3. Scatter Plot with Regression Line

```python
def prism_scatter(x_data, y_data, xlabel='', ylabel='', title='',
                  color=None, figsize=(5, 5), show_regression=True,
                  show_r2=True, show_ci=True):
    """
    Prism-style scatter plot with optional linear regression.

    Parameters:
        x_data, y_data: array-like data
        show_regression: overlay best-fit line
        show_r2: show R² value on plot
        show_ci: show 95% confidence interval band
    """
    apply_prism_style()
    color = color or PRISM_COLORS[1]

    fig, ax = plt.subplots(figsize=figsize)

    ax.scatter(x_data, y_data, color=color, s=40, edgecolors='black',
               linewidth=0.5, zorder=3, alpha=0.8)

    if show_regression:
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_data, y_data)
        x_line = np.linspace(min(x_data), max(x_data), 100)
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, color='black', linewidth=1.5, linestyle='-', zorder=2)

        if show_ci:
            n = len(x_data)
            y_pred = slope * np.array(x_data) + intercept
            se = np.sqrt(np.sum((np.array(y_data) - y_pred)**2) / (n - 2))
            x_mean = np.mean(x_data)
            sx2 = np.sum((np.array(x_data) - x_mean)**2)
            ci = 1.96 * se * np.sqrt(1/n + (x_line - x_mean)**2 / sx2)
            ax.fill_between(x_line, y_line - ci, y_line + ci,
                            color='gray', alpha=0.15, zorder=1)

        if show_r2:
            r2_text = f'R² = {r_value**2:.4f}\nP {"< 0.0001" if p_value < 0.0001 else f"= {p_value:.4f}"}'
            ax.text(0.05, 0.95, r2_text, transform=ax.transAxes,
                    fontsize=10, verticalalignment='top',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='none'))

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)

    plt.tight_layout()
    return fig, ax
```

### 4. Dot Plot / Strip Plot with Mean ± SEM

```python
def prism_dot_plot(groups, point_data, ylabel='', title='',
                   colors=None, figsize=(4, 5), show_mean_line=True,
                   error_type='SEM'):
    """
    Prism-style dot plot showing individual data points with mean ± SEM.

    Parameters:
        groups: list of group names
        point_data: list of arrays, one per group
        show_mean_line: overlay mean ± SEM horizontal lines
        error_type: 'SEM' or 'SD'
    """
    apply_prism_style()
    colors = colors or PRISM_COLORS

    fig, ax = plt.subplots(figsize=figsize)
    x = np.arange(len(groups))

    for i, pts in enumerate(point_data):
        jitter = np.random.uniform(-0.2, 0.2, len(pts))
        ax.scatter(x[i] + jitter, pts, color=colors[i % len(colors)],
                   s=35, edgecolors='black', linewidth=0.5, zorder=3, alpha=0.8)

        if show_mean_line:
            mean = np.mean(pts)
            err = stats.sem(pts) if error_type == 'SEM' else np.std(pts)
            # Mean horizontal line
            ax.plot([x[i] - 0.25, x[i] + 0.25], [mean, mean],
                    color='black', linewidth=2, zorder=4)
            # Error bars
            ax.errorbar(x[i], mean, yerr=err, fmt='none', ecolor='black',
                        elinewidth=1.5, capsize=6, capthick=1.5, zorder=4)

    ax.set_xticks(x)
    ax.set_xticklabels(groups)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    return fig, ax
```

### 5. Box Plot (Prism Style)

```python
def prism_box_plot(groups, point_data, ylabel='', title='',
                   colors=None, figsize=(4, 5), show_points=True,
                   whisker_style='min-max'):
    """
    Prism-style box plot.

    Parameters:
        groups: list of group names
        point_data: list of arrays, one per group
        show_points: overlay individual data points
        whisker_style: 'min-max' (Prism default) or 'tukey' (1.5 IQR)
    """
    apply_prism_style()
    colors = colors or PRISM_COLORS

    fig, ax = plt.subplots(figsize=figsize)

    whis = (0, 100) if whisker_style == 'min-max' else 1.5

    bp = ax.boxplot(point_data, labels=groups, widths=0.5,
                    patch_artist=True, whis=whis,
                    boxprops=dict(linewidth=1.5),
                    whiskerprops=dict(linewidth=1.5, color='black'),
                    capprops=dict(linewidth=1.5, color='black'),
                    medianprops=dict(linewidth=2, color='black'),
                    flierprops=dict(marker='o', markersize=4))

    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_edgecolor('black')
        patch.set_alpha(0.7)

    if show_points:
        for i, pts in enumerate(point_data):
            jitter = np.random.uniform(-0.12, 0.12, len(pts))
            ax.scatter(i + 1 + jitter, pts, color='black',
                       s=15, alpha=0.6, zorder=3, edgecolors='none')

    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)

    plt.tight_layout()
    return fig, ax
```

### 6. Kaplan-Meier Survival Curve

```python
def prism_survival_curve(time_data, event_data, group_labels,
                         xlabel='Time', ylabel='Survival Probability',
                         title='', colors=None, figsize=(6, 5),
                         show_censoring=True, show_ci=False,
                         show_median=False, show_at_risk=False):
    """
    Prism-style Kaplan-Meier survival curve.

    Parameters:
        time_data: list of arrays, time-to-event for each group
        event_data: list of arrays, event indicator (1=event, 0=censored)
        group_labels: list of group names
        show_censoring: show tick marks for censored observations
        show_ci: show 95% confidence intervals
        show_median: add median survival lines
        show_at_risk: add number-at-risk table below
    """
    apply_prism_style()
    colors = colors or PRISM_COLORS

    fig, ax = plt.subplots(figsize=figsize)

    for i, (times, events, label) in enumerate(zip(time_data, event_data, group_labels)):
        color = colors[i % len(colors)]

        # Sort by time
        order = np.argsort(times)
        times = np.array(times)[order]
        events = np.array(events)[order]

        # Kaplan-Meier estimator
        unique_times = np.unique(times[events == 1])
        survival = 1.0
        km_times = [0]
        km_survival = [1.0]

        for t in unique_times:
            at_risk = np.sum(times >= t)
            died = np.sum((times == t) & (events == 1))
            survival *= (1 - died / at_risk)
            km_times.append(t)
            km_survival.append(survival)

        # Extend to max time
        km_times.append(max(times))
        km_survival.append(km_survival[-1])

        # Step function
        ax.step(km_times, km_survival, where='post', color=color,
                linewidth=2, label=label, zorder=2)

        # Censoring marks
        if show_censoring:
            censor_times = times[events == 0]
            for ct in censor_times:
                idx = np.searchsorted(km_times, ct, side='right') - 1
                if idx >= 0 and idx < len(km_survival):
                    ax.plot(ct, km_survival[idx], '|', color=color,
                            markersize=8, markeredgewidth=2, zorder=3)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlim(left=0)
    ax.legend(loc='lower left')

    plt.tight_layout()
    return fig, ax
```

### 7. Dose-Response Curve (Sigmoidal)

```python
def prism_dose_response(doses, responses, group_labels=None,
                        xlabel='Concentration (log M)', ylabel='Response (%)',
                        title='', colors=None, figsize=(5, 4),
                        log_scale=True, show_ic50=True):
    """
    Prism-style dose-response (4PL sigmoidal) curve.

    Parameters:
        doses: list of arrays (concentration values per group)
        responses: list of arrays (response values per group)
        group_labels: list of group names
        log_scale: use log10 x-axis
        show_ic50: annotate IC50/EC50 on curve
    """
    from scipy.optimize import curve_fit
    apply_prism_style()
    colors = colors or PRISM_COLORS

    def four_pl(x, bottom, top, ic50, hill):
        return bottom + (top - bottom) / (1 + 10**((ic50 - x) * hill))

    fig, ax = plt.subplots(figsize=figsize)

    if not isinstance(doses[0], (list, np.ndarray)):
        doses = [doses]
        responses = [responses]
        group_labels = group_labels or ['']

    for i, (dose, resp) in enumerate(zip(doses, responses)):
        color = colors[i % len(colors)]
        label = group_labels[i] if group_labels else f'Group {i+1}'

        x = np.log10(dose) if log_scale else np.array(dose)
        y = np.array(resp)

        ax.scatter(x, y, color=color, s=30, edgecolors='black',
                   linewidth=0.5, zorder=3)

        try:
            popt, _ = curve_fit(four_pl, x, y,
                                p0=[min(y), max(y), np.median(x), 1],
                                maxfev=10000)
            x_fit = np.linspace(min(x), max(x), 200)
            y_fit = four_pl(x_fit, *popt)
            ax.plot(x_fit, y_fit, color=color, linewidth=2, label=label, zorder=2)

            if show_ic50:
                ic50_val = popt[2]
                y_at_ic50 = four_pl(ic50_val, *popt)
                ax.axhline(y=y_at_ic50, color='gray', linestyle=':', linewidth=0.8, alpha=0.5)
                ax.axvline(x=ic50_val, color='gray', linestyle=':', linewidth=0.8, alpha=0.5)
        except RuntimeError:
            ax.plot(x, y, color=color, linewidth=1.5, label=label, zorder=2)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    if group_labels and len(group_labels) > 1:
        ax.legend(loc='best')

    plt.tight_layout()
    return fig, ax
```

### 8. Violin Plot

```python
def prism_violin(groups, point_data, ylabel='', title='',
                 colors=None, figsize=(4, 5), show_median=True,
                 show_quartiles=True, show_points=False):
    """
    Prism-style violin plot.
    """
    apply_prism_style()
    colors = colors or PRISM_COLORS

    fig, ax = plt.subplots(figsize=figsize)

    parts = ax.violinplot(point_data, positions=range(len(groups)),
                          showmeans=False, showmedians=False, showextrema=False)

    for i, pc in enumerate(parts['bodies']):
        pc.set_facecolor(colors[i % len(colors)])
        pc.set_edgecolor('black')
        pc.set_linewidth(1.2)
        pc.set_alpha(0.7)

    for i, pts in enumerate(point_data):
        q1, median, q3 = np.percentile(pts, [25, 50, 75])
        if show_median:
            ax.scatter(i, median, color='white', s=30, zorder=5, edgecolors='black', linewidth=1.5)
        if show_quartiles:
            ax.vlines(i, q1, q3, color='black', linewidth=3, zorder=4)
            ax.vlines(i, min(pts), max(pts), color='black', linewidth=1, zorder=4)

        if show_points:
            jitter = np.random.uniform(-0.1, 0.1, len(pts))
            ax.scatter(i + jitter, pts, color='black', s=8, alpha=0.4, zorder=3)

    ax.set_xticks(range(len(groups)))
    ax.set_xticklabels(groups)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)

    plt.tight_layout()
    return fig, ax
```

### 9. Line Chart (Time Course / XY Plot)

```python
def prism_line_chart(x_data, y_data_list, group_labels, errors_list=None,
                     xlabel='', ylabel='', title='', colors=None,
                     figsize=(6, 4.5), markers=None):
    """
    Prism-style line chart with optional error bars.

    Parameters:
        x_data: shared x-axis values
        y_data_list: list of y-value arrays (one per group)
        group_labels: list of group names
        errors_list: list of error arrays (optional)
        markers: list of marker styles (defaults to Prism-like markers)
    """
    apply_prism_style()
    colors = colors or PRISM_COLORS
    markers = markers or ['o', 's', '^', 'D', 'v', 'P', 'X', 'h']

    fig, ax = plt.subplots(figsize=figsize)

    for i, (y_data, label) in enumerate(zip(y_data_list, group_labels)):
        color = colors[i % len(colors)]
        marker = markers[i % len(markers)]

        ax.plot(x_data, y_data, color=color, linewidth=2,
                marker=marker, markersize=7, markerfacecolor=color,
                markeredgecolor='black', markeredgewidth=0.5,
                label=label, zorder=2)

        if errors_list and errors_list[i] is not None:
            ax.errorbar(x_data, y_data, yerr=errors_list[i],
                        fmt='none', ecolor=color, elinewidth=1.2,
                        capsize=3, capthick=1.2, zorder=1)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.legend(loc='best')

    plt.tight_layout()
    return fig, ax
```

### 10. Before-After / Paired Comparison

```python
def prism_paired_plot(before, after, group_labels=('Before', 'After'),
                      ylabel='', title='', color=None, figsize=(3, 5),
                      show_stats=True):
    """
    Prism-style before-after paired comparison plot.
    """
    apply_prism_style()
    color = color or PRISM_COLORS[1]

    fig, ax = plt.subplots(figsize=figsize)

    for b, a in zip(before, after):
        ax.plot([0, 1], [b, a], color='gray', linewidth=0.8,
                alpha=0.5, zorder=1)

    ax.scatter([0]*len(before), before, color='black', s=40,
               edgecolors='black', linewidth=0.5, zorder=3)
    ax.scatter([1]*len(after), after, color=color, s=40,
               edgecolors='black', linewidth=0.5, zorder=3)

    # Mean ± SEM
    for i, (data, x_pos) in enumerate(zip([before, after], [0, 1])):
        mean = np.mean(data)
        sem = stats.sem(data)
        ax.errorbar(x_pos + 0.3, mean, yerr=sem, fmt='_', color='black',
                    markersize=15, markeredgewidth=2,
                    elinewidth=1.5, capsize=0, zorder=4)

    if show_stats:
        t_stat, p_val = stats.ttest_rel(before, after)
        sig = '***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'
        y_max = max(max(before), max(after))
        ax.plot([0, 0, 1, 1], [y_max*1.1, y_max*1.15, y_max*1.15, y_max*1.1],
                color='black', linewidth=1.2)
        ax.text(0.5, y_max*1.17, sig, ha='center', fontsize=12, fontweight='bold')

    ax.set_xticks([0, 1])
    ax.set_xticklabels(group_labels)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.set_xlim(-0.5, 1.5)

    plt.tight_layout()
    return fig, ax
```

## Statistical Annotation Helpers

```python
def add_stat_bracket(ax, x1, x2, y, label, bracket_height=None, fontsize=11):
    """Add a statistical significance bracket between two x positions."""
    if bracket_height is None:
        bracket_height = (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.03
    ax.plot([x1, x1, x2, x2],
            [y, y + bracket_height, y + bracket_height, y],
            color='black', linewidth=1.2, clip_on=False)
    ax.text((x1 + x2) / 2, y + bracket_height * 1.3, label,
            ha='center', va='bottom', fontsize=fontsize, fontweight='bold')

def p_to_stars(p_value):
    """Convert p-value to significance stars (Prism convention)."""
    if p_value < 0.0001:
        return '****'
    elif p_value < 0.001:
        return '***'
    elif p_value < 0.01:
        return '**'
    elif p_value < 0.05:
        return '*'
    else:
        return 'ns'
```

## Multi-Panel Figure (Prism-Style)

```python
def prism_multipanel(n_rows, n_cols, figsize=None, panel_labels=True):
    """
    Create a multi-panel figure with Prism-style panel labels (A, B, C...).

    Returns: fig, axes (flattened array)
    """
    apply_prism_style()
    if figsize is None:
        figsize = (4 * n_cols, 4 * n_rows)

    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_rows * n_cols == 1:
        axes = np.array([axes])
    axes_flat = axes.flatten()

    if panel_labels:
        for i, ax in enumerate(axes_flat):
            label = chr(65 + i)  # A, B, C, ...
            ax.text(-0.15, 1.1, label, transform=ax.transAxes,
                    fontsize=16, fontweight='bold', va='top')

    return fig, axes_flat
```

## Export Guidelines

```python
def save_prism_figure(fig, filename, formats=None):
    """
    Save figure in publication-quality formats.

    Parameters:
        fig: matplotlib figure
        filename: base filename (without extension)
        formats: list of formats ['png', 'pdf', 'svg', 'tiff']
    """
    formats = formats or ['png', 'pdf']
    for fmt in formats:
        fig.savefig(f'{filename}.{fmt}',
                    dpi=300,
                    bbox_inches='tight',
                    facecolor='white',
                    edgecolor='none',
                    transparent=False)
    print(f"Saved: {', '.join(f'{filename}.{f}' for f in formats)}")
```

## Usage Rules

1. **Always call `apply_prism_style()` before creating any figure** to ensure consistent styling.
2. **Bar charts must start at Y=0** — this is a Prism convention and scientific standard.
3. **Error bars**: default to SEM for biological data; clearly state SEM vs SD in figure legends.
4. **Colors**: use `PRISM_COLORS` by default; switch to `PRISM_COLORBLIND` if accessibility is important.
5. **Font**: Arial is Prism's default; fallback to Helvetica or sans-serif.
6. **Export**: always save at 300 DPI minimum; provide PDF for vector graphics.
7. **Statistical annotations**: use `*`, `**`, `***`, `****`, `ns` convention with brackets.
8. **Figure size**: keep individual panels around 3-5 inches wide for journal column widths.
9. **Axis labels**: bold, 12pt; tick labels: regular, 11pt.
10. **No grid lines, no top/right spines** — this is the signature Prism look.
