class ResonanceMatcher:
    @staticmethod
    def calculate_score(user_profile, candidate):
        """
        計算使用者與候選人的共振分數。
        邏輯：價值觀(重疊) + 夢想(關鍵字) + 天賦(互補)
        """
        score = 0
        details = []
        c_profile = candidate.get('profile', {})

        # 1. 價值觀共鳴 (Values Alignment) - 權重 x10
        u_vals = set(v.lower() for v in user_profile.get('core_values', []))
        c_vals = set(v.lower() for v in c_profile.get('core_values', []))
        overlap = u_vals.intersection(c_vals)
        
        if overlap:
            score += len(overlap) * 10
            details.append(f"Values Match: {', '.join(overlap)}")
        
        # 2. 夢想同頻 (Dream Direction) - 權重 x5
        # 簡單字串比對
        u_dreams = " ".join(user_profile.get('dream_domain', [])).lower()
        c_dreams = " ".join(c_profile.get('dream_domain', [])).lower()
        keywords = ["startup", "education", "tech", "social", "art", "policy", "health"]
        
        matched_dream = False
        for k in keywords:
            if k in u_dreams and k in c_dreams:
                score += 5
                details.append(f"Dream Match: {k}")
                matched_dream = True
        
        # 3. 天賦互補 (Talent Complementarity) - 權重 x3
        # 只有在價值觀或夢想有對到的情況下，才計算天賦互補
        if score > 0:
            u_talents = set(t.lower() for t in user_profile.get('top_talents', []))
            c_talents = set(t.lower() for t in c_profile.get('top_talents', []))
            
            # 如果天賦完全沒重疊，視為互補 (例如 技術 vs 行銷)
            if u_talents.isdisjoint(c_talents):
                score += 3
                details.append("Talent Complementarity (Good Team!)")

        return score, details

    @staticmethod
    def find_top_matches(user_profile, database, top_k=3):
        results = []
        for candidate in database:
            score, details = ResonanceMatcher.calculate_score(user_profile, candidate)
            results.append({
                "candidate": candidate,
                "score": score,
                "details": details
            })
        
        # 依分數高低排序
        return sorted(results, key=lambda x: x['score'], reverse=True)[:top_k]