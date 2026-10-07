import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

MASTER_SEED = 20261003
ARMS = ["ENGLISH_ONLY", "HINDI_ONLY", "CODE_SWITCHING"]
LATIN_SQUARE = {
    1: ["PMEGP", "PM_VISHWAKARMA", "PM_SVANIDHI"],
    2: ["PM_VISHWAKARMA", "PM_SVANIDHI", "PMEGP"],
    3: ["PM_SVANIDHI", "PMEGP", "PM_VISHWAKARMA"]
}

def wilson_ci(k, n, confidence=0.95):
    if n == 0: return 0.0, 0.0, 0.0
    p = k / n
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    denominator = 1 + z**2 / n
    centre_adjusted = p + z**2 / (2 * n)
    adjusted_error = z * np.sqrt((p * (1 - p) + z**2 / (4 * n)) / n)
    lower = (centre_adjusted - adjusted_error) / denominator
    upper = (centre_adjusted + adjusted_error) / denominator
    return p, max(0.0, lower), min(1.0, upper)

def generate_single_dataset(seed, n_per_arm=48, eff_en=0.70, eff_cs=0.56, tau=0.60, sigma_err=1.50):
    np.random.seed(seed)
    n_total = n_per_arm * 3
    participant_ids = [f"p_{i+1:03d}" for i in range(n_total)]
    arms = np.repeat(ARMS, n_per_arm)
    ails_raw = np.clip(np.random.normal(36.0, 8.0, n_total).round(), 12, 60).astype(int)
    ails_c = ails_raw - ails_raw.mean()
    order_ids = np.random.choice([1, 2, 3], size=n_total)
    u_0i = np.random.normal(0, tau, size=n_total)
    
    rows = []
    scen_eff = {"PMEGP": 0.0, "PM_VISHWAKARMA": -0.20, "PM_SVANIDHI": +0.20}
    pos_eff = {1: -0.10, 2: 0.0, 3: +0.10}
    
    for idx in range(n_total):
        p_id = participant_ids[idx]
        arm = arms[idx]
        ac_val = ails_c[idx]
        u_i = u_0i[idx]
        ord_id = order_ids[idx]
        
        a_eff = eff_en if arm == "ENGLISH_ONLY" else (eff_cs if arm == "CODE_SWITCHING" else 0.0)
        task_list = LATIN_SQUARE[ord_id]
        
        for pos_idx, scenario in enumerate(task_list, start=1):
            base_val = 6.50 + a_eff + scen_eff[scenario] + pos_eff[pos_idx] + 0.05 * ac_val + u_i
            err = np.random.normal(0, sigma_err)
            dq = round(float(np.clip(base_val + err, 0.0, 10.0)), 2)
            rows.append({
                "participant_id": p_id,
                "arm": arm,
                "scenario": scenario,
                "position": pos_idx,
                "decision_quality": dq
            })
    return pd.DataFrame(rows)

def sim_070():
    print("Simulating C1 = +0.70 across 1,000 replicates...", flush=True)
    b_vals, se_vals, p_vals = [], [], []
    b_c2_vals, p_c2_vals = [], []
    
    for r in range(1000):
        df = generate_single_dataset(seed=MASTER_SEED + 70000 + r, eff_en=0.70, eff_cs=0.56)
        try:
            mod = smf.mixedlm("decision_quality ~ C(arm, Treatment('HINDI_ONLY')) + C(scenario) + C(position)", data=df, groups=df["participant_id"])
            res = mod.fit(reml=True, disp=False)
            b = res.params.get("C(arm, Treatment('HINDI_ONLY'))[T.ENGLISH_ONLY]", 0.0)
            se = res.bse.get("C(arm, Treatment('HINDI_ONLY'))[T.ENGLISH_ONLY]", 0.0)
            p = res.pvalues.get("C(arm, Treatment('HINDI_ONLY'))[T.ENGLISH_ONLY]", 1.0)
            
            b_c2 = res.params.get("C(arm, Treatment('HINDI_ONLY'))[T.CODE_SWITCHING]", 0.0)
            p_c2 = res.pvalues.get("C(arm, Treatment('HINDI_ONLY'))[T.CODE_SWITCHING]", 1.0)
            
            b_vals.append(b)
            se_vals.append(se)
            p_vals.append(p)
            b_c2_vals.append(b_c2)
            p_c2_vals.append(p_c2)
        except Exception:
            pass
            
    mean_b = np.mean(b_vals)
    bias = mean_b - 0.70
    rmse = np.sqrt(np.mean((np.array(b_vals) - 0.70)**2))
    covers = [(b - 1.96*se <= 0.70 <= b + 1.96*se) for b, se in zip(b_vals, se_vals)]
    pows = [p < 0.05 for p in p_vals]
    
    cov_p, cov_l, cov_h = wilson_ci(sum(covers), len(covers))
    pow_p, pow_l, pow_h = wilson_ci(sum(pows), len(pows))
    
    mean_b_c2 = np.mean(b_c2_vals)
    bias_c2 = mean_b_c2 - 0.56
    pows_c2 = [p < 0.05 for p in p_c2_vals]
    pow_c2_p, pow_c2_l, pow_c2_h = wilson_ci(sum(pows_c2), len(pows_c2))
    
    print(f"C1 (+0.70) -> Est: {mean_b:.3f}, Bias: {bias:.3f}, RMSE: {rmse:.3f}, Coverage: {cov_p*100:.1f}% [{cov_l*100:.1f}%-{cov_h*100:.1f}%], Power: {pow_p*100:.1f}% [{pow_l*100:.1f}%-{pow_h*100:.1f}%]", flush=True)
    print(f"C2 (+0.56) -> Est: {mean_b_c2:.3f}, Bias: {bias_c2:.3f}, Power: {pow_c2_p*100:.1f}% [{pow_c2_l*100:.1f}%-{pow_c2_h*100:.1f}%]", flush=True)

if __name__ == "__main__":
    sim_070()
