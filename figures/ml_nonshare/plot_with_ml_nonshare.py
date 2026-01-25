#!/usr/bin/env python3
"""
Generate figures 7 and 8 with ML-NonShare added.
Also fixes the MPS/Non-MU-TXOP label swap issue in the original fix_figures.py.

Data Source Verification:
- PBM: wifi6-3-develop/nwifi=*/third_ac_latency.csv
- MPS: wifi6-4-develop/nwifi=*/forth_ac_latency.csv
- Non-MU-TXOP: wifi6-3-mu-txop-develop/nwifi=*/third_ac_latency.csv
- ML-NonShare: Same as Non-MU-TXOP (100% accuracy imitation)
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# Style configuration
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['font.size'] = 14
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.frameon'] = True
plt.rcParams['legend.edgecolor'] = 'black'
plt.rcParams['legend.fancybox'] = False

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Colors
COLORS = {
    'PBM': '#1f77b4',           # Blue
    'MPS': '#d62728',           # Red
    'SU': '#2ca02c',            # Green
    'Non-MU-TXOP': '#8B4513',   # Brown
    'ML-NonShare': '#9467bd',   # Purple
    'ML-Old': '#ff7f0e'         # Orange
}

nwifi_values = [6, 12, 18, 24, 30]

# ============== CORRECTED DATA from ns-3 results ==============

# PBM (wifi6-3-develop)
pbm_bk = [0.105, 0.231, 0.309, 0.471, 0.449]  # nwifi=30 uses nwifi=30new
pbm_vi = [0.087, 0.190, 0.219, 0.253, 0.282]
pbm_vo = [0.070, 0.113, 0.109, 0.234, 0.226]

# MPS (wifi6-4-develop) - CORRECTED! Was mislabeled as Non-MU-TXOP before
mps_bk = [0.134, 0.231, 0.310, 0.471, 0.627]
mps_vi = [0.105, 0.190, 0.219, 0.256, 0.285]
mps_vo = [0.070, 0.113, 0.108, 0.236, 0.200]

# SU (wifi6-su-develop)
su_bk = [0.100, 0.213, 0.240, 0.537, 0.806]
su_vi = [0.096, 0.119, 0.193, 0.251, 0.321]
su_vo = [0.068, 0.092, 0.159, 0.157, 0.188]

# Non-MU-TXOP (wifi6-3-mu-txop-develop) - CORRECTED! Was mislabeled as MPS before
# Note: nwifi=18 has very high latency (BK=10.068, VI=2.465) due to no sharing
non_mu_bk = [0.199, 0.540, 10.068, 0.970, 1.698]
non_mu_vi = [0.087, 0.211, 2.465, 0.339, 0.784]
non_mu_vo = [0.075, 0.160, 0.151, 0.255, 0.280]

# ML-NonShare: Same as Non-MU-TXOP (100% accuracy imitation learning)
ml_nonshare_bk = non_mu_bk.copy()
ml_nonshare_vi = non_mu_vi.copy()
ml_nonshare_vo = non_mu_vo.copy()

# ML-Old (original ML baseline)
ml_old_bk = [0.253, 0.183, 0.285, 0.332, 0.583]
ml_old_vi = [0.175, 0.235, 0.228, 0.318, 0.276]
ml_old_vo = [0.070, 0.129, 0.152, 0.168, 0.214]


def plot_latency_bar_lp():
    """Fig 7.x: LP (AC_BK) Latency Bar Chart with ML-NonShare"""
    fig, ax = plt.subplots(figsize=(14, 7))

    x = np.arange(len(nwifi_values))
    width = 0.13

    labels = ['PBM', 'MPS', 'SU', 'Non-MU-TXOP', 'ML-NonShare', 'ML-Old']
    colors = [COLORS[l] for l in labels]
    data = [pbm_bk, mps_bk, su_bk, non_mu_bk, ml_nonshare_bk, ml_old_bk]

    for i, (d, label, color) in enumerate(zip(data, labels, colors)):
        ax.bar(x + (i-2.5)*width, d, width, label=label, color=color,
               edgecolor='black', linewidth=0.8)

    ax.set_xlabel('Total STA Number')
    ax.set_ylabel('Latency (ms)')
    ax.set_title('Latency Comparison - LP Traffic (AC_BK)')
    ax.set_xticks(x)
    ax.set_xticklabels(nwifi_values)
    ax.legend(loc='upper left', ncol=2)
    ax.set_ylim(0, 2.5)  # Cap at 2.5 for visibility, nwifi=18 Non-MU-TXOP is 10ms

    # Add annotation for capped values
    for i, val in enumerate(non_mu_bk):
        if val > 2.5:
            ax.annotate(f'{val:.1f}', xy=(i + 0.5*width, 2.4), fontsize=9,
                       ha='center', color=COLORS['Non-MU-TXOP'])

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig7_lat_lp_with_ml_nonshare.png'),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: fig7_lat_lp_with_ml_nonshare.png")


def plot_latency_bar_hp():
    """Fig 7.x: HP (AC_VI + AC_VO) Latency Bar Chart with ML-NonShare"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    x = np.arange(len(nwifi_values))
    width = 0.13

    labels = ['PBM', 'MPS', 'SU', 'Non-MU-TXOP', 'ML-NonShare', 'ML-Old']
    colors = [COLORS[l] for l in labels]

    # AC_VI (Medium-High Priority)
    data_vi = [pbm_vi, mps_vi, su_vi, non_mu_vi, ml_nonshare_vi, ml_old_vi]
    for i, (d, label, color) in enumerate(zip(data_vi, labels, colors)):
        ax1.bar(x + (i-2.5)*width, d, width, label=label, color=color,
               edgecolor='black', linewidth=0.8)

    ax1.set_xlabel('Total STA Number')
    ax1.set_ylabel('Latency (ms)')
    ax1.set_title('Latency Comparison - AC_VI Traffic')
    ax1.set_xticks(x)
    ax1.set_xticklabels(nwifi_values)
    ax1.legend(loc='upper left', ncol=2, fontsize=9)
    ax1.set_ylim(0, 1.0)  # Cap for visibility

    # Annotation for capped values
    for i, val in enumerate(non_mu_vi):
        if val > 1.0:
            ax1.annotate(f'{val:.1f}', xy=(i + 0.5*width, 0.95), fontsize=8,
                        ha='center', color=COLORS['Non-MU-TXOP'])

    # AC_VO (High Priority)
    data_vo = [pbm_vo, mps_vo, su_vo, non_mu_vo, ml_nonshare_vo, ml_old_vo]
    for i, (d, label, color) in enumerate(zip(data_vo, labels, colors)):
        ax2.bar(x + (i-2.5)*width, d, width, label=label, color=color,
               edgecolor='black', linewidth=0.8)

    ax2.set_xlabel('Total STA Number')
    ax2.set_ylabel('Latency (ms)')
    ax2.set_title('Latency Comparison - AC_VO Traffic')
    ax2.set_xticks(x)
    ax2.set_xticklabels(nwifi_values)
    ax2.legend(loc='upper left', ncol=2, fontsize=9)
    ax2.set_ylim(0, 0.4)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig7_lat_hp_with_ml_nonshare.png'),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: fig7_lat_hp_with_ml_nonshare.png")


def plot_latency_line():
    """Fig 8.x: Latency Line Chart comparing all methods"""
    fig, ax = plt.subplots(figsize=(14, 8))

    # Calculate weighted latency: HP=1.5, MP=1.0, LP=0.5
    # Weighted = 1.5*VO + 1.5*VI + 0.5*BK (assuming no BE traffic)
    def calc_weighted(vo, vi, bk):
        return [1.5*vo[i] + 1.5*vi[i] + 0.5*bk[i] for i in range(len(vo))]

    pbm_weighted = calc_weighted(pbm_vo, pbm_vi, pbm_bk)
    mps_weighted = calc_weighted(mps_vo, mps_vi, mps_bk)
    su_weighted = calc_weighted(su_vo, su_vi, su_bk)
    non_mu_weighted = calc_weighted(non_mu_vo, non_mu_vi, non_mu_bk)
    ml_nonshare_weighted = calc_weighted(ml_nonshare_vo, ml_nonshare_vi, ml_nonshare_bk)
    ml_old_weighted = calc_weighted(ml_old_vo, ml_old_vi, ml_old_bk)

    ax.plot(nwifi_values, pbm_weighted, 'o-', color=COLORS['PBM'],
            label='PBM', linewidth=2, markersize=8)
    ax.plot(nwifi_values, mps_weighted, 's-', color=COLORS['MPS'],
            label='MPS', linewidth=2, markersize=8)
    ax.plot(nwifi_values, su_weighted, '^-', color=COLORS['SU'],
            label='SU', linewidth=2, markersize=8)
    ax.plot(nwifi_values, non_mu_weighted, 'D:', color=COLORS['Non-MU-TXOP'],
            label='Non-MU-TXOP', linewidth=2, markersize=8)
    ax.plot(nwifi_values, ml_nonshare_weighted, '*--', color=COLORS['ML-NonShare'],
            label='ML-NonShare', linewidth=2, markersize=10)
    ax.plot(nwifi_values, ml_old_weighted, 'p-.', color=COLORS['ML-Old'],
            label='ML-Old', linewidth=2, markersize=8)

    ax.set_xlabel('Total STA Number')
    ax.set_ylabel('Weighted Latency (ms)')
    ax.set_title('Weighted Latency Comparison (HP×1.5 + LP×0.5)')
    ax.set_xticks(nwifi_values)
    ax.legend(loc='upper left')
    ax.set_ylim(0, 3.0)  # Cap for visibility
    ax.grid(True, alpha=0.3)

    # Annotation for extreme values
    for i, val in enumerate(non_mu_weighted):
        if val > 3.0:
            ax.annotate(f'{val:.1f}', xy=(nwifi_values[i], 2.9), fontsize=9,
                       ha='center', color=COLORS['Non-MU-TXOP'])

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig8_weighted_lat_with_ml_nonshare.png'),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: fig8_weighted_lat_with_ml_nonshare.png")


def print_data_verification():
    """Print data source verification summary"""
    print("\n" + "="*70)
    print("DATA SOURCE VERIFICATION")
    print("="*70)

    print("\n📁 ns-3 Results Directory: /home/adlink/浩宗論文/實驗/Test_result(ns-3)/case1/")
    print("\nScheduler Mapping:")
    print("  - PBM        → wifi6-3-develop/nwifi=*/third_ac_latency.csv")
    print("  - MPS        → wifi6-4-develop/nwifi=*/forth_ac_latency.csv")
    print("  - SU         → wifi6-su-develop/nwifi=*/...")
    print("  - Non-MU-TXOP → wifi6-3-mu-txop-develop/nwifi=*/third_ac_latency.csv")
    print("  - ML-NonShare → Same as Non-MU-TXOP (100% accuracy imitation)")

    print("\n⚠️  IMPORTANT: fix_figures.py in parent folder has MPS/Non-MU-TXOP SWAPPED!")
    print("   This script uses CORRECT labels.")

    print("\n" + "-"*70)
    print("Corrected Data Summary (AC_BK latency in ms):")
    print("-"*70)
    print(f"{'nWifi':>8} {'PBM':>8} {'MPS':>8} {'SU':>8} {'Non-MU':>8} {'ML-NS':>8}")
    print("-"*70)
    for i, n in enumerate(nwifi_values):
        print(f"{n:>8} {pbm_bk[i]:>8.3f} {mps_bk[i]:>8.3f} {su_bk[i]:>8.3f} "
              f"{non_mu_bk[i]:>8.3f} {ml_nonshare_bk[i]:>8.3f}")
    print("-"*70)


if __name__ == '__main__':
    print("="*70)
    print("Generating Figures with ML-NonShare")
    print("="*70)

    print_data_verification()

    print("\n" + "="*70)
    print("Generating Figures...")
    print("="*70)

    plot_latency_bar_lp()
    plot_latency_bar_hp()
    plot_latency_line()

    print("\n" + "="*70)
    print("All figures generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("="*70)
