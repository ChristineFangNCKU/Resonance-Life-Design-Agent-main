import matplotlib.pyplot as plt
import numpy as np

def plot_resonance_spectrum(matches):
    """
    繪製共振光譜分析圖 (堆疊長條圖)
    """
    print("[System]: Generating Resonance Visualization...")

    # 準備數據 (取前 6 名，避免圖表太擠)
    top_matches = matches[:6]
    names = [m['candidate']['name'] for m in top_matches]
    
    # 提取各維度分數
    v_scores = [m['breakdown']['values'] for m in top_matches]
    d_scores = [m['breakdown']['dreams'] for m in top_matches]
    t_scores = [m['breakdown']['talents'] for m in top_matches]

    # 設定圖表參數
    x = np.arange(len(names))
    width = 0.5

    # 針對 Mac 用戶的字體設定 (避免中文亂碼，雖然目前名字是英文)
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS'] 
    plt.rcParams['axes.unicode_minus'] = False

    fig, ax = plt.subplots(figsize=(10, 6))

    # 繪製堆疊長條圖
    # 底部：價值觀 (Values)
    p1 = ax.bar(x, v_scores, width, label='Values Alignment', color='#ff9999', edgecolor='white')
    # 中間：夢想 (Dreams) - bottom 要設為 v_scores
    p2 = ax.bar(x, d_scores, width, bottom=v_scores, label='Dream Direction', color='#66b3ff', edgecolor='white')
    # 頂部：天賦 (Talents) - bottom 要設為 v + d
    p3 = ax.bar(x, t_scores, width, bottom=np.add(v_scores, d_scores), label='Talent Complementarity', color='#99ff99', edgecolor='white')

    # 美化圖表
    ax.set_ylabel('Resonance Score')
    ax.set_title('Resonance Spectrum Analysis (共振光譜)')
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=15)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # 在柱狀圖上方標示總分
    for i in range(len(names)):
        total = v_scores[i] + d_scores[i] + t_scores[i]
        if total > 0:
            ax.text(i, total + 0.5, str(total), ha='center', fontweight='bold')

    # 調整版面並顯示
    plt.tight_layout()
    plt.show() # 這會跳出一個視窗