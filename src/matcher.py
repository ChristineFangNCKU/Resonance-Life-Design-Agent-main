class ResonanceMatcher:
    @staticmethod
    def calculate_score(user_profile, candidate):
        score = 0
        # 新增 breakdown 字典來記錄各項得分
        breakdown = {"values": 0, "dreams": 0, "talents": 0}
        details = []
        c_profile = candidate.get('profile', {})

        # 1. 價值觀共鳴 (Values) - 權重 x10
        u_vals = set(v.lower() for v in user_profile.get('core_values', []))
        c_vals = set(v.lower() for v in c_profile.get('core_values', []))
        overlap = u_vals.intersection(c_vals)
        
        if overlap:
            points = len(overlap) * 10
            score += points
            breakdown["values"] += points
            details.append(f"Values: {', '.join(overlap)}")
        
        # 2. 夢想同頻 (Dreams) - 權重 x5
        u_dreams = " ".join(user_profile.get('dream_domain', [])).lower()
        c_dreams = " ".join(c_profile.get('dream_domain', [])).lower()
        keywords = ["startup", "education", "tech", "social", "art", "policy", "health", "design"]
        
        for k in keywords:
            if k in u_dreams and k in c_dreams:
                points = 5
                score += points
                breakdown["dreams"] += points
                details.append(f"Dream: {k}")
        
        # 3. 天賦互補 (Talents) - 權重 x3
        if score > 0: # 只有在大方向契合時才考慮互補
            u_talents = set(t.lower() for t in user_profile.get('top_talents', []))
            c_talents = set(t.lower() for t in c_profile.get('top_talents', []))
            
            if u_talents.isdisjoint(c_talents):
                points = 3
                score += points
                breakdown["talents"] += points
                details.append("Talent Complementarity")

        return score, breakdown, details

    @staticmethod
    def find_top_matches(user_profile, database):
        results = []
        for candidate in database:
            # 接收 breakdown
            score, breakdown, details = ResonanceMatcher.calculate_score(user_profile, candidate)
            results.append({
                "candidate": candidate,
                "score": score,
                "breakdown": breakdown, # 存入結果
                "details": details
            })
        
        # 依分數高低排序
        return sorted(results, key=lambda x: x['score'], reverse=True)