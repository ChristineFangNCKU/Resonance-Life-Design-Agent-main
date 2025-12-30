import os
import json
import webbrowser
from colorama import Fore, Style

# 這裡是將 React 邏輯轉譯為單一 HTML 檔案的模板
# 我們直接使用 CDN 引入 React (為了簡化) 或更簡單：直接用原生 JS 渲染 DOM
# 為了 Demo 最極致的穩定性，這裡採用「原生 JS 樣板字串」法，完全模擬 React 的輸出結果

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resonance Result</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
        body { font-family: 'Inter', sans-serif; }
        /* 隱藏捲軸但保留功能 */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased min-h-screen p-8">
    
    <header class="max-w-7xl mx-auto mb-10 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
        </div>
        <div>
            <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Resonance</h1>
            <p class="text-sm text-slate-500 font-medium">Talent & Values Matching Database</p>
        </div>
    </header>

    <main class="max-w-7xl mx-auto">
        <div id="card-container" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            </div>
        
        <div class="mt-12 text-center border-t border-slate-200 pt-8">
           <p class="text-sm text-slate-400" id="footer-text">
             Displaying candidates from the secure resonance database.
           </p>
        </div>
    </main>

    <script>
        // 【關鍵】：Python 資料會從這裡注入
        const users = {{USER_DATA_PLACEHOLDER}};
        const MAX_SCORE = 50; 

        // 輔助函式：生成標籤 (對應 Tag.tsx)
        function createTag(label, type) {
            let colorClass = '';
            switch(type) {
                case 'CORE_VALUE': // Red/Warm
                    colorClass = 'bg-rose-100 text-rose-800 border-rose-200';
                    break;
                case 'TOP_TALENT': // Green/Teal
                    colorClass = 'bg-emerald-100 text-emerald-800 border-emerald-200';
                    break;
                case 'DREAM_DOMAIN': // Blue/Purple
                    colorClass = 'bg-indigo-100 text-indigo-800 border-indigo-200';
                    break;
                default:
                    colorClass = 'bg-slate-100 text-slate-800 border-slate-200';
            }
            return `<span class="inline-block px-3 py-1 rounded-full text-xs font-semibold border ${colorClass} mr-2 mb-2 transition-colors duration-200">${label}</span>`;
        }

        const container = document.getElementById('card-container');
        document.getElementById('footer-text').innerText = `Displaying ${users.length} candidates from the secure resonance database.`;

        users.forEach(user => {
            // 計算寬度 (對應 UserCard.tsx 的邏輯)
            const breakdown = user.breakdown || { values: 0, dreams: 0, talents: 0 };
            const totalScore = user.score; // 直接用 Python 傳來的總分
            
            const w_v = (breakdown.values / MAX_SCORE) * 100;
            const w_d = (breakdown.dreams / MAX_SCORE) * 100;
            const w_t = (breakdown.talents / MAX_SCORE) * 100;

            // 生成標籤 HTML
            const valuesTags = user.profile.core_values.map(v => createTag(v, 'CORE_VALUE')).join('');
            const talentsTags = user.profile.top_talents.map(v => createTag(v, 'TOP_TALENT')).join('');
            const dreamsTags = user.profile.dream_domain.map(v => createTag(v, 'DREAM_DOMAIN')).join('');

            // 建立卡片 DOM (完全複製 UserCard.tsx 的結構)
            const card = document.createElement('div');
            card.className = "group relative flex flex-col h-full bg-white rounded-xl shadow-md border border-slate-100 hover:shadow-xl hover:-translate-y-1 hover:border-indigo-100 transition-all duration-300 ease-out overflow-hidden";
            
            card.innerHTML = `
                <div class="p-6 pb-2 border-b border-slate-50">
                    <div class="flex justify-between items-baseline mb-1">
                        <h2 class="text-xl font-bold text-slate-900 group-hover:text-indigo-600 transition-colors">${user.name}</h2>
                        <span class="text-xs font-mono text-slate-400">#${user.id}</span>
                    </div>
                    <h3 class="text-sm font-medium text-slate-500 uppercase tracking-wide">${user.major}</h3>
                </div>

                <div class="px-6 py-4 bg-slate-50/50 flex-grow">
                    <div class="relative pl-4 border-l-4 border-slate-300 group-hover:border-indigo-400 transition-colors duration-300">
                        <p class="text-sm italic text-slate-600 leading-relaxed line-clamp-3 group-hover:line-clamp-none transition-all duration-500 ease-in-out">
                            "${user.interview_summary}"
                        </p>
                    </div>
                </div>

                <div class="px-6 pt-4 pb-4 space-y-4 bg-white mt-auto">
                    <div>
                        <h4 class="text-[10px] uppercase font-bold text-rose-500 mb-2 flex items-center gap-1">
                            <span class="w-1.5 h-1.5 rounded-full bg-rose-500"></span> Core Values
                        </h4>
                        <div class="flex flex-wrap">${valuesTags}</div>
                    </div>
                    <div>
                        <h4 class="text-[10px] uppercase font-bold text-emerald-600 mb-2 flex items-center gap-1">
                            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> Top Talents
                        </h4>
                        <div class="flex flex-wrap">${talentsTags}</div>
                    </div>
                    <div>
                        <h4 class="text-[10px] uppercase font-bold text-indigo-600 mb-2 flex items-center gap-1">
                            <span class="w-1.5 h-1.5 rounded-full bg-indigo-500"></span> Dream Domains
                        </h4>
                        <div class="flex flex-wrap">${dreamsTags}</div>
                    </div>
                </div>

                <div class="px-6 pt-2 pb-5 border-t border-slate-100 bg-white">
                    <div class="flex justify-between items-end mb-2">
                        <span class="text-xs font-bold text-slate-700 uppercase tracking-wider">
                            Resonance Score: <span class="text-slate-900 text-sm">${totalScore}</span>
                        </span>
                    </div>
                    <div class="flex h-3 w-full bg-gray-200 rounded-full overflow-hidden">
                        <div style="width: ${w_v}%" class="bg-rose-500 h-full" title="Values: ${breakdown.values}"></div>
                        <div style="width: ${w_d}%" class="bg-blue-500 h-full" title="Dreams: ${breakdown.dreams}"></div>
                        <div style="width: ${w_t}%" class="bg-emerald-500 h-full" title="Talents: ${breakdown.talents}"></div>
                    </div>
                    <div class="flex items-center gap-3 mt-2 text-[10px] font-medium text-slate-500">
                        <div class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-rose-500"></span> Values</div>
                        <div class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-blue-500"></span> Dreams</div>
                        <div class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-emerald-500"></span> Talents</div>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    </script>
</body>
</html>
"""

def generate_web_report(matches):
    """
    接收 matches 資料，生成與 AI Studio 設計一致的網頁
    """
    print(f"{Fore.CYAN}[System]: Generating High-Fidelity Web Interface...{Style.RESET_ALL}")
    
    # 1. 資料轉換：確保資料結構符合前端預期
    js_data = []
    for m in matches:
        candidate = m['candidate']
        
        # 安全機制：確保 breakdown 存在，如果沒有則給預設值
        breakdown = m.get('breakdown', {"values": 0, "dreams": 0, "talents": 0})
        
        user_obj = {
            "id": candidate.get('id', 'u000'),
            "name": candidate['name'],
            "major": candidate['major'],
            "interview_summary": candidate['interview_summary'],
            "profile": candidate['profile'],
            # 這裡解決了你的第一個問題：動態傳入 Python 算出來的分數
            "score": m['score'],
            "breakdown": breakdown 
        }
        js_data.append(user_obj)
    
    # 2. 注入資料到 HTML
    final_html = HTML_TEMPLATE.replace(
        "{{USER_DATA_PLACEHOLDER}}", 
        json.dumps(js_data, ensure_ascii=False)
    )
    
    # 3. 輸出與開啟
    output_path = os.path.abspath("resonance_report.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)
        
    print(f"{Fore.GREEN}[System]: Report ready! Opening in browser...{Style.RESET_ALL}")
    webbrowser.open(f"file://{output_path}")