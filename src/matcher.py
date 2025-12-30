class ResonanceMatcher:
    @staticmethod
    def calculate_score(user_profile, candidate):
        score = 0
        breakdown = {"values": 0, "dreams": 0, "talents": 0}
        details = []
        c_profile = candidate.get('profile', {})

        # 1. 價值觀共鳴 (Values)
        # 因為 LLM 已經嘗試將使用者的詞 mapped 到知識庫，而 Mock DB 的詞也在知識庫裡
        # 所以這裡直接比對字串即可 (轉小寫以防萬一)
        u_vals = set(v.lower() for v in user_profile.get('core_values', []))
        c_vals = set(v.lower() for v in c_profile.get('core_values', []))
        
        overlap = u_vals.intersection(c_vals)
        if overlap:
            points = len(overlap) * 10
            score += points
            breakdown["values"] += points
            details.append(f"Values: {', '.join(overlap)}")
        
        # 2. 夢想同頻 (Dreams)
        # 現在夢想也具備學習能力了，所以邏輯跟價值觀一樣，用集合交集
        # 為了增加容錯，我們也做簡單的關鍵字包含檢查
        u_dreams = set(d.lower() for d in user_profile.get('dream_domain', []))
        c_dreams_raw = c_profile.get('dream_domain', [])
        c_dreams_norm = set(d.lower() for d in c_dreams_raw)
        
        # A. 直接命中 (例如 "Social Impact" vs "Social Impact")
        dream_overlap = u_dreams.intersection(c_dreams_norm)
        
        # B. 模糊命中 (例如 "Social Impact" 包含 "social")
        # 如果直接命中沒有分，再檢查是否有部分字串重疊
        if not dream_overlap:
            for u_d in u_dreams:
                for c_d in c_dreams_norm:
                    # 避免太短的字 (e.g., "art" vs "start") 造成誤判，設定長度限制
                    if len(u_d) > 3 and (u_d in c_d or c_d in u_d):
                        dream_overlap.add(c_d) 
        
        if dream_overlap:
            points = 5 * len(dream_overlap)
            score += points
            breakdown["dreams"] += points
            details.append(f"Dream: {', '.join(dream_overlap)}")
        
        # 3. 天賦互補 (Talents)
        if score > 0:
            u_talents = set(t.lower() for t in user_profile.get('top_talents', []))
            c_talents = set(t.lower() for t in c_profile.get('top_talents', []))
            
            # 如果完全沒重疊 (交集為空)，且兩邊都有資料，視為互補
            if u_talents.isdisjoint(c_talents) and u_talents and c_talents:
                points = 3
                score += points
                breakdown["talents"] += points
                details.append("Talent Complementarity")

        return score, breakdown, details

    @staticmethod
    def find_top_matches(user_profile, database):
        results = []
        for candidate in database:
            score, breakdown, details = ResonanceMatcher.calculate_score(user_profile, candidate)
            results.append({
                "candidate": candidate,
                "score": score,
                "breakdown": breakdown,
                "details": details
            })
        
        return sorted(results, key=lambda x: x['score'], reverse=True)