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

def generate_single_dataset(seed, n_per_arm=48, eff_en=1.20, eff_cs=1.00, beta_int_en=0.08, tau=0.60, sigma_err=1.50):
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
        int_eff = beta_int_en * ac_val if arm == "ENGLISH_ONLY" else 0.0
        task_list = LATIN_SQUARE[ord_id]
        
        for pos_idx, scenario in enumerate(task_list, start=1):
            base_val = 6.50 + a_eff + scen_eff[scenario] + pos_eff[pos_idx] + 0.05 * ac_val + int_eff + u_i
            err = np.random.normal(0, sigma_err)
            dq = round(float(np.clip(base_val + err, 0.0, 10.0)), 2)
            rows.append({
                "participant_id": p_id,
                "arm": arm,
                "ails_centered": round(ac_val, 3),
                "scenario": scenario,
                "position": pos_idx,
                "decision_quality": dq
            })
    return pd.DataFrame(rows)

def audit_h3_coverage():
    print("Auditing H3 Coverage with CORRECT SE key...", flush=True)
    beta_grid = [0.00, 0.02, 0.04, 0.06, 0.08, 0.09, 0.10, 0.12]
    
    for beta_int in beta_grid:
        b_vals, se_vals, p_vals = [], [], []
        for r in range(100):
            df = generate_single_dataset(seed=MASTER_SEED + 20000 + r, beta_int_en=beta_int)
            try:
                mod = smf.mixedlm("decision_quality ~ C(arm, Treatment('HINDI_ONLY')) * ails_centered + C(scenario) + C(position)", data=df, groups=df["participant_id"])
                res = mod.fit(reml=True, disp=False)
                key = "C(arm, Treatment('HINDI_ONLY'))[T.ENGLISH_ONLY]:ails_centered"
                b = res.params.get(key, 0.0)
                se = res.bse.get(key, 0.0) # CORRECT SE KEY!
                p = res.pvalues.get(key, 1.0)
                b_vals.append(b)
                se_vals.append(se)
                p_vals.append(p)
            except Exception as e:
                pass
                
        mean_b = np.mean(b_vals)
        mean_se = np.mean(se_vals)
        covers = [(b - 1.96*se <= beta_int <= b + 1.96*se) for b, se in zip(b_vals, se_vals)]
        pows = [p < 0.05 for p in p_vals]
        cov_p, cov_l, cov_h = wilson_ci(sum(covers), len(covers))
        pow_p, pow_l, pow_h = wilson_ci(sum(pows), len(pows))
        
        print(f"Beta={beta_int:.2f} | Est={mean_b:.4f} | SE={mean_se:.4f} | Coverage={cov_p*100:.1f}% [{cov_l*100:.1f}%-{cov_h*100:.1f}%] | Power={pow_p*100:.1f}%", flush=True)

if __name__ == "__main__":
    audit_h3_coverage()
